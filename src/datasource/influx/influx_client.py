import influxdb_client
from os import environ

class InfluxClient:
    """
    This class is a wrapper around the InfluxDB client.  It reads the
    environment variables for the InfluxDB token, org and url and
    creates the client.
    """
    def __init__(self):
        self.token = environ.get("INFLUXDB_TOKEN")
        self.org = environ.get("INFLUXDB_ORG")
        self.url = environ.get("INFLUXDM_URI")

    def get_client(self):
        """
        This method creates the InfluxDB client and returns it.
        """

        client = influxdb_client.InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )
        return client