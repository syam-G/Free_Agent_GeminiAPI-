import os
import datetime
from utils.logger import logger

def get_current_time() -> str:
    """Returns the current date, time, and day of the week."""
    now = datetime.datetime.now()
    timestamp = now.strftime("%A, %Y-%m-%d %H:%M:%S")
    logger.info("Tool executed: get_current_time -> %s", timestamp)
    return timestamp

def list_workspace_files() -> list:
    """Returns a list of visible files in the current working directory."""
    try:
        files = os.listdir(".")
        visible = [f for f in files if not f.startswith(".") and f != "venv"]
        logger.info("Tool executed: list_workspace_files -> found %d items", len(visible))
        return visible
    except Exception as e:
        logger.error("Tool failure in list_workspace_files: %s", e)
        return [f"Error: {str(e)}"]