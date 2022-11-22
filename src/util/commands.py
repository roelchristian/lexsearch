from src import this_os
import os
from src.web import ra
from src.web import lawphil as lp
from src import cache_dir
import sys
from dotenv import load_dotenv
from src import __version__

load_dotenv()

def parse_search(command):
    if len(command.split()) == 2:
        search_term = command.split()[1]
        search_type = lp.get_type(search_term)
        if not search_type:
            ra_number = None
        else:
            ra_number = lp.get_search_term(search_term) 
        return search_type, ra_number
    else:
        if len(command.split()) == 1:
            print("Please enter a search term.")
        elif len(command.split()) == 3:
            # check if search term is like RA 7610 or GR 123456
            search_term = command.split()[1] + command.split()[2]
            search_type = lp.get_type(search_term)
            if not search_type:
                ra_number = None
            else:
                ra_number = lp.get_search_term(search_term)
            return search_type, ra_number

        elif len(command.split()) > 3:
            print("Invalid search term. Type /? to show the help message.")
    
        return None, None

def perform_search(search_type, search_term):
    if search_type == "ra":
        ra.process_ra(search_term, cache_dir)
    elif search_type == "gr":
        print("GR search not implemented yet.")
    elif search_type is None or search_term is None:
        return

def print_help_message():
    
    print(f"""
    Welcome to LexSearch!
    Version {os.getenv('VERSION')}

    This command line utility allows you to search for Philippine laws and jurisprudence right from your terminal.

    The following commands are available:

    /q to quit
    /? to display the help message
    /c to clear the screen
    /s to search for a statute or a decision
        * This should be followed by the search term.
        * Valid search terms start with "RA" or "GR"
        * For example, to search for RA 7610, type "/s RA7610 or /s RA 7610"
    /h to display the search history
    /x to display the settings
    /v to display the version number
    """)

def print_version():
    print(f"LexSearch version {__version__}")
    print(f"Python version {sys.version}")