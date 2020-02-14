# cli_obj.py
#
# Commandline Interface Object
#
# Contains information common to all objects, such as name and description.
# Contains a generic serialisation command which scans the internal dict
# and serialises all JSON-approved object types.

from settings import JSON_DEBUG

class CLIObject():  
    def __init__(self,name,desc):
        self.TYPE=str(self.__class__)
        self.name = name
        self.desc = desc
        self.__jsonable = dict()
        
    def serialise(self):

        if JSON_DEBUG:
            print("Serialising all these:\n----\n%s\n----\n"%(self.__dict__.keys()))
        for i in self.__dict__.keys():
            if JSON_DEBUG:
                print("Trying to serialise %s ..." % (str(self.__dict__[i])))
            if "serialise" in dir(self.__dict__[i]):
                self.__dict__[i] = self.__dict__[i].serialise()
                if JSON_DEBUG:
                    print("OK")
            else:
                if JSON_DEBUG:
                    print("no serialise()")
                self.__jsonable[i] = self.__dict__[i]
        self.__jsonable["__SERIALISED_CLASS"] = self.TYPE
        return self.__jsonable

