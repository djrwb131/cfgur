# command_mode.py
#
# Command mode class
#
# Contains the mode, description, and available commands.
from cli_obj import CLIObject
from param_tree import ParamTree
class CommandMode(CLIObject):
    def __init__(self,cmd,name=None,desc=None,subcmds=None,params=None):
        if type(cmd) == dict and not name and not desc and not subcmds and not params:
            self.__dict__ = cmd
            super().__init__(self.name,self.desc)
        else:
            self.entry_cmd = cmd
            if not subcmds:
                subcmds = dict()
            self.commands = subcmds
            super().__init__(name,desc)
            if not params:
                self.params=ParamTree(cmd)
            else:
                self.params = params
        
    def add_command(self,command):
        if not command in self.commands:
            self.commands[str(command)]=command
        elif DEBUG:
            print("INFO: %s was already added!" % (command))
            
    def add_param(self,param,chain):
        self.params.add_param(param,chain)
        pass
