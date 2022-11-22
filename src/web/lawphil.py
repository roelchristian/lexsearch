import requests
import re
import datetime as dt
from src.util.history import log_search_history
from src.web.req import sources
from number_parser import parse_ordinal
import collections

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
    url = construct_url(ra_number, year, "lawphil")
    
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
            url = construct_url(ra_number, year, "lawphil")
                

def construct_url(ra_number, year, source):

    if source not in sources:
        print("Invalid source.")
        return None
    elif source == "lawphil":
        url = f"https://lawphil.net/statutes/repacts/ra{year}/ra_{ra_number}_{year}.html"
        return url
    else:
        print("Selected source is not yet supported.")
        return None

def is_valid_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return True
    else:
        return False

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

        # add the paragraph text to the section text and preserve the line breaks
        section_text += paragraph_text + '\r\r'

    #TODO: Find a way to strip \r\r from the last item when appending

    # add the last section to the dict
    section_dict[section_number] = section_text
    
    #get last item in dict
    last_item = list(section_dict.items())[-1]

    # Remove everything after the string "Approved" in the last section (including the string "Approved")
    head, sep, tail = last_item[1].partition('Approved')
    section_dict[last_item[0]] = head

    # rename keys from '1' to 'Section 1'
    section_dict = {f'Section {key}': value for key, value in section_dict.items()}

    # remove first sentence from each section
    for key, value in section_dict.items():
        section_dict[key] = re.sub(r'^.*?\.\s', '', value)
    
    # split the value of each key into a dict with the following keys: 'section_number', 'section_text', 'section_title'
    sections = []
    for key, value in section_dict.items():
        section_number = re.search(r'\d+', key).group()
        # section title is the first sentence of the section, everything before the first period excluding the period
        
        section_title = re.search(r'(^.*?)(?:\.)', value).group()
        # remove full stop from section title if section title ends with a full stop
        if section_title.endswith('.'):
            section_title = section_title[:-1]
        # section text is the rest of the section starting from the first capital letter
        section_text = re.search(r'([A-Z].*)', value).group()

        if section_text == section_title:
            section_title = key
        section_dict[key] = {'section_number': section_number, 'section_title': section_title, 'section_text': section_text}
        # append the dict to the sections list
        sections.append(section_dict[key])
    
    sections = {'section': sections}
    section_dict = {'sections': sections}
    metadata_dict = get_metadata_from_soup(soup)

    # create new key 'metadata' and assign the metadata dict to it
    section_dict['metadata'] = metadata_dict

    # order the keys alphabetically
    section_dict = collections.OrderedDict(sorted(section_dict.items()))


    return section_dict


def get_metadata_from_soup(soup):


    metadata = {}
    metadata['date_saved'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #RA DETAILS

    long_title = soup.find('meta', attrs={'name': 'description'})['content']
    long_title = re.sub(r'^Republic Acts -\s', '', long_title)
    ra_title = soup.title.text.strip()
    serial_number = re.search(r'\d+', ra_title).group()
    ra_details = {
        'serial_number': serial_number,
        'ra_title': ra_title,
        'long_title': long_title
    }

    metadata['ra_details'] = ra_details


    # CONGRESS DETAILS

    congress = soup.find('hr', attrs={'color': '#000080', 'size': '-1'}).find_next_siblings('p', limit=2)
    congress = [paragraph.text for paragraph in congress]
    congress = ' '.join(congress)
    congress = congress.strip()

    # get all words up to substring "Congress" including "Congress"
    congress_val = re.search(r'(.+?)(?:Congress)', congress).group()
    # get all words from congress_val except the last word and trim for trailing whitespace
    congress_ordinal = re.sub(r'\s\w+$', '', congress_val).strip()
    # subtract congress_val from congress to get the congress number
    session = congress.replace(congress_val, '')
 
    print(congress)
    print(type(congress)) 
    # check if not valid session, ie not containing the string "Session"
    if not re.search(r'Session', session):
        # set session to None
        session = None

    if session is not None and re.search(r'Session', session):
        session = re.search(r'(.+?)(?:Session)', session).group()
        session_ordinal = re.sub(r'(Regular|Extraordinary|Special)\sSession', '', session).strip()
        session_ordinal = parse_ordinal(session_ordinal)
        session_type = re.search(r'(Regular|Extraordinary|Special)\sSession', session).group()
    else:
        session_ordinal = None
        session_type = None

    # create dicts for congress and session
    session_dict = {'session_long_name': session, 'session_type': session_type, 'session_number': session_ordinal}
    congress_dict = {'congress_long_name': congress_val, 'congress_number': parse_ordinal(congress_ordinal), 'session' : session_dict}
    metadata['congress'] = congress_dict

    return metadata