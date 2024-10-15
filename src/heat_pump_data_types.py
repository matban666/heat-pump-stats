from datasource.data_types import DataTypes, DataTypeFloat, DataTypeString
from utils.temp_sanity_checker import TempSanityChecker

class HeatPumpDataTypes():
    def __init__(self):
        self.create_data_types()
        self.sanity_check_outdoor_temp = TempSanityChecker()
        self.sanity_check_indoor_temp = TempSanityChecker()

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
            DataTypeFloat(name='INV Primary Current', data_source_name='ESPAltherma - INV Primary Current', unit='A'),
            DataTypeFloat(name='INV Secondary Current', data_source_name='ESPAltherma - INV Secondary Current', unit='A'),
        ])

    def sanity_check(self, data_frame):
        data_frame['Outdoor Temp'] = self.sanity_check_outdoor_temp.check(data_frame['Outdoor Temp'])
        data_frame['Indoor Temp'] = self.sanity_check_indoor_temp.check(data_frame['Indoor Temp'])
        return data_frame

    def get_data_types(self):
        return self.data_types.get_data_types()