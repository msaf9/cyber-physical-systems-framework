from components.pid_controller import PIDController
from components.actuators import EmergencyValve

class Controller:
    def __init__(self, env, network, sensors, actuators, data_logger):
        self.env = env
        self.network = network
        self.sensors = sensors
        self.actuators = actuators
        self.data_logger = data_logger
        self.pid_controller = PIDController(Kp=1.0, Ki=0.1, Kd=0.05)
        self.temperature_setpoint = 80  # From config
        self.temperature_deadline = 0.5  # From config
        self.pressure_deadline = 0.3  # From config
        self.emergency_deadline = 0.1  # From config

    def control_loop(self):
        while True:
            start_time = self.env.now  # Use simulation time instead of real time

            for sensor in self.sensors:
                transmission = yield self.network.transmit(sensor.read())
                
                if transmission is None:
                    self.data_logger.log(self.env.now, f"{sensor.sensor_type}_error", "Packet lost")
                    continue

                self.data_logger.log(self.env.now, sensor.sensor_type, transmission)

                if sensor.sensor_type == "temperature":
                    self.handle_temperature(transmission, start_time)
                elif sensor.sensor_type == "pressure":
                    self.handle_pressure(transmission, start_time)

            yield self.env.timeout(0.1)  # 100ms control loop

    def handle_temperature(self, temperature, start_time):
        control_output = self.pid_controller.update(self.temperature_setpoint, temperature)
        
        for actuator in self.actuators:
            if actuator.actuator_type == "CoolantValve":
                action = "OPEN" if control_output > 0 else "CLOSE"
                actuator.perform_action(action)
                self.data_logger.log(self.env.now, actuator.actuator_type, action)

        execution_time = self.env.now - start_time  # Track time using simulation clock
        if execution_time > self.temperature_deadline:
            self.data_logger.log(self.env.now, "DEADLINE_MISS", f"Temperature control: {execution_time:.3f}s")

    def handle_pressure(self, pressure, start_time):
        # Ensure pressure is non-negative and within a reasonable range
        if pressure < 0:
            pressure = 0  # Reset to 0 if negative value is received
        elif pressure > 150:  # Assuming 150 kPa as the max acceptable pressure
            pressure = 150  # Cap the pressure to 150 kPa to prevent abnormal behavior

        # Check for critical pressure condition (over 100 kPa)
        if pressure > 100:  # kPa, critical pressure
            for actuator in self.actuators:
                if isinstance(actuator, EmergencyValve):
                    actuator.emergency_shutdown()
                    self.data_logger.log(self.env.now, "EMERGENCY_SHUTDOWN", "Activated")

        # Calculate execution time for pressure control
        execution_time = self.env.now - start_time  # Track time using simulation clock

        # Log the pressure control execution time
        self.data_logger.log(self.env.now, "pressure", f"control: {execution_time:.3f}s")
        
        # Check if deadlines were missed
        if execution_time > self.pressure_deadline:
            self.data_logger.log(self.env.now, "DEADLINE_MISS", f"Pressure control: {execution_time:.3f}s")
        
        if execution_time > self.emergency_deadline:
            self.data_logger.log(self.env.now, "DEADLINE_MISS", f"Emergency response: {execution_time:.3f}s")
            