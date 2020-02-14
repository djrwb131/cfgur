## handler.py - Gtk signal handler class
from inspect import currentframe
class Handler():
    def __init__(self):
        print("Handler initialized.")

    def onDestroy(self, *args):
        self.default(currentframe().f_code.co_name,*args)
        print("Handler heard an onDestroy. Exitting!")

    
        
