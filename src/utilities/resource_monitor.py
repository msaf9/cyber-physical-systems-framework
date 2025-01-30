import psutil

class ResourceMonitor:
    def __init__(self):
        self.cpu_usage = []
        self.memory_usage = []

    def log_resources(self):
        self.cpu_usage.append(psutil.cpu_percent(interval=1))
        self.memory_usage.append(psutil.virtual_memory().percent)

    def get_usage(self):
        return self.cpu_usage, self.memory_usage
    