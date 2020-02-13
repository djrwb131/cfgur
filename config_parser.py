import re
import json
import string

APPENDIX_START  = 558
APPENDIX_END    = 578
DEBUG = True
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
    def __init__(self,param,desc,regex=""):
        self.param=param
        self.desc=desc
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

    def __str__(self):
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

    def __str__(self):
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
        elif DEBUG:
            print("INFO: %s was already added!" % (command))
            
    def add_param(self,param,chain):
        self.params.add_param(param,chain)
        pass
    
    def __str__(self):
        return self.name

    def serialise(self):
        b=self.__dict__
        b["type"]="CommandMode"
        return b
                
class CommandTree():
    """
    Contains the entire tree of possible commands and command modes.
    Commands and command modes are put into dictionary entry, to keep track
    of the chain for each configuration option.
    """
    def __init__(self,root_mode):
        """
        Initialises the CommandTree map and sets the root_mode.
        Args:
            root_mode: the root CommandMode for this CommandTree. (required)

        """
        self.map = dict()
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
            
            
        # this may not be a good idea - are there some commands which only work in int-range?
        elif mode == "Interface Range Config":
            newmode = "Interface Config"
        else:
            if mode == "Line Config":
                if DEBUG:
                    print("%s is actually 3 modes. Adding to Line SSH and Line telnet..." % (mode) )
                self.map["Line Config (telnet)"][0].add_command(cmd)
                self.map["Line Config (ssh)"][0].add_command(cmd)
                newmode = "Line Config (console)"
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
        self.map[mode_clean][0].add_command(cmd)

    def get_parent_mode(self,mode):
        """
        Returns the parent CommandMode of the CommandMode given.
        Args:
            (CommandMode|str) mode: the CommandMode whose parent is to be returned.
        """
        return self.map[str(mode)][1]

    def serialise(self):
        b=self.__dict__
        b["type"]="CommandTree"
        return b

# The command mode information is spread across the whole document.
# It's easier just to create these manually, rather than write a parser
# for it.
user_desc           = \
"Contains a limited set of commands to view basic system information."
user_mode           = CommandMode("", "User EXEC", user_desc)

enable_desc         = \
"Allows you to issue any EXEC command, enter the VLAN mode, or enter the Global Configuration mode."        
enable_mode         = CommandMode("enable", "Privileged EXEC", enable_desc)

configure_desc      = \
"Groups general setup commands and permits you to make modifications to the running configuration."
configure_mode      = CommandMode("configure", "Global Config", configure_desc)

vlan_database_desc  = \
"Groups all the VLAN commands."
vlan_database_mode  = CommandMode("vlan database", "VLAN Config", vlan_database_desc)

interface_desc      = \
"Manages the operation of an interface and provides access to the router interface configuration \
commands. Use this mode to set up a physical port for a specific logical connection operation."
interface_mode      = CommandMode( ("interface","interface loopback","interface tunnel"),"Interface Config", interface_desc)

line_console_desc   = \
"Contains commands to configure USB and RS-232 console settings."
line_console_mode   = CommandMode( "line console", "Line Config (console)", line_console_desc)

line_ssh_desc       = \
"Contains commands to configure inbound SSH settings."
line_ssh_mode       = CommandMode( "line ssh", "Line Config (ssh)", line_ssh_desc)

line_telnet_desc       = \
"Contains commands to configure inbound telnet settings."
line_telnet_mode    = CommandMode( "line telnet", "Line Config (telnet)", line_telnet_desc)

policymap_desc      = \
"Contains the QoS Policy-Map configuration commands."                
policymap_mode      = CommandMode( "policy-map", "Policy-Map Config", policymap_desc)

policy_class_desc   = \
"Consists of class creation, deletion, and matching commands. The class match \
commands specify Layer 2, Layer 3, and general match criteria. "
policy_class_mode   = CommandMode( "class", "Policy-Class-Map Config", policy_class_desc)

classmap_desc       = \
"Contains the QoS class map configuration commands for IPv4."
classmap_mode       = CommandMode( "class-map", "Class-Map Config", classmap_desc)
ipv6_classmap_desc  = \
"Contains the QoS class map configuration commands for IPv6."
ipv6_classmap_mode  = CommandMode( "class-map ipv6", "IPv6-Class-Map Config", ipv6_classmap_desc)
mac_accesslist_desc = \
"Allows you to create a MAC Access-List and to enter the mode containing MAC \
Access-List configuration commands."
mac_accesslist_mode = CommandMode( "mac access-list extended", "Mac-Access-List Config", mac_accesslist_desc)

tacacs_server_desc  = \
"Contains commands to configure properties for the TACACS servers."
tacacs_server_mode  = CommandMode( "tacacs-server host", "TACACS Config", tacacs_server_desc)

dhcp_pool_desc      = \
"Contains the DHCP server IP address pool configuration commands."
dhcp_pool_mode      = CommandMode( "ip dhcp pool", "DHCP Pool Config", dhcp_pool_desc)

arp_accesslist_desc = \
"Contains commands to add ARP ACL rules in an ARP Access List."
arp_accesslist_mode = CommandMode( "arp access-list", "ARP Access-List Config", arp_accesslist_desc)

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
cmd_tree.add_command_mode(ipv6_classmap_mode,configure_mode)
cmd_tree.add_command_mode(mac_accesslist_mode,configure_mode)
cmd_tree.add_command_mode(tacacs_server_mode,configure_mode)
cmd_tree.add_command_mode(dhcp_pool_mode,configure_mode)
cmd_tree.add_command_mode(arp_accesslist_mode,configure_mode)

# These modes are not listed in Chapter 1

vlan_desc           = \
"NODOCS: Contains commands to configure private and RSPAN VLANs."
vlan_mode           = CommandMode("vlan", "Private VLAN Config", vlan_desc)

time_range_desc     = \
"NODOCS: Contains commands for time-range based ACL rules."
time_range_mode     = CommandMode("time-range", "Time-Range Config", time_range_desc)

ipv4_acl_desc       = \
"NODOCS: Contains commands for configuring extended (named) IP ACLs."
ipv4_acl_mode       = CommandMode("ip access-list", "IPv4-Access-List Config", ipv4_acl_desc)

ipv6_acl_desc       = \
"NODOCS: Contains commands for configuring IPv6 ACLs."
ipv6_acl_mode       = CommandMode("ipv6 access-list", "IPv6-Access-List Config", ipv4_acl_desc)

aaa_ias_desc        = \
"NODOCS: Contains configuration options for users in the IAS database."
aaa_ias_mode        = CommandMode("aaa ias-username", "AAA IAS User Config", aaa_ias_desc)

mailserver_desc     = \
"NODOCS: Contains configuration commands for SMTP mailserver (email alerts)."
mailserver_mode     = CommandMode("mail-server", "Mail Server Config", mailserver_desc)

cmd_tree.add_command_mode(vlan_mode,configure_mode)
cmd_tree.add_command_mode(time_range_mode,configure_mode)
cmd_tree.add_command_mode(ipv4_acl_mode,configure_mode)
cmd_tree.add_command_mode(ipv6_acl_mode,configure_mode)
cmd_tree.add_command_mode(aaa_ias_mode,configure_mode)
cmd_tree.add_command_mode(mailserver_mode,configure_mode)

cmd_tree.add_command_mode(policy_class_mode,policymap_mode)

#TODO: clean this up
def get_page(num):
    f=open("pages/cli-%i.txt" % (num),"rb")
    buf = f.read().decode("iso8859")
    f.close()
    return buf

#TODO: clean this up
def next_line(page,line):
    #TODO: something other than this, this is awful
    global pagenum
    i = line + 1
    if i == len(page):
        pagenum += 1
        page = get_page(pagenum).split('\n')[2:-4]
        i = 0
    return (page, i)

#TODO: clean this up
def is_cmd(cstrb,l):
    cstra=cstrb.strip()
    if not cstra:
        return False
    if cstra[0:3] == "no ":
        cstr = cstra[3:]
    else:
        cstr = cstra
    if cstr[0] in string.ascii_uppercase:
        if cstr == "Ezconfig":
            return True
        return False
    for i in l:
        if cstr in i[0]:
            return True
    return False

cmds=[]
fmtcmds=[]
print("Scanning appendix...")
for i in range(APPENDIX_START,APPENDIX_END+1):
    # grab page string, split by newline, remove header and footer
    c = get_page(i).split('\n')[2:-4]
    # create Command objects from each line
    for j in c:
        # get rid of formatting and artifacts
        t = j.split('.')
        # add a tuple to the cmds list for later parsing
        
        # the ACL commands are the only commands in the appendix which use
        # {} in their title.
        # we can parse them separately.
        if not t[0].strip(' ')[0][0] == '{':
            cmds.append( ( t[0].strip(' '), t[-1].strip(' ') ) )
        else:
            fmtcmds.append( ( t[0].strip(' '), t[-1].strip(' ') ) )
            



##        Now for the bulk of the computation!
##        Each command has its own paragraph, which have no real delimiters
##        except for the command titles.
##
##        Luckily, command titles have no formatting. They are simply the full
##        lowercase command, as they would be typed into the CLI.
##        
##        For example, the line "aaa accounting" will begin information about
##        the aaa accounting command. Then, it will have its description, format
##        table, and terms/definitions table. Then, the line "no aaa accounting"
##        shows that the paragraph about "aaa accounting" has ended.
##        
##        A lot of the time, the next command title after a given will be
##        its negation (such as "no aaa accounting"), but this is not ensured.
##        So, we should grab a list of every valid command before parsing anything.
##        Then, we can scan each line to see if it's a valid command name, on its
##        own line. If so, the paragraph is complete, and we can stop parsing.
##
##        A list of every valid command is in the appendix (pages 558-578). Negations
##        are not listed, and not all commands can be negated. This should be kept
##        in mind whilst parsing.
from time import sleep        
print("Scanning commands...")
pagenum = 0
for cmd in cmds:
    # some commands in the appendix list their command mode in brackets
    # lets strip that off, because the info is in the format table as well
    name = cmd[0].split('(')[0].strip()
    pagenum = int(cmd[1])
    page = get_page(pagenum).split('\n')[2:-4]
    i = 0
    end = len(page)
    
    while page[i].split('(')[0].strip() != name:
        page, i = next_line(page, i)
    start = i
    done = False
    modes = []
    fmt = ""
    desc = ""

    page, i = next_line(page, i)
    while not done:
        
        if page[i][:7] == " Format":
            tabs=8
            while not page[i][tabs] in string.ascii_letters:
                tabs+=1
            fmt = page[i][tabs:]
            page, i = next_line(page, i)
            
            while page[i][:tabs] == ''.join(" " for i in range(tabs)):
                fmt += page[i].strip(" ")
                page, i = next_line(page, i)

        
        elif page[i][:5] == " Mode":
            if len(modes) > 0:
                # false positive, we already found the modes.
                # Just add it to the description I guess.
                # TODO: anything but this
                desc += page[i] + '\n'
                page, i = next_line(page, i)
                continue
                
            tabs=6
            
            if len(page[i]) <= tabs:
                page, i = next_line(page, i)
                continue
            
            while not page[i][tabs] in string.ascii_letters:
                tabs += 1
                
            modes.append(page[i][tabs:].strip())
            tabscmp = tabs
            page, i = next_line(page, i)
            while True:
                if len(page[i]) < tabs:
                    break
                
                tabscmp = 6
                if page[i][:tabscmp] == "      ":
                    while not page[i][tabscmp] in string.ascii_letters:
                        tabscmp += 1
                    
                if not tabscmp == tabs:
                    break
                modes.append(page[i][tabscmp:].strip())
                page, i = next_line(page, i)

        
        elif is_cmd(page[i],cmds):
            try:
                c = Command(name,desc)
                c.fmtstr = fmt
                for m in modes:
                    cmd_tree.add_command(c,m)
                done = True
            except Exception as e:
                print("---%s---\nFormat: %s\nModes: %s\nDesc:\n%s\n\n" % (name,fmt,modes,desc))
                print("ERROR happened on page ", str(pagenum))
                raise e
            
        else:
            desc += page[i] + '\n'
            page, i = next_line(page, i)

for cmd in fmtcmds:
    # these are more of a group of commands
    # we need to split them into their own CommandModes
    pass
    
        
