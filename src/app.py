"""Main application menu loop and orchestration module."""

import sys
from src.exceptions import (
    ActivityLoggerError,
    AuthenticationError,
    CalculationError,
    FileOperationError,
    CriticalSystemError,
)
from src.logger_config import setup_logging, get_logger
import src.auth as auth
import src.calculator as calculator
import src.file_ops as file_ops

logger = get_logger("app")


def print_banner() -> None:
    """Prints application header banner."""
    print("\n" + "=" * 55)
    print("        ACTIVITY LOGGER APPLICATION")
    print("=" * 55)


def display_menu() -> None:
    """Displays the menu options with current session state."""
    current_user = auth.get_current_user()
    status = f"Logged in as: [{current_user}]" if current_user else "Status: [Not Logged In]"
    
    print("\n" + "-" * 55)
    print(f"  {status}")
    print("-" * 55)
    print("  1. Login")
    print("  2. Calculate")
    print("  3. Read a File")
    print("  4. Write a File")
    print("  5. Logout")
    print("  6. Trigger Unexpected Critical Failure (Demo)")
    print("  7. Exit Application")
    print("-" * 55)


def handle_login() -> None:
    """Handles user login workflow with exception safety."""
    print("\n--- [1] User Login ---")
    if auth.is_authenticated():
        print(f"[!] Already logged in as '{auth.get_current_user()}'. Please logout first.")
        return

    username = input("Enter username (demo users: admin, alice, omkar): ").strip()
    password = input("Enter password (demo: admin123, secret456, password789): ")

    try:
        success = auth.login(username, password)
        if success:
            print(f"[OK] Successfully logged in as '{username}'.")
        else:
            print("[!] Login could not be completed.")
    except AuthenticationError as exc:
        print(f"[ERROR] Login failed: {exc}")
    except Exception as exc:
        logger.critical("Unexpected application failure during login: %s", exc, exc_info=True)
        print(f"[ERROR] Unexpected error during login: {exc}")


def handle_calculate() -> None:
    """Handles calculator workflow with exception safety."""
    print("\n--- [2] Calculate ---")
    print("Operations:")
    print("  1. Addition (+)")
    print("  2. Subtraction (-)")
    print("  3. Multiplication (*)")
    print("  4. Division (/)")
    print("  5. Exponentiation (^)")
    print("  6. Square Root (sqrt)")

    op_choice = input("Select operation (1-6): ").strip()

    if op_choice not in ("1", "2", "3", "4", "5", "6", "add", "subtract", "multiply", "divide", "power", "sqrt", "+", "-", "*", "/"):
        logger.warning("Invalid calculation operation selected by user: '%s'", op_choice)
        print("[!] Invalid operation choice.")
        return

    try:
        if op_choice in ("6", "sqrt"):
            raw_val = input("Enter number: ").strip()
            try:
                val = float(raw_val)
            except ValueError:
                logger.warning("Invalid numeric input provided for square root: '%s'", raw_val)
                print(f"[!] '{raw_val}' is not a valid number.")
                return
            result = calculator.calculate("sqrt", val)
            print(f"[OK] Result: sqrt({val}) = {result}")
        else:
            raw_a = input("Enter first number: ").strip()
            raw_b = input("Enter second number: ").strip()
            try:
                val_a = float(raw_a)
                val_b = float(raw_b)
            except ValueError:
                logger.warning("Invalid numeric inputs provided: '%s', '%s'", raw_a, raw_b)
                print("[!] Both inputs must be valid numbers.")
                return

            op_map = {
                "1": "add", "+": "add", "add": "add",
                "2": "subtract", "-": "subtract", "subtract": "subtract",
                "3": "multiply", "*": "multiply", "multiply": "multiply",
                "4": "divide", "/": "divide", "divide": "divide",
                "5": "power", "^": "power", "power": "power",
            }
            op_name = op_map.get(op_choice, op_choice)
            result = calculator.calculate(op_name, val_a, val_b)
            print(f"[OK] Result: {val_a} {op_name} {val_b} = {result}")

    except CalculationError as exc:
        print(f"[ERROR] Calculation error: {exc}")
    except Exception as exc:
        logger.critical("Unexpected application failure during calculation: %s", exc, exc_info=True)
        print(f"[ERROR] An unexpected calculation error occurred: {exc}")


def handle_read_file() -> None:
    """Handles file reading workflow with exception safety."""
    print("\n--- [3] Read a File ---")
    path_input = input("Enter file path to read (e.g. sample_files/welcome.txt): ").strip()
    
    if not path_input:
        logger.warning("Empty file path entered for read operation")
        print("[!] File path cannot be empty.")
        return

    try:
        content = file_ops.read_file(path_input)
        if not content.strip():
            print(f"[!] Warning: File '{path_input}' was empty.")
        else:
            print(f"\n[OK] File Content ({path_input}):")
            print("-" * 40)
            print(content)
            print("-" * 40)
    except FileOperationError as exc:
        print(f"[ERROR] Read failed: {exc}")
    except Exception as exc:
        logger.critical("Unexpected application failure during file read: %s", exc, exc_info=True)
        print(f"[ERROR] An unexpected file error occurred: {exc}")


def handle_write_file() -> None:
    """Handles file writing workflow with exception safety."""
    print("\n--- [4] Write a File ---")
    path_input = input("Enter file path to write (e.g. sample_files/output.txt): ").strip()

    if not path_input:
        logger.warning("Empty file path entered for write operation")
        print("[!] File path cannot be empty.")
        return

    print("Choose write mode:")
    print("  1. Overwrite ('w')")
    print("  2. Append ('a')")
    mode_choice = input("Select mode [1/2] (default 1): ").strip()
    mode = "a" if mode_choice == "2" else "w"

    content = input("Enter content to write into file (press Enter directly for empty content): ")

    try:
        bytes_written = file_ops.write_file(path_input, content, mode=mode)
        print(f"[OK] Successfully wrote {bytes_written} characters to '{path_input}'.")
    except FileOperationError as exc:
        print(f"[ERROR] Write failed: {exc}")
    except Exception as exc:
        logger.critical("Unexpected application failure during file write: %s", exc, exc_info=True)
        print(f"[ERROR] An unexpected write error occurred: {exc}")


def handle_logout() -> None:
    """Handles user logout workflow with exception safety."""
    print("\n--- [5] User Logout ---")
    try:
        success = auth.logout()
        if success:
            print("[OK] Successfully logged out.")
        else:
            print("[!] No active user was logged in.")
    except Exception as exc:
        logger.critical("Unexpected application failure during logout: %s", exc, exc_info=True)
        print(f"[ERROR] Unexpected logout error: {exc}")


def handle_critical_demo() -> None:
    """Simulates an unexpected critical system failure to demonstrate CRITICAL logging."""
    print("\n--- [6] Simulate Unexpected Critical Failure ---")
    try:
        logger.debug("Simulating fatal system exception...")
        raise CriticalSystemError("Simulated hardware bus or memory fault in core processing engine.")
    except Exception as exc:
        logger.critical("Unexpected application failure: %s", exc, exc_info=True)
        print(f"[!] Simulated Critical Error Captured: '{exc}'")
        print("[OK] Exception handled gracefully. Application will NOT terminate.")


def run_app() -> None:
    """Main application loop with top-level error immunity."""
    setup_logging()
    logger.info("Activity Logger Application initialized")
    print_banner()

    while True:
        try:
            display_menu()
            choice = input("Enter choice (1-7): ").strip()

            if choice == "1":
                handle_login()
            elif choice == "2":
                handle_calculate()
            elif choice == "3":
                handle_read_file()
            elif choice == "4":
                handle_write_file()
            elif choice == "5":
                handle_logout()
            elif choice == "6":
                handle_critical_demo()
            elif choice == "7":
                logger.info("User requested application exit. Shutting down gracefully.")
                print("\n[OK] Thank you for using Activity Logger. Goodbye!")
                break
            else:
                logger.warning("User entered unrecognized menu option: '%s'", choice)
                print(f"[!] Invalid option '{choice}'. Please select a number between 1 and 7.")

        except KeyboardInterrupt:
            logger.warning("Application interrupted by KeyboardInterrupt (Ctrl+C)")
            print("\n\n[!] Application interrupted. Exiting cleanly.")
            break
        except Exception as exc:
            # Top-level safety net: application will never crash completely on unexpected errors
            logger.critical("Unexpected application failure: %s", exc, exc_info=True)
            print(f"\n[CRITICAL ERROR] An unhandled exception occurred: {exc}")
            print("[OK] Top-level handler recovered the session. Continuing execution...\n")


if __name__ == "__main__":
    run_app()
