from src import this_os
import os

def clear_screen():
    print(this_os)
    if this_os == "nt":
        os.system("cls")
    else:
        os.system("clear")