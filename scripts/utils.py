"""Collection of classes and functions used in multiple scripts."""

import os
import sys
import logging
import smtplib

from email.mime.text import MIMEText
from logging.handlers import RotatingFileHandler


class WeatherInfo:
    def __init__(self, temperature, wind_speed, humidity):
        """Instantiates the WeatherInfo class with the received, unpacked parameters
        :param temperature: int/float (-100, 100)
        :param wind_speed: int/float [0, 200)
        :param humidity: int/float [0, 100)
        """

        # −89.2°C lowest ever recorded, 56.7°C highest ever recorded
        if not isinstance(temperature, (int, float)):
            raise Exception(f'Temperature is not a number (int/float): {temperature}')
        elif temperature > 100 or temperature < -100:
            raise Exception(f'Temperature is out of range: {temperature}°C')

        # 103.266 m/s highest ever recorded
        if not isinstance(wind_speed, (int, float)):
            raise Exception(f'Wind speed is not a number (int/float): {wind_speed}')
        elif wind_speed > 200 or wind_speed < 0:
            raise Exception(f'Wind speed is out of range: {wind_speed}m/s')

        if not isinstance(humidity, (int, float)):
            raise Exception(f'Humidity is not a number (int/float): {humidity}')
        elif humidity > 100 or humidity < 0:
            raise Exception(f'Humidity is out of range: {humidity}%')

        self.temperature = float(temperature)
        self.wind_speed = float(wind_speed)
        self.humidity = float(humidity)

    def __str__(self):
        return f'WeatherInfo: [Temperature: {self.temperature:.2f}°C    Wind speed: {self.wind_speed:.2f}m/s    ' \
               f'Humidity: {self.humidity:.2f}%]'


class GmailClient:
    def __init__(self, sender: str, password: str):
        """Instantiates the GmailClient class with sender credentials.
        :param sender: str
        :param password: str
        """
        if not sender.endswith('@gmail.com'):
            raise Exception('Sender address is not a Gmail address.')

        self.sender = sender
        self.password = password

    def send_email(self, receiver: str, subject: str, body: str):
        """Sends a gmail email using SSL protocol with port 465.
        :param receiver: str
        :param subject: str
        :param body: str
        """
        if not receiver.endswith('@gmail.com'):
            raise Exception('Receiver address is not a Gmail address.')

        message = MIMEText(body, 'plain')
        message['From'] = self.sender
        message['To'] = receiver
        message['Subject'] = subject

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.ehlo()
            server.login(user=self.sender, password=self.password)
            server.sendmail(self.sender, receiver, str(message))


def get_logger(log_name: str, logs_directory_path: str, log_max_size=1024):
    """Returns a customised logging object using RotatingFileHandler.
    :param log_name: str
    :param logs_directory_path: str
    :param log_max_size: int
    :return: logging.log
    """
    log_file_info = os.path.join(logs_directory_path, f'{log_name}.log')

    if not os.path.exists(logs_directory_path):
        os.makedirs(logs_directory_path)

    log_formatter = logging.Formatter(
        '%(asctime)-19s [%(filename)s:%(lineno)s - %(funcName)s() ] [%(levelname)-s] %(message)s')

    log = logging.getLogger(log_name)
    log.setLevel(logging.DEBUG)

    # stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    log.addHandler(stream_handler)

    # info, warnings & errors
    handler = RotatingFileHandler(log_file_info, maxBytes=log_max_size, backupCount=3)
    handler.setFormatter(log_formatter)
    handler.setLevel(logging.INFO)
    log.addHandler(handler)

    return log


def is_number(n: str):
    """Checks if a string represents a number (int/float)
    :param n: str
    :return: bool
    """
    try:
        float(n)
        return True
    except ValueError:
        return False
