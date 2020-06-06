import requests
import re
from pprint import pprint
import time

'''
Weather service return sample:

sample output current-weather: https://openweathermap.org/api/one-call-api
sample output onecall: https://openweathermap.org/api/one-call-api

TEST:
import bot_weather
import pprint
import requests
w = bot_weather.Weather(None, xxx)
url = w.dailyurl + '&q=New York&cnt=1'
rtn = requests.get(url).json()
pprint.pprint(rtn)

'''

class CurData:
    def __init__(self, json):
        self.name = json['name']
        self.wDescr = json['weather'][0]['description']
        self.temp = json['main']['temp']
        self.windSpeed = json['wind']['speed']
        self.lat = json['coord']['lat']
        self.lon = json['coord']['lon']
        
class ForecastData:
    def __init__(self, json):
        dt = json['daily'][0]
        self.sunrise = dt['sunrise']
        self.sunset = dt['sunset']
        self.max = dt['temp']['max']
        self.min = dt['temp']['min']
        self.humidity = dt['humidity']
        self.lat = json['lat']
        self.lon = json['lon']

        # TODO: support
        #   self.chanceRain = dt['rain']
        
class Weather:
    def __init__(self, ctx, apikey):
        self.ctx = ctx
        self.apikey = apikey
        self.baseurl = "http://api.openweathermap.org/data/2.5/weather?" + "appid=" + self.apikey + "&units=imperial"

        now =  int(time.time())
        dt = now - now%86400
        #self.onecallBase = "https://api.openweathermap.org/data/2.5/onecall/timemachine?" + "appid=" + self.apikey + "&units=imperial" + "&dt={}".format(dt)
        self.onecallBase = "https://api.openweathermap.org/data/2.5/onecall?" + "appid=" + self.apikey + "&units=imperial" + "&dt={}".format(dt)

    def getWeather(self, *args):
        if len(args) == 0:
            return "need param"
        # TODO:
        #   1. set wind direction
        #   2. temperature forecast.
        #
        cur = self.currentWeather(*args)
        fore = self.owmOneCall(*args)
        rtn = 'city:{} {}  {}F(min: {}F, max: {}F)  wind-speed({})'.format( cur.name, cur.wDescr, cur.temp, fore.min, fore.max, cur.windSpeed)
        return rtn
    
    def interpreteLocation(self, loc):
        loc = loc.strip()
        pZip = re.compile('^[0-9]{5}$')
        if pZip.match(loc):
            return 'zip={}'.format(loc)
        else:
            return 'q={}'.format(loc)

    def currentWeather(self, *args):
        loc = self.interpreteLocation(args[0])
        url =  self.baseurl + "&" + loc
        data = requests.get(url).json()   # weather-data
        self.curDataCache = CurData(data)
        return self.curDataCache
        
    def owmOneCall(self, *args):
        url = self.onecallBase + '&exclude=minutely,hourly&' + 'lat={}&lon={}'.format(self.curDataCache.lat, self.curDataCache.lon)
        data = requests.get(url).json()   # weather-data

        # working url:
        #   https://api.openweathermap.org/data/2.5/onecall?lat=33.441792&lon=-94.037689&exclude=minutely,hourly&appid=897b26a1e9df68982e49636091afbaf4
        # bad url:
        #   https://api.openweathermap.org/data/2.5/onecall?appid=897b26a1e9df68982e49636091afbaf4&units=imperial&exclude=minutely,hourly&lat=40.71&lon=-74.01
        print('[ {} ]'.format(url))

        return ForecastData(data)
        
        
