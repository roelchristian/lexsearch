from src import __version__
from src.util.term import clear_screen
import settings

def display_settings():
    print(f"Lex Search Version {__version__}")
    print("Configure Lex Search settings here.\n")

    settings_index = 1

    for name in vars(settings):
        # show only user defined variables
        if not name.startswith("__"):
            
            print(f"[{settings_index}] {name} = {getattr(settings, name)}")
            settings_index += 1

    print("\nType /q to quit and return to the main menu or enter the number of the setting you want to change.")

    while True:
        command = input("command >> ")

        if command == "/q":
            clear_screen()
            break
        elif command.isdigit():
            if int(command) > 0 and int(command) <= len(vars(settings)):
                setting_name = list(vars(settings))[int(command) - 1]
                print(f"Enter a new value for {setting_name} or type /q to quit.")
                new_value = input(f"{setting_name} = ")
                if new_value == "/q":
                    clear_screen()
                    break
                else:
                    setattr(settings, setting_name, new_value)
                    print(f"{setting_name} = {getattr(settings, setting_name)}")
            else:
                print("Invalid setting number. Type /q to quit.")
        else:
            print("Invalid command. Type /q to quit.")

