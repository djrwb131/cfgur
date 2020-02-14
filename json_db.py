# json_db.py
#
# Custom encoder/decoder for command classes
#

from json import JSONEncoder,JSONDecoder,load
from command import Command
from command_tree import CommandTree
from command_mode import CommandMode
from param import Param
from param_tree import ParamTree
from settings import CLASS_KEY, JSON_DEBUG, JSON_FILENAME

SERIALISABLE_CLASSES = ( Command, CommandTree, CommandMode, Param, ParamTree )

# This encoder scans the object for embedded, serialisable objects. If
# found, it will serialise each one recursively. This encoder is very
# generic and will likely work with any class - but requires each
# class to be put into the SERIALISABLE_CLASSES constant, for posterity.
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


            
# This decoder checks the CLASS_KEY field of a decoded object.
# If the object was encoded using serialise(), this field will
# contain the name of the class object it was serialised from.
#
# If the CLASS_KEY field is accessible, this decoder will check
# the try to instantiate this class using relevant info from the dict,
# then return an instance of the class.
#
# If the decoded object is not a dict, or has no CLASS_KEY field,
# the decoder will return the object as-is.
#
# If the object has a CLASS_KEY field, but no instantiation rule,
# the decoder will raise an exception.

class Decoder(JSONDecoder):
    def decode(self, s):
        t=super().decode(s)
        if type(t) == dict and CLASS_KEY in t.keys():
            return self.deserialise(t)
        return t

# recursive deserialisation
    def deserialise_map(self,inp):
        if JSON_DEBUG:
            print("Deserialising map:\n----\n%s\n----\n" % (str(inp.keys())))
        ret = dict()
        for k in inp.keys():
            if inp[k] and CLASS_KEY in inp[k]:
                ret[k] = self.deserialise(inp[k])
            else:
                ret[k] = inp[k]
        return ret

# takes a dict containing a CLASS_KEY and
# returns its deserialised class
    def deserialise(self,t):
        if not type(t) == dict or not CLASS_KEY in t:
            return t
        if JSON_DEBUG:
            print(type(t))
            print("deserialise to ( %s )"% ((t[CLASS_KEY])))
            print("keys: %s" % t.keys())
        c = t[CLASS_KEY]
        for i in t.keys():
            if t[i] == dict:
                t[i]=self.deserialise_map(t[i])
        # instantiation rules        
        if c == str(Param):
            return Param(t)
        
        if c == str(Command):
            return Command(t)
        
        if c == str(CommandMode):
            return CommandMode(t)
        
        if c == str(ParamTree):
            return ParamTree(t)
        
        if c == str(CommandTree):
            return CommandTree(t)
        
        raise TypeError("No instantiation rule for %s %s" % (CLASS_KEY,c))

# Convenience function to load the command tree
def get_command_tree():
    cfg = open(JSON_FILENAME,"rb")
    ctd = load(cfg,cls=Decoder)
    cfg.close()
    return ctd
