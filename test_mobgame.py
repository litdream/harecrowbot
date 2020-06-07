import pytest
import time
import copy
from bot_mobgame import GameState, Mobgame
from bot_mobgame import SEC_EXPIRE_DURATION as duration

@pytest.fixture
def resource_gamestate(request):
    # reference:
    #   https://pythontesting.net/framework/pytest/pytest-fixtures-easy-example/

    game = Mobgame()
    return game

def test_gameinit(resource_gamestate):
    game = resource_gamestate
    assert(game.state == GameState.STOPPED)
    assert(game.scoreboard == {})
    assert(game.startAt == 0)
    assert(game.expireAt == 0)

    game.scoreboard['ray'] = 1
    assert(game.scoreboard != {})
    game.reset()
    assert(game.scoreboard == {})
    
    game.setup()
    assert(game.startAt > 0)
    assert(game.expireAt > 0)
    assert( not game.expired())
    assert(game.state == GameState.RUNNING)

    try:
        game.setup()
        assert(False)
    except Exception as err:
        errstr = err.__str__()
        assert( errstr == 'Game is still in progress.')
    
def test_expired_init(resource_gamestate):
    game = resource_gamestate

    # Initial case
    assert( game.state == GameState.STOPPED)
    now = time.time()
    game.startAt -= ( duration + 30 )
    game.expireAt -= ( duration + 1 )
    assert( game.expired())
    assert( game.state == GameState.EXPIRED)
    
    # Simulating in the middle
    game.reset()
    game.setup()    
    assert( game.state == GameState.RUNNING)
    game.startAt = now - duration//2
    game.expireAt = now + duration//2
    assert( not game.expired())


def test_scoreboard(resource_gamestate):
    game = resource_gamestate
    game.setup()

    assert( game.score() == '')
    game.scoreboard['john'] = ['ant','fly']
    assert( game.score() == "(2) john: ['ant', 'fly']" )

    game.scoreboard['do'] = ['guitar','pick','amp']
    assert( game.score() == '''\
(3) do: ['guitar', 'pick', 'amp']
(2) john: ['ant', 'fly']''')

    
def test_hit_mob_happypath(resource_gamestate):
    game = resource_gamestate
    game.setup()

    assert( game.state == GameState.RUNNING )
    users = ['lalala', 'dadada', 'mamama' ]
    mobs = copy.deepcopy(game.mobs)
    for i, mob in enumerate(mobs):
        rtn = game.hit( users[i%3], mob )
        assert( len( rtn.split('\n')) == 1 )

    rtn = None
    all_boss = copy.deepcopy(game.boss)
    for boss in all_boss:
        rtn = game.hit( 'dadada', boss )
    assert( len(rtn.split('\n')) > 1 )
    assert( game.state == GameState.STOPPED)

    # If ended, complain
    try:
        game.hit('lalala','dadada')
        assert(False)
    except Exception as err:
        errstr = err.__str__()
        assert( errstr.startswith( 'Game is not in progress. ' ))
        
    
def test_hit_mob_edgecase(resource_gamestate):
    game = resource_gamestate
    game.setup()

    rtn = game.hit("lalala", "not-existing-mob")
    assert( rtn == 'No such mob( not-existing-mob )' )

    game.mobs[0] = 'duplicate-mob'
    rtn = game.hit('lalala', 'duplicate-mob')
    assert( rtn == 'SUCCESS! ( duplicate-mob )')
    rtn = game.hit('dadada', 'duplicate-mob')
    assert( rtn == 'No such mob( duplicate-mob )')


def test_list(resource_gamestate):
    game = resource_gamestate
    rtn = game.list()
    assert(rtn == 'No mob: Please start game.' )
    
    game.setup()
    game.boss = []
    game.mobs = [ 'abc', 'def', 'ghi' ]
    rtn = game.list()
    assert(rtn == '[ abc def ghi ]')
