import sys
import os
from src import this_os
from src.web import ra
from src.web import lawphil as lp
from src.util import caching as ch
from src.util.history import log_search_history, get_search_history_dir
from dotenv import load_dotenv

cache_dir = ch.get_cache_dir()
load_dotenv()

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

def validate_search(command):
    if len(command.split()) == 2:
        search_term = command.split()[1]
        search_type = lp.get_type(search_term)
        ra_number = lp.get_search_term(search_term)
        log_search_history(search_term)
        if search_type == "ra":
            ra.process_ra(ra_number, cache_dir)
        elif search_type == "gr":
            print("GR search is not yet implemented.")
        else:
            print("Invalid search term.")

def print_help_message():
    
    print(f"""
    Welcome to LexSearch!
    Version {os.getenv('VERSION')}

    This command line utility allows you to search for Philippine laws and jurisprudence right from your terminal.

    The following commands are available:

    /q to quit
    /h to display the help message
    /c to clear the screen
    /s to search for a statute or a decision
        * This should be followed by the search term.
        * Valid search terms start with "RA" or "GR"
        * For example, to search for RA 7610, type "/s RA7610"
    /k to display the search history
    /x to display the settings
    /v to display the version number
    """)

def print_version():
    print(f"LexSearch version {os.getenv('VERSION')}")
    print(f"Python version {sys.version}")

def show_history():
    '''
    prompt the user to enter the index of the search term if they want to search again
    '''

    # get the search history
    history = get_search_history_dir()
    
    # Open text file and save the contents to a list
    with open(history, 'r') as f:
        history_list = f.readlines()

    # print the search history

    # check if the search history is empty
    if len(history_list) == 0:
        print("Search history is empty.")
        return

    # get the last 10 search terms
    last_ten = history_list[-10:]

    for i in range(len(last_ten)):
        print(f"[{i+1}] {last_ten[i]}")

    # prompt the user to enter the index of the search term if they want to search again
    while True:
        index = input("Enter the index of the search term if you want to search again or press 0 to go back: ")
        if index == '0':
            break
        elif index.isnumeric():
            index = int(index)
            if index > 0 and index <= len(last_ten):
                search_term = last_ten[index-1]
                # remove the timestamp
                search_term = search_term.split()[2]

                search_type = lp.get_type(search_term)
                
                ra_number = lp.get_search_term(search_term)
                if search_type == "ra":
                    ra.process_ra(ra_number, cache_dir)
                elif search_type == "gr":
                    print("GR search is not yet implemented.")
                else:
                    print("Invalid search term.")
            else:
                print("Invalid index.")
        else:
            print("Invalid index.")

def clear_screen():
    print(this_os)
    if this_os == "nt":
        os.system("cls")
    else:
        os.system("clear")