from openai import OpenAI
import os
import argparse


def chat() -> None:
    client = OpenAI()

    messages = [{"role": "developer", "content": "You are a helpful assistant."}]
    user_prefix = "YOU"
    assistant_prefix = "ASSISTANT"

    print('\n')
    while True:
        user_input = input(f"{user_prefix}: ")
        if user_input.lower() == "exit":
            print("Exiting chat. Goodbye!")
            break
        messages.append({"role": "user", "content": user_input})
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        response = completion.choices[0].message.content
        print(f"\n{assistant_prefix}: {response}\n")

def main():
    parser = argparse.ArgumentParser(description="Chat with OpenAI's GPT-4o model.")
    subparsers = parser.add_subparsers(dest="command")  # Subcommand names will be stored in args.command
    
    set_api_key_parser = subparsers.add_parser('set-api-key', help="set the OpenAI API key")
    chat_parser = subparsers.add_parser('chat', help="start a new chat session")
    args = parser.parse_args()

    if args.command is None:
        print("\n############# termGPT #############")
        print("\nWelcome to termGPT! A command line interface for OpenAI's GPT models.")

        print("\n-You can start a new chat session by typing: 'termgpt chat'")
        print("-You can exit the chat session by typing: 'exit'")

        if not os.getenv("OPENAI_API_KEY"):
            print("\nIMPORTANT: It looks like you have not set your API key yet.\n")
            print("Please run the following command to set your API key: export OPENAI_API_KEY=<your_api_key>\n")

    if args.command == "chat":
        if not os.getenv("OPENAI_API_KEY"):
            print("API key not set. Please set your API key first by running 'export OPEN_AI_API_KEY=<your_api_key>'")

        try:
            chat()
        except Exception as e:
            print(f"termGPT encountered an error while trying to start chat session: {e}.")


if __name__ == "__main__":
    main()