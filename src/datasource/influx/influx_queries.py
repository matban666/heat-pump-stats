from datetime import datetime, timedelta
from pprint import pprint
from datasource.influx.influx_client import InfluxClient
from os import environ

class HeatpumpQuery(InfluxClient):
    """
    This class has query methods to get heatpump data from influxdb
    """

    def __init__(self, first_date, last_date, name):
        """
        Initialize the HeatpumpQuery object.

        Parameters:
        - first_date (datetime): The start date for querying data.
        - last_date (datetime): The end date for querying data.

        
        """

        super().__init__()
        
        self.name = name
        self.adjusted_start_time = first_date - timedelta(days=1) # this is because some values rarely change
        self.adjusted_stop_time = last_date + timedelta(days=1) # this is because?

        self._sample_rate = int(int(environ.get('GRANULARITY', 30)) / 2)

    def get_heatpump_data(self, query, heatpump_data):
        client = self.get_client()

        query_api = client.query_api()

        result = query_api.query(org=self.org, query=query)

        for table in result:
            for record in table.records:
                heatpump_data.add_data(record.get_time(), self.name, record.get_value())

class StringQuery(HeatpumpQuery):
    def __init__(self, first_date, last_date, heatpump_data, field, name):   
        """
        This class has a query to get numeric data from influxdb

        Parameters:
        - first_date (datetime): The start date for querying data.
        - last_date (datetime): The end date for querying data.
        - heatpump_data (HeatPumpData): The heatpump data object to store the data.
        - field (str): The field to query from influxdb.
        - name (str): Our name for the field in the loaded data.
        """
        super().__init__(first_date, last_date, name)

        query = f'from(bucket: "homeassistant")\
            |> range(start: {self.adjusted_start_time.strftime("%Y-%m-%dT%H:%M:%SZ")}, stop: {self.adjusted_stop_time.strftime("%Y-%m-%d")})\
            |> filter(fn: (r) => r["_field"] == "{field}")\
            |> aggregateWindow(every: {self._sample_rate}s, fn: last, createEmpty: false)'
        
        self.get_heatpump_data(query, heatpump_data)


class ValueQuery(HeatpumpQuery):
    """
    This class has a query to get numeric data from influxdb

    Parameters:
    - first_date (datetime): The start date for querying data.
    - last_date (datetime): The end date for querying data.
    - heatpump_data (HeatPumpData): The heatpump data object to store the data.
    - measurement (str): The measurement to query from influxdb.
    - friendly_name (str): Friendly Name of the measurement to query from influxdb.
    - name (str): Our name for the field in the loaded data.
    
    """

    def __init__(self, first_date, last_date, heatpump_data, measurement, friendly_name, name):   
        super().__init__(first_date, last_date, name)

        query = f'from(bucket: "homeassistant")\
            |> range(start: {self.adjusted_start_time.strftime("%Y-%m-%dT%H:%M:%SZ")}, stop: {self.adjusted_stop_time.strftime("%Y-%m-%d")})\
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")\
            |> filter(fn: (r) => r["_field"] == "value")\
            |> filter(fn: (r) => r["friendly_name"] == "{friendly_name}")\
            |> aggregateWindow(every: {self._sample_rate}s, fn: last, createEmpty: false)'
        
        self.get_heatpump_data(query, heatpump_data)
  