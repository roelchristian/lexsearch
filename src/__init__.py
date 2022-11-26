import os
from src.util.caching import get_cache_dir, stylesheet_cache

cache_dir = get_cache_dir()
this_os = os.name

cache_stylesheet_path, stylesheet_path = stylesheet_cache()
__version__ = "0.2.0"
