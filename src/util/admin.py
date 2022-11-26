from src import cache_dir
from src.util.term import clear_screen, progress_bar
from src.util.settings import display_settings
import os
import src.web.lawphil as lp
import requests 
from bs4 import BeautifulSoup
from src import cache_dir
import src.util.caching as ch

def display_admin_menu():
    '''
    Prints the admin window with the following options:
    [1] Clear app cache
    [2] Configure settings
    [3] Download lawphil database (for offline use)
    [4] Exit
    '''

    while True:
        print("Admin Menu")
        print("[1] Clear app cache")
        print("[2] Configure settings")
        print("[3] Download lawphil database (for offline use)")
        print("[4] (or /q) Return to main menu")

        command = input("command >> ")

        if command == "1":
            clear_app_cache()
        elif command == "2":
            display_settings()
        elif command == "3":
            download_lawphil_db()
        elif command == "4" or command == "/q":
            clear_screen()
            break
        else:
            print("Invalid command. Type /q to quit.")

def clear_app_cache():
    '''
    Clears the app cache.
    '''

    print("Are you sure you want to clear the app cache? Type /q to quit or /y to continue.")
    command = input("command >> ")

    if command == "/y":
        for file in os.listdir(cache_dir):
            os.remove(os.path.join(cache_dir, file))
        print("App cache cleared.")
    elif command == "/q":
        clear_screen()
    else:
        print("Invalid command. Type /q to quit.")

import time
import random

def download_lawphil_db():
    '''
    Downloads the lawphil database for offline use.
    '''
    download_confirmation = input("This will download the lawphil database. This may take a while. Continue? (y/n) ")
    if download_confirmation == "y":
        
        for i in range(9000, 10000):

            # autothrottle to prevent overloading the lawphil server
            # random sleep from 0.1 to 0.7 seconds
            time.sleep(random.uniform(0.1, 0.7))

            max =  10000
            
            year = lp.get_year(i)
            if year is not None:
                url = lp.construct_url(i, year, "lawphil")
               

                r = requests.get(url)
                if r.status_code == 200:
                    try:
                        soup = BeautifulSoup(r.text, "html.parser")
                        ra_text = lp.get_sections(soup)
                        cache_file_name = f"ra_{i}"
                        ch.create_cache_file(ra_text, cache_file_name, cache_dir)
                        time.sleep(0.1)
                    except Exception as e:
                        max = max - 1
                        pass
                else:
                    max = max - 1
                    continue
            else:
                # continue to next i
                max = max - 1
                continue

        
            progress_bar(i, max)
            

    elif download_confirmation == "n":
        pass

