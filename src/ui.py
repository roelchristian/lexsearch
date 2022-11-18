from src.util.commands import clear_screen, validate_search
from src.util.commands import print_help_message, print_version, show_history


def print_welcome_message():
    print("Welcome to LexSearch!")
    print("Type /h for help.")
    print("Type /q to quit.")


# do not close app until user types /q
def command_window():
    clear_screen()
    print_welcome_message()
    while True:
        command = input("lexsearch >> ")
        if command == "/q":
            clear_screen()
            break
        elif command == "/h":
            print_help_message()
        elif command == "/c":
            clear_screen()
        elif command == "/v":
            print_version()
        elif command == "/k":
            show_history()
        elif command.startswith("/s"):
            validate_search(command)        
        else:
            print("Invalid command. Type /h to show the help message.")
