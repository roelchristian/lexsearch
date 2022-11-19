from src.util.commands import clear_screen, parse_search, perform_search
from src.util.commands import print_help_message, print_version
from src.util.history import show_history


def print_welcome_message():
    print("Welcome to LexSearch!")
    print("Type /? for help.")
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
        elif command == "/?":
            print_help_message()
        elif command == "/c":
            clear_screen()
        elif command == "/v":
            print_version()
        elif command == "/h":
            show_history()
        elif command.startswith("/s"):
            search_type, search_term = parse_search(command)
            perform_search(search_type, search_term)
                
        else:
            print("Invalid command. Type /? to show the help message.")
