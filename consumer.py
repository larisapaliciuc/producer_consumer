#!/usr/bin/env python

"""Consumer like component that retrieves weather data via an IPC shared memory and notifies via email the temperature
fluctuates above a set threshold.

Features:
    * Logging
    * Error handling: API key expired, call limit exceeded, city does not exist, wrong api key
"""

__author__ = 'Larisa Paliciuc'
__email__ = 'larisa.elena.paliciuc@gmail.com'
__version__ = '1.0.0'
__date__ = '2021.11.06'
__status__ = 'Beta'


import configparser
from multiprocessing import shared_memory


def load_config(ini_path='settings.ini'):
    config = configparser.ConfigParser()
    config.read(ini_path)

    global city_name
    city_name = config['GLOBAL']['CITY_NAME']

    global shared_memory_name
    shared_memory_name = config['GLOBAL']['SHARED_MEMORY_NAME']

    global sleep_time
    sleep_time = int(config['CONSUMER']['SLEEP_TIME'])


def read_from_shared_memory():
    """ Reads the weather data from shared memory.
    :return: bytes
    """
    with shared_memory.SharedMemory(name=shared_memory_name, size=5) as shm:
        data = shm.buf

    return data