import funcy
import typing
from typing import Any
import requests
import rx
import pdb
from rxw.models import *


def default_unit(key: str) -> Unit:
    """
    given a json key, returns the unit for that key's
    corresponding measurement
    """
    units = {
        'temp': Unit(Unit.degree_symbol()+"C"),
        'deg': Unit(Unit.degree_symbol()),
        'speed': Unit('m/sec'),
        'presssure': Unit('hPa'),
        'humidity': Unit('%'),
        }
    return units[key] if key in units else None

class CurrentConditions:
    """ class to handle communications with OpenWeatherMap """

    host = 'api.openweathermap.org'


    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch(self, zip: str, temp_only: bool=False):
        self.rx_fetch(zip) \
                .flat_map(lambda js, _: self.parse_weather(js)) \
                .subscribe(on_next= lambda w: w.display(temp_only))

    def rx_fetch(self, zip: str) -> rx.Observable:
        """
        creates an and returns obsersable on the
        current conditions api request
        """
        url = "http://"+self.host+'/data/2.5/weather'
        def observable(observer):
            params = {'zip': zip, 'appid': self.api_key}
            rsp = requests.get(url, params=params)

            try:
                rsp.raise_for_status()
                observer.on_next(rsp.json())
                observer.on_completed()
            except requests.HTTPError as e:
                observer.on_error(e)
            return lambda: None

        return rx.Observable.create(observable)


    def parse_weather(self, json: dict) -> WeatherForecast:
        location = Location(id=json['id'])
        location.name = json['name']
        location.country = json['sys']['country']
        weather = WeatherForecast(location)
        lat = json['coord']['lat']
        lon = json['coord']['lon']
        weather.location.geo_location = GeoPoint(lat,lon)
        cc = ClimateCondition()
        main = json['main']
        cc.temperature = Measurement(main['temp'], default_unit('temp'))
        cc.humidity = Measurement(main['humidity'], default_unit('humidity'))
        wind = json['wind']
        speed = Measurement(wind['speed'], default_unit('speed'))
        dir = Measurement(wind['deg'], default_unit('deg'))
        cc.wind = Vector(speed, dir)
        ps = json['weather']
        params = [Parameter(p['main'],p['description']) for p in ps]
        cc.conditions = params
        weather.current = cc
        return rx.Observable.from_callable(lambda: weather)


