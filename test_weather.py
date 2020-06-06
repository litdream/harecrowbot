import os
import pytest
import bot_weather
from dotenv import load_dotenv

class dummy:
    pass

@pytest.fixture(scope='module')
def resource_apikey(request):
    # reference:
    #   https://pythontesting.net/framework/pytest/pytest-fixtures-easy-example/
    homedir = os.environ['HOME']
    load_dotenv( dotenv_path=os.path.join(homedir,".harecrowbot/env") )
    OWMID = os.getenv('OPENWM_TOKEN')

    ctx = dummy
    ctx.message = dummy
    ctx.message.author = "HarecrowCpp#321"

    return ctx, OWMID
    
def test_location(resource_apikey):
    ctx, apikey = resource_apikey
    w = bot_weather.Weather(ctx, apikey)
    
    assert( w.interpreteLocation('20105') == 'zip=20105')
    assert( w.interpreteLocation('New York') == 'q=New York')

def test_emptyarg():
    w = bot_weather.Weather(None, '')
    rtn = w.getWeather()
    assert( rtn == 'need param')

def test_current_weather(resource_apikey):
    ctx, apikey = resource_apikey
    w = bot_weather.Weather(ctx, apikey)
    
    cur = w.currentWeather( ('10005') )
    assert( cur.name == 'New York' )
    assert( cur.lat == 40.71 )
    assert( cur.lon == -74.01 )

def test_oneCall(resource_apikey):
    ctx, apikey = resource_apikey
    w = bot_weather.Weather(ctx, apikey)
    
    cur = w.currentWeather( ('10005') )
    fore = w.owmOneCall( ('10005') )
    assert( fore.lat == 40.71 )
    assert( fore.lon == -74.01 )
