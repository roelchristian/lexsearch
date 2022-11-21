import requests

sources = {
    "lawphil": "https://lawphil.net",
    "chanrobles": "https://www.chanrobles.com",
    "scj": "https://sc.judiciary.gov.ph",
}

def check_connection(source):
    '''
    Check if the source is online.
    '''

    if source not in sources:
        print("Error: Invalid source.")
        return False
    url = sources[source]
    try:
        r = requests.get(url, timeout=3)
        return True
    except requests.exceptions.ConnectionError or requests.exceptions.Timeout:
        print("Error: Connection timed out.")
        return False