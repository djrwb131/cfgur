import json
from command import CommandTree,CommandMode,Command
from json_db import Encoder
from const_cmdmodes import *
from string import ascii_uppercase,ascii_letters
from settings import DEBUG

APPENDIX_START  = 558
APPENDIX_END    = 578

enc = Encoder

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
    if cstr[0] in ascii_uppercase:
        if cstr == "Ezconfig":
            return True
        return False
    for i in l:
        if cstr in i[0]:
            return True
    return False

def init():
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
    print("Scanning %i commands..." % (len(cmds)+len(fmtcmds)))
    global pagenum
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
                while not page[i][tabs] in ascii_letters:
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
                
                while not page[i][tabs] in ascii_letters:
                    tabs += 1
                    
                modes.append(page[i][tabs:].strip())
                tabscmp = tabs
                page, i = next_line(page, i)
                while True:
                    if len(page[i]) < tabs:
                        break
                    
                    tabscmp = 6
                    if page[i][:tabscmp] == "      ":
                        while not page[i][tabscmp] in ascii_letters:
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
        print("WARNING: Due to odd formatting in the appendix, [%s] was not parsed." % (cmd,))
        
    print("Writing results to json...")
    f = open("cmd_tree.json","w")
    json.dump(cmd_tree,f,cls=enc)
    f.close()
    print("Complete!")

        
