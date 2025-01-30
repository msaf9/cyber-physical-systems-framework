class Actuator:
    def __init__(self, actuator_type):
        self.actuator_type = actuator_type
        self.state = "CLOSED"

    def perform_action(self, action):
        self.state = action
        print(f"[{self.actuator_type}] Action: {action}")

class EmergencyValve(Actuator):
    def __init__(self):
        super().__init__("EmergencyShutdownValve")

    def emergency_shutdown(self):
        self.state = "CLOSED"
        print("EMERGENCY SHUTDOWN ACTIVATED")
        