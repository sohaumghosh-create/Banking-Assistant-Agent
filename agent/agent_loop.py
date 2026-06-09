import json

from agent.gemini_client import call_gemini
from tools.registry import AVAILABLE_TOOLS


def process_user_query(
        user_input: str,
        messages: list
):
    messages.append({"role": "user","parts": [{"text": user_input}]})

    while True:
        print("[Agent thinking...]")
        response = call_gemini(messages)

        if response.get("status") == "call_tool":
            tool_name = response.get("tool_name")
            args = response.get("arguments",{})
            print(f"[Executing Tool]: {tool_name}(**{args})")
            tool_function = AVAILABLE_TOOLS.get(tool_name)

            if tool_function:
                tool_result = tool_function(**args)
            else:
                tool_result = {"error": f"Tool {tool_name} not registered."}

            messages.append({
                "role": "model",
                "parts": [{
                    "text":f"Called tool {tool_name}. Result: {json.dumps(tool_result)}"
                }]
            })
            messages.append({
                "role": "user",
                "parts": [{
                    "text":"Continue processing. Call another tool if necessary, or provide your final answer."
                }]
            })

        elif response.get("status") == "final_answer":
            answer = response.get(
                "answer",
                "Unable to generate a response."
            )
            messages.append({
                "role": "model",
                "parts": [{"text": answer}]
            })
            return answer

        else:
            return "Unexpected response received from agent."