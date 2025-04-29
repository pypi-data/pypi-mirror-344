import os
import mmap
import shutil
from pathlib import Path
from typing import Optional, List, Tuple, Any # Added typing imports
from loguru import logger
import queue # For type hinting log_queue

# --- Constants ---
DEFAULT_WINDOW_SIZE_MB = 20
DEFAULT_BUFFER_SIZE_MB = 10

# --- Helper Functions ---

def _log_message(message: str, log_queue: Optional[queue.Queue] = None) -> None:
    """Logs a message either to a queue or the default logger."""
    if log_queue:
        log_queue.put(message)
    else:
        # Use debug level for boundary finding details, info for major steps
        if "Boundary found" in message or "Warning: Found" in message or "Warning: No safe" in message:
            logger.debug(message)
        else:
            logger.info(message)

def _find_boundary_near_target(
    memory_map: mmap.mmap,
    target_position: int,
    file_size: int,
    record_begin_bytes: bytes,
    record_end_bytes: bytes,
    window_size_bytes: int,
    previous_boundary: int,
    log_queue: Optional[queue.Queue] = None
) -> int:
    """
    Searches for the nearest record boundary (end or start) around a target position.

    Args:
        memory_map: The memory-mapped file object.
        target_position: The ideal split position.
        file_size: The total size of the file.
        record_begin_bytes: The byte representation of the record start marker.
        record_end_bytes: The byte representation of the record end marker.
        window_size_bytes: The size of the window around the target to search within.
        previous_boundary: The position of the previous boundary found.
        log_queue: Optional queue for logging.

    Returns:
        The calculated boundary position. Falls back to target if no marker is found nearby.
    """
    window_start = max(0, target_position - window_size_bytes // 2)
    window_end = min(file_size, target_position + window_size_bytes) # Adjusted window end logic slightly

    # 1. Search backwards from target for the nearest preceding record_end
    # Ensure search area doesn't go beyond the target itself initially for rfind
    search_area_before = memory_map[window_start : min(target_position + len(record_end_bytes), window_end)]
    # Adjust rfind end position to be relative to the start of the slice
    rfind_end_limit = target_position - window_start + len(record_end_bytes)
    last_end_pos_relative = search_area_before.rfind(record_end_bytes, 0, rfind_end_limit)

    if last_end_pos_relative != -1:
        safe_boundary = window_start + last_end_pos_relative + len(record_end_bytes)
        # Ensure the found boundary is after the previous one
        if safe_boundary > previous_boundary:
            _log_message(f"Boundary found after record_end near {target_position:,} at {safe_boundary:,}", log_queue)
            return safe_boundary
        else:
             _log_message(f"Warning: Found record_end near {target_position:,} at {safe_boundary:,} but it's before previous boundary {previous_boundary:,}. Proceeding to check for record_begin.", log_queue)


    # 2. If no suitable record_end found, search forwards from target for the next record_begin
    # Ensure search area starts slightly before target to catch markers spanning the target
    search_area_after_start = max(0, target_position - len(record_begin_bytes) + 1) # +1 to avoid finding the start of the *previous* record if target is exactly at a start
    search_area_after = memory_map[search_area_after_start : window_end]
    first_begin_pos_relative = search_area_after.find(record_begin_bytes)

    if first_begin_pos_relative != -1:
        safe_boundary = search_area_after_start + first_begin_pos_relative
        # Ensure the found boundary is after the previous one
        if safe_boundary > previous_boundary:
            _log_message(f"Boundary found at record_begin near {target_position:,} at {safe_boundary:,}", log_queue)
            return safe_boundary
        else:
            # This case is less likely if the end marker search failed, but possible with overlapping markers
             _log_message(f"Warning: Found record_begin near {target_position:,} at {safe_boundary:,} but it's before previous boundary {previous_boundary:,}. Using target fallback.", log_queue)
             # Fall through to target fallback

    # 3. Fallback if no suitable boundary found
    _log_message(f"Warning: No safe boundary found near {target_position:,}. Using target fallback position.", log_queue)
    # Ensure fallback is at least one byte after the previous boundary
    fallback_boundary = max(target_position, previous_boundary + 1)
    # Ensure fallback doesn't exceed file size (edge case for last chunk)
    return min(fallback_boundary, file_size)


def _write_chunk_to_file(
    input_file_obj: Any, # File object opened in binary read mode
    output_chunk_filepath: Path,
    start_pos: int,
    end_pos: int,
    buffer_size_bytes: int,
    log_queue: Optional[queue.Queue] = None
) -> None:
    """
    Reads a chunk from the input file and writes it to the output file.

    Args:
        input_file_obj: The opened input file object.
        output_chunk_filepath: Path object for the output chunk file.
        start_pos: Starting byte position in the input file.
        end_pos: Ending byte position in the input file.
        buffer_size_bytes: Size of the read buffer in bytes.
        log_queue: Optional queue for logging.
    """
    chunk_size = end_pos - start_pos
    if chunk_size <= 0:
        _log_message(f"Skipping empty chunk (boundaries: {start_pos}-{end_pos}) for '{output_chunk_filepath}'.", log_queue)
        return # Don't create empty files unless necessary? Or create them? Decided not to.

    _log_message(f"Writing chunk ({chunk_size:,} bytes) to '{output_chunk_filepath}'", log_queue)
    input_file_obj.seek(start_pos)
    bytes_written = 0
    try:
        with open(output_chunk_filepath, 'wb') as output_chunk_file_obj:
            while bytes_written < chunk_size:
                bytes_to_read = min(buffer_size_bytes, chunk_size - bytes_written)
                chunk_data = input_file_obj.read(bytes_to_read)
                if not chunk_data:
                    _log_message(f"Warning: Unexpected end of file reached while reading chunk for '{output_chunk_filepath}'. Expected {chunk_size} bytes, got {bytes_written}.", log_queue)
                    break # Should not happen if boundaries are correct, but safety check
                output_chunk_file_obj.write(chunk_data)
                bytes_written += len(chunk_data)
        if bytes_written != chunk_size:
             _log_message(f"Warning: Final size mismatch for '{output_chunk_filepath}'. Expected {chunk_size}, wrote {bytes_written}.", log_queue)
    except IOError as e:
        logger.error(f"Error writing chunk file '{output_chunk_filepath}': {e}")
        # Consider if partial file should be removed
        raise


# --- Core Functions ---

def chunk_preview(
    filename: str,
    num_chunks: int,
    record_begin: str,
    record_end: str,
    log_queue: Optional[queue.Queue] = None
) -> List[int]:
    """
    Calculates potential byte boundaries for splitting a file into chunks
    based on record markers, without actually splitting the file.

    Args:
        filename (str): Path to the input file.
        num_chunks (int): Desired number of chunks.
        record_begin (str): String marking the beginning of a record.
        record_end (str): String marking the end of a record.
        log_queue (Optional[queue.Queue]): Optional queue for logging in
                                           multiprocessing scenarios.

    Returns:
        List[int]: A sorted list of byte offsets representing the calculated
                   chunk boundaries. Includes 0 and the file size.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If num_chunks is not positive.
        Exception: For other potential errors during file access or boundary search.
    """
    _log_message(f"Starting chunk preview for '{filename}' with {num_chunks} desired chunks.", log_queue)
    input_filepath = Path(filename) # Use pathlib

    try:
        file_size = input_filepath.stat().st_size
    except FileNotFoundError:
        logger.error(f"Error: Input file not found: {filename}")
        raise
    except Exception as e:
        logger.error(f"Error accessing file stats for {filename}: {e}")
        raise

    if file_size == 0:
        _log_message("Warning: Input file is empty.", log_queue)
        return [0, 0]

    if num_chunks <= 0:
        # Raise error instead of defaulting, makes behavior more explicit
        # _log_message("Warning: Number of chunks must be positive. Defaulting to 1 chunk.", log_queue)
        # num_chunks = 1
        raise ValueError("Number of chunks must be positive.")

    if num_chunks == 1:
        _log_message("Single chunk requested, returning [0, file_size].", log_queue)
        return [0, file_size]

    # --- Calculate Target Positions ---
    # Ideal positions if file were split evenly
    ideal_chunk_size = file_size / num_chunks # Use float division for potentially more accurate targets
    target_positions = [int(i * ideal_chunk_size) for i in range(1, num_chunks)]
    _log_message(f"Target positions: {target_positions}", log_queue)


    boundaries = [0]
    record_begin_bytes = record_begin.encode('utf-8', errors='replace')
    record_end_bytes = record_end.encode('utf-8', errors='replace')
    # Use a fraction of the ideal chunk size as the window, capped at a max
    window_size_bytes = min(DEFAULT_WINDOW_SIZE_MB * 1024 * 1024, int(ideal_chunk_size * 0.5) if ideal_chunk_size > 0 else file_size)
    _log_message(f"Using boundary search window size: {window_size_bytes:,} bytes", log_queue)


    # --- Find Boundaries using Memory Mapping ---
    try:
        with open(input_filepath, "rb") as file_obj: # Open in binary read mode
             # Use ACCESS_READ as we only need to read for preview
            with mmap.mmap(file_obj.fileno(), 0, access=mmap.ACCESS_READ) as memory_map:
                for target_pos in target_positions:
                    # Pass the last found boundary to the helper function
                    boundary = _find_boundary_near_target(
                        memory_map,
                        target_pos,
                        file_size,
                        record_begin_bytes,
                        record_end_bytes,
                        window_size_bytes,
                        boundaries[-1], # Pass the previous boundary
                        log_queue
                    )
                    # Only add if it's truly after the previous one (should be handled by helper, but double check)
                    if boundary > boundaries[-1]:
                        boundaries.append(boundary)
                    else:
                        # This indicates a potential issue in _find_boundary_near_target or very dense markers
                        _log_message(f"Warning: Calculated boundary {boundary:,} is not after previous boundary {boundaries[-1]:,}. Skipping.", log_queue)


    except FileNotFoundError: # Should be caught earlier by stat, but keep for safety
        logger.error(f"Error: Input file not found during mmap: {filename}")
        raise
    except ValueError as e: # mmap can raise ValueError for empty files on some OS
        if file_size == 0:
             _log_message("File is empty, cannot memory map.", log_queue)
             return [0, 0]
        else:
            logger.exception(f"ValueError during boundary finding (potentially mmap issue): {e}")
            raise
    except Exception as e:
        logger.exception(f"Error finding boundaries: {e}")
        raise

    # --- Finalize Boundaries ---
    # Ensure file_size is the last boundary
    if not boundaries or boundaries[-1] < file_size:
         boundaries.append(file_size)

    # Remove duplicates and sort (should be mostly sorted already)
    # Filter out boundaries outside the valid range [0, file_size] (safety check)
    valid_boundaries = sorted(list(set(b for b in boundaries if 0 <= b <= file_size)))

    # Ensure 0 is the first boundary if the list isn't empty
    if valid_boundaries and valid_boundaries[0] != 0:
        valid_boundaries.insert(0, 0)
    elif not valid_boundaries and file_size >= 0: # Handle edge case where only [file_size] might remain
        valid_boundaries = [0, file_size] if file_size > 0 else [0, 0]


    _log_message(f"Previewed boundaries ({len(valid_boundaries)-1} potential chunks): {valid_boundaries}", log_queue)
    return valid_boundaries


def chunk_it(
    filename: str,
    num_chunks: int,
    record_begin: str,
    record_end: str,
    output_dir: str = ".",
    log_queue: Optional[queue.Queue] = None
) -> List[str]:
    """
    Chunks the input file into smaller files based on record boundaries.

    First, it calculates the boundaries using `chunk_preview`, then reads
    the data between those boundaries and writes it to separate part files.

    Args:
        filename (str): Path to the input file.
        num_chunks (int): Desired number of chunks (actual number may vary).
        record_begin (str): String marking the beginning of a record.
        record_end (str): String marking the end of a record.
        output_dir (str): Directory to save the chunk files. Defaults to current dir.
                          Will be created if it doesn't exist.
        log_queue (Optional[queue.Queue]): Optional queue for logging in
                                           multiprocessing scenarios.

    Returns:
        List[str]: A list of absolute paths to the created chunk files.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If num_chunks is not positive.
        Exception: For other potential errors during file access or writing.
    """
    _log_message(f"Starting chunking process for '{filename}' into {num_chunks} chunks.", log_queue)
    input_filepath = Path(filename)
    output_path = Path(output_dir)

    # Ensure output directory exists
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        _log_message(f"Ensured output directory exists: '{output_path}'", log_queue)
    except Exception as e:
        logger.error(f"Failed to create output directory '{output_path}': {e}")
        raise

    # 1. Get the boundaries using the preview function
    try:
        boundaries = chunk_preview(filename, num_chunks, record_begin, record_end, log_queue)
    except Exception as e:
        logger.error(f"Failed to determine chunk boundaries for '{filename}': {e}")
        raise # Re-raise after logging

    actual_chunks = len(boundaries) - 1
    if actual_chunks <= 0:
        # This can happen if the file is empty or preview returns [0, 0] or [0]
        _log_message(f"No valid chunks determined for '{filename}'. No files will be created.", log_queue)
        return []

    _log_message(f"Determined {actual_chunks} actual chunks based on boundaries.", log_queue)

    # --- Write Chunks ---
    created_chunk_filepaths: List[Path] = []
    base_filename = input_filepath.name
    buffer_size_bytes = DEFAULT_BUFFER_SIZE_MB * 1024 * 1024

    try:
        with open(input_filepath, 'rb') as input_file_obj:
            for chunk_index in range(actual_chunks):
                start_pos = boundaries[chunk_index]
                end_pos = boundaries[chunk_index+1]

                # Construct output filename using pathlib
                chunk_output_filename = f"{base_filename}.part{chunk_index+1}"
                chunk_output_filepath = output_path / chunk_output_filename

                # Write the chunk using the helper function
                _write_chunk_to_file(
                    input_file_obj,
                    chunk_output_filepath,
                    start_pos,
                    end_pos,
                    buffer_size_bytes,
                    log_queue
                )
                # Only add if the file was likely created (size > 0 check is inside helper)
                # Check existence here to be sure
                if chunk_output_filepath.exists() and chunk_output_filepath.stat().st_size > 0:
                     created_chunk_filepaths.append(chunk_output_filepath)
                elif end_pos - start_pos > 0:
                     _log_message(f"Chunk file '{chunk_output_filepath}' was not created or is empty despite non-zero size.", log_queue)


    except FileNotFoundError: # Should be caught by preview, but safety
        logger.error(f"Error: Input file not found during chunking: {filename}")
        raise
    except Exception as e:
        logger.exception(f"Error during chunk writing process: {e}")
        # Consider cleanup of partially written files? For now, leave them.
        raise

    # Convert Path objects to strings for the return value as per original signature
    created_chunk_filepath_strs = [str(p.resolve()) for p in created_chunk_filepaths]

    _log_message(f"Finished chunking. Created {len(created_chunk_filepath_strs)} files in '{output_path}'.", log_queue)
    return created_chunk_filepath_strs


# Remove the __main__ block as per guidelines (use CLI entry point and pytest)
# if __name__ == "__main__":
#     # ... (old testing code removed) ...
#     pass