import os

'''
Simplified Changelog:

    0.1    initial
    0.2    begin to support :hello
    0.3    support :weather
    0.3r1  :weather is refactored and supports daily min/max
'''

class Version:
    def __init__(self, ctx):
        self.ctx = ctx
        self.major = 0
        self.minor = 3
        self.release = 1

    def version(self):
        if self.release == 0:
            return "harecrowbot v{}.{}".format(self.major, self.minor)
        else:
            return "harecrowbot v{}.{}r{}".format(self.major, self.minor, self.release)
        
