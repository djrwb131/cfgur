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

        
# see https://mail.gnome.org/archives/gtk-app-devel-list/2012-December/msg00003.html
# - use builders to get what you need, then toss them out asap
# - you can make copies of widgets and windows by making new builders
# - you can add specific parts of a glade file by including a tuple with
#   add_objects_from_file(filename, tuple(objects))

from settings import GLADE_FILENAME
builder = Gtk.Builder()
builder.add_from_file(GLADE_FILENAME)

from handler import Handler
ctree = reparse()
h = Handler(ctree)
builder.connect_signals(h)

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
# does one or more passes; if the list gets smaller, do another pass
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
 
