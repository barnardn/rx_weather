import funcy
import typing
import requests
import rx


class CurrentConditionsClient:
    """ class to handle communications with OpenWeatherMap """

    host = 'api.openweathermap.org'


    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_conditions(self, zip: str) -> rx.Observable:
        url = "http://"+self.host+'/data/2.5/weather'
        def observable(observer):
            params = {'zip': zip, 'appid': self.api_key}
            rsp = requests.get(url, params=params)

            try:
                rsp.raise_for_status()
                observer.on_next(rsp)
                observer.on_completed()
            except request.HTTPError as e:
                observer.on_error(e)
            return lambda: None

        return rx.Observable.create(observable)
