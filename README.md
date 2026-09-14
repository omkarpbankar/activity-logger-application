# Activity Logger Application

A modular, menu-driven Python application demonstrating professional multi-level logging (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`), separated into clean modules with resilient exception handling.

---

## Features & Menu Options

1. **Login**: Authenticate users against credentials, track active sessions, log logins, and prevent multiple duplicate sessions.
2. **Calculate**: Perform arithmetic operations (Addition, Subtraction, Multiplication, Division, Exponentiation, Square Root) with input validation and zero-division protection.
3. **Read a File**: Read text files safely with automatic warnings for empty files and error logging for missing/inaccessible files.
4. **Write a File**: Write or append content to files, automatically ensuring directory hierarchy creation.
5. **Logout**: Safely terminate active user sessions.
6. **Trigger Critical Error Demo**: Demonstrate `CRITICAL` logging and verify that unexpected failures are handled without crashing the application.
7. **Exit**: Gracefully terminate the application.

---

## Logging Architecture

Logs are stored inside the `logs/` directory:
- **`logs/application.log`**: Captures all events across levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
- **`logs/error.log`**: Captures only high-severity events (`ERROR` and `CRITICAL`) with detailed exception tracebacks.

### Log Levels & Example Outputs

| Level | Description | Example Event |
|---|---|---|
| **DEBUG** | Diagnostic and step-by-step internal state details | `Checking credentials for user 'admin'` |
| **INFO** | Confirming expected regular operational milestones | `INFO User 'admin' logged in`<br>`INFO Calculation completed: 25.0 + 75.0 = 100.0`<br>`INFO File read successfully`<br>`INFO File written successfully`<br>`INFO User 'admin' logged out` |
| **WARNING** | Unexpected situations or degraded conditions that don't block operation | `WARNING File was empty: 'sample_files/empty.txt'`<br>`WARNING Login rejected: Username cannot be empty` |
| **ERROR** | Operation-level failures that prevent completing a specific task | `ERROR File could not be opened: 'sample_files/missing.txt' (File not found)`<br>`ERROR Division by zero attempted: 10.0 / 0.0` |
| **CRITICAL** | Severe / unexpected system faults captured by resilience handlers | `CRITICAL Unexpected application failure: Simulated hardware bus or memory fault` |

---

## Project Structure

```
activity-logger-application/
├── logs/
│   ├── application.log      # All log records (DEBUG to CRITICAL)
│   └── error.log            # Filtered log records (ERROR & CRITICAL only)
├── sample_files/
│   ├── welcome.txt          # Sample text file for read operations
│   ├── empty.txt            # Empty file for WARNING demonstration
│   └── demo_output.txt      # Sample output target for write operations
├── src/
│   ├── __init__.py          # Package initialization
│   ├── app.py               # Menu UI, user interaction loop & top-level exception guards
│   ├── auth.py              # User authentication & session management module
│   ├── calculator.py        # Arithmetic calculations & math validation module
│   ├── exceptions.py        # Custom exception hierarchy
│   ├── file_ops.py          # File reading and writing operations
│   └── logger_config.py     # Centralized logging setup, handlers, and formatters
├── tests/
│   ├── __init__.py          # Test package
│   ├── test_auth.py         # Unit tests for authentication
│   ├── test_calculator.py   # Unit tests for calculator
│   ├── test_file_ops.py     # Unit tests for file operations
│   └── test_logging.py      # Unit tests for logging channels & levels
├── main.py                  # Application entrypoint
└── README.md                # Project documentation
```

---

## Getting Started

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.12)

### 2. Running the Application
Launch the menu-driven application:
```bash
python main.py
```

Demo Credentials:
- `admin` / `admin123`
- `alice` / `secret456`
- `omkar` / `password789`

### 3. Running the Automated Test Suite
Execute all unit tests covering all modules and logging verifications:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## Exception Handling & Fault Tolerance

Every operation is wrapped with layered exception handling:
1. **Module Level**: Specific exceptions (e.g. `AuthenticationError`, `CalculationError`, `FileOperationError`) are raised and logged with appropriate severity.
2. **Action Level**: Handlers in `src/app.py` catch operational exceptions and inform the user cleanly without interrupting the flow.
3. **Application Loop Level**: The top-level menu loop contains an outer safety guard that intercepts any unhandled runtime exceptions, logs them as `CRITICAL`, and keeps the application alive.
