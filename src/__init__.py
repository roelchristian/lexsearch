import os
from src.util.caching import get_cache_dir

cache_dir = get_cache_dir()
this_os = os.name

__version__ = "0.1.0"
