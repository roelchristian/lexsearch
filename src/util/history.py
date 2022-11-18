import os
import datetime as dt

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



