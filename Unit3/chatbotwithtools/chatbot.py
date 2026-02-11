from tools.calculator import calculate
from tools.web_search import web_search
from tools.api_tools import get_joke

def detect_tool(user_input: str):
    user_input = user_input.lower()

    if any(op in user_input for op in ["+", "-", "*", "/", "%"]):
        return "calculator"

    if "search" in user_input or "latest" in user_input:
        return "web_search"

    if "joke" in user_input:
        return "api"

    return "none"


def chatbot():
    print("🤖 Smart Tool Chatbot (type 'exit' to quit)")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("Bot: 👋 Goodbye!")
            break

        tool = detect_tool(user_input)

        if tool == "calculator":
            print("Bot:", calculate(user_input))

        elif tool == "web_search":
            print("Bot:", web_search(user_input))

        elif tool == "api":
            print("Bot:", get_joke())

        else:
            print("Bot: 🤔 I can calculate, search, or call APIs. Try again!")


if __name__ == "__main__":
    chatbot()
