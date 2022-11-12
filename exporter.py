from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client import start_http_server
import json
import time
import yaml
import subprocess

class CustomCollector(object):

    def __init__(self):
        #with open("data.json") as file:
        #    jdata = file.read()
        jdata = '{"timestamp":"2022-11-11 16:19:32.007","user_info":{"IP":"193.85.33.238","Lat":"50.05","Lon":"14.4","Isp":"T-Mobile Czech DSL","VLoc":"","VLat":"","VLon":""},"servers":[{"url":"http://speedtest3.t-mobile.cz:8080/speedtest/upload.php","lat":"50.0833","lon":"14.4167","name":"Prague","country":"Czechia","sponsor":"T-Mobile Czechia a.s.","id":"18718","url_2":"","host":"speedtest3.t-mobile.cz.prod.hosts.ooklaserver.net:8080","distance":3.894275259128835,"latency":11031946,"dl_speed":74.70320240773965,"ul_speed":81.8931560314277}]}'
        #res = subprocess.check_output(["./speedtest", "--json"])
        #jdata = res.decode("utf-8")
        ddata = json.loads(jdata)
        self.lat = round(ddata["servers"][0]["latency"], 2)
        self.dl = round(ddata["servers"][0]["dl_speed"], 2)
        self.up = round(ddata["servers"][0]["ul_speed"], 2)
    def collect(self):
        yield GaugeMetricFamily('my_speedtest_gauge', 'Help text', value=10)
        c = CounterMetricFamily('Speedtest', 'Help text dva', labels=['foo'])
        c.add_metric(['ul_speed'], self.up)
        c.add_metric(['dl_speed'], self.dl)
        c.add_metric(['latency'], self.lat)
        yield c

start_http_server(9000)
REGISTRY.register(CustomCollector())
while True:
    time.sleep(1)
