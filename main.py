import sys
from core.agent import EnterpriseAgent
from utils.logger import logger

FUNNY_BANNER = r"""
  ______                      _   _____ 
 |  ____|                    | | |_   _|
 | |__ _   _ _ __  _ __  _   | |   | |  
 |  __| | | | '_ \| '_ \| |  | |   | |  
 | |  | |_| | | | | | | | |__| |  _| |_ 
 |_|   \__,_|_| |_|_| |_|\____/  |_____|

   -- The AI Agent with a Sense of Humor --
"""

def main():
    print(FUNNY_BANNER)
    print("🤖 Agent: 'System booted successfully! I'm ready to assist (or pretend to work).' \n")

    try:
        agent = EnterpriseAgent()
    except Exception as e:
        logger.critical("Failed to start agent: %s", e)
        print(f"\n[!] Failed to start agent: {e}\n")
        sys.exit(1)

    print("=" * 65)
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

        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break
        except Exception as e:
            print(f"\n[!] Error: {e}\n")

if __name__ == "__main__":
    main()
