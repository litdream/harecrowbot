import pytest
import time
import copy
from bot_numguess import Numgame, MAX_CHANCE

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
    assert( m.startswith('345(1b 0s)'))
    assert( game.status() == 'jaron: 345(1b 0s)' )

    s, m = game.match('jake', '124')
    assert( s == 2 )
    assert( m.startswith('124(0b 2s)'))
    assert( game.status() == '''\
jaron: 345(1b 0s)
jake: 124(0b 2s)''')
    
    s, m = game.match('jake', '123')
    assert( s == 3 )
    assert( m.startswith('123(0b 3s)'))

def test_all_finished(resource_gamestate):
    game= resource_gamestate
    game.num = '456'
    
    # u1 and u2
    s,m = game.match('jake', '123')
    s,m = game.match('jaron','123')

    # u1 will run out of chance first.
    for i in range(1, MAX_CHANCE):
        s,m = game.match('jake', '123')
    assert(s == 0)
    assert(m.startswith('123(0b 0s)'))

    try:
        s,m = game.match('jake', '123')
        assert(False)
    except Exception as err:
        assert(s == 0)
        msg = err.__str__()
        assert(msg.startswith("You ran out of"))

    # Now, u2 runs out of chances, which makes
    #   entier contestants run out of chance.
    for i in range(1, MAX_CHANCE-1):
        s,m = game.match('jaron', '123')
    assert(s == 0)
    assert(m.startswith('123(0b 0s)'))
    
    try:
        s,m = game.match('jaron', '123')
        assert(False)
    except Exception as err:
        assert(s == 0)
        msg = err.__str__()
        assert(msg.startswith("HaHaHa"))
        assert(msg.endswith("456."))

def test_final_chance(resource_gamestate):
    game= resource_gamestate
    game.num = '456'
    for i in range(1, MAX_CHANCE):
        s,m = game.match('jake', '123')
    assert(s == 0)
    assert(m.startswith('123(0b 0s)'))
    
    s,m = game.match('jake', '456')
    assert(s == 3)
    assert(m.startswith('456(0b 3s)'))
