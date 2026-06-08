import json
from agent import call_gemini
from tools import AVAILABLE_TOOLS

def start_interactive_cli():
    messages = []

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit"]:
            print("Thank you for using Banking Assistant. Goodbye!")
            break

        messages.append({
            "role": "user",
            "parts": [{"text": user_input}]
        })

        while True:
            print("[Agent thinking...]")
            response = call_gemini(messages)

            if response.get("status") == "call_tool":
                tool_name = response.get("tool_name")
                args = response.get("arguments", {})

                print(f"[Executing Tool]: {tool_name}(**{args})")

                tool_function = AVAILABLE_TOOLS.get(tool_name)
                if tool_function:
                    tool_result = tool_function(**args)
                else:
                    tool_result = {"error": f"Tool {tool_name} not registered."}

                messages.append({
                    "role": "model",
                    "parts": [{"text": f"Called tool {tool_name}. Result: {json.dumps(tool_result)}"}]
                })
                messages.append({
                    "role": "user",
                    "parts": [{"text": "Continue processing. Call another tool if necessary, or provide your final answer."}]
                })

            elif response.get("status") == "final_answer":
                print(f"\nAgent: {response.get('answer')}")

                messages.append({
                    "role": "model",
                    "parts": [{"text": response.get("answer")}]
                })
                break

if __name__ == "__main__":
    start_interactive_cli()