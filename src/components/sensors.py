import random

class Sensor:
    def __init__(self, sensor_type, location):
        self.sensor_type = sensor_type
        self.location = location

    def read(self):
        if self.sensor_type == "temperature":
            return random.uniform(75, 85)  # Temperature in °C
        elif self.sensor_type == "pressure":
            return random.uniform(95, 105)  # Pressure in kPa
        elif self.sensor_type == "flow_rate":
            return random.uniform(0.8, 1.2)  # Flow rate in L/s
        else:
            raise ValueError("Unknown sensor type")
