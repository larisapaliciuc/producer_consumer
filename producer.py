#!/usr/bin/env python

"""Producer like component that retrieves weather data from a public API and feeds it via IPC shared memory to a
consumer component.

Features:
    * Logging
    * Error handling: API key expired, call limit exceeded, city does not exist, wrong api key
"""

__author__ = 'Larisa Paliciuc'
__email__ = 'larisa.elena.paliciuc@gmail.com'
__version__ = '1.0.0'
__date__ = '2021.11.06'
__status__ = 'Beta'


import datetime
import time
import logging
import requests
import traceback
from weather import WeatherInfo

sleep_time = 60 * 60  # 1h
city_name = 'London'
api_key = '7b9503e2075e80031043cb28f5741d98'
api_call_url = f'api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&lang=en&units=metric'


def retrieve_weather_data():
    """Retrieves the weather data from a free RestAPI provider and returns it as a bytes object.
    :return: bytes
    """

    weather_data = None

    try:
        response_json = requests.get(api_call_url).json()

        if response_json['cod'] != 200:  # OK
            raise Exception(f'[Bad request] code:{response_json["cod"]}')

        temperature = response_json['main']['temp']
        wind_speed = response_json['wind']['speed']
        humidity = response_json['main']['humidity']

        wi = WeatherInfo(temperature, wind_speed, humidity)

        weather_data = wi.pack_data()

    except ValueError as ve:
        # log.error(ve)
        pass
    except Exception as e:
        if str(e).startswith('[Bad request]'):
            # log.error(str(e))
            pass
        else:
            # log.error(traceback.format_exc())
            pass

    return weather_data


def write_in_shared_memory(data):
    pass
    # put lock on shared memory
    # write in shared memory
    # release lock


def main():
    # load config, init
    while True:
        start_time = datetime.datetime.now()

        weather_data = retrieve_weather_data()

        if weather_data:
            write_in_shared_memory(weather_data)

        cycle_duration = (datetime.datetime.now() - start_time).seconds
        if cycle_duration > sleep_time:
            # log.warn(f'Cycle took more than expected: {cycle_duration} seconds.')
            pass
        else:
            time.sleep(sleep_time - cycle_duration)


if __name__ == '__main__':
    main()
