"""Producer like component that retrieves weather data from a public API and feeds it via IPC shared memory to a
consumer component."""

import time
import datetime
import requests
import traceback
import configparser
import multiprocessing

from scripts.utils import *


class Producer:
    def __init__(self):
        """Instantiates the Producer class with variables from settings.ini"""
        config = configparser.ConfigParser()
        config.read('settings.ini')

        if not config['GLOBAL']['CITY_NAME'].isalpha():
            raise Exception('CITY_NAME cannot contain non-alpha characters.')
        self.city_name = config['GLOBAL']['CITY_NAME']

        if not is_number(config['PRODUCER']['SLEEP_TIME']):
            raise Exception('SLEEP_TIME is not a number.')
        self.sleep_time = int(config['PRODUCER']['SLEEP_TIME'])

        self.api_key = config['PRODUCER']['API_KEY']

        # This will be instantiated later to allow for multiprocessing
        self.log = None

    def run(self, queue: multiprocessing.Queue):
        """Writes the WeatherInfo class in queue.
        :param queue: multiprocessing.Queue
        """
        self.log = get_logger('producer', 'logs')
        self.log.info('Process started')

        while True:
            start_time = datetime.datetime.now()

            weather_info = self.__retrieve_weather_info()

            if weather_info:
                # queue is synchronized and the put function blocks execution until a free slot is available
                self.log.info(f'Sending {weather_info}')
                queue.put(weather_info)

            # Adjusting for elapsed time when sleeping
            cycle_duration = (datetime.datetime.now() - start_time).seconds
            if cycle_duration > self.sleep_time:
                self.log.warning(f'Cycle took more than expected: {cycle_duration} seconds.')
            else:
                time.sleep(self.sleep_time - cycle_duration)

    def __retrieve_weather_info(self):
        """Retrieves the weather data from a free API provider and returns it as a bytes object.
        :return: WeatherInfo
        """

        weather_info = None
        try:
            api_call_url = f' http://api.openweathermap.org/data/2.5/weather?q={self.city_name}' \
                           f'&appid={self.api_key}&lang=en&units=metric'

            response_json = requests.get(api_call_url).json()

            if response_json['cod'] != 200:  # OK
                raise Exception(f'[Bad request] code:{response_json["cod"]}')

            # todo: remove after testing
            import random
            temperature = response_json['main']['temp'] + random.random()

            # temperature = response_json['main']['temp']
            wind_speed = response_json['wind']['speed']
            humidity = response_json['main']['humidity']

            weather_info = WeatherInfo(temperature, wind_speed, humidity)

        except ValueError:
            self.log.error(traceback.format_exc())

        except Exception as e:
            if str(e).startswith('[Bad request]'):
                self.log.error(str(e))
            else:
                self.log.error(traceback.format_exc())

        return weather_info
