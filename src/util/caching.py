import os
import sys
import json
import gzip
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

    # get the list of cache files
    cache_files = [file for file in os.listdir(cache_dir) if file.endswith('.cache')]
    
    # check if the RA number is in the cache
    if ra_number + '.cache' in cache_files:
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
