class Core_Error(BaseException):
    """General Core exception occurred"""

class Config_Error(Core_Error):
    """General config error"""

class Unknown_Entity(Config_Error):
    """Unknown entry"""

class Incorrect_Value(Config_Error):
    """Incorrect value was given"""