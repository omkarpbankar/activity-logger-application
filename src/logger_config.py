"""Logging configuration for the Activity Logger Application."""

import logging
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_LOG_DIR = BASE_DIR / "logs"
APPLICATION_LOG_FILE = "application.log"
ERROR_LOG_FILE = "error.log"

_is_configured = False


def setup_logging(
    log_dir: str | Path | None = None,
    console_output: bool = False,
    log_level: int = logging.DEBUG,
) -> logging.Logger:
    """
    Configures and returns the root logger for the application.
    
    Creates:
    - application.log: logs DEBUG, INFO, WARNING, ERROR, CRITICAL
    - error.log: logs ERROR and CRITICAL
    
    Args:
        log_dir: Directory where log files are stored. Defaults to 'logs/'.
        console_output: If True, attaches a StreamHandler to console.
        log_level: Base logging level (default DEBUG).
        
    Returns:
        The configured root logger.
    """
    global _is_configured

    target_dir = Path(log_dir) if log_dir else DEFAULT_LOG_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    app_log_path = target_dir / APPLICATION_LOG_FILE
    err_log_path = target_dir / ERROR_LOG_FILE

    root_logger = logging.getLogger("activity_logger")
    root_logger.setLevel(log_level)

    # Close and clear existing handlers to prevent duplicate logs on multiple setups
    if root_logger.hasHandlers():
        for handler in list(root_logger.handlers):
            handler.close()
        root_logger.handlers.clear()

    # Formatter for log files
    formatter = logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 1. Application Log Handler (DEBUG and above)
    app_handler = logging.FileHandler(app_log_path, encoding="utf-8")
    app_handler.setLevel(logging.DEBUG)
    app_handler.setFormatter(formatter)
    root_logger.addHandler(app_handler)

    # 2. Error Log Handler (ERROR and CRITICAL)
    err_handler = logging.FileHandler(err_log_path, encoding="utf-8")
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(formatter)
    root_logger.addHandler(err_handler)

    # 3. Optional Console Handler (useful for CLI/Debugging)
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

    _is_configured = True
    return root_logger


def get_logger(module_name: str) -> logging.Logger:
    """
    Returns a child logger under the 'activity_logger' namespace.
    Ensures logging is initialized before returning.
    """
    if not _is_configured:
        setup_logging()
    
    # Strip any redundant parent prefixes if passed
    if module_name.startswith("activity_logger."):
        clean_name = module_name
    elif module_name == "activity_logger":
        clean_name = "activity_logger"
    else:
        clean_name = f"activity_logger.{module_name}"
        
    return logging.getLogger(clean_name)
