# My First AI Agent (Hands-On Learning)

A zero-cost, hands-on autonomous AI agent built in Python using Google Gemini (Free Tier).

## Project Setup

1. **Get your Free API Key**:
   - Go to [Google AI Studio](https://aistudio.google.com/apikey).
   - Sign in with any Google account (no credit card needed).
   - Click **Create API key** and copy it.

2. **Add your API Key**:
   - In this folder (`D:\Ai\Antigravity\Project1`), create a file named `.env` (or copy `.env.example` to `.env`).
   - Add your key:
     ```env
     GEMINI_API_KEY=AIzaSy...your_actual_key_here
     ```

3. **Run the Agent**:
   - Simply double-click `run.bat` or run in terminal:
     ```powershell
     .\venv\Scripts\python.exe agent.py
     ```

## What This Agent Demonstrates:
- **Brain**: Powered by `gemini-3.5-flash` (fast, free tier).
- **Persona**: Custom system prompt defining role and operating bounds.
- **Tools**:
  - `get_current_time()`: Autonomous datetime checking.
  - `calculate()`: Safe mathematical calculations.
  - `list_workspace_files()`: Reading local directory contents.
  - `save_note()`: Persisting information to disk.
- **Autonomous Tool Calling**: Gemini detects when a tool is needed, executes it, inspects the result, and gives a natural response.
