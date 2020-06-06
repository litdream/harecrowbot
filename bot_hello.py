import os

class Hello:
    def __init__(self, ctx):
        self.ctx = ctx
        self.hito = ctx.message.author
        
    def hello(self):
        return "Hello, {}".format(self.hito)
