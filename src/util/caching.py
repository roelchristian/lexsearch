import gzip
import json
import os
import shutil

import settings


def get_cache_dir():
    '''
    This function returns the path to the cache directory.
    '''

    # get the home directory
    home_dir = os.path.expanduser('~')

    # get the app directory
    app_dir = os.path.join(home_dir, '.lexsearch')

    # get the cache directory
    cache_dir = os.path.join(app_dir, 'cache')

    # check if the cache directory exists
    if not os.path.exists(cache_dir):
        # create the cache directory
        os.makedirs(cache_dir)


    return cache_dir

def create_cache_file(dict, filename, cache_dir):
    '''
    This function creates a cache file from a dict by serializing it to JSON and then compressing it as a gzip file. The resulting file is stored in the specified cache directory with a .cache extension.
    '''

    # get the cache file path
    cache_file_path = os.path.join(cache_dir, filename + '.cache')

    # serialize the dict to JSON
    json_string = json.dumps(dict)

    # compress the JSON string
    with gzip.open(cache_file_path, 'wb') as f:
        f.write(json_string.encode('utf-8'))


def cache_soup(soup, ra_number, cache_dir):
    '''
    This function caches a BeautifulSoup object by zippping it into a gzip file and storing it in the cache directory.
    '''

    # get the cache file path
    cache_file_path = os.path.join(cache_dir, 'ra_'+ ra_number + '_soup.cache')


    # create new div "lexsearch" and add it to the start of the body
    soup.body.insert(0, soup.new_tag('div', id='lexsearch', style='font-size: 90%; text-align: center; padding: 15px;'))
    soup.find('div', id='lexsearch').append(soup.new_tag('p'))
    soup.find('div', id='lexsearch').find('p').append(soup.new_tag('p'))
    soup.find('div', id='lexsearch').find('p').find('p').append(soup.new_string('This page was generated by Lex Search, a free and open source tool for searching Philippine laws and jurisprudence.'))
    soup.find('div', id='lexsearch').find('p').find('p').append(soup.new_string(' For more information, visit '))
    soup.find('div', id='lexsearch').find('p').find('p').append(soup.new_tag('a', href='https://github.com/roelchristian/lexsearch'))
    soup.find('div', id='lexsearch').find('p').find('p').find('a').append(soup.new_string("the project's GitHub page"))
    soup.find('div', id='lexsearch').find('p').find('p').append(soup.new_string('.'))

    # remove script tags
    for script in soup.find_all('script'):
        script.decompose()

    # compress the BeautifulSoup object
    with gzip.open(cache_file_path, 'wb') as f:
        f.write(soup.encode('utf-8'))

def read_soup_from_cache(file_name, cache_dir):
    '''
    This function reads a BeautifulSoup object from the cache directory.
    '''

    # get the cache file path
    cache_file_path = os.path.join(cache_dir, file_name + '.cache')

    # read the compressed BeautifulSoup object
    with gzip.open(cache_file_path, 'rb') as f:
        soup = f.read()
        # remove \n from the soup
        soup = soup.replace(b'\n', b'')

    return soup
    

def read_cache_file(filename, cache_dir):
    '''
    This function reads a cache file from the specified cache directory and returns the deserialized dict.
    '''

    # get the cache file path
    cache_file_path = os.path.join(cache_dir, filename + '.cache')

    # read the compressed JSON string
    with gzip.open(cache_file_path, 'rb') as f:
        json_string = f.read()

    # deserialize the JSON string
    dict = json.loads(json_string)

    return dict

def is_in_cache(ra_number):
    '''
    This function checks if an RA number is in the cache.
    '''

    # get the cache directory
    cache_dir = get_cache_dir()
    cache_file_name = f"ra_{ra_number}"

    # check if the cache file exists
    if os.path.exists(os.path.join(cache_dir, cache_file_name + '.cache')):
        return True
    else:
        return False

def clean_up_cache_dir(cache_dir):
    '''
    This function cleans up the cache directory by deleting cache files as soon as the maximum cache size is reached for the whole directory or as soon as the maximum cache age is reached for a single cache file.
    '''

    # get the maximum cache size in bytes
    max_cache_size = settings.MAX_CACHE_SIZE_MB * 1024 * 1024

    # get the list of cache files
    cache_files = os.listdir(cache_dir)

    # get the total size of the cache directory
    total_size = 0
    for cache_file in cache_files:
        total_size += os.path.getsize(os.path.join(cache_dir, cache_file))

    # check if the total size of the cache directory is greater than the maximum cache size
    if total_size > max_cache_size:
        # delete the oldest cache file
        oldest_cache_file = min(cache_files, key=lambda p: os.path.getmtime(os.path.join(cache_dir, p)))
        os.remove(os.path.join(cache_dir, oldest_cache_file))

def stylesheet_cache():
    '''
    This function saves the default style sheet to the cache directory.
    '''
    app_dir = os.path.expanduser('~/.lexsearch')
    cache_stylesheet_path = os.path.join(app_dir, 'stylesheet', 'ra_style.css')

    # copy static/css/ra_style.css to the cache file path
    stylesheet_path = os.path.join(settings.BASE_DIR, 'static/css/style.css')

    return cache_stylesheet_path, stylesheet_path

def copy_stylesheet(source_sheet, destination_sheet):
    '''
    This function copies the default style sheet to the app directory.
    '''

    # check if there is a "stylesheet" directory in the app directory
    app_dir = os.path.expanduser('~/.lexsearch')
    stylesheet_dir = os.path.join(app_dir, 'stylesheet')
    if not os.path.exists(stylesheet_dir):
        os.makedirs(stylesheet_dir)

    # copy the style sheet
    shutil.copyfile(source_sheet, destination_sheet)

    