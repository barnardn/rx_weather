import typing
from typing import List, NewType, NamedTuple
from datetime import datetime


class Unit:
    """ defines a unit of measure, "km/h or degress C """

    @property
    def symbol(self) -> str:
        return self._symbol

    def __init__(self, sym: str):
        self._symbol = sym

    def __str__(self):
        return self.symbol

    @staticmethod
    def degree_symbol():
        """ return a degrees utf-8 character """
        return u'\N{DEGREE SIGN}'


Measurement = NamedTuple( "Measurement",
                [('value', float),
                 ('unit', Unit)])

GeoPoint = NamedTuple('GeoPoint',
                      [('lat', float),
                       ('lon', float)])

Parameter = NamedTuple('Parameter',
                       [('name', str),
                        ('description', str)])

Vector = NamedTuple('Vector',
                    [('magnitude', Measurement),
                     ('direction', Measurement)])



class Location:
    """ geographical weather area """

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_value: str):
        self._name = new_value

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, new_value: str):
        self._country = new_value

    @property
    def geo_location(self) -> GeoPoint:
        return self._geo

    @geo_location.setter
    def geo_location(self, geo: GeoPoint):
        self._geo = geo

    def __init__(self, id: int):
        self.id = id


class SolarTimes:
    """ sunrise and sunset times """

    @property
    def sunrise(self) -> datetime:
        return self._sunrise

    @sunrise.setter
    def sunrise(self, new_value: datetime):
        self._sunrise = new_value

    @property
    def sunset(self) -> datetime:
        return self._sunset

    @sunset.setter
    def sunset(self, new_value: datetime):
        self._sunset = new_value


class ClimateCondition:
    """
    represents all the atttributes we care to display
    as weather
    """

    @property
    def temperature(self) -> Measurement:
        return self._temp

    @temperature.setter
    def temperature(self, new_value: Measurement):
        self._temp = new_value

    @property
    def humidity(self) -> Measurement:
        return self._humidity

    @humidity.setter
    def humidity(self, new_value: Measurement):
        self._humidity = new_value

    @property
    def wind(self) -> Vector:
        return self._wind

    @wind.setter
    def wind(self, new_value: Vector):
        self._wind = new_value

    @property
    def conditions(self) -> List[Parameter]:
        return self._conditions

    @conditions.setter
    def set_conditions(self, new_value: List[Parameter]):
        self._conditions = new_value


class WeatherForecast:
    """
    models a weather forecast. a forecast is basically
    just a series of climate conditions for a location on
    a specific date
    """
    @property
    def location(self) -> Location:
        return self._location

    @location.setter
    def set_loc(self, new_value):
        self._location = new_value

    @property
    def current(self) -> ClimateCondition:
        return self._cur_condition

    @current.setter
    def current(self, new_value: ClimateCondition):
        self._cur_condtition = new_value

    def __init__(selef, location: Location):
        self.location = location

