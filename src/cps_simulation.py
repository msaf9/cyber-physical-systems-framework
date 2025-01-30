# Imports
import simpy
import configparser
from components.sensors import Sensor
from components.actuators import Actuator, EmergencyValve
from components.controller import Controller
from components.network import Network
from utilities.data_logger import DataLogger
from utilities.graph_plotter import GraphPlotter
from utilities.resource_monitor import ResourceMonitor
from utilities.realtime_metrics import RealTimeMetrics

def main():
    config = configparser.ConfigParser()
    config.read('simulation_config.ini')

    env = simpy.Environment()

    sensors = [
        Sensor("temperature", "Reactor1"),
        Sensor("pressure", "Reactor1"),
        Sensor("flow_rate", "Input1")
    ]
    actuators = [
        Actuator("CoolantValve"),
        Actuator("InputValve"),
        EmergencyValve()
    ]

    network = Network(env, float(config['NETWORK']['packet_loss_probability']))
    data_logger = DataLogger()
    resource_monitor = ResourceMonitor()
    controller = Controller(env, network, sensors, actuators, data_logger)
    rt_metrics = RealTimeMetrics()

    env.process(controller.control_loop())
    env.process(monitor_resources(env, resource_monitor))

    env.run(until=int(config['SIMULATION']['duration']))

    data_logger.close()
    rt_metrics.analyze(data_logger.get_logs())
    GraphPlotter.plot_logs(data_logger.get_logs())
    GraphPlotter.plot_resource_usage(resource_monitor.get_usage())
    GraphPlotter.plot_realtime_metrics(rt_metrics.get_metrics())

def monitor_resources(env, resource_monitor):
    while True:
        resource_monitor.log_resources()
        yield env.timeout(1)

if __name__ == "__main__":
    main()
