# param.py
#
# Command parameters and input validation
#
class Param():
    def __init__(self,param,desc,regex=""):
        self.param=param
        self.desc=desc
        if regex:
            self.regex=re.compile(regex)
        else:
            self.regex=""
            
    def validate(self,arg):
        if not self.regex:
            return False
        return True if self.regex.search(arg) else False

    def serialise(self):
        b = {
            "_serialised_class":"Param",
            "param":self.param,
            "desc":self.desc,
            "regex":self.regex
            }
        return b
    
