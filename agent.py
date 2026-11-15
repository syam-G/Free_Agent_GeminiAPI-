"""
My First AI Agent
-----------------
An autonomous AI agent using Google Gemini (Free Tier) and Python.
Demonstrates:
1. Brain: Gemini 2.5 Flash foundation model.
2. Persona / System Prompt: Defines role, constraints, and instructions.
3. Tools: Custom Python functions the agent can autonomously call.
4. ReAct Loop: Model decides when to use tools, inspects outputs, and answers.
"""

import os
import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY == "your_api_key_here":
    print("\n[!] Error: GEMINI_API_KEY is not set.")
    print("Please open the .env file in this directory and paste your API key from:")
    print("https://aistudio.google.com/apikey\n")
    exit(1)

# Initialize the Gemini Client
client = genai.Client(api_key=API_KEY)


# =====================================================================
# 2. DEFINE AGENT TOOLS (The Agent's Hands and Eyes)
# Any standard Python function with type hints and docstrings
# can be used by the model automatically as a tool!
# =====================================================================

def get_current_time() -> str:
    """Returns the current date, time, and day of the week."""
    now = datetime.datetime.now()
    return now.strftime("%A, %Y-%m-%d %H:%M:%S")

def calculate(expression: str) -> str:
    """Safely evaluates a basic mathematical expression (e.g. '14 * 25 + 10')."""
    try:
        # Allow only safe characters for arithmetic
        allowed = set("0123456789+-*/(). %")
        if not set(expression).issubset(allowed):
            return "Error: Unsupported characters in mathematical expression."
        result = eval(expression, {"__builtins__": None}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Math error: {str(e)}"

def list_workspace_files() -> list:
    """Returns a list of files present in the current working directory."""
    try:
        files = os.listdir(".")
        # Filter out hidden or virtual environment folders
        visible_files = [f for f in files if not f.startswith(".") and f != "venv"]
        return visible_files
    except Exception as e:
        return [f"Error listing files: {str(e)}"]

def save_note(title: str, content: str) -> str:
    """Saves a short text note to a file on disk."""
    try:
        filename = f"{title.replace(' ', '_').lower()}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Note successfully saved as '{filename}'."
    except Exception as e:
        return f"Error saving note: {str(e)}"


# Bundle tools into a list
my_tools = [get_current_time, calculate, list_workspace_files, save_note]


# =====================================================================
# 3. CONFIGURE AGENT PERSONA & SETTINGS
# =====================================================================

SYSTEM_INSTRUCTION = """
You are a helpful, smart personal AI assistant and problem solver.
You have access to tools to fetch current time, perform math calculations,
inspect local files, and save notes.

Guidelines:
1. Always use tools when real-world information, computation, or disk operations are needed.
2. Be concise, polite, and explain your actions clearly.
3. If asked to do something you do not have tools for, state what you can and cannot do.
"""

# Create a multi-turn chat session with tools enabled
chat = client.chats.create(
    model="gemini-3.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.2,      # Low temperature for accurate tool use and logic
        tools=my_tools,       # Gives the agent hands/tools
    )
)


# =====================================================================
# 4. INTERACTIVE AGENT LOOP
# =====================================================================

def main():
    print("=" * 60)
    print("🤖 AI Agent Initialized and Ready! (Model: Gemini 3.5 Flash)")
    print("Available Tools: Current Time, Calculator, List Files, Save Notes")
    print("Type 'exit' or 'quit' to end the session.")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nYou > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("\nGoodbye!")
                break

            # The agent receives the message, autonomously chooses tools,
            # executes them, and returns the response.
            print("\n[Agent thinking & checking tools...]")
            response = chat.send_message(user_input)
            print(f"\nAgent > {response.text}")

        except KeyboardInterrupt:
            print("\nSession stopped.")
            break
        except Exception as e:
            print(f"\n[!] An error occurred: {e}")

if __name__ == "__main__":
    main()
