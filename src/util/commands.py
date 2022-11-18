from src import this_os
import os
from src.util.history import log_search_history, get_search_history_dir
from src.web import ra
from src.web import lawphil as lp
from src import cache_dir
import sys
from dotenv import load_dotenv

load_dotenv()

def clear_screen():
    print(this_os)
    if this_os == "nt":
        os.system("cls")
    else:
        os.system("clear")


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