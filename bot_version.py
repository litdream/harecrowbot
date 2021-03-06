import os

'''
Simplified Changelog:

    0.1    initial
    0.2    begin to support ;hello
    0.3    support ;weather
    0.3r1  ;weather is refactored and supports daily min/max
    0.4    ;mob game is supported
    0.4r1  ;mob is reserved.  Change to ;mox.  And, duplicate init bugfix.
    0.4r2  ;mob interface change, and command prefix changed from ':' to ';' 
    0.5    ;laugh support
    0.6    ;num game support.
    0.6r1  ;num max_chance is 5, (or configurable)
           ;num, if everyone runs out, Bot will reveal the answer.
'''

'''
TODO:  
  - Record historic best for both ;num and ;mox
    - This need database.
  - version can support list features, and history

'''


class Version:
    def __init__(self, ctx):
        self.ctx = ctx
        self.major = 0
        self.minor = 6
        self.release = 1

    def version(self):
        if self.release == 0:
            return "harecrowbot v{}.{}".format(self.major, self.minor)
        else:
            return "harecrowbot v{}.{}r{}".format(self.major, self.minor, self.release)
        
