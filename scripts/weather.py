class WeatherInfo:
    def __init__(self, temperature, wind_speed, humidity):
        """Instantiates the WeatherInfo class with the received, unpacked parameters
        :param temperature: int/float (-100, 100)
        :param wind_speed: int/float [0, 200)
        :param humidity: int/float [0, 100)
        """

        # −89.2°C lowest ever recorded, 56.7°C highest ever recorded
        if not isinstance(temperature, (int, float)) or temperature > 100 or temperature < -100:
            raise Exception(f'Temperature is out of range: {temperature}°C')

        # 103.266 m/s highest ever recorded
        if not isinstance(wind_speed, (int, float)) or wind_speed > 200 or wind_speed < 0:
            raise Exception(f'Wind speed is out of range: {wind_speed}m/s')

        if not isinstance(humidity, (int, float)) or humidity > 100 or humidity < 0:
            raise Exception(f'Humidity is out of range: {humidity}%')

        self.temperature = float(temperature)
        self.wind_speed = float(wind_speed)
        self.humidity = float(humidity)
