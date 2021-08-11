from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class data:
    def __init__(self,measurement, field, tags, value, timestamp):
        self._measurement = measurement
        self._field = field
        self._tags = tags
        self._value = value
        self._timestamp = timestamp

    def get_measurement(self):
        return self._measurement

    def get_field(self):
        return self._field

    def get_tags(self):
        return self._tags

    def get_value(self):
        return self._value

    def get_timestamp(self):
        return self._timestamp

    measurement = property(fget = get_measurement)
    field = property(fget = get_field)
    tags = property(fget = get_tags)
    value = property(fget = get_value)
    timestamp = property(fget = get_timestamp)

    def write_datas(self,influx_writer, org="Me" , bucket="Binance"):
        measurement = self._measurement
        field = self._field
        tags = self._tags
        timestamp = self._timestamp
        value = self._value

        point = Point(measurement)
        for key in tags:
            point.tag(key,tags[key])
        
        point.field(field, value).time(timestamp, WritePrecision.NS)#datetime.fromtimestamp(timestamp), WritePrecision.NS)
        influx_writer.write(bucket, org, point)

def connect_InfluxDB(token, url):
    # You can generate a Token from the "Tokens Tab" in the UI
    
    client = InfluxDBClient(url=url, token=token) 
    influx_writer = client.write_api(write_options=SYNCHRONOUS)
    return influx_writer

