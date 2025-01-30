import pytest
import os
import sys

# Dynamically set up the Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this test file
project_root = os.path.dirname(current_dir)  # Project root directory
sys.path.insert(0, project_root)  # Add project root to Python path

# Import the PIDController class after setting up the path
from src.components.pid_controller import PIDController


@pytest.mark.parametrize("Kp, Ki, Kd, setpoint, measured_value, expected_output", [
    (1.0, 0.1, 0.05, 100, 90, 11.5),  # Test with positive error
    (2.0, 0.2, 0.1, 50, 60, -23.0),  # Test with negative error
    (0.5, 0.05, 0.02, 0, 0, 0.0),  # Test with zero error
    (1.0, 0.0, 0.0, 20, 15, 5.0),  # Test with proportional-only
    (0.0, 1.0, 0.0, 10, 5, 5.0),  # Test with integral-only
    (0.0, 0.0, 1.0, 5, 2, 3.0),  # Test with derivative-only
])
def test_pid_controller_update(Kp, Ki, Kd, setpoint, measured_value, expected_output):
    """
    Test the PID controller's update method with different gains and inputs.
    """
    pid = PIDController(Kp, Ki, Kd)
    output = pid.update(setpoint, measured_value)
    assert round(output, 2) == round(expected_output, 2), (
        f"Expected {expected_output}, but got {output}"
    )

def test_pid_controller_integral_accumulation():
    """
    Test the accumulation of the integral term over multiple updates.
    """
    pid = PIDController(Kp=0.0, Ki=1.0, Kd=0.0)
    setpoint = 10
    measured_values = [8, 9, 9.5]
    expected_outputs = [2, 3, 3.5]  # Integral accumulates error over time

    outputs = []
    for measured_value in measured_values:
        outputs.append(pid.update(setpoint, measured_value))

    assert [round(output, 2) for output in outputs] == expected_outputs, (
        f"Expected {expected_outputs}, but got {outputs}"
    )

def test_pid_controller_derivative_response():
    """
    Test the derivative term response to a rapid change in error.
    """
    pid = PIDController(Kp=0.0, Ki=0.0, Kd=1.0)
    setpoint = 10

    # Simulate rapid error changes
    measured_values = [5, 8, 10]
    expected_derivative_outputs = [5.0, -3.0, -2.0]  # Corrected Derivative of error based on sign

    outputs = []
    for measured_value in measured_values:
        outputs.append(pid.update(setpoint, measured_value))

    assert [round(output, 2) for output in outputs] == expected_derivative_outputs, (
        f"Expected {expected_derivative_outputs}, but got {[round(output, 2) for output in outputs]}"
    )

def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.previous_error = 0.0
        self.integral = 0.0

def update(self, setpoint, measured_value):
    error = setpoint - measured_value
    self.integral += error
    derivative = error - self.previous_error

    # Compute the PID output
    output = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)

    # Update the previous error
    self.previous_error = error

    return output

def test_pid_controller_reset_integral():
    """
    Test resetting the integral term between updates.
    """
    pid = PIDController(Kp=1.0, Ki=1.0, Kd=0.0)
    setpoint = 10
    measured_value = 5

    # First update to accumulate integral
    pid.update(setpoint, measured_value)

    # Reset integral manually and test
    pid.integral = 0.0
    output = pid.update(setpoint, measured_value)
    expected_output = 10.0  # Without integral term, only proportional gain matters

    assert round(output, 2) == expected_output, (
        f"Expected {expected_output}, but got {round(output, 2)}"
    )

if __name__ == "__main__":
    # Run pytest programmatically
    pytest.main(["-v", os.path.abspath(__file__)])
    