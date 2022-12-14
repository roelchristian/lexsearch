from src import cache_stylesheet_path, stylesheet_path
from src.util.caching import copy_stylesheet
from src.util.commands import (parse_search, perform_search,
                               print_help_message, print_version,
                               print_about_info)
from src.util.history import show_history
from src.util.admin import display_admin_menu
from src.util.term import clear_screen
from src.web import initialize_sources


def print_welcome_message():
    print("Welcome to Lex Search!")
    print("Type /? for help.")
    print("Type /q to quit.")

# do not close app until user types /q
def command_window():
    clear_screen()

    copy_stylesheet(stylesheet_path, cache_stylesheet_path)

    sources = initialize_sources()
    
    clear_screen()
    
    print_welcome_message()
    default_online_source = sources[0]
    print(f"Default online source for this session: {default_online_source}")

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
        elif command == "/a":
            print_about_info()
        elif command == "/h":
            show_history()
        elif command.startswith("/s"):
            search_type, search_term = parse_search(command)
            perform_search(search_type, search_term)
        elif command.startswith("/x"):
            display_admin_menu()
                
        else:
            print("Invalid command. Type /? to show the help message.")
