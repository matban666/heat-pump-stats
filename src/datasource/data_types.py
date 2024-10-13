from abc import ABC, abstractmethod

class DataType(ABC):
    """
        Abstract class for data types
    """
    def __init__(self, name: str, data_source_name: str, unit: str=None):
        """
        Constructor for the data type class

        Attributes:
            name (str): The name of the data type that is used in the script.
            data_source_name (str): The name of the data type that is used the store
            unit (str): The unit of the data type that is used in the data store
        """
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
    """
    Class for string data types
    """
    def __init__(self, name, data_source_name, unit=None):
        super().__init__(name=name, data_source_name=data_source_name, unit=unit)
    
    def get_default_value(self):
        return ""

class DataTypeFloat(DataType):
    """
    Class for float data types
    """
    def __init__(self, name, data_source_name, unit=None):
        super().__init__(name=name, data_source_name=data_source_name, unit=unit)

    def get_default_value(self):
        return 0.0


class DataTypes():
    """
    Class to store the data types with enough information to query from influx.
    """

    def __init__(self):
        self._data_types = []
    
    def get_data_types(self):
        return self._data_types

    def add_data_types(self, data_types):
        self._data_types += data_types
