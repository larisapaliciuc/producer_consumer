#!/usr/bin/env python

"""Consumer like component that retrieves weather data via an IPC shared memory and notifies via email the temperature
fluctuates above a set threshold.

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
import configparser

from scripts import logger


class Consumer:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')

        self.city_name = config['GLOBAL']['CITY_NAME']
        self.sleep_time = int(config['CONSUMER']['SLEEP_TIME'])
        self.temperature_threshold = float(config['CONSUMER']['TEMPERATURE_THRESHOLD'])

        self.log = None

    def run(self, queue):
        self.log = logger.get_logger('consumer', 'logs')

        self.log.info('Process started')

        previous_weather_info = None
        while True:
            start_time = datetime.datetime.now()

            weather_info = queue.get()

            if previous_weather_info:
                temperature_difference = abs(weather_info.temperature - previous_weather_info.temperature)
                if temperature_difference > self.temperature_threshold:
                    self.log.warning(f'Temperature threshold exceeded with {temperature_difference}°C')
                    #send email

            previous_weather_info = weather_info

            cycle_duration = (datetime.datetime.now() - start_time).seconds
            if cycle_duration < self.sleep_time:
                time.sleep(self.sleep_time - cycle_duration)
