import re
import json
class Encoder(json.JSONEncoder):
    def default(self, o):
        try:
            s = o.serialise()
        except AttributeError:
            s = o
        finally:
            return s
            

class Decoder(json.JSONDecoder):
    def decode(self, s):
        t=super().decode(s)
        
        if t["type"] == "Param":
            return Param(t["param"],t["regex"])
        if t["type"] == "Command":
            return Command(t["cmd"],t["desc"],t["params"])
        if t["type"] == "CommandMode":
            return CommandMode(t["cmd"],t["desc"],t["subcmds"],t["params"],t["parent_mode"])
        if t["type"] == "ParamTree":
            return ParamTree(t["cmd"],t["pmap"])
        if t["type"] == "CommandTree":
            return CommandTree(t["root_mode"])
    
enc = Encoder()
dec = Decoder()
class Param():
    def __init__(self,param,regex=""):
        self.param=param
        if regex:
            self.regex=re.compile(regex)
        else:
            self.regex=""
            
    def validate(self,arg):
        if not self.regex:
            return False
        return True if self.regex.search(arg) else False

    def serialise(self):
        b= self.__dict__
        b["type"]="Param"
        return b
    
class ParamTree():
    def __init__(self,cmd,pmap=dict()):
        self.pmap = pmap
        self.cmd = cmd
        
    def add_param(self,param,chain):
        r = self.pmap
        for j in chain.reverse():
            if not j in r:
                r[str(j)]=dict()
                r=r[str(j)]
        if not r[str(param)]:
            r[str(param)]=param

    def __repr__(self):
        return self.cmd

    def serialise(self):
        b=self.__dict__
        b["type"]="ParamTree"
        return b

class Command():
    def __init__(self,cmd,desc,params = None):
        self.cmd = cmd
        self.desc = desc
        if not params:
            self.params = ParamTree(cmd)
        else:
            self.params = params
                 
    def parse(self,string):
        tokens=string.split(" ")

    def __repr__(self):
        return self.cmd
    
    def add_param(self,param,chain):
        self.params.add_param(param,chain)

    def serialise(self):
        return [ "Command", self.cmd, self.desc, self.params ]
        
class CommandMode():
    def __init__(self,cmd,name,desc,subcmds=dict(),params=None,parent=None):
        self.cmd = cmd
        self.name = name
        self.desc = desc
        self.commands = subcmds
        if not params:
            self.params=ParamTree(cmd)
        else:
            self.params = params
        self.parent_mode = parent
        
    def add_command(self,command):
        if not command in self.commands:
            self.commands[str(command)]=command
        else:
            print("INFO: %s was already added!" % (command))
            
    def add_param(self,param,chain):
        self.params.add_param(param,chain)
        pass
    
    def __repr__(self):
        return self.name

    def serialise(self):
        b=self.__dict__
        b["type"]="CommandMode"
        return b
                
class CommandTree():
    def __init__(self,root_mode):
        self.map = dict()
        self.root_mode = root_mode
        self.map[str(root_mode)]=(root_mode,None)
        
    def add_command_mode(self,mode,parent_mode):
        if not type(mode) == CommandMode:
            raise Exception("Cannot use %s for a command mode." % type(mode))
        if not str(parent_mode) in self.map:
            raise Exception("Parent mode %s for %s not found. Please add that first." % (parent_mode, mode))
        if not str(mode) in self.map:
            self.map[str(mode)]=(mode,parent_mode)
        else:
            print("INFO: %s was already added!" % (mode))
                           
    def add_command(self,cmd,mode):
        self.map[str(mode)].add_command(cmd)

    def get_parent_mode(self,mode):
        return self.map[str(mode)][1]
                
    def get_command_mode(self,mode):
        return self.map[str(mode)][0]

    def __repr__(self):
        return "Root command tree"

    def serialise(self):
        b=self.__dict__
        b["type"]="CommandTree"
        return b

    
        
f = open("commands.txt","r")
a = f.read()
for line in a.split("\n"):
    if not line:
        continue
    if line[0]=="#":
        cmode=line[1:]
        exec("%s = []" % cmode)
    else:
        l=line.split(":")
        if not len(l) == 2:
            print("ERROR PARSING: [%s]" % (line) )
            continue
        exec("%s.append(Command(\"%s\",\"%s\"))" % (cmode,l[0],l[1]))
        
user_desc           = \
"Contains a limited set of commands to view basic system information."
user_mode           = CommandMode("", "User EXEC", user_desc, user_subcmds)

enable_desc         = \
"Allows you to issue any EXEC command, enter the VLAN mode, or enter the Global Configuration mode."        
enable_mode         = CommandMode("enable", "Privileged EXEC", enable_desc, enable_subcmds)

configure_desc      = \
"Groups general setup commands and permits you to make modifications to the running configuration."
configure_mode      = CommandMode("configure", "Global Config", configure_desc, configure_subcmds)

vlan_database_desc  = \
"Groups all the VLAN commands."
vlan_database_mode  = CommandMode("vlan database", "VLAN Config", vlan_database_desc, vlan_database_subcmds)

interface_desc      = \
"Manages the operation of an interface and provides access to the router interface configuration \
commands. Use this mode to set up a physical port for a specific logical connection operation."
interface_mode      = CommandMode( ("interface","interface loopback","interface tunnel"),"Interface Config", interface_desc, interface_subcmds)

line_console_desc   = \
"Contains commands to configure USB and RS-232 console settings."
line_console_mode   = CommandMode( "line console", "Line Config (console)", line_console_desc, line_console_subcmds)

line_ssh_desc       = \
"Contains commands to configure inbound SSH settings."
line_ssh_mode       = CommandMode( "line ssh", "Line Config (ssh)", line_ssh_desc, line_ssh_subcmds)

line_telnet_desc       = \
"Contains commands to configure inbound telnet settings."
line_telnet_mode    = CommandMode( "line telnet", "Line Config (telnet)", line_telnet_desc, line_telnet_subcmds)

policymap_desc      = \
"Contains the QoS Policy-Map configuration commands."                
policymap_mode      = CommandMode( "policy-map", "Policy Map Config", policymap_desc, policymap_subcmds)

policy_class_desc   = \
"Consists of class creation, deletion, and matching commands. The class match \
commands specify Layer 2, Layer 3, and general match criteria. "
policy_class_mode   = CommandMode( "class", "Policy Class Config", policy_class_desc, policy_class_subcmds)

classmap_desc       = \
"Contains the QoS class map configuration commands for IPv4."
classmap_mode       = CommandMode( "class-map", "Class Map Config", classmap_desc, classmap_subcmds)

mac_accesslist_desc = \
"Allows you to create a MAC Access-List and to enter the mode containing MAC \
Access-List configuration commands."
mac_accesslist_mode = CommandMode( "mac access-list extended", "MAC Access-list Config", mac_accesslist_desc, mac_accesslist_subcmds)

tacacs_server_desc  = \
"Contains commands to configure properties for the TACACS servers."
tacacs_server_mode  = CommandMode( "tacacs-server host", "TACACS Config", tacacs_server_desc, tacacs_server_subcmds)

dhcp_pool_desc      = \
"Contains the DHCP server IP address pool configuration commands."
dhcp_pool_mode      = CommandMode( "ip dhcp pool", "DHCP Pool Config", dhcp_pool_desc, dhcp_pool_subcmds)

arp_accesslist_desc = \
"Contains commands to add ARP ACL rules in an ARP Access List."
arp_accesslist_mode = CommandMode( "arp access-list", "ARP Access-List Config Mode", arp_accesslist_desc, arp_accesslist_subcmds)

vlan_desc           = \
"NOT IN DOCS: Contains commands to configure private and RSPAN VLANs."
vlan_mode           = CommandMode("vlan", "Private VLAN Config", vlan_desc, vlan_subcmds)
    
cmd_tree = CommandTree(user_mode)
cmd_tree.add_command_mode(enable_mode,user_mode)

cmd_tree.add_command_mode(vlan_database_mode,enable_mode)
cmd_tree.add_command_mode(configure_mode,enable_mode)

cmd_tree.add_command_mode(interface_mode,configure_mode)
cmd_tree.add_command_mode(line_console_mode,configure_mode)
cmd_tree.add_command_mode(line_ssh_mode,configure_mode)
cmd_tree.add_command_mode(line_telnet_mode,configure_mode)
cmd_tree.add_command_mode(policymap_mode,configure_mode)
cmd_tree.add_command_mode(classmap_mode,configure_mode)
cmd_tree.add_command_mode(mac_accesslist_mode,configure_mode)
cmd_tree.add_command_mode(tacacs_server_mode,configure_mode)
cmd_tree.add_command_mode(dhcp_pool_mode,configure_mode)
cmd_tree.add_command_mode(arp_accesslist_mode,configure_mode)
cmd_tree.add_command_mode(vlan_mode,configure_mode)

cmd_tree.add_command_mode(policy_class_mode,policymap_mode)

