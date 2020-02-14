# param.py
#
# Command parameters and input validation
#
from cli_obj import CLIObject
class Param(CLIObject):
    def __init__(self,param,desc,regex=""):
        if type(param) == dict and not desc and not regex:
            self.__dict__ = param
        else:
            self.param = param
            self.desc = desc
            self.regex = regex
        super().__init__(self.param,self.desc)
        
    def validate(self,arg):
        if not self.regex:
            return False
        return True if self.regex.search(arg) else False

    
