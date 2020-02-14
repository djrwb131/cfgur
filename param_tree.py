from cli_obj import CLIObject
class ParamTree(CLIObject):
    def __init__(self,cmd,pmap=dict()):
        if type(cmd) == dict and not pmap:
            self.__dict__ = cmd
            super().__init__(self.name,"Parameter tree for %s" % (self.name,))
        else:
            super().__init__(cmd,"Parameter tree for %s" % (cmd,))
            self.pmap = pmap
        
    def add_param(self,param,chain):
        r = self.pmap
        for j in chain.reverse():
            if not j in r:
                r[str(j)]=dict()
                r=r[str(j)]
        if not r[str(param)]:
            r[str(param)]=param

