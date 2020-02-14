# command.py
#
# Command tree and descriptions
#
from param_tree import ParamTree
from settings import DEBUG

class Command():
    def __init__(self,cmd,desc,params = None):
        self.cmd = cmd
        self.desc = desc
        if not params:
            self.params = ParamTree(cmd)
        else:
            self.params = params
                 
    def parse(self,istr):
        tokens=istr.split(" ")

    def __str__(self):
        return self.cmd
    
    def add_param(self,param,chain):
        self.params.add_param(param,chain)

                
