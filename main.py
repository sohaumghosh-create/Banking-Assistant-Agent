from agent.agent_loop import process_user_query


def start_interactive_cli():

    messages = []
    while True:

        user_input = input("\nYou: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Thank you for using Banking Assistant. Goodbye!")
            break

        answer = process_user_query(user_input,messages)
        print(f"\nAgent: {answer}")


if __name__ == "__main__":
    start_interactive_cli()