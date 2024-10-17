from datasource.influx.influx_queries import StringQuery, ValueQuery
from datasource.data_types import DataTypeFloat, DataTypeString

class InfluxQueryFactory:
    def __init__(self):
        """
        Don't instantiate this class is a static class
        """
        raise NotImplementedError

    @staticmethod
    def query_influx(data_types, the_first_date, the_last_date, data_ingestor):
        for data_type in data_types.get_data_types():
            print('Querying: ', data_type.get_name())
            if isinstance(data_type, DataTypeString):
                StringQuery(the_first_date, the_last_date, data_ingestor=data_ingestor, 
                            field=data_type.get_data_source_name(), 
                            name=data_type.get_name())
            elif isinstance(data_type, DataTypeFloat):
                ValueQuery(the_first_date, the_last_date, data_ingestor=data_ingestor, 
                            measurement=data_type.get_unit(), 
                            friendly_name=data_type.get_data_source_name(), 
                            name=data_type.get_name())
