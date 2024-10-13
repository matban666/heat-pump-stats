
from utils.time import ceil_dt
from abc import ABC, abstractmethod

class DataIngestor(ABC):
    @abstractmethod
    def add_data(self, time, name, value):
        """
        Implement this in derived class.  It is called by somthing that loads data.  
        This separates the method of loading data from the method of storing it.

        Parameters:
        - time (datetime): The time at which the data is recorded.
        - name (str): The name of the data.
        - value (float/str): The value of the data.
        """
        raise NotImplementedError

class DataByTime(DataIngestor):
    def __init__(self, local_timezone):
        """
        Initializes the heat pump object.
        Parameters:
        - local_timezone: The local timezone of the heat pump.
        Returns:
        None
        """
        self.local_timezone = local_timezone
        self._data = {}

    def add_data(self, time, name, value):
        """
        Called when a data item is loaded.
        Parameters:
        - time (datetime): The time at which the data is recorded.
        - name (str): The name of the data.
        - value (float/str): The value of the data.
        Returns:
        None
        """
        time_rounded = ceil_dt(time)

        local_time = time_rounded.astimezone(self.local_timezone)

        if local_time in self._data:
            self._data[local_time][name] = value
        else:
            self._data[local_time] = {name: value}

    def get_data(self):
        return self._data