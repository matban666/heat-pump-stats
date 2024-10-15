import pickle
from os import environ
from collections import OrderedDict
from datasource.influx.query_influx import QueryInflux
from tzlocal import get_localzone
from datasource.data_ingestor import DataByTime

class DataLoader:
    """
    A class to loed time series data data.  Can load data from influx or from a pickle file. 
    Currently tied to influx but could be extended to other data sources.

    Attributes:
        data (dict): A dictionary to store the heat pump data.
    Methods:
        __init__(the_first_date, the_last_date): Initializes the DataLoader object with the given first and last dates.
        add_data(time, name, value): Adds data to the heat pump data dictionary.
        get_sorted_data(): Returns the heat pump data dictionary sorted by time.
        pickle_data(filename='heat_pump_data.pickle'): Pickles the heat pump data to a file.
        unpickle_data(filename='heat_pump_data.pickle'): Unpickles the heat pump data from a file.
    """
    
    def __init__(self, the_first_date, the_last_date, data_types, from_pickle=None):
        """
        Initialize the DataLoader object.
        Parameters:
        - the_first_date (datetime): The start date for querying data.
        - the_last_date (datetime): The end date for querying data.
        - data_types (DataTypes): The data types to query from influx.
        - from_pickle (str): The name of the pickle file to load data from or None to load from influx.
        """        

        self.data_types = data_types

        self.local_timezone = get_localzone()

        if from_pickle is not None:
            print("Loading from last pickle...")
            self._data = self.unpickle_data(filename=from_pickle)    
        else:
            print(f"Loading from influx {environ.get("INFLUXDM_URI")}...")

            data_ingestor = DataByTime(self.local_timezone)

            QueryInflux.query_influx(data_types, the_first_date, the_last_date, data_ingestor)

            self._data = data_ingestor.get_data()

            # Pickle the data so that we can re-run the script without querying influx
            self.pickle_data() 

    def pickle_data(self, filename: str='data.pickle'):
        """
        It's Pickling Time with pickling Jeff and Joby's here as well.
        Pickle the data from inlfux so that it can be re-run for testing

        Parameters:
        - filename (str): The name of the pickle file to save the data to.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self._data, f)

    def unpickle_data(self, filename: str='data.pickle') -> dict:
        """
        Load the data from the pickle file.

        Parameters:
        - filename (str): The name of the pickle file to load the data from.
        """
        with open (filename, 'rb') as f:
            return pickle.load(f)

    def get_sorted_data(self) -> OrderedDict:
        """
        Returns the heat pump data dictionary sorted by time. So that it can be processed in order.
        """
        return OrderedDict(sorted(self._data.items()))
    
    def data_by_time(self, the_first_date=None, the_last_date=None):
        """
        Generator to iterate through the sorted heat pump data.
        The loaded data may be bigger if it was loaded from a pickle file and will be bigger
        if it was loaded from influx as we query one day before and after the requested dates.
        So this generator allows us to window into the exact time range that was asked for.

        Yields:
        data in time order

        Parameters:
        - the_first_date (datetime): The first date to start iterating from.
        - the_last_date (datetime): The last date to iterate to.
        """

        # Each incomimg data frame will have one or more keys depending on the 
        # data available for the timestamp. Therefore, we keep track of all 
        # values in current_data and update the values as they come in.  This
        # way we always have a full set of values to send to the period manager
        current_data = {data_type.get_name(): data_type.get_default_value() for data_type in self.data_types.get_data_types()}

        for time, data in self.get_sorted_data().items():

            for k, v, in data.items():
                # update our current data with the new data to fill in any missing values
                current_data[k] = v

            if the_first_date is not None and time < the_first_date:
                # we are in the extra early data before the requested time window so ignore it
                continue

            if the_last_date is not None and time > the_last_date:
                # we have gone past the requested time window so break
                break

            current_data['DateTime'] = time

            yield current_data

