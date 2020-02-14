# command.py
#
# Command tree and descriptions
#
from cli_obj import CLIObject
from param_tree import ParamTree
from settings import DEBUG

class Command(CLIObject):
    def __init__(self,name,desc = None,params = None):
        if type(name) == dict and not desc and not params:
            self.__dict__ = name
            super().__init__(self.name,self.desc)
        else:  
            super().__init__(name,desc)
            if not params:
                self.params = ParamTree(name)
            else:
                self.params = params
                 
    def parse(self,istr):
        tokens=istr.split(" ")

    def add_param(self,param,chain):
        self.params.add_param(param,chain)

                
