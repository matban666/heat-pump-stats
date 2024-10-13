import pickle
from collections import OrderedDict
from datasource.data_types import DataTypes, DataTypeFloat, DataTypeString
from datasource.influx.query_influx import QueryInflux
from tzlocal import get_localzone
from datasource.data_ingestor import DataByTime

class HeatPumpData:
    """
    A class representing heat pump data.  Can load data from influx or from a pickle file. SOLID would require these
    two responsibilities to be separated a bit better I think.
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

        self.create_data_types()

        self.local_timezone = get_localzone()

        if from_pickle is not None:
            print("Loading from last pickle...")
            self._data = self.unpickle_data(filename=from_pickle)    
        else:
            print("Loading from influx...")

            data_ingestor = DataByTime(self.local_timezone)

            QueryInflux.query_influx(self.data_types, the_first_date, the_last_date, data_ingestor)

            self._data = data_ingestor.get_data()

            self.pickle_data() 

    def create_data_types(self):
        self.data_types = DataTypes()
        self.data_types.add_data_types([
            DataTypeString(name='Operation Mode', data_source_name='Operation Mode_str'),
            DataTypeString(name='Three Way Valve', data_source_name='3way valve(On:DHW_Off:Space)_str'),
            DataTypeString(name='Thermostat', data_source_name='Thermostat ON/OFF_str'),
            DataTypeString(name='Defrost Operation', data_source_name='Defrost Operation_str'),     
            DataTypeString(name='BUH Step1', data_source_name='BUH Step1_str'),      
            DataTypeString(name='BUH Step2', data_source_name='BUH Step2_str'),      
            DataTypeString(name='Freeze Protection For Water Piping', data_source_name='Freeze Protection for water piping_str'),
            DataTypeString(name='Freeze Protection', data_source_name='Freeze Protection_str'),
            DataTypeString(name='Low Noise Control', data_source_name='Low noise control_str'),
            DataTypeString(name='Silent Mode', data_source_name='Silent Mode_str'),
            DataTypeFloat(name='Power In', data_source_name='Heat Pump 7 1MIN', unit='W'),
            DataTypeFloat(name='Immersion Power', data_source_name='Immersion 3 1MIN', unit='W'),
            DataTypeFloat(name='Flow Rate', data_source_name='ESPAltherma - Flow Sensor', unit='l/min'),
            DataTypeFloat(name='Flow Temp', data_source_name='ESPAltherma - Leaving Water Temperature After BUH', unit='°C'),
            DataTypeFloat(name='Return Temp', data_source_name='ESPAltherma - Inlet Water Temperature', unit='°C'),
            DataTypeFloat(name='CH Setpoint', data_source_name='ESPAltherma - RT Setpoint', unit='°C'),
            DataTypeFloat(name='Delta T', data_source_name='ESPAltherma - Heat Pump Delta T', unit='°C'),
            DataTypeFloat(name='Flow Setpoint', data_source_name='ESPAltherma - LW Setpoint (main)', unit='°C'),
            DataTypeFloat(name='DHW Temp', data_source_name='ESPAltherma - Hot Water Tank Temp', unit='°C'),
            DataTypeFloat(name='Indoor Temp', data_source_name='ESPAltherma - Indoor Temperature', unit='°C'),
            DataTypeFloat(name='Outdoor Temp', data_source_name='ESPAltherma - Outdoor Air Temperature', unit='°C'),
            DataTypeFloat(name='Target Delta T', data_source_name='ESPAltherma - Target Delta T', unit='°C'),
            DataTypeFloat(name='DHW Setpoint', data_source_name='ESPAltherma - DHW Setpoint', unit='°C'),
        ])

    def get_data_types(self):
        return self.data_types.get_data_types()

    def pickle_data(self, filename: str='heat_pump_data.pickle'):
        """
        It's Pickling Time with pickling Jeff and Joby's here as well.
        Pickle the data from inlfux so that it can be re-run for testing

        Parameters:
        - filename (str): The name of the pickle file to save the data to.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self._data, f)

    def unpickle_data(self, filename: str='heat_pump_data.pickle') -> dict:
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
        Tuple of (time, data) sorted by time.

        Parameters:
        - the_first_date (datetime): The first date to start iterating from.
        - the_last_date (datetime): The last date to iterate to.
        """
        for time, data in self.get_sorted_data().items():
            if the_first_date is not None and time < the_first_date:
                continue

            if the_last_date is not None and time > the_last_date:
                break

            yield time, data

