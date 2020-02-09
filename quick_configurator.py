import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="Quick Configurator")

        self.box_commandline = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box_commandline)
        self.commandline = Gtk.Entry()
        self.commandline.set_text("TEST")
        self.box_commandline.pack_start(self.commandline,True,True,0)
window = MainWindow()
window.show_all()
window.connect("destroy",Gtk.main_quit)
Gtk.main()
