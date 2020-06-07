import pytest
import time
from bot_mobgame import GameState, Mobgame
from bot_mobgame import SEC_EXPIRE_DURATION as duration

@pytest.fixture(scope='module')
def resource_gamestate(request):
    # reference:
    #   https://pythontesting.net/framework/pytest/pytest-fixtures-easy-example/

    game = Mobgame()
    return game

def test_gameinit(resource_gamestate):
    game = resource_gamestate
    assert(game.state == GameState.STOPPED)
    assert(game.scoreboard == {})

    game.scoreboard['ray'] = 1
    assert(game.scoreboard != {})
    game.reset()
    assert(game.scoreboard == {})
    assert(game.startAt == 0)
    assert(game.expireAt == 0)
    
    game.setup()
    assert(game.startAt > 0)
    assert(game.expireAt > 0)
    assert( not game.expired())

def test_expired_init(resource_gamestate):
    game = resource_gamestate

    # Initial case
    assert( not game.expired())
    assert( game.state == GameState.STOPPED)
    now = time.time()
    game.startAt -= ( duration + 30 )
    game.expireAt -= ( duration + 1 )
    assert( game.expired())
    assert( game.state == GameState.STOPPED)
    
    # Simulating in the middle
    game.reset()
    assert( not game.expired())
    assert( game.state == GameState.STOPPED)
    game.startAt = now - duration//2
    game.expireAt = now + duration//2
    assert( not game.expired())
    assert( game.state == GameState.STOPPED)
