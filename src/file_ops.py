"""File operations module with comprehensive logging and error handling."""

import os
from pathlib import Path
from src.exceptions import FileOperationError
from src.logger_config import get_logger

logger = get_logger("file_ops")


def read_file(file_path: str | Path) -> str:
    """
    Reads the content of a file.
    
    Logs:
    - DEBUG: Attempting to read file
    - INFO: File read successfully
    - WARNING: File was empty
    - ERROR: File could not be opened
    """
    path = Path(file_path)
    logger.debug("Opening file for reading: '%s'", path)

    if not path.exists():
        logger.error("File could not be opened: '%s' (File not found)", path)
        raise FileOperationError(f"File not found: '{path}'")

    if not path.is_file():
        logger.error("File could not be opened: '%s' (Target is not a regular file)", path)
        raise FileOperationError(f"Target is not a file: '{path}'")

    try:
        content = path.read_text(encoding="utf-8")
    except PermissionError as exc:
        logger.error("File could not be opened: '%s' (Permission denied: %s)", path, exc)
        raise FileOperationError(f"Permission denied: '{path}'") from exc
    except UnicodeDecodeError as exc:
        logger.error("File could not be opened: '%s' (Unicode decode error: %s)", path, exc)
        raise FileOperationError(f"Cannot decode file as UTF-8 text: '{path}'") from exc
    except Exception as exc:
        logger.error("File could not be opened: '%s' (%s)", path, exc)
        raise FileOperationError(f"Error reading file '{path}': {exc}") from exc

    if len(content.strip()) == 0:
        logger.warning("File was empty: '%s'", path)
    else:
        logger.info("File read successfully: '%s' (%d bytes, %d characters)", path, path.stat().st_size, len(content))

    return content


def write_file(file_path: str | Path, content: str, mode: str = "w") -> int:
    """
    Writes content to a file.
    
    Logs:
    - DEBUG: Attempting to write file
    - INFO: File written successfully
    - WARNING: File written with empty content
    - ERROR: File could not be written
    """
    path = Path(file_path)
    logger.debug("Opening file for writing (mode='%s'): '%s'", mode, path)

    try:
        # Create parent directories if they don't exist
        if path.parent and not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            logger.debug("Created parent directories for: '%s'", path)

        if mode == "a":
            with open(path, "a", encoding="utf-8") as f:
                bytes_written = f.write(content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                bytes_written = f.write(content)

    except PermissionError as exc:
        logger.error("File could not be written: '%s' (Permission denied: %s)", path, exc)
        raise FileOperationError(f"Permission denied when writing to '{path}'") from exc
    except Exception as exc:
        logger.error("File could not be written: '%s' (%s)", path, exc)
        raise FileOperationError(f"Error writing to file '{path}': {exc}") from exc

    if len(content) == 0:
        logger.warning("File was empty or written with empty content: '%s'", path)
    else:
        logger.info("File written successfully: '%s' (%d characters written)", path, bytes_written)

    return bytes_written
