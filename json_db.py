# json_tc.py
#
# Custom encoder/decoder for command classes
#

from json import JSONEncoder,JSONDecoder
from command import Command,CommandTree,CommandMode
from param import Param,ParamTree
# This encoder just tries to call serialise, which allows a class to
# return a serialisable version of itself. If the object has no serialise()
# member, the JSONEncoder superclass will automatically try to serialise
# it using its own encode() function. Therefore, the encoder returns it as-is.
#
# This will allow the JSONEncoder to throw an exception if the object
# is not JSON-approved, and does not have a serialise() member.

class Encoder(JSONEncoder):
    def default(self, o):
        try:
            s = o.serialise()
        except AttributeError:
            s = o
        finally:
            return s

            
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
        if type(t) == dict and "_serialised_class" in t.keys():
            return self.deserialise(t)
        return t
        
# instantiation rules
    def deserialise(self,t):
        print("deserialise( %s )"% (str(t)))
        if t["_serialised_class"] == "Param":
            return Param(t["param"],t["regex"])
        if t["_serialised_class"] == "Command":
            return Command(t["cmd"],t["desc"],t["params"])
        if t["_serialised_class"] == "CommandMode":
            return CommandMode(t["cmd"],t["desc"],t["subcmds"],t["params"],t["parent_mode"])
        if t["_serialised_class"] == "ParamTree":
            return ParamTree(t["cmd"],t["pmap"])
        if t["_serialised_class"] == "CommandTree":
            return CommandTree(t)
        print("ERROR: no instantiation rule for _serialised_class %s. Returning as-is..." % (t["_serialised_class"]))
        return t
