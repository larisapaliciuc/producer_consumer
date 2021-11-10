"""Consumer like component that retrieves weather data via an IPC shared memory (multiprocessing.Queue()) and notifies
 via email if the temperature fluctuates above a set threshold."""

import time
import keyring
import traceback
import configparser
import multiprocessing
from datetime import datetime

from scripts.utils import *


class Consumer:
    def __init__(self):
        """Instantiates the Consumer class with variables from settings.ini"""

        config = configparser.ConfigParser()
        config.read('settings.ini')

        if not config['GLOBAL']['CITY_NAME'].isalpha():
            raise Exception('CITY_NAME cannot contain non-alpha characters.')
        self.city_name = config['GLOBAL']['CITY_NAME']

        if not is_number(config['CONSUMER']['SLEEP_TIME']):
            raise Exception('SLEEP_TIME is not a number.')
        self.sleep_time = float(config['CONSUMER']['SLEEP_TIME'])

        if not is_number(config['CONSUMER']['TEMPERATURE_THRESHOLD']):
            raise Exception('TEMPERATURE_THRESHOLD is not a number.')
        self.temperature_threshold = float(config['CONSUMER']['TEMPERATURE_THRESHOLD'])

        if not config['EMAIL']['SENDER'].endswith('@gmail.com'):
            raise Exception('Sender address is not a Gmail address.')
        self.email_sender = config['EMAIL']['SENDER']

        if not config['EMAIL']['RECEIVER'].endswith('@gmail.com'):
            raise Exception('Receiver address is not a Gmail address.')
        self.email_receiver = config['EMAIL']['RECEIVER']

        # The password is kept in Credential Manager for security reasons.
        self.email_password = keyring.get_password(config['EMAIL']['SERVICE_NAME'], self.email_sender)

        if self.email_password is None:
            raise Exception('Could not find password for the specified service.')

        # This will be instantiated later to allow for multiprocessing
        self.log = None

    def run(self, queue: multiprocessing.Queue):
        """ Reads the WeatherInfo class from queue and sends an email if the weather temperature fluctuates above a set
        threshold.
        :param queue: multiprocessing.Queue
        """

        if type(queue) is not multiprocessing.queues.Queue:
            raise TypeError('Parameter queue must be of type multiprocessing.Queue.')

        self.log = get_logger(f'consumer_{os.getpid()}', 'logs')
        self.log.info('Process started')

        gmail = GmailClient(self.email_sender, self.email_password)

        previous_weather_info = None
        while True:
            start_time = datetime.now()

            try:
                # queue is synchronized and the get function blocks execution until data are available
                weather_info = queue.get()
                self.log.info(f'Received {weather_info}')

                if not isinstance(weather_info, WeatherInfo):
                    raise Exception(f'Received data are not of type WeatherInfo! weather_info: {weather_info}')

                if previous_weather_info:
                    temperature_difference = abs(weather_info.temperature - previous_weather_info.temperature)

                    if temperature_difference > self.temperature_threshold:
                        self.log.info(f'Sending warning email: Temperature threshold exceeded with '
                                      f'{temperature_difference:.2f}°C in {self.city_name}.')

                        gmail.send_email(self.email_receiver, 'Producer Consumer Warning',
                                         f'Temperature threshold exceeded with {temperature_difference:.2f}°C '
                                         f'in {self.city_name}.')

                previous_weather_info = weather_info
            except Exception:
                self.log.error(traceback.format_exc())

            # Adjusting for elapsed time when sleeping
            cycle_duration = (datetime.now() - start_time).seconds
            if cycle_duration < self.sleep_time:
                time.sleep(self.sleep_time - cycle_duration)
