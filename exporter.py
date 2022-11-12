from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client import start_http_server
import time

jdata = '{"timestamp":"2022-11-11 14:50:17.612","user_info":{"IP":"193.85.33.238","Lat":"50.05","Lon":"14.4","Isp":"T-Mobile Czech DSL","VLoc":"","VLat":"","VLon":""},"servers":[{"url":"http://speedtest3.t-mobile.cz:8080/speedtest/upload.php","lat":"50.0833","lon":"14.4167","name":"Prague","country":"Czechia","sponsor":"T-Mobile Czechia a.s.","id":"18718","url_2":"","host":"speedtest3.t-mobile.cz.prod.hosts.ooklaserver.net:8080","distance":3.894275259128835,"latency":14989499,"dl_speed":72.5304334108666,"ul_speed":91.27684749287172}]}'
class CustomCollector(object):
    def collect(self):
        #yield GaugeMetricFamily('my_gauge', 'Help text', value=7)
        c = CounterMetricFamily('Speedtest', 'Help text dva', labels=['foo'])
        c.add_metric(['ul_speed'], 1.7)  #TODO json
        c.add_metric(['dl_speed'], 1.7)
        c.add_metric(['latency'], 3.8)
        yield c

start_http_server(9000)
REGISTRY.register(CustomCollector())
while True:
    time.sleep(1)
