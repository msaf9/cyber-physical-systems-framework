import logging
import csv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLogger:
    def __init__(self):
        self.logs = []
        self.csv_file = open('simulation_data.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'Component', 'Data'])

    def log(self, timestamp, component, data):
        logging.info(f'{timestamp} - {component}: {data}')
        self.logs.append({'time': timestamp, 'component': component, 'data': data})
        self.csv_writer.writerow([timestamp, component, data])

    def get_logs(self):
        return self.logs

    def close(self):
        self.csv_file.close()
        