import pickle
from datetime import datetime, timedelta
from pprint import pprint
from collections import OrderedDict
from datasource.data_types import DataTypes, DataTypeFloat, DataTypeString
from datasource.influx.influx_queries import StringQuery, ValueQuery
from utils.time import ceil_dt

class HeatPumpData:
    """
    A class representing heat pump data.  Can load data from influx or from a pickle file. SOLID would require these
    two responsibilities to be separated.
    Attributes:
        data (dict): A dictionary to store the heat pump data.
    Methods:
        __init__(the_first_date, the_last_date): Initializes the HeatPumpData object with the given first and last dates.
        add_data(time, name, value): Adds data to the heat pump data dictionary.
        get_sorted_data(): Returns the heat pump data dictionary sorted by time.
        pickle_data(filename='heat_pump_data.pickle'): Pickles the heat pump data to a file.
        unpickle_data(filename='heat_pump_data.pickle'): Unpickles the heat pump data from a file.
    """
    
    def __init__(self, the_first_date, the_last_date, from_pickle=None):
        """
        Initialize the HeatPumpData object.
        Parameters:
        - the_first_date (datetime): The start date for querying data.
        - the_last_date (datetime): The end date for querying data.
        - from_pickle (str): The name of the pickle file to load data from or None to load from influx.
        """        

        if from_pickle is not None:
            print("Loading from last pickle...")
            self._data = self.unpickle_data(filename=from_pickle)    
        else:
            print("Loading from influx...")
            self._data = {}

            for data_type in DataTypes().get_data_types():
                print('Querying: ', data_type.get_name())
                if isinstance(data_type, DataTypeString):
                    StringQuery(the_first_date, the_last_date, heatpump_data=self, 
                                field=data_type.get_data_source_name(), 
                                name=data_type.get_name())
                elif isinstance(data_type, DataTypeFloat):
                    ValueQuery(the_first_date, the_last_date, heatpump_data=self, 
                               measurement=data_type.get_unit(), 
                               friendly_name=data_type.get_data_source_name(), 
                               name=data_type.get_name())
     
            # save the data so that we can re-run the analysis
            self.pickle_data() 

    def add_data(self, time, name, value):
        """
        Adds data to the heat pump object.  If the time already exists, the data is updated.
        Parameters:
        - time (str): The time at which the data is recorded.
        - name (str): The name of the data.
        - value (float): The value of the data.
        Returns:
        None
        """
        time_rounded = ceil_dt(time)

        if time_rounded in self._data:
            self._data[time_rounded][name] = value
        else:
            self._data[time_rounded] = {name: value}

    def pickle_data(self, filename='heat_pump_data.pickle'):
        """
        It's Pickling Time with pickling Jeff and Joby's here as well.
        Pickle the data from inlfux so that it can be re-run for testing
        """
        with open(filename, 'wb') as f:
            pickle.dump(self._data, f)

    def unpickle_data(self, filename='heat_pump_data.pickle'):
        """
        Load the data from the pickle file.
        """
        with open (filename, 'rb') as f:
            return pickle.load(f)

    def get_sorted_data(self):
        """
        Returns the heat pump data dictionary sorted by time. So that it can be processed in order.
        """
        return OrderedDict(sorted(self._data.items()))
    
    def data_by_time(self, the_first_date=None, the_last_date=None):
        """
        Generator to iterate through the sorted heat pump data.
        Yields:
        Tuple of (time, data) sorted by time.
        """
        for time, data in self.get_sorted_data().items():
            if the_first_date is not None and time < the_first_date:
                continue

            if the_last_date is not None and time > the_last_date:
                break

            yield time, data
    

if __name__ == "__main__":
    """
    Main function just to test the HeatPumpData class.
    """
    the_first_date = datetime(year=2024, month=10, day=1)
    the_last_date = datetime.now() + timedelta(days=1)

    heatpump_data = HeatPumpData(the_first_date, the_last_date)

    for k,v in heatpump_data.get_sorted_data().items():
        print(k,v)

