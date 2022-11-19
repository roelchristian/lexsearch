import requests
import re
import datetime as dt
from src.util.history import log_search_history

def get_type(search_term):

    search_term = search_term.upper()
    log_search_history(search_term)

    if search_term.startswith("RA"):
        return "ra"
    elif search_term.startswith("GR"):
        return "gr"
    else:
        print("Invalid search term. Type /? to show the help message.")
        return None

def get_search_term(search_term):
    # get everything after the second character
    ra_number = search_term[2:]
    return ra_number

def get_year(ra_number):
    '''
    This function will get the year through trial and error.
    '''
    # year thresholds
    year_thresholds = [2009, 2000, 1990, 1980, 1970, 1960, 1950, 1946]
    if int(ra_number) >= 10000:
        year = year_thresholds[0]
    elif int(ra_number) >= 9000:
        year = year_thresholds[1]
    elif int(ra_number) >= 8000:
        year = year_thresholds[2]
    elif int(ra_number) >= 7000:
        year = year_thresholds[3]
    elif int(ra_number) >= 6000:
        year = year_thresholds[4]
    elif int(ra_number) >= 5000:
        year = year_thresholds[5]
    elif int(ra_number) >= 4000:
        year = year_thresholds[6]
    elif int(ra_number) >= 1:
        year = year_thresholds[7]

    # get index of year in year_thresholds
    year_index = year_thresholds.index(year)
    if year_index == 0:
        next_threshold = None
    else:
        next_threshold = year_thresholds[year_index - 1]

    # construct a url from the year and ra number
    url = construct_url(ra_number, year)
    
    # if url is valid, return the year
    # if not valid add 1 to year and try again until a valid url is found but stop at the next threshold or if year is current year
    # if no valid url is found, return None
    # return the year if valid url is found

    while True:
        if is_valid_url(url):
            return year
        else:
            year += 1
            if year == next_threshold or year == dt.datetime.now().year:
                return None
            url = construct_url(ra_number, year)
                

def construct_url(ra_number, year):
    url = f"https://lawphil.net/statutes/repacts/ra{year}/ra_{ra_number}_{year}.html"
    return url

def is_valid_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return True
    else:
        return False

def get_title(soup):
    title = soup.find("h1").text
    return title

def get_sections(soup):
    '''
    A section is one or more paragraphs beginning with:
    The word section or sec. followed by a space and a number, case insensitive.
    A section ends where another section begins.
    The match should include the section number and the section text as well.

    For example, the following text:
    Section 1. This is the first section.
    Section 2. This is the second section.
    This is the second section's second paragraph, it is included in the second section.
    Section 3. This is the third section.

    Should be matched as:
    Section 1. This is the first section.
    Section 2. This is the second section.<p>This is the second section's second paragraph, it is included in the second section.
    Section 3. This is the third section.

    '''
    # get all the paragraphs
    paragraphs = soup.find_all("p")

    # initialize the section number
    section_number = 0

    # initialize the section text
    section_text = ''

    # initialize the section dict
    section_dict = {}

    # loop through the paragraphs
    for paragraph in paragraphs:
        # get the paragraph text
        paragraph_text = paragraph.text

        # check if the paragraph is a section
        if re.match(r'section\s\d+|sec\.\s\d+', paragraph_text, re.IGNORECASE):
            # check if the section number is not zero
            if section_number != 0:
                # add the section to the dict
                section_dict[section_number] = section_text

            # get the section number
            section_number = re.search(r'\d+', paragraph_text, re.IGNORECASE).group()

            # reset the section text
            section_text = ''

        # add the paragraph text to the section text
        section_text += paragraph_text

    # add the last section to the dict
    section_dict[section_number] = section_text

    # Get the last item in the dict
    last_item = list(section_dict.items())[-1]

    # Remove anything after the words "Approved:" or "Approved," in the last item
    last_item = re.sub(r'approved:.*|approved,.*', '', last_item[1], re.IGNORECASE)

    # Replace the last item in the dict with the modified last item
    section_dict[last_item[0]] = last_item

    
    return section_dict


           
