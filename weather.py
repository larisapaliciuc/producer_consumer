import struct


class WeatherInfo:
    def __init__(self, temperature, wind_speed, humidity):
        """Instantiates the WeatherInfo class with the received, unpacked parameters
        :param temperature: float (-100, 100)
        :param wind_speed: float [0, 200)
        :param humidity: int [0, 100)
        """

        # −89.2°C lowest ever recorded,  56.7°C highest ever recorded
        if not (type(temperature) != float or temperature > 100 or temperature < -100):
            raise Exception(f'Temperature is out of range: {temperature}°C')

        if not (type(wind_speed) != float or wind_speed > 200 or wind_speed < 0):  # 103.266 m/s highest ever recorded
            raise Exception(f'Wind speed is out of range: {wind_speed} m/s')

        if not (type(humidity) != int or humidity > 100 or humidity < 0):
            raise Exception(f'Humidity is out of range: {humidity}%')

        self.temperature = temperature
        self.wind_speed = wind_speed
        self.humidity = humidity

    @staticmethod
    def unpack_data(data):
        """Unpacks WeatherInfo parameters from a bytes object.
        Format is: little endian, short(temperature), unsigned short(wind speed), unsigned char(humidity %) - 5 bytes
        :param data: bytes
        :return: tuple (float, float, int)
        """

        if len(data) != 5:
            raise Exception(f'Weather data buffer needs to be of size 5 bytes, found {len(data)} bytes')

        temperature, wind_speed, humidity = struct.unpack('<hHB', data)

        return temperature / 100, wind_speed / 100, humidity  # restore the two decimal precision

    def pack_data(self):
        """Packs the WeatherInfo class into a bytes object of size 5.
        Format is: little endian, short(temperature), unsigned short(wind speed), unsigned char(humidity %) - 5 bytes
        :return: bytes
        """

        temperature = int(self.temperature * 100)
        wind_speed = int(self.wind_speed * 100)
        humidity = self.humidity

        return struct.pack('<hHB', temperature, wind_speed, humidity)
