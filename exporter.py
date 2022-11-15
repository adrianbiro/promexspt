from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client import start_http_server
import json
import time
import yaml
import subprocess
import os


class CustomCollector(object):
    def __init__(self):
        self.hostdict = {
            hn: subprocess.check_output([",checkssl", hn]) for hn in hostnamelist
        }

    def collect(self):
        c = CounterMetricFamily("SSL", "Days to expiration", labels=["TODO"])
        for k, v in self.hostdict.items():
            c.add_metric(str(k), v)
        yield c


if __name__ == "__main__":
    port = 9000
    frequency = 1
    if os.path.exists("config.yaml"):
        with open("config.yaml", "r") as config_file:
            try:
                config = yaml.safe_load(config_file)
                port = int(config["port"])
                frequency = config["scrape_frequency"]
                # hostnamelist = config["google.com", "youtube.com"]
                hostnamelist = ["google.com", "youtube.com"]
            except yaml.YAMLError as error:
                print(error)

    start_http_server(port)
    REGISTRY.register(CustomCollector())
    while True:
        # period between collection
        time.sleep(frequency)
