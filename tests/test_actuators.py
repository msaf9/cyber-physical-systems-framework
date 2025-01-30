import pytest
import os
import sys

# Dynamically set up the Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this test file
project_root = os.path.dirname(current_dir)  # Project root directory
sys.path.insert(0, project_root)  # Add project root to Python path

# Import the Actuator class after setting up the path
from src.components.actuators import Actuator


@pytest.mark.parametrize("action, expected_state", [
    ("ON", "ON"),
    ("OFF", "OFF"),
    ("UNKNOWN", "UNKNOWN"),  # Test cases for valid actions
])
def test_actuator_action(action, expected_state):
    """
    Test the perform_action method with valid actions.
    """
    actuator = Actuator("Motor")
    actuator.perform_action(action)
    assert actuator.state == expected_state, f"Expected state {expected_state}, but got {actuator.state}"


if __name__ == "__main__":
    # Run pytest programmatically
    pytest.main(["-v", os.path.abspath(__file__)])
    