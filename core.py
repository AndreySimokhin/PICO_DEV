from .config import Config_Entry, Config_Entries
from .exceptions import Core_Error


class Core:
    config: Config_Entries = []

    def __init__(self):
        pass