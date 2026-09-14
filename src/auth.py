"""Authentication module for user login and session management."""

from src.exceptions import AuthenticationError
from src.logger_config import get_logger

logger = get_logger("auth")

# In-memory mock user database
_USERS_DB = {
    "admin": "admin123",
    "alice": "secret456",
    "omkar": "password789",
    "guest": "guestpass",
}

# Session state
_current_user: str | None = None


def login(username: str, password: str) -> bool:
    """
    Authenticates a user and starts a new session.
    
    Logs:
    - DEBUG: Checking credentials
    - INFO: User logged in
    - WARNING: Failed login attempt or already logged in
    """
    global _current_user

    clean_username = username.strip() if username else ""

    if _current_user is not None:
        logger.warning(
            "Login rejected: User '%s' is already logged in. Please logout first.",
            _current_user,
        )
        return False

    if not clean_username:
        logger.warning("Login rejected: Username cannot be empty")
        raise AuthenticationError("Username cannot be empty.")

    logger.debug("Checking credentials for user '%s'", clean_username)

    if clean_username not in _USERS_DB:
        logger.warning(
            "Failed login attempt: User '%s' not found in database", clean_username
        )
        raise AuthenticationError(f"User '{clean_username}' does not exist.")

    if _USERS_DB[clean_username] != password:
        logger.warning(
            "Failed login attempt: Invalid password provided for user '%s'",
            clean_username,
        )
        raise AuthenticationError("Invalid password provided.")

    _current_user = clean_username
    logger.info("User '%s' logged in", clean_username)
    return True


def logout() -> bool:
    """
    Logs out the current active user session.
    
    Logs:
    - INFO: User logged out
    - WARNING: No active user to logout
    """
    global _current_user

    if _current_user is None:
        logger.warning("Logout attempted with no active session")
        return False

    logged_out_user = _current_user
    _current_user = None
    logger.info("User '%s' logged out", logged_out_user)
    return True


def get_current_user() -> str | None:
    """Returns the currently logged-in username or None."""
    return _current_user


def is_authenticated() -> bool:
    """Checks if a user is currently logged in."""
    return _current_user is not None


def reset_session() -> None:
    """Resets the authentication session state (used for testing/cleanup)."""
    global _current_user
    _current_user = None
