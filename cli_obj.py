# cli_obj.py
#
# Commandline Interface Object
#
# Contains information common to all objects, such as name and description.
# Contains a generic serialisation command which scans the internal dict
# and serialises all JSON-approved object types.

from settings import JSON_DEBUG,CLASS_KEY

class CLIObject():  
    def __init__(self,name,desc):
        self.__dict__[CLASS_KEY]=str(self.__class__)
        self.name = name
        self.desc = desc
        
    def __str__(self):
        return self.name
    
