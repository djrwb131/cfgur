#!/usr/bin/python3
import gi

#TODO: add Gtk support in subclasses of Command*
# or find another clean way of implementing UI connections

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import json_db

def load_json():
    return json_db.get_command_tree()

def reparse():
    import config_parser
    config_parser.init()
    return config_parser.cmd_tree

def hello(button):
    print("Hello world!")
    
def goodbye(button):
    print("Goodbye world!")
    Gtk.main_quit()
    
def setSelectedCommandMode(commandModeTree):
    global selected_mode
    store, paths = commandModeTree.get_selection().get_selected_rows()
    path = paths[0] # can't have mode than one mode active at a time
    selected_mode = store[path][0]
    print("Selected mode is now [ %s ]" % (str(selected_mode)))
    pass

def updateCommandList(commandList):
    global ctree
    global selected_mode
    if not selected_mode:
        return
    commandList.clear()
    print("Found %i commands" % ( len(ctree.modes[selected_mode].commands.keys())))
    for cmd in ctree.modes[selected_mode].commands.keys():
        r = commandList.append()
        commandList.set(r, { 0:cmd } )
        
handlers = {
    "onMainWindowDestroy": goodbye,
    "hello": hello,
    "commandModeChanged": setSelectedCommandMode,
    "commandListNeedsUpdate": updateCommandList
    }
builder = Gtk.Builder()
builder.add_from_file("ui.glade")
builder.connect_signals(handlers)

ctree = reparse() 
window = builder.get_object("mainWindow")
gtree = builder.get_object("commandModeTreeStore")
clist = builder.get_object("commandListStore")
selected_mode = None
modepass=list(ctree.get_all_modes())


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

# solves the issue of a command mode's parent not being loaded
# does several passes; if the list gets smaller, do another pass
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
                       
window.show_all()  
Gtk.main()
 
