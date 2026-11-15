from utils.logger import logger

def calculate(expression: str) -> str:
    """Safely evaluates a basic mathematical expression (e.g., '14 * 25 + 10')."""
    try:
        allowed = set("0123456789+-*/(). %")
        if not set(expression).issubset(allowed):
            logger.warning("calculate rejected due to invalid characters: %s", expression)
            return "Error: Unsupported characters in mathematical expression."
        
        result = eval(expression, {"__builtins__": None}, {})
        logger.info("Tool executed: calculate('%s') = %s", expression, result)
        return f"Result: {result}"
    except Exception as e:
        logger.error("calculate failed on expression '%s': %s", expression, e)
        return f"Math error: {str(e)}"