import src.util.caching as ch
import src.cli as cli

cache_dir = ch.get_cache_dir()
ch.clean_up_cache_dir(cache_dir)

cli.command_window()




