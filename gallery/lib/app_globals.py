"""The application's Globals object"""

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self, config):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        print 123123
        self.cache = CacheManager(**parse_cache_config_options(config))
