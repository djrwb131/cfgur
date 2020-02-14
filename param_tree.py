class ParamTree():
    def __init__(self,cmd,pmap=dict()):
        self.pmap = pmap
        self.cmd = cmd
        
    def add_param(self,param,chain):
        r = self.pmap
        for j in chain.reverse():
            if not j in r:
                r[str(j)]=dict()
                r=r[str(j)]
        if not r[str(param)]:
            r[str(param)]=param

    def __str__(self):
        return self.cmd

    def serialise(self):
        b = {
            "_serialised_class":"ParamTree",
            "pmap":self.pmap,
            "cmd":self.cmd
            }
        return b

