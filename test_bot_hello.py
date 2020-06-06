import pytest
import bot_hello

class dummy:
    pass

def test_hello():
    ctx = dummy
    ctx.message = dummy
    ctx.message.author = "HarecrowCpp#321"
    
    h = bot_hello.Hello(ctx)
    assert( h.hello() == 'Hello, HarecrowCpp.' )

def test_hello2():
    ctx = dummy
    ctx.message = dummy
    ctx.message.author = "NoIdUser"
    
    h = bot_hello.Hello(ctx)
    assert( h.hello() == 'Hello, NoIdUser.' )
    
