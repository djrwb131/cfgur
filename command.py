# command.py
#
# Command tree and descriptions
#
from param import ParamTree
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

    def serialise(self):
        b = {
            "_serialised_class":"Command",
            "cmd":self.cmd,
            "desc":self.desc,
            "params":self.params
            }
        return b
        
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

    def serialise(self):
        b=  {
            "_serialised_class":"CommandMode",
            "cmd":self.cmd,
            "name":self.name,
            "desc":self.desc,
            "commands":self.commands,
            "params":self.params
            }
        return b
                
class CommandTree():
    """
    Contains the entire tree of possible commands and command modes.
    Commands and command modes are put into dictionary entry, to keep track
    of the chain for each configuration option.
    """
    def __init__(self,root_mode,map=dict()):
        """
        Initialises the CommandTree map and sets the root_mode.
        Args:
            root_mode: the root CommandMode for this CommandTree. (required)

        """
        self.map = map
        self.root_mode = root_mode
        self.map[str(root_mode)]=(root_mode,None)
            
    def add_command_mode(self,mode,parent_mode=None):
        """
        Adds a command mode to the CommandTree.
        Args:
            (CommandMode|str) mode: the CommandMode to be added. (required)
            (CommandMode|str) parent_mode: the CommandMode from which this mode is accessible. (optional - default is root_mode)
        """
        if not parent_mode:
            parent_mode = self.root_mode
        if not type(mode) == CommandMode:
            raise Exception("Cannot use %s for a command mode." % type(mode))
        if not str(parent_mode) in self.map:
            raise Exception("Parent mode %s for %s not found. Please add that first." % (parent_mode, mode))
        if not str(mode) in self.map:
            self.map[str(mode)]=(mode,parent_mode)
        elif DEBUG:
            print("INFO: %s was already added!" % (mode))

    def _mode_cleanup(self,m):
        # Command modes have a number of ways they are refered to, as
        # well as numerous typos. This map cleans things up.
        
        #TODO: clean up these issues in a more robust way
        mode = str(m)
        newmode = mode
        if mode == "Line console":
            newmode = "Line Config (console)"
        elif mode == "Line telnet":
            newmode = "Line Config (telnet)"
        elif mode == "Line SSH":
            newmode = "Line Config (ssh)"
        elif mode == "Privileged Exec" or mode == "Privileged Exec Mode":
            newmode = "Privileged EXEC"
        elif mode == "Global ConfigC":
            newmode = "Global Config"
        elif mode == "VLAN configuration":
            newmode = "Private VLAN Config"
        elif mode == "VLAN Mode" or mode == "VLAN database":
            newmode = "VLAN Config"
        elif mode == "Ipv4-Access-List Config":
            newmode = "IPv4-Access-List Config"
        elif mode == "ARP Access-List Config Mode" or mode == "ARP Access-list Config":
            newmode = "ARP Access-List Config"
        elif mode == "Ipv6-Access-List Config":
            newmode = "IPv6-Access-List Config"
        elif mode == "Ipv6-Class-Map Config" or mode == "Ipv6-Class-Map Configuration mode":
            newmode = "IPv6-Class-Map Config"
        elif mode == "AAA User Config":
            newmode = "AAA IAS User Config"
            
            
        # this may not be a good idea - are there some commands which only work in int or int-range?
        elif mode == "Interface Range Config":
            newmode = "Interface Config"
        else:
            if mode == "Line Config":
                if DEBUG:
                    print("Line Config is actually 3 modes! Nice!")
                newmode = ("Line Config (console)", "Line Config (telnet)", "Line Config (ssh)")
            else:
                return mode
        if DEBUG: 
            print( "%s -> %s" % (mode, newmode) )
        return newmode
        
        
    def add_command(self,cmd,mode):
        """
        Adds a command to the specified CommandMode.
        Args:
            Command cmd: the Command to be added.
            (CommandMode|str) mode: the CommandMode to add this command to.
        """
        mode_clean = self._mode_cleanup(mode)
        if type(mode_clean) == tuple:
            for j in mode_clean:
                self.map[j][0].add_command(cmd)
        else:
            self.map[mode_clean][0].add_command(cmd)
            
    def get_all_modes(self):
        return self.map.keys()
    
    def get_parent_mode(self,mode):
        """
        Returns the parent CommandMode of the CommandMode given.
        Args:
            (CommandMode|str) mode: the CommandMode whose parent is to be returned.
        """
        return self.map[str(mode)][1]

    def serialise(self):
        b = {
            "_serialised_class":"CommandTree",
            "map":self.map,
            "root_mode":self.root_mode
            }
        return b
