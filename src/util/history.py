import datetime as dt
import os

from src import this_os


def get_search_history_dir():
    app_folder = os.path.join(os.path.expanduser('~'), '.lexsearch')
    history_file = os.path.join(app_folder, 'search_history.lexsearch')
    return history_file


def log_search_history(search_term):
    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_file = get_search_history_dir()
    # check if the history file exists
    if not os.path.exists(history_file):
        # create the history file
        with open(history_file, 'w') as f:
            f.write('')

    # append the search term to the history file
    with open(history_file, 'a') as f:
        f.write(timestamp + " " + search_term + '\n')

def clear_history():
    if os.path.exists(get_search_history_dir()):
        os.remove(get_search_history_dir())
    else:
        return

def show_history():
    history_file = get_search_history_dir()
    if not os.path.exists(history_file):
        print("No search history found.")
        return

    """
    This will print the search history in the following format:
    [number] [timestamp] [search term]

    Example:
    [1] 2020-01-01 12:00:00 search term
    [2] 2020-01-01 12:00:00 search term
    ...
    [10] 2020-01-01 12:00:00 search term

    PAGE X OF Y
    
    For each page, ten search terms will be shown. The user will be prompted to
    enter a number corresponding to the search term they want to search again.

    
    If the user enters '/q', the search history will be exited. If the user enters
    a number that is not valid, the user will be prompted to enter a valid number.
    If the user enters '/c', the search history will be cleared. If the user enters
    '/n', the next page will be shown. If the user enters '/p', the previous page will
    be shown. If the user enters '/a', the user will be brought to the first page.
    If the user enters '/z', the user will be brought to the last page.

    Lines are displayed in reverse order, with the most recent search term at
    the top. The numbers are displayed in ascending order, with the most recent
    search term at [1], and the oldest search term at [n]. The screen will be
    cleared after each page is shown.

    The commands are displayed at the bottom of the screen like this:
    /number to search the corresponding item
    /q to quit          /c to clear history 
    /n for next page    /p for previous page 
    /a for first page   /z for last page
    ENTER YOUR COMMAND: 
    """

    # get the number of lines in the history file
    with open(history_file, 'r') as f:
        lines = f.readlines()
        num_lines = len(lines)

    # get the number of pages
    num_pages = num_lines // 10
    if num_lines % 10 != 0:
        num_pages += 1

    # get the current page
    current_page = 1

    # get the current line
    current_line = num_lines

    # get the current line number
    current_line_number = 1

    # get the current page number
    current_page_number = 1

    while True:
        # clear the screen
        if this_os == "nt":
            os.system("cls")
        else:
            os.system("clear")
        
        print("SEARCH HISTORY")
        print("==============\n")

        # print the lines
        for i in range(10):
            if current_line > 0:
                print(f"[{current_line_number}] {lines[current_line - 1]}", end='')
                current_line -= 1
                current_line_number += 1

        # print the page number
        print(f"\nPAGE {current_page_number} OF {num_pages}")

        # print the commands, should be at the bottom of the screen not indented

        print("<number> to search the corresponding item")
        print("/q to quit          /c to clear history")
        print("/n for next page    /p for previous page")
        print("/a for first page   /z for last page")
        print("ENTER YOUR COMMAND: ", end='')
        command = input()

        # check if the user entered a number
        if command.isdigit():
            # get the line number
            line_number = int(command)

            # check if the line number is valid
            if line_number < 1 or line_number > num_lines:
                print("Invalid line number.")
                input("Press ENTER to continue.")
                continue

            # get the search term
            search_term = lines[line_number - 1].split()[2]

            # return the search term
            return search_term

        # check if the user entered a command
        if command == "/q":
            # exit the search history
            return
        elif command == "/c":
            # clear the search history
            clear_history()
            return
        elif command == "/n":
            # check if the current page is the last page
            if current_page == num_pages:
                print("This is the last page.")
                continue

            # go to the next page
            current_page += 1
            current_page_number += 1
            current_line_number = current_page * 10 - 9
        elif command == "/p":
            # check if the current page is the first page
            if current_page == 1:
                print("This is the first page.")
                continue

            # go to the previous page
            current_page -= 1
            current_page_number -= 1
            current_line_number = current_page * 10 - 9
        elif command == "/a":
            # go to the first page
            current_page = 1
            current_page_number = 1
            current_line_number = 1
        elif command == "/z":
            # go to the last page
            current_page = num_pages
            current_page_number = num_pages
            current_line_number = num_lines - (num_lines % 10) + 1
        else:
            print("Invalid command.")
            

   