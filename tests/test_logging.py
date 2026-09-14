"""Tests for logging configuration, log file generation, and log level routing."""

import logging
import tempfile
import unittest
from pathlib import Path

from src import auth, calculator, file_ops
from src.exceptions import AuthenticationError, CalculationError, FileOperationError
from src.logger_config import setup_logging, get_logger


class TestLogging(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_dir = Path(self.temp_dir.name) / "logs"
        self.root_logger = setup_logging(log_dir=self.log_dir)
        auth.reset_session()

    def tearDown(self):
        # Close all handlers before directory cleanup
        for handler in list(self.root_logger.handlers):
            handler.close()
            self.root_logger.removeHandler(handler)
        self.temp_dir.cleanup()

    def _get_app_log_content(self) -> str:
        app_log = self.log_dir / "application.log"
        for handler in self.root_logger.handlers:
            handler.flush()
        if app_log.exists():
            return app_log.read_text(encoding="utf-8")
        return ""

    def _get_err_log_content(self) -> str:
        err_log = self.log_dir / "error.log"
        for handler in self.root_logger.handlers:
            handler.flush()
        if err_log.exists():
            return err_log.read_text(encoding="utf-8")
        return ""

    def test_all_five_log_levels(self):
        logger = get_logger("test_levels")
        
        logger.debug("Sample DEBUG level message")
        logger.info("Sample INFO level message")
        logger.warning("Sample WARNING level message")
        logger.error("Sample ERROR level message")
        logger.critical("Sample CRITICAL level message")

        app_content = self._get_app_log_content()
        err_content = self._get_err_log_content()

        # application.log must have all 5 levels
        self.assertIn("[DEBUG]", app_content)
        self.assertIn("Sample DEBUG level message", app_content)
        self.assertIn("[INFO]", app_content)
        self.assertIn("Sample INFO level message", app_content)
        self.assertIn("[WARNING]", app_content)
        self.assertIn("Sample WARNING level message", app_content)
        self.assertIn("[ERROR]", app_content)
        self.assertIn("Sample ERROR level message", app_content)
        self.assertIn("[CRITICAL]", app_content)
        self.assertIn("Sample CRITICAL level message", app_content)

        # error.log must ONLY have ERROR and CRITICAL
        self.assertNotIn("[DEBUG]", err_content)
        self.assertNotIn("[INFO]", err_content)
        self.assertNotIn("[WARNING]", err_content)
        self.assertIn("[ERROR]", err_content)
        self.assertIn("Sample ERROR level message", err_content)
        self.assertIn("[CRITICAL]", err_content)
        self.assertIn("Sample CRITICAL level message", err_content)

    def test_auth_logging_info_and_warning(self):
        # Successful login -> INFO User logged in
        auth.login("admin", "admin123")
        app_content = self._get_app_log_content()
        self.assertIn("INFO", app_content)
        self.assertIn("User 'admin' logged in", app_content)

        # Logout -> INFO User logged out
        auth.logout()
        app_content = self._get_app_log_content()
        self.assertIn("User 'admin' logged out", app_content)

        # Failed login -> WARNING
        with self.assertRaises(AuthenticationError):
            auth.login("admin", "wrong_password")
        app_content = self._get_app_log_content()
        self.assertIn("WARNING", app_content)
        self.assertIn("Invalid password provided for user 'admin'", app_content)

    def test_calculator_logging_info_and_error(self):
        # Calculation completed -> INFO
        calculator.calculate("add", 15, 30)
        app_content = self._get_app_log_content()
        self.assertIn("Calculation completed", app_content)
        self.assertIn("15", app_content)

        # Division by zero -> ERROR
        with self.assertRaises(CalculationError):
            calculator.calculate("divide", 50, 0)
        
        app_content = self._get_app_log_content()
        err_content = self._get_err_log_content()
        self.assertIn("Division by zero attempted", app_content)
        self.assertIn("Division by zero attempted", err_content)

    def test_file_ops_logging_warning_and_error(self):
        temp_file = Path(self.temp_dir.name) / "test_empty.txt"
        temp_file.touch()

        # Read empty file -> WARNING File was empty
        file_ops.read_file(temp_file)
        app_content = self._get_app_log_content()
        self.assertIn("WARNING", app_content)
        self.assertIn("File was empty", app_content)

        # Read missing file -> ERROR File could not be opened
        missing_file = Path(self.temp_dir.name) / "missing_file_xyz.txt"
        with self.assertRaises(FileOperationError):
            file_ops.read_file(missing_file)

        app_content = self._get_app_log_content()
        err_content = self._get_err_log_content()
        self.assertIn("File could not be opened", app_content)
        self.assertIn("File could not be opened", err_content)

    def test_critical_logging(self):
        logger = get_logger("critical_test")
        try:
            raise RuntimeError("Corrupted database memory index")
        except RuntimeError as exc:
            logger.critical("Unexpected application failure: %s", exc, exc_info=True)

        app_content = self._get_app_log_content()
        err_content = self._get_err_log_content()

        self.assertIn("CRITICAL", app_content)
        self.assertIn("Unexpected application failure", app_content)
        self.assertIn("CRITICAL", err_content)
        self.assertIn("Unexpected application failure", err_content)
        self.assertIn("RuntimeError: Corrupted database memory index", err_content)


if __name__ == "__main__":
    unittest.main()
