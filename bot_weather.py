import requests
import re
from pprint import pprint

'''
Weather service return sample:

{'base': 'stations',
 'clouds': {'all': 90},
 'cod': 200,
 'coord': {'lat': 40.71, 'lon': -74.01},
 'dt': 1591446956,
 'id': 5128581,
 'main': {'feels_like': 299.19,
          'humidity': 94,
          'pressure': 1009,
          'temp': 296.03,
          'temp_max': 297.04,
          'temp_min': 294.82},
 'name': 'New York',
 'sys': {'country': 'US',
         'id': 4610,
         'sunrise': 1591435523,
         'sunset': 1591489473,
         'type': 1},
 'timezone': -14400,
 'visibility': 12874,
 'weather': [{'description': 'overcast clouds',
              'icon': '04d',
              'id': 804,
              'main': 'Clouds'}],
 'wind': {'deg': 250, 'speed': 2.1}}


import bot_weather
import pprint
import requests
w = bot_weather.Weather(None, xxx)
url = w.dailyurl + '&q=New York&cnt=1'
rtn = requests.get(url).json()
pprint.pprint(rtn)

'''
class Weather:
    def __init__(self, ctx, apikey):
        self.ctx = ctx
        self.apikey = apikey
        self.baseurl = "http://api.openweathermap.org/data/2.5/weather?" + "appid=" + self.apikey + "&units=imperial"
        self.dailyurl = "http://api.openweathermap.org/data/2.5/forecast/daily?" + "appid=" + self.apikey + "&units=imperial"
        
    def getWeather(self, *args):
        if len(args) == 0:
            return "need param"
        loc = self.interpreteLocation(args[0])
        url =  self.baseurl + "&" + loc
        data = requests.get(url).json()   # weather-data
        pprint(data)    # for debug
        
        # TODO:
        #   1. set wind direction
        #   2. temperature forecast.
        #
        rtn = 'city:{} {}  {}F wind-speed({})'.format( data['name'], data['weather'][0]['description'],  data['main']['temp'], data['wind']['speed'] )
        return rtn
    
    def interpreteLocation(self, loc):
        loc = loc.strip()
        pZip = re.compile('^\d{5}$')
        if pZip.match(loc):
            return 'zip={}'.format(loc)
        else:
            return 'q={}'.format(loc)
