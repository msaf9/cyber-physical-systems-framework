class RealTimeMetrics:
    def __init__(self):
        self.deadline_misses = 0
        self.total_executions = 0
        self.response_times = []

    def analyze(self, logs):
        for log in logs:
            if log['component'] == "DEADLINE_MISS":
                self.deadline_misses += 1
            elif log['component'] in ["temperature", "pressure"]:
                self.total_executions += 1
                # Extract response time from the log data
                if isinstance(log['data'], str) and 'control:' in log['data']:
                    try:
                        response_time = float(log['data'].split(':')[1].strip().rstrip('s'))
                        self.response_times.append(response_time)
                    except ValueError:
                        pass  # Skip if we can't parse the response time

    def get_metrics(self):
        return {
            "deadline_miss_rate": self.deadline_misses / max(self.total_executions, 1),
            "average_response_time": sum(self.response_times) / max(len(self.response_times), 1),
            "max_response_time": max(self.response_times) if self.response_times else 0
        }
    