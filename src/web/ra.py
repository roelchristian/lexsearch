from src.util import caching as ch
from src.web import lawphil as lp
import requests
import re
import sys
from bs4 import BeautifulSoup
from src.util.term import clear_screen
from src.util.download import download_file, parse_download_request
from src.util.caching import cache_soup
from src.web.requests import check_connection

metadata_fields = [
    "Title",
    "Date Saved",
    "Long Title"
]

def process_ra(ra_number, cache_dir):

    print("Searching for RA " + ra_number + "...")

    cache_file_name = f"ra_{ra_number}"
    soup_cache_file_name = f"ra_{ra_number}_soup"
    is_in_cache_val = ch.is_in_cache(ra_number)

    # check if the RA number is in the cache
    if is_in_cache_val == True:
        ra_text = ch.read_cache_file(cache_file_name, cache_dir)
        ra_text_soup = ch.read_soup_from_cache(soup_cache_file_name, cache_dir)

    else:
        year = lp.get_year(ra_number)

        if year is None:
            print("Invalid RA number.")
            return

        if check_connection("lawphil") == False:
            return

        url = lp.construct_url(ra_number, year, "lawphil")

        if lp.is_valid_url(url):
            print("Reading from lawphil...")
            get_url = requests.get(url)
            soup = BeautifulSoup(get_url.text, 'html.parser')
            soup_size = sys.getsizeof(soup)
            cache_soup(soup, ra_number, cache_dir)
            
            print(f"Downloaded {soup_size} bytes from {url}.")
            ra_text = lp.get_sections(soup)
            ch.create_cache_file(ra_text, cache_file_name, cache_dir)
            # get title
            title = soup.title.text
            print(f"Showing details for: {title}")

    # get section to print from user
    # or print all sections by pressing 0 or Enter
    # or go to return to main menu by pressing q
    clear_screen()
    while True:
        
        sec_count = len(ra_text)-len(metadata_fields)

        # print how many sections are available
        print("\n[RA VIEW]\n")
        print(f"There are {sec_count} sections in this RA.")

        section_number = input("Enter section number to print,\nor 0 to print all sections,\nor /q to return to main menu\nor /d to download the text of this statute): ")

        if section_number == '/q':
            clear_screen()
            return

        elif section_number == '0' or section_number == '':
            print("")
            # print all key value pairs in the dict except where key is "Title" or "Date Saved"
            for key, value in ra_text.items():
                if key not in metadata_fields:
                    print(f"[{key}]\n{value}\n")
                
            print("\n[END OF SELECTION]")


        elif section_number.isnumeric():
            # check if section number is less than or equal to the number of sections
            if int(section_number) <= sec_count:
                print("")
                section_number = f"Section {section_number}"
                print(f"[{section_number}]\n{ra_text[section_number]}")
                print("\n[END OF SELECTION]")
            else:
                print("Invalid section number.")

        elif section_number == '/d':
            download_mode, output_file_format = parse_download_request()
            if download_mode == "dict":
                download_file(ra_text, "dict", output_file_format)
            elif download_mode == "soup":
                if is_in_cache_val == True:
                    download_file(ra_text_soup, "soup", output_file_format)
                else:
                    download_file(soup, "soup", output_file_format)
            else:
                print("Invalid download mode.")
                return

        else:
            print("Invalid input.")

        # Wait for user to press Enter before looping again
        input("\nPress Enter to continue...")
        clear_screen()
        
        


        