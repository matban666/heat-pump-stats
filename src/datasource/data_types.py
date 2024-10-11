from abc import ABC, abstractmethod

class DataType(ABC):
    """
        Abstract class for data types
        Attributes:
            name (str): The name of the data type that is used in the script.
            data_source_name (str): The name of the data type that is used the store
            unit (str): The unit of the data type that is used in the data store
    """
    def __init__(self, name, data_source_name, unit=None):
        self._name = name
        self._data_source_name = data_source_name
        self._unit = unit

    @abstractmethod
    def get_default_value(self):
        """
        Abstract method to get the default value of the data type.
        """
        raise NotImplementedError
    
    def get_name(self):
        return self._name
    
    def get_data_source_name(self):
        return self._data_source_name
    
    def get_unit(self):
        return self._unit

class DataTypeString(DataType):
    def __init__(self, name, data_source_name, unit=None):
        super().__init__(name=name, data_source_name=data_source_name, unit=unit)
    
    def get_default_value(self):
        return ""

class DataTypeFloat(DataType):
    def __init__(self, name, data_source_name, unit=None):
        super().__init__(name=name, data_source_name=data_source_name, unit=unit)

    def get_default_value(self):
        return 0.0


class DataTypes():
    def __init__(self):
        self._data_types = [
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
        ]
    
    def get_data_types(self):
        return self._data_types


