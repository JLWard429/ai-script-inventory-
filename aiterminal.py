import sys
from ai.conversation import Conversation
from ai.memory import Memory
from ai.script_parser import ScriptParser

def main():
    print("Welcome to the Superhuman AI Terminal!")
    memory = Memory()
    conversation = Conversation(memory)
    parser = ScriptParser()

    while True:
        user_input = input(">>> ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        command = parser.parse(user_input)
        response = conversation.respond(command)
        print(response)

if __name__ == "__main__":
    main()