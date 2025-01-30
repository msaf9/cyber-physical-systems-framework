import sys
import os

# Dynamically set the project root to the PYTHONPATH (ensure it points to the src directory)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, project_root)

# test_controller.py
import pytest
from components.sensors import Sensor

# Test for temperature sensor
def test_temperature_sensor():
    sensor = Sensor(sensor_type="temperature", location="Room 1")
    temperature = sensor.read()
    assert 75 <= temperature <= 85, f"Temperature out of range: {temperature}°C"

# Test for pressure sensor
def test_pressure_sensor():
    sensor = Sensor(sensor_type="pressure", location="Room 2")
    pressure = sensor.read()
    assert 95 <= pressure <= 105, f"Pressure out of range: {pressure} kPa"

# Test for flow rate sensor
def test_flow_rate_sensor():
    sensor = Sensor(sensor_type="flow_rate", location="Room 3")
    flow_rate = sensor.read()
    assert 0.8 <= flow_rate <= 1.2, f"Flow rate out of range: {flow_rate} L/s"

# Example of running the tests
if __name__ == "__main__":
    pytest.main()
    