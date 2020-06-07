import pytest
from bot_mobgame import GameState, Mobgame

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

