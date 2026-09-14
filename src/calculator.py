"""Calculator module for arithmetic operations with comprehensive logging."""

import math
from src.exceptions import CalculationError
from src.logger_config import get_logger

logger = get_logger("calculator")


def add(a: float, b: float) -> float:
    """Adds two numbers."""
    logger.debug("Performing addition: %s + %s", a, b)
    result = a + b
    logger.info("Calculation completed: %s + %s = %s", a, b, result)
    return result


def subtract(a: float, b: float) -> float:
    """Subtracts b from a."""
    logger.debug("Performing subtraction: %s - %s", a, b)
    result = a - b
    logger.info("Calculation completed: %s - %s = %s", a, b, result)
    return result


def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    logger.debug("Performing multiplication: %s * %s", a, b)
    if a == 0 or b == 0:
        logger.warning("Multiplication with zero results in zero (operands: %s, %s)", a, b)
    result = a * b
    logger.info("Calculation completed: %s * %s = %s", a, b, result)
    return result


def divide(a: float, b: float) -> float:
    """
    Divides a by b.
    
    Logs ERROR and raises CalculationError if b == 0.
    """
    logger.debug("Performing division: %s / %s", a, b)
    if b == 0:
        logger.error("Division by zero attempted: %s / %s", a, b)
        raise CalculationError("Cannot divide by zero.")
    
    result = a / b
    logger.info("Calculation completed: %s / %s = %s", a, b, result)
    return result


def power(base: float, exponent: float) -> float:
    """Raises base to the exponent."""
    logger.debug("Performing exponentiation: %s ^ %s", base, exponent)
    if exponent > 1000 or exponent < -1000:
        logger.warning("Large exponent detected (%s), potential overflow risk", exponent)
    try:
        result = math.pow(base, exponent)
    except OverflowError as exc:
        logger.error("Calculation overflow error: %s ^ %s: %s", base, exponent, exc)
        raise CalculationError(f"Calculation overflow: {exc}") from exc
    except ValueError as exc:
        logger.error("Invalid math domain for power: %s ^ %s: %s", base, exponent, exc)
        raise CalculationError(f"Math domain error: {exc}") from exc

    logger.info("Calculation completed: %s ^ %s = %s", base, exponent, result)
    return result


def square_root(a: float) -> float:
    """
    Computes square root of a number.
    Logs ERROR and raises CalculationError if a < 0.
    """
    logger.debug("Performing square root: sqrt(%s)", a)
    if a < 0:
        logger.error("Square root of negative number attempted: sqrt(%s)", a)
        raise CalculationError("Cannot calculate square root of a negative number in real domain.")

    result = math.sqrt(a)
    logger.info("Calculation completed: sqrt(%s) = %s", a, result)
    return result


def calculate(operation: str, *operands: float) -> float:
    """
    Generic dispatcher for calculator operations.
    
    Operations: 'add', 'subtract', 'multiply', 'divide', 'power', 'sqrt'
    """
    op = operation.strip().lower()
    logger.debug("Calculating operation '%s' with operands: %s", op, operands)

    if op in ("add", "+", "1"):
        if len(operands) != 2:
            logger.error("Addition requires exactly 2 operands, got %d", len(operands))
            raise CalculationError("Addition requires 2 numbers.")
        return add(operands[0], operands[1])

    elif op in ("subtract", "-", "2"):
        if len(operands) != 2:
            logger.error("Subtraction requires exactly 2 operands, got %d", len(operands))
            raise CalculationError("Subtraction requires 2 numbers.")
        return subtract(operands[0], operands[1])

    elif op in ("multiply", "*", "3"):
        if len(operands) != 2:
            logger.error("Multiplication requires exactly 2 operands, got %d", len(operands))
            raise CalculationError("Multiplication requires 2 numbers.")
        return multiply(operands[0], operands[1])

    elif op in ("divide", "/", "4"):
        if len(operands) != 2:
            logger.error("Division requires exactly 2 operands, got %d", len(operands))
            raise CalculationError("Division requires 2 numbers.")
        return divide(operands[0], operands[1])

    elif op in ("power", "^", "**", "5"):
        if len(operands) != 2:
            logger.error("Power requires exactly 2 operands (base, exponent), got %d", len(operands))
            raise CalculationError("Power operation requires base and exponent.")
        return power(operands[0], operands[1])

    elif op in ("sqrt", "square_root", "6"):
        if len(operands) != 1:
            logger.error("Square root requires exactly 1 operand, got %d", len(operands))
            raise CalculationError("Square root requires 1 number.")
        return square_root(operands[0])

    else:
        logger.error("Invalid calculation operation requested: '%s'", op)
        raise CalculationError(f"Unsupported operation: '{operation}'")
