import os
import pytest
import bot_weather
from dotenv import load_dotenv

class dummy:
    pass

def test_location():
    apikey = '12345'
    
    ctx = dummy
    ctx.message = dummy
    ctx.message.author = "HarecrowCpp#321"

    w = bot_weather.Weather(ctx, apikey)
    assert( w.interpreteLocation('20105') == 'zip=20105')
    assert( w.interpreteLocation('New York') == 'q=New York')

def test_emptyarg():
    w = bot_weather.Weather(None, '')
    rtn = w.getWeather()
    assert( rtn == 'need param')

    
