import sys
import os
import pytest  # Using pytest for a structured approach

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from components.sensors import Sensor

def test_temperature_sensor():
    sensor = Sensor("temperature", "Room1")
    data = sensor.read()
    assert 75 <= data <= 85, f"Temperature sensor reading out of range: {data}"

def test_pressure_sensor():
    sensor = Sensor("pressure", "Room2")
    data = sensor.read()
    assert 95 <= data <= 105, f"Pressure sensor reading out of range: {data}"

def test_flow_rate_sensor():
    sensor = Sensor("flow_rate", "Pipeline1")
    data = sensor.read()
    assert 0.8 <= data <= 1.2, f"Flow rate sensor reading out of range: {data}"

def test_invalid_sensor_type():
    with pytest.raises(ValueError, match="Unknown sensor type"):
        sensor = Sensor("invalid", "Unknown")
        sensor.read()

if __name__ == "__main__":
    pytest.main()
    