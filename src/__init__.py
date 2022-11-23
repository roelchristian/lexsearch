import os
from src.util.caching import get_cache_dir, save_style_sheet_to_cache

cache_dir = get_cache_dir()
this_os = os.name
stylesheet_path = save_style_sheet_to_cache()

__version__ = "0.1.0"
