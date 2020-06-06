import os

class Hello:
    def __init__(self, ctx):
        self.ctx = ctx
        self.hito = ctx.message.author
        
    def hello(self):
        greetuser = self.hito.__str__()
        if greetuser.find('#') > -1:
            greetuser = greetuser.split('#')[0]
        return "Hello, {}.".format(greetuser)
            
