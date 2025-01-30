import pytest
import os
import sys
from simpy import Environment

# Dynamically set up the Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this test file
project_root = os.path.dirname(current_dir)  # Project root directory
sys.path.insert(0, project_root)  # Add project root to Python path

# Import the Network class after setting up the path
from src.components.network import Network


@pytest.mark.parametrize("packet_loss_probability, jitter_range", [
    (0.1, (0.1, 0.5)),
    (0.5, (0.05, 0.2)),
    (0.0, (0.0, 0.1)),  # No packet loss
])
def test_network_transmission(packet_loss_probability, jitter_range):
    """
    Test the transmit method with different packet loss probabilities and jitter ranges.
    """
    env = Environment()
    network = Network(env, packet_loss_probability, jitter_range)
    
    data = "test_data"
    event = network.transmit(data)
    env.run(until=event)
    transmitted_data = event.value

    # Check for packet loss
    if packet_loss_probability > 0 and transmitted_data is None:
        assert transmitted_data is None, "Expected packet loss but data was transmitted."

    # If data is transmitted, ensure the value matches
    if transmitted_data is not None:
        assert transmitted_data == data, f"Expected {data}, but got {transmitted_data}"


def test_jitter_range_effect():
    """
    Test that the delay introduced by jitter range is within the expected bounds.
    """
    env = Environment()
    jitter_range = (0.2, 0.5)
    network = Network(env, packet_loss_probability=0.0, jitter_range=jitter_range)

    data = "test_data"
    event = network.transmit(data)
    env.run(until=event)
    delay = env.now  # The simulation clock advances by the delay

    # Ensure delay is within the specified jitter range
    assert jitter_range[0] <= delay <= jitter_range[1], f"Expected delay within {jitter_range}, but got {delay}"


@pytest.mark.parametrize("packet_loss_probability", [0.0, 1.0])
def test_packet_loss_extremes(packet_loss_probability):
    """
    Test the transmit method with edge cases for packet loss probabilities.
    """
    env = Environment()
    network = Network(env, packet_loss_probability, jitter_range=(0.1, 0.2))

    data = "test_data"
    event = network.transmit(data)
    env.run(until=event)
    transmitted_data = event.value

    if packet_loss_probability == 1.0:
        assert transmitted_data is None, "Expected packet loss but data was transmitted."
    elif packet_loss_probability == 0.0:
        assert transmitted_data == data, f"Expected {data}, but got {transmitted_data}"


if __name__ == "__main__":
    # Run pytest programmatically
    pytest.main(["-v", os.path.abspath(__file__)])
    