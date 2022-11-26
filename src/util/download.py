import datetime as dt
import os
import platform
import subprocess

import settings
from src.util import render


def open_file(file_path):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', file_path))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(file_path)
    else:                                   # linux variants
        subprocess.call(('xdg-open', file_path))

def get_download_directory():
    default_download_directory = os.path.join(os.path.expanduser('~'), 'Downloads', 'lexsearch')

    if settings.DOWNLOAD_LOCATION == "DEFAULT":
        # create directory if it doesn't exist
        if not os.path.exists(default_download_directory):
            os.makedirs(default_download_directory)
        return default_download_directory
    else:
        # create directory if it doesn't exist and is a valid path
        # otherwise throw an error
        if os.path.exists(settings.DOWNLOAD_LOCATION):
            return settings.DOWNLOAD_LOCATION
        else:
            raise Exception("DOWNLOAD_LOCATION is not a valid path. Go to settings.py and change DOWNLOAD_LOCATION to a valid path or replace it with 'DEFAULT'.")

        
def download_file(object_to_download, output_format):
    '''
    Downloads a file to the user's Downloads folder.
    :param object_to_download: The object to download.
    :param output_format: The output format. Either "json", "xml", "html", "yaml", or "txt".
    '''

    download_location = get_download_directory()
    timestamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "export_lexsearch_" + timestamp + "." + output_format

    if output_format == "json":
        import json
        with open(os.path.join(download_location, file_name), "w") as f:
            statute = {"lex_search_content" : object_to_download}
            json.dump(statute, f, indent=4)
    elif output_format == "xml":
        import xmltodict
        with open(os.path.join(download_location, file_name), "w") as f:
            statute = {"lex_search_content" : object_to_download}
            f.write(xmltodict.unparse(statute, pretty=True))
    elif output_format == "yaml":
        import yaml
        with open(os.path.join(download_location, file_name), "w") as f:
            statute = {"lex_search_content" : object_to_download}
            yaml.dump(statute, f, sort_keys=False, encoding='utf-8')
    elif output_format == "html":
        with open(os.path.join(download_location, file_name), "w") as f:
            # write html string to file
            f.write(render.render_html_from_json(object_to_download))
    elif output_format == "txt":
        with open(os.path.join(download_location, file_name), "w") as f:
            # write txt string to file
            html = render.render_html_from_json(object_to_download)
            # strip html tags
            text = render.strip_html_tags(html)
            f.write(text)

            
    print ("Downloaded to " + os.path.join(download_location, file_name))
    
    # Ask user if they want to open the file
    open_file_prompt = input("Open file? (y/N): ")
    if open_file_prompt == "y" or open_file_prompt == "Y":
        # Open file in default application
        open_file(os.path.join(download_location, file_name))



def parse_download_request():
    '''
    Returns the download mode and output format based on the user's input.
    '''
    # Prompt user for file format from list or enter for default
    # [1] json, [2] xml, [3] html, [4] yaml, [5] txt
    # default is txt
    
    print("\nPlease select format of downloaded file:")

    formats = { "1" : "json",
                "2" : "xml",
                "3" : "yaml",
                "4" : "html",
                "5" : "txt" }

    # print in a single line
    formats_str = ""
    for key, value in formats.items():
        formats_str += "[" + key + "] " + value + " "
    print(formats_str)

    file_format = input("Enter number or press Enter for default: ")

    if file_format == '':
        file_format_value = 'txt'
    elif file_format not in formats.keys():
        file_format_value = None
    else: 
        file_format_value = formats[file_format]
    
    return file_format_value