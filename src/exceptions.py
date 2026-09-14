"""Custom exception classes for Activity Logger Application."""


class ActivityLoggerError(Exception):
    """Base exception for the application."""
    pass


class AuthenticationError(ActivityLoggerError):
    """Raised when authentication fails."""
    pass


class CalculationError(ActivityLoggerError):
    """Raised when a calculation operation fails."""
    pass


class FileOperationError(ActivityLoggerError):
    """Raised when file reading or writing fails."""
    pass


class CriticalSystemError(ActivityLoggerError):
    """Raised to simulate unexpected critical system failure."""
    pass
