# command_mode.py
#
# Command mode class
#
# Contains the mode, description, and available commands.
from cli_obj import CLIObject
from param_tree import ParamTree
class CommandMode():
    def __init__(self,cmd,name,desc,subcmds=dict(),params=None):
        self.cmd = cmd
        self.name = name
        self.desc = desc
        self.commands = subcmds
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
    
    def __str__(self):
        return self.name
