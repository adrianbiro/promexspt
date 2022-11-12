from prometheus_client.core import (
    GaugeMetricFamily,
    CounterMetricFamily,
    REGISTRY,
)
from prometheus_client import start_http_server
import json
import time
import datetime
import yaml
import subprocess
import os


class CustomCollector(object):
    def __init__(self):
        # with open("data.json") as file:
        #    jdata = file.read()
        jdata = '{"timestamp":"2022-11-11 16:19:32.007","user_info":{"IP":"193.85.33.238","Lat":"50.05","Lon":"14.4","Isp":"T-Mobile Czech DSL","VLoc":"","VLat":"","VLon":""},"servers":[{"url":"http://speedtest3.t-mobile.cz:8080/speedtest/upload.php","lat":"50.0833","lon":"14.4167","name":"Prague","country":"Czechia","sponsor":"T-Mobile Czechia a.s.","id":"18718","url_2":"","host":"speedtest3.t-mobile.cz.prod.hosts.ooklaserver.net:8080","distance":3.894275259128835,"latency":11031946,"dl_speed":74.70320240773965,"ul_speed":81.8931560314277}]}'
        res = subprocess.check_output(["./speedtest", "--json"])
        jdata = res.decode("utf-8")
        ddata = json.loads(jdata)
        self.lat = round(
            ((ddata["servers"][0]["latency"] / 1000000.0) % 60), 2
        )  # micros to sec
        self.dl = round(ddata["servers"][0]["dl_speed"], 2)  # mbps
        self.up = round(ddata["servers"][0]["ul_speed"], 2)

    def collect(self):
        yield GaugeMetricFamily("my_speedtest_gauge", "Help text", value=10)
        c = CounterMetricFamily(
            "Speedtest", "Up and Down in mbps, Latency in sec", labels=["TODO"]
        )
        c.add_metric(["Upload"], self.up)
        c.add_metric(["Download"], self.dl)
        c.add_metric(["Latency"], self.lat)
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
            except yaml.YAMLError as error:
                print(error)

    start_http_server(port)
    REGISTRY.register(CustomCollector())
    while True:
        # period between collection
        time.sleep(frequency)
