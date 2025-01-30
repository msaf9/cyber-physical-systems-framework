import matplotlib.pyplot as plt
import numpy as np

class GraphPlotter:
    @staticmethod
    def plot_logs(logs):
        times = [log["time"] for log in logs]
        data = [log["data"] for log in logs]
        components = [log["component"] for log in logs]

        plt.figure(figsize=(10, 6))
        for component in set(components):
            component_data = [data[i] for i in range(len(data)) if components[i] == component]
            component_times = [times[i] for i in range(len(times)) if components[i] == component]
            plt.plot(component_times, component_data, label=component)

        # Customize x-axis ticks to reduce clutter
        xticks_interval = max(len(times) // 10, 1)  # Adjust based on the number of points
        xticks = np.arange(min(times), max(times) + 1, xticks_interval)
        plt.xticks(xticks)

        plt.xlabel("Time (s)")
        plt.ylabel("Sensor Value")
        plt.legend()
        plt.title("Sensor Data Over Time")
        plt.tight_layout()  # Ensure layout fits nicely
        plt.show()

    @staticmethod
    def plot_resource_usage(usage_data):
        cpu_usage, memory_usage = usage_data
        times = list(range(len(cpu_usage)))

        plt.figure(figsize=(10, 6))
        plt.plot(times, cpu_usage, label="CPU Usage")
        plt.plot(times, memory_usage, label="Memory Usage")
        plt.xlabel("Time (s)")
        plt.ylabel("Usage (%)")
        plt.legend()
        plt.title("Resource Usage Over Time")
        plt.show()

    @staticmethod
    def plot_realtime_metrics(metrics):
        deadlines_missed = metrics["deadline_miss_rate"] * 100  # to percentage
        avg_response_time = metrics["average_response_time"] * 1000  # to milliseconds
        max_response_time = metrics["max_response_time"] * 1000  # to milliseconds

        plt.figure(figsize=(10, 6))
        labels = ["Deadlines Missed (%)", "Avg Response Time (ms)", "Max Response Time (ms)"]
        values = [deadlines_missed, avg_response_time, max_response_time]
        colors = ["red", "orange", "blue"]

        plt.bar(labels, values, color=colors)

        plt.ylabel("Value")
        plt.title("Real-Time Metrics Analysis")
        
        # Add value labels on top of each bar
        for i, v in enumerate(values):
            plt.text(i, v, f'{v:.2f}', ha='center', va='bottom')

        plt.ylim(0, max(values) * 1.1)  # Set y-axis limit to 110% of max value
        plt.show()
        