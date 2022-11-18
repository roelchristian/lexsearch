import src.util.caching as ch
import src.lawphil as lp
import requests
import re
import sys
from bs4 import BeautifulSoup

def process_ra(ra_number, cache_dir):

    year = lp.get_year(ra_number)

    cache_file_name = f"ra_{ra_number}_{year}"

    # check if the RA number is in the cache
    if ch.is_in_cache(cache_file_name):
        ra_text = ch.read_cache_file(cache_file_name, cache_dir)


    else:
        url = lp.construct_url(ra_number, year)

        if lp.is_valid_url(url):
            print("Reading from lawphil...")
            get_url = requests.get(url)
            soup = BeautifulSoup(get_url.text, 'html.parser')
            soup_size = sys.getsizeof(soup)
            print(f"Downloaded {soup_size} bytes from {url}.")
            ra_text = lp.get_sections(soup)
            ch.create_cache_file(ra_text, cache_file_name, cache_dir)

            # get title
            title = soup.title.text
            print(title)

    # get section to print
    section_to_print = input("Enter section to print or press 0 to print all: ")

    # check if the user wants to print all sections
    if section_to_print == '0':
        # print all sections
        for section in ra_text:
            print(section + ' ' + ra_text[section])

    else:
        # validate if the section to print is valid, ie is a number
        # if not valid, prompt the user to enter a valid section or type 0 to print all or type q to quit
        while not re.match(r'\d+', section_to_print):
            section_to_print = input("Enter a valid section to print or press 0 to print all or press q to quit: ")
            if section_to_print == 'q':
                sys.exit()
        
        # print the section
        print(ra_text[section_to_print])