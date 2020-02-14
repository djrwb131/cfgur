# json_tc.py
#
# Custom encoder/decoder for command classes
#

from json import JSONEncoder,JSONDecoder
from command import Command
from command_tree import CommandTree
from command_mode import CommandMode
from param import Param
from param_tree import ParamTree
from settings import CLASS_KEY, JSON_DEBUG
# This encoder just tries to call serialise, which allows a class to
# return a serialisable version of itself. If the object has no serialise()
# member, the JSONEncoder superclass will automatically try to serialise
# it using its own encode() function. Therefore, the encoder returns it as-is.
#
# This will allow the JSONEncoder to throw an exception if the object
# is not JSON-approved, and does not have a serialise() member.
SERIALISABLE_CLASSES = ( Command, CommandTree, CommandMode, Param, ParamTree )

class Encoder(JSONEncoder):
    def default(self, o):
        if type(o) in SERIALISABLE_CLASSES:
            jsonable = dict()
            for k in o.__dict__.keys():
                if type(o.__dict__[k]) in SERIALISABLE_CLASSES:
                    jsonable[k] = self.default(o.__dict__[k])
                else:
                    jsonable[k] = o.__dict__[k]
            return jsonable
        else:
            return o


            
# This decoder checks the _serialised_class field of a decoded object.
# If the object was encoded using serialise(), this field will
# contain the name of the class object it was serialised from.
#
# If the _serialised_class field is accessible, this decoder will check
# the try to instantiate this class using relevant info from the dict,
# then return an instance of the class.
#
# If the decoded object is not a dict, or has no _serialised_class field,
# the decoder will return the object as-is.
#
# If the object has a _serialised_class field, but no instantiation rule,
# the decoder will emit a warning and return the object as-is.

class Decoder(JSONDecoder):
    def decode(self, s):
        t=super().decode(s)
        if type(t) == dict and CLASS_KEY in t.keys():
            return self.deserialise(t)
        return t

# recursive deserialisation
    def deserialise_map(self,inp):
        ret = dict()
        for k in inp.keys():
            if CLASS_KEY in inp[k]:
                ret[k] = self.deserialise(inp[k])
            else:
                ret[k] = inp[k]
        return ret

# takes a dict containing a CLASS_KEY and
# returns its deserialised class
    def deserialise(self,t):
        if JSON_DEBUG:
            print("deserialise( %s )"% ((t[CLASS_KEY])))
        c = t[CLASS_KEY]
        
        # instantiation rules        
        if c == str(Param):
            return Param(t["param"],t["regex"])
        
        if c == str(Command):
            params = self.deserialise_map(t["params"])
            return Command(t["cmd"],t["desc"],params)
        
        if c == str(CommandMode):
            commands = self.deserialise_map(t["commands"])
            params = self.deserialise_map(t["params"])
            return CommandMode(t["cmd"],t["desc"],commands,params)
        
        if c == str(ParamTree):
            m = self.deserialise_map(t["pmap"])
            return ParamTree(t["cmd"],m)
        
        if c == str(CommandTree):
            m = self.deserialise_map(t["map"])
            r = self.deserialise(t["root_mode"])
            return CommandTree(r,m)
        
        raise TypeError("No instantiation rule for %s %s" % (CLASS_KEY,c))
