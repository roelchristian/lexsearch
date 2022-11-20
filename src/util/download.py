import settings
import datetime as dt
import os
import subprocess
import platform

def open_file(file_path):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', file_path))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(file_path)
    else:                                   # linux variants
        subprocess.call(('xdg-open', file_path))

def get_download_directory():
    if settings.DOWNLOAD_LOCATION == "DEFAULT":
        return os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        if os.path.exists(settings.DOWNLOAD_LOCATION):
            if os.path.isdir(settings.DOWNLOAD_LOCATION):
                return settings.DOWNLOAD_LOCATION
            else:
                return os.path.join(os.path.expanduser("~"), "Downloads")
        else:
            return os.path.join(os.path.expanduser("~"), "Downloads")

download_modes = {
    "dict" : ["json", "xml", "csv"],
    "soup" : ["html", "txt"]
}

def download_file(object_to_download, download_mode, output_format):
    '''
    Downloads a file to the user's Downloads folder.
    :param object_to_download: The object to download.
    :param download_mode: The download mode. Either "dict" or "soup".
    :param output_format: The output format. Either "json", "xml", "csv", "html", or "txt".
    '''

    download_location = get_download_directory()
    timestamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "export_lexsearch_" + timestamp + "." + output_format

    for download_mode in download_modes:
        if output_format in download_modes[download_mode]:
            if download_mode == "dict":
                if output_format == "json":
                    import json
                    with open(os.path.join(download_location, file_name), "w") as f:
                        json.dump(object_to_download, f)
                elif output_format == "xml":
                    import xmltodict
                    with open(os.path.join(download_location, file_name), "w") as f:
                        statute = {"root" : object_to_download}
                        f.write(xmltodict.unparse(statute, pretty=True))
                elif output_format == "csv":
                    import csv
                    with open(os.path.join(download_location, file_name), "w") as f:
                        writer = csv.writer(f)
                        for key, value in object_to_download.items():
                            writer.writerow([key, value])

            elif download_mode == "soup":
                if output_format == "html":
                    with open(os.path.join(download_location, file_name), "w") as f:
                        # replace /n in html with <br>
                        f.write(str(object_to_download).replace("/n", "<br>"))

                elif output_format == "txt":
                    with open(os.path.join(download_location, file_name), "w") as f:
                        # convert soup to text
                        f.write(object_to_download.get_text())

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
    # [1] json, [2] xml, [3] csv, [4] html, [5] txt
    # default is txt
    
    print("\nPlease select format of downloaded file:")
    print("[1] json [2] xml [3] csv [4] html [5] txt\n")

    formats = { "1" : "json", "2" : "xml", "3" : "csv", "4" : "html", "5" : "txt" }

    file_format = input("Enter number or press Enter for default: ")

    if file_format == '':
        file_format_value = 'txt'
    elif file_format not in formats.keys():
        file_format_value = None
    else: 
        file_format_value = formats[file_format]
    
    if file_format_value is not None:
        if file_format_value in download_modes["dict"]:
            download_mode = "dict"
        elif file_format_value in download_modes["soup"]:
            download_mode = "soup"
    else:
        download_mode = None
    
    return download_mode, file_format_value