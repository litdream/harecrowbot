import os

class Version:
    def __init__(self, ctx):
        self.ctx = ctx
        self.major = 0
        self.minor = 2
        self.release = 0

    def version(self):
        if self.release == 0:
            return "harecrowbot v{}.{}".format(self.major, self.minor)
        else:
            return "harecrowbot v{}.{}r{}".format(self.major, self.minor, self.release)
        
