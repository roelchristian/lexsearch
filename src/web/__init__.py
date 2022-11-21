from src.web.req import check_connection, sources

# go over each source and check if it is online
# if it is online, add it to the list of online sources and get the url of the first item in the list
# if it is not online, print a message saying that it is offline

def initialize_sources():
    online_sources = []

    print("Welcome to Lex Search! Please wait while we initialize your connection to available online sources...")

    for source in sources.keys():
        print(f"Checking connection to {source.upper()}...")
        if check_connection(source) == True:
            print(f"{source.upper()} is online.")
            online_sources.append(source)
        else:
            print(f"{source.upper()} is offline.")

    if len(online_sources) > 0:
        print(f"Online sources: {online_sources}")
    else:
        print("No online sources.")
    return online_sources





