from utils.logger import logger

def save_note(title: str, content: str) -> str:
    """Persists a text note to a file on disk."""
    try:
        filename = f"{title.replace(' ', '_').lower()}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("Tool executed: save_note -> saved '%s'", filename)
        return f"Note successfully saved as '{filename}'."
    except Exception as e:
        logger.error("save_note failed for title '%s': %s", title, e)
        return f"Error saving note: {str(e)}"