import influxdb_client
from os import environ

class InfluxClient:
    def __init__(self):
        self.token = environ.get("INFLUXDB_TOKEN")
        self.org = environ.get("INFLUXDB_ORG")
        self.url = environ.get("INFLUXDM_URI")

    def get_client(self):
        client = influxdb_client.InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )
        return client