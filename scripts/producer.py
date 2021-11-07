#!/usr/bin/env python

"""Producer like component that retrieves weather data from a public API and feeds it via IPC shared memory to a
consumer component.

Features:
    * Logging
"""

__author__ = 'Larisa Paliciuc'
__email__ = 'larisa.elena.paliciuc@gmail.com'
__version__ = '1.0.0'
__date__ = '2021.11.06'
__status__ = 'Beta'


import time
import datetime
import requests
import traceback
import configparser

from scripts import logger
from scripts.weather import WeatherInfo


class Producer:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')

        self.city_name = config['GLOBAL']['CITY_NAME']

        self.sleep_time = int(config['PRODUCER']['SLEEP_TIME'])
        self.api_key = config['PRODUCER']['API_KEY']

        self.log = None

    def run(self, queue):
        self.log = logger.get_logger('producer', 'logs')

        self.log.info('Process started')
        while True:
            start_time = datetime.datetime.now()

            weather_info = self.__retrieve_weather_info()

            if weather_info:
                queue.put(weather_info)

            cycle_duration = (datetime.datetime.now() - start_time).seconds
            if cycle_duration > self.sleep_time:
                self.log.warning(f'Cycle took more than expected: {cycle_duration} seconds.')
                pass
            else:
                time.sleep(self.sleep_time - cycle_duration)

    def __retrieve_weather_info(self):
        """Retrieves the weather data from a free RestAPI provider and returns it as a bytes object.
        :return: bytes
        """

        weather_info = None
        try:
            api_call_url = f' http://api.openweathermap.org/data/2.5/weather?q={self.city_name}' \
                           f'&appid={self.api_key}&lang=en&units=metric'

            response_json = requests.get(api_call_url).json()

            if response_json['cod'] != 200:  # OK
                raise Exception(f'[Bad request] code:{response_json["cod"]}')

            temperature = response_json['main']['temp']
            wind_speed = response_json['wind']['speed']
            humidity = response_json['main']['humidity']

            weather_info = WeatherInfo(temperature, wind_speed, humidity)

        except ValueError as ve:
            self.log.error(ve)

        except Exception as e:
            if str(e).startswith('[Bad request]'):
                self.log.error(str(e))
            else:
                self.log.error(traceback.format_exc())

        return weather_info
