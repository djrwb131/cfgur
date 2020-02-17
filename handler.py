## handler.py - Gtk signal handler class
from inspect import currentframe
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Handler():
    def __init__(self,ct):
        self.selectedMode = str(ct.root_mode)
        self.commandTree = ct
        print("Handler initialized.")

    def onMainWindowDestroy(self, *args):
##        print("Handler heard an onDestroy. Exitting!")
        Gtk.main_quit()

    def on_commandList_row_activated(self, *args):
        sel,path,col = args[:3]
        view = sel.get_tree_view()
        if col.get_name() == "lvc_commandname":
            cindex = view.get_columns().index(col)  
            cmd = self.commandTree[self.selectedMode][view.get_model()[path][cindex]]
            builder = Gtk.Builder()
            builder.add_objects_from_file("ui.glade",("commandInfoDialog",))

            builder.get_object("cid_tv_format").get_buffer().insert_at_cursor(cmd.fmtstr,len(cmd.fmtstr))
            builder.get_object("cid_tv_synopsis").get_buffer().insert_at_cursor(cmd.desc,len(cmd.desc))
            builder.get_object("cid_tv_termdef").get_buffer().insert_at_cursor("TBI",len("TBI"))
            builder.connect_signals(self)
            
            dialog = builder.get_object("commandInfoDialog")
            print("opening dialog for %s ... " % str(cmd))
            dialog.show_all()

    def on_cid_closeButton_clicked(self, *args):
        return self.on_commandInfoDialog_destroy(args[0])
    def on_commandInfoDialog_close(self, *args):
        return self.on_commandInfoDialog_destroy(*args)
    def on_commandInfoDialog_destroy(self, *args):
        return args[0].destroy()
        
    def on_commandList_show(self, *args):
        self.on_commandList_stale(*args)
        
    def on_commandModeSelection_changed(self, *args):
        commandModeTree = args[0]
        store, paths = commandModeTree.get_selection().get_selected_rows()
        path = paths[0]
        self.selectedMode = store[path][0]
        
    def on_commandList_stale(self, *args):
        commandList = args[0]
        commandList.clear()
        for cmd in self.commandTree[self.selectedMode].commands:
            r = commandList.append()
            # commandList.set( r, { 0:cmd.name, 1:cmd.default, 2:cmd.default } )
            commandList.set( r, { 0:cmd } )
