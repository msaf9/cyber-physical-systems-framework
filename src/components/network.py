import random
from simpy import Event

class Network:
    def __init__(self, env, packet_loss_probability=0.1, jitter_range=(0.1, 0.5)):
        self.env = env
        self.packet_loss_probability = packet_loss_probability
        self.jitter_range = jitter_range

    def transmit(self, data):
        if random.random() < self.packet_loss_probability:
            # Simulate packet loss
            return self.env.timeout(0, value=None)
        
        delay = random.uniform(*self.jitter_range)
        return self.env.timeout(delay, value=data)
    