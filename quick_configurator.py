#!/usr/bin/python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

try:
    cfg = open("cmd_tree.json","r")
    from json_db import Decoder
    import json
    ctree = json.load(cfg,cls=Decoder)
    cfg.close()
    
except Exception as e:
    print("ERROR LOADING JSON FILE: %s" % (e,))
    import config_parser
    config_parser.init()
    ctree = config_parser.cmd_tree

def hello(button):
    print("Hello world!")
    
def goodbye(button):
    print("Goodbye world!")
    Gtk.main_quit()
    
def switchMode(commandModeTree):
    global clist
    
    pass
handlers = {
    "onMainWindowDestroy": goodbye,
    "hello": hello,
    "commandModeChanged": switchMode
    }
builder = Gtk.Builder()
builder.add_from_file("ui.glade")
builder.connect_signals(handlers)
    
window = builder.get_object("mainWindow")
gtree = builder.get_object("commandModeTreeStore")
clist = builder.get_object("commandListStore")
select = builder.get_object("commandModeSelection")
modepass=list(ctree.get_all_modes())


#This is ridiculous. We'll need to add gtk info into the config_parser itself
#Getting rows by data within them is unusually hard - am I missing something?
def get_iter_by_value(tree,col,value,row=False):
    if not row:
        row = tree.get_iter_first()
    if tree[row][col] == value:
        return row
    if tree.iter_n_children(row) == 0:
        return None
    for i in range(tree.iter_n_children(row)):
        ret = get_iter_by_value(tree,col,value,tree.iter_nth_child(row,i))
        if ret:
            return ret
    return None

while len(modepass) > 0:
    removed = []
    for i in modepass:
        parent=ctree.get_parent_mode(i)
        if parent == None:
            r = gtree.append(None)
            gtree.set(r, {0:i} )
            removed.append(i)
        else:
            a = get_iter_by_value(gtree,0,str(parent))
            if a:
                r = gtree.append(a)
                gtree.set(r,{0:i})
                removed.append(i)
    if len(removed) == 0:
        print("Some modes could not be added, as their parents could not be found:")
        for i in modepass:
            print(i)
        break
    for i in removed:
        modepass.remove(i)
                       
#window.show_all()  
#Gtk.main()
 
