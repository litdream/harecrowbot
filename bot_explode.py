import os
import random

class Explode:
    def __init__(self, ctx):
        self.ctx = ctx
        author = ctx.message.author
        self.toUser = author.__str__()
        
    def explode(self):
        return "{}: Really? Why in the world would I ever explode myself???".format(self.toUser)
