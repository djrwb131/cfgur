# command_tree.py
#
# Command tree class
#
# Contains the entire command structure
from cli_obj import CLIObject
from command_mode import CommandMode
from settings import DEBUG

class CommandTree(CLIObject):
    """
    Contains the entire tree of possible commands and command modes.
    Commands and command modes are put into dictionary entry, to keep track
    of the chain for each configuration option.
    """
    def __init__(self,root_mode,m=dict(),p=dict()):
        """
        Args:
            root_mode: the root CommandMode for this CommandTree. (required)
            m:         if restoring from save, this will be the already-deserialised dict of CommandModes.

        """
        super().__init__("Command Tree","Python class to manage the general command structure.")
        if len(m) and not len(p):
            raise Exception("CommandTree.__init__() had a modes dict but the parent dict was empty :(")
        if len(p) and not len(m):
            raise Exception("CommandTree.__init__() had a parents dict but an empty modes dict - cannot instantiate")
        self.modes = m
        self.parents = p
        self.root_mode = root_mode
        self.modes[str(root_mode)]=root_mode
        self.parents[str(root_mode)]=None
            
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
        if not str(parent_mode) in self.modes:
            raise Exception("Parent mode %s for %s not found. Please add that first." % (parent_mode, mode))
        if not str(mode) in self.modes:
            self.modes[str(mode)]=mode
            self.parents[str(mode)]=parent_mode
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
        Adds a command to the specified CommandMode. This is a wrapper function which
        cleans up the mode name and calls the pertinent CommandMode's add_command().
        Args:
            Command cmd: the Command to be added.
            (CommandMode|str) mode: the CommandMode to add this command to.
        """
        mode_clean = self._mode_cleanup(mode)
        if type(mode_clean) == tuple:
            for j in mode_clean:
                self.modes[j].add_command(cmd)
        else:
            self.modes[mode_clean].add_command(cmd)
            
    def get_all_modes(self):
        return self.modes.keys()
    
    def get_parent_mode(self,mode):
        """
        Returns the parent CommandMode of the CommandMode given.
        Args:
            (CommandMode|str) mode: the CommandMode whose parent is to be returned.
        """
        return self.parents[str(mode)]
