import pytest
import time
import copy
from bot_numguess import Numgame

@pytest.fixture
def resource_gamestate(request):
    # reference:
    #   https://pythontesting.net/framework/pytest/pytest-fixtures-easy-example/

    game = Numgame()
    return game

def test_init(resource_gamestate):
    game = resource_gamestate
    assert( len(set(game.num)) == 3)

def test_match(resource_gamestate):
    game = resource_gamestate
    assert( game.status() == '' )
    game.num = '123'
    
    s, m = game.match('jaron', '345')
    assert( s == 0 )
    assert( m == '345(1b 0s)')
    assert( game.status() == 'jaron: 345(1b 0s)' )

    s, m = game.match('jake', '124')
    assert( s == 2 )
    assert( m == '124(0b 2s)')
    assert( game.status() == '''\
jaron: 345(1b 0s)
jake: 124(0b 2s)''')
    
    s, m = game.match('jake', '123')
    assert( s == 3 )
    assert( m == '123(0b 3s)')

