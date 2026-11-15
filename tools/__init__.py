from .system_tools import get_current_time, list_workspace_files
from .math_tools import calculate
from .note_tools import save_note

# Consolidated tool registry for the agent
ALL_TOOLS = [
    get_current_time,
    list_workspace_files,
    calculate,
    save_note,
]