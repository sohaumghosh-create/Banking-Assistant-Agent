import json
from agent import call_gemini
from tools import AVAILABLE_TOOLS

def start_interactive_cli():
    # Initialize session history
    messages = []

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit"]:
            print("Thank you for using Banking Assistant. Goodbye!")
            break

        # Append user query to conversation timeline
        messages.append({
            "role": "user",
            "parts": [{"text": user_input}]
        })

        # Internal loop to let the agent call multiple tools back-to-back if needed
        while True:
            print("[Agent thinking...]")
            response = call_gemini(messages)

            # Scenario A: Agent needs data from a tool
            if response.get("status") == "call_tool":
                tool_name = response.get("tool_name")
                args = response.get("arguments", {})

                print(f"[Executing Tool]: {tool_name}(**{args})")

                tool_function = AVAILABLE_TOOLS.get(tool_name)
                if tool_function:
                    tool_result = tool_function(**args)
                else:
                    tool_result = {"error": f"Tool {tool_name} not registered."}

                # Feed the tool data back into history
                messages.append({
                    "role": "model",
                    "parts": [{"text": f"Called tool {tool_name}. Result: {json.dumps(tool_result)}"}]
                })
                messages.append({
                    "role": "user",
                    "parts": [{"text": "Continue processing. Call another tool if necessary, or provide your final answer."}]
                })

            # Scenario B: Agent is ready with the final response
            elif response.get("status") == "final_answer":
                print(f"\nAgent: {response.get('answer')}")

                # Keep the answer in conversational context for follow-up questions
                messages.append({
                    "role": "model",
                    "parts": [{"text": response.get("answer")}]
                })
                break

if __name__ == "__main__":
    start_interactive_cli()