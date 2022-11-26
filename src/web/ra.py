import sys

import requests
from bs4 import BeautifulSoup

from src.util import caching as ch
from src.util.download import download_file, parse_download_request
from src.util.term import clear_screen
from src.web import lawphil as lp
from src.web.req import check_connection

metadata_fields = [
    "ra_title",
    "date_saved",
    "long_title",
    "congress",
    "session"
]

def process_ra(ra_number, cache_dir):

    print("Searching for RA " + ra_number + "...")

    cache_file_name = f"ra_{ra_number}"

    # check if the RA number is in the cache
    if ch.is_in_cache(ra_number) == True:
        ra_text = ch.read_cache_file(cache_file_name, cache_dir)
  
    else:
        year = lp.get_year(ra_number)

        if year is None:
            print("Invalid RA number.")
            return

        if check_connection("lawphil") == False:
            return

        url = lp.construct_url(ra_number, year, "lawphil")

        if lp.is_valid_url(url) == True:
            print("Reading from lawphil...")
            get_url = requests.get(url)

            soup = BeautifulSoup(get_url.text, 'html.parser')
            soup_size = sys.getsizeof(soup)
            
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
        ra_text_sections = ra_text["sections"]

        sec_count = len(ra_text_sections)
        # print how many sections are available
        print("\n[RA VIEW]\n")
        print(f"There are {sec_count} sections in this RA.")

        section_number = input("Enter section number to print,\nor 0 to print all sections,\nor /q to return to main menu\nor /d to download the text of this statute): ")

        if section_number == '/q':
            clear_screen()
            return

        elif section_number == '0' or section_number == '':
            print("")
            # print all sections
            for section in ra_text_sections:
                section_number_print = section["section_number"]
                if section["section_title"] == f"Section {section_number_print}":
                    section_title_print = None
                else:
                    section_title_print = section["section_title"]
                section_text_print = section["section_text"]

                if section_title_print is not None:
                    print(f"[Section {section_number_print}] {section_title_print}\n{section_text_print}\n")
                else:
                    print(f"[Section {section_number_print}]\n{section_text_print}\n")
                
            print("\n[END OF SELECTION]")


        elif section_number.isnumeric():
            # check if section number is less than or equal to the number of sections
            if int(section_number) <= sec_count:
                print("")
                # print the section
                section = ra_text_sections[int(section_number) - 1]
                section_number_print = section["section_number"]
                if section["section_title"] == f"Section {section_number_print}":
                    section_title_print = None
                else:
                    section_title_print = section["section_title"]
                section_text_print = section["section_text"]

                if section_title_print is not None:
                    print(f"[Section {section_number_print}] {section_title_print}\n{section_text_print}\n")
                else:
                    print(f"[Section {section_number_print}]\n{section_text_print}\n")

                print("\n[END OF SELECTION]")
            else:
                print("Invalid section number.")

        elif section_number == '/d':
            output_file_format = parse_download_request()
            download_file(ra_text, output_file_format)
            
        else:
            print("Invalid input.")

        # Wait for user to press Enter before looping again
        input("\nPress Enter to continue...")
        clear_screen()
        
        


        