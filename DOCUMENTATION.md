# Enterprise AI Agent: Architecture, Source Code & Customization Guide

## 1. Project Overview & Architecture

This project implements an **Autonomous Enterprise AI Agent** in Python powered by Google Gemini foundation models. Unlike standard single-turn LLMs or chatbots, an AI Agent operates in a dynamic **Observation-Reasoning-Action (ReAct)** loop, choosing and executing Python tools autonomously to fulfill complex user instructions.

```text
[User Query] 
     │
     ▼
[Agent Orchestrator (core/agent.py)] ──> [System Prompts & Constraints (core/prompts.py)]
     │
     ▼
[Foundation Model (Gemini Flash)]
     │
     ├── (Tool Needed?) ──> [Execute Python Tool (tools/)] ──> [Observation Result] ──┐
     │                                                                                │
     └── (No Tool Needed / Completed) ────────────────────────────────────────────────┴──> [Final Answer]
```

---

## 2. Directory Layout & Module Responsibilities

```text
Project1/
├── config/
│   ├── __init__.py
│   └── settings.py          # Centralized configuration & environment validation
├── core/
│   ├── __init__.py
│   ├── prompts.py           # Personas, business rules, and safety guardrails
│   └── agent.py             # Agent orchestrator and session lifecycle
├── tools/
│   ├── __init__.py          # Consolidated registry of agent tools
│   ├── system_tools.py      # Datetime, workspace inspection
│   ├── math_tools.py        # Safe calculation engine
│   └── note_tools.py        # Persistent disk storage
├── utils/
│   ├── __init__.py
│   └── logger.py            # Enterprise structured console & file logging
├── .env                     # Local secrets and hyperparameter overrides
├── .env.example             # Clean environment variable template
├── .gitignore               # Secrets, virtual environments, cache exclusion
├── requirements.txt         # Explicit version-pinned Python packages
├── run.bat                  # One-click Windows runner
└── main.py                  # User-facing CLI entrypoint
```

---

## 3. The Developer Customization Manual ("Where to Change What")

### 3.1 Changing the AI Model Brain
* **Where to change**: File `.env` (Variable: `GEMINI_MODEL`)
* **Options**:
  - `gemini-3.5-flash-lite`: ~1.5s latency, ultra fast, great for interactive CLI and tools.
  - `gemini-3.5-flash`: ~6.5s latency, standard model.
  - `gemini-3.7-flash`: Balanced performance.

### 3.2 Changing Tone, Style & Persona
* **Where to change**: File `core/prompts.py` (Variable: `ENTERPRISE_SYSTEM_INSTRUCTION`)

### 3.3 Adding Rules, Constraints & Restrictions
* **Where to change**: File `core/prompts.py`

### 3.4 Adding or Modifying Tools
* **Where to change**:
  1. Add function in `tools/system_tools.py` (or a new module in `tools/`).
  2. Include type hints and Google-style docstrings.
  3. Register the function in `tools/__init__.py` inside `ALL_TOOLS`.

### 3.5 Tuning Algorithm & Hyperparameters
* **Where to change**: `.env` (`AGENT_TEMPERATURE=0.2`) and `core/agent.py` (`types.ThinkingConfig(thinking_budget=0)`).

### 3.6 Adjusting Logging & Observability
* **Where to change**: `.env` (`LOG_LEVEL=INFO` or `DEBUG`).

---

## 4. Troubleshooting Guide

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'core.prompts'` | Filename typo (e.g. `promts.py`). | Rename to `core/prompts.py`. |
| `404 NOT_FOUND` | Retired model checkpoint. | Change `GEMINI_MODEL=gemini-3.5-flash-lite` in `.env`. |
| `503 UNAVAILABLE` | Temporary cloud spike. | Retry or swap model in `.env`. |
| `[Errno 11001]` | Network/firewall issue. | Check internet connection. |

---

## 5. Complete Source Code by File

### 5.1 `config/settings.py`
```python
import os
import sys
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    MODEL_NAME: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    TEMPERATURE: float = float(os.getenv("AGENT_TEMPERATURE", "0.2"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    @classmethod
    def validate(cls):
        """Validates critical enterprise configurations before launching."""
        if not cls.API_KEY or cls.API_KEY == "your_gemini_api_key_here":
            print("[CRITICAL] GEMINI_API_KEY is not set in environment or .env file.")
            print("[CRITICAL] Please configure your key in .env before running.")
            sys.exit(1)

settings = Settings()
```

### 5.2 `utils/logger.py`
```python
import logging
import sys
from config.settings import settings

def setup_logger(name: str = "AIAgent") -> logging.Logger:
    """Configures structured enterprise console logging."""
    logger = logging.getLogger(name)
    level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-7s | [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = setup_logger()
```

### 5.3 `tools/system_tools.py`
```python
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
```

### 5.4 `tools/math_tools.py`
```python
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
```

### 5.5 `tools/note_tools.py`
```python
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
```

### 5.6 `tools/__init__.py`
```python
from .system_tools import get_current_time, list_workspace_files
from .math_tools import calculate
from .note_tools import save_note

ALL_TOOLS = [
    get_current_time,
    list_workspace_files,
    calculate,
    save_note,
]
```

### 5.7 `core/prompts.py`
```python
ENTERPRISE_SYSTEM_INSTRUCTION = """
You are an Enterprise AI Assistant designed to assist team members with automation, calculations, and local workspace tasks.

Operational Guidelines:
1. Always utilize available tools whenever real-time data, math, or file operations are required.
2. Provide clear, professional, and concise answers.
3. If an action is outside your granted tool capabilities, clearly inform the user what you can and cannot do.
4. Maintain a polite and collaborative tone at all times.
"""
```

### 5.8 `core/agent.py`
```python
from google import genai
from google.genai import types
from config.settings import settings
from utils.logger import logger
from core.prompts import ENTERPRISE_SYSTEM_INSTRUCTION
from tools import ALL_TOOLS

class EnterpriseAgent:
    """Manages the lifecycle of an autonomous AI Agent."""

    def __init__(self):
        settings.validate()
        
        logger.info("Initializing Gemini Client (Model: %s, Temperature: %s)", 
                    settings.MODEL_NAME, settings.TEMPERATURE)
        self.client = genai.Client(api_key=settings.API_KEY)
        
        self.chat = self.client.chats.create(
            model=settings.MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=ENTERPRISE_SYSTEM_INSTRUCTION,
                temperature=settings.TEMPERATURE,
                tools=ALL_TOOLS,
            )
        )
        logger.info("Agent initialized with %d registered tools.", len(ALL_TOOLS))

    def ask(self, message: str) -> str:
        """Sends a message to the agent and returns the final synthesized response."""
        logger.info("User prompt received: '%s'", message)
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            logger.error("Error during agent execution: %s", e)
            raise e
```

### 5.9 `main.py`
```python
import sys
from core.agent import EnterpriseAgent
from utils.logger import logger

def main():
    try:
        agent = EnterpriseAgent()
    except Exception as e:
        logger.critical("Failed to start agent: %s", e)
        sys.exit(1)

    print("\n" + "=" * 65)
    print("🏢 Enterprise AI Agent CLI Ready")
    print("Type your request below, or type 'exit' / 'quit' to close.")
    print("=" * 65 + "\n")

    while True:
        try:
            user_input = input("You > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("\nSession ended. Have a productive day!")
                break

            response = agent.ask(user_input)
            print(f"\nAgent > {response}\n")

        except KeyboardInterrupt:
            print("\nSession interrupted.")
            break
        except Exception as e:
            print(f"\n[!] Error: {e}\n")

if __name__ == "__main__":
    main()
```

### 5.10 `requirements.txt`
```text
google-genai>=3.0.0
python-dotenv>=1.0.0
python-docx>=1.2.0
```

### 5.11 `.env.example`
```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite

# Agent Hyperparameters
AGENT_TEMPERATURE=0.2
LOG_LEVEL=INFO
```

### 5.12 `run.bat`
```bat
@echo off
echo Starting AI Agent...
"%~dp0venv\Scripts\python.exe" "%~dp0main.py"
pause
```
