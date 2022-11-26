import src.ui as ui
import src.util.caching as ch
from src import cache_dir


def main():
    ch.clean_up_cache_dir(cache_dir)
    ui.command_window()

if __name__ == "__main__":
    main()