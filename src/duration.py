from utils.calculations import power_from_flow, cop
from datetime import timedelta
from utils.state_counter import StateCounter
from utils.rolling_min_max_mean import RollingMinMaxMean
from utils.rolling_energy import RollingEnergy
from os import environ

class Duration():
    def __init__(self, duration_type, data_frame):
        self._duration_type = duration_type

        self._first_frame = None
        self._current_frame = None

        self._defrost_counter = StateCounter()
        self._bh1_counter = StateCounter()
        self._bh2_counter = StateCounter()
        self._freeze_protection_counter = StateCounter()
        self._freeze_protection_water_piping_counter = StateCounter()
        self._low_noise_control_counter = StateCounter()
        self._silent_mode_counter = StateCounter()

        self._outside_temp = RollingMinMaxMean()
        self._delta_t = RollingMinMaxMean()
        self._flow_setpoint = RollingMinMaxMean()
        self._wc_offset = RollingMinMaxMean()

        granularity = int(environ.get('GRANULARITY', 30))
        self._energy_in = RollingEnergy(granularity, data_frame['DateTime'])
        self._energy_out = RollingEnergy(granularity, data_frame['DateTime'])
        self._energy_ch_in = RollingEnergy(granularity, data_frame['DateTime'])
        self._energy_ch_out = RollingEnergy(granularity, data_frame['DateTime'])
        self._energy_dhw_in = RollingEnergy(granularity, data_frame['DateTime'])
        self._energy_dhw_out = RollingEnergy(granularity, data_frame['DateTime'])
        self._energy_standby = RollingEnergy(granularity, data_frame['DateTime'])
        self._energy_immersion = RollingEnergy(granularity, data_frame['DateTime'])
        self._energy_buh = RollingEnergy(granularity, data_frame['DateTime'])

        self._cop_average = 0
        self._cop_ch = 0
        self._cop_dhw = 0
        self._cop_dhw_inc_immersion = 0
        self._cop_average_inc_immersion = 0

        self._update_duration(data_frame)

    def _update_duration(self, data_frame):
        self._current_frame = data_frame.copy()
        if self._first_frame is None:
            self._first_frame = data_frame.copy()

        self.update_current_frame()

    def update_current_frame(self):
        self._current_operation_mode = self._current_frame['Operation Mode']
        self._current_three_way_valve = self._current_frame ['Three Way Valve']

        power_in = self._current_frame['Power In'] / 1000.0
        power_out = power_from_flow(self._current_frame['Flow Rate'], self._current_frame['Delta T'])
      
        friendly_operation_mode = self.get_friendly_operation_mode(self._current_frame)

        # Update the rolling min/max/mean values
        self._outside_temp.update(self._current_frame['Outdoor Temp'])
        self._delta_t.update(self._current_frame['Delta T'])
        self._flow_setpoint.update(self._current_frame['Flow Setpoint'])
        self._wc_offset.update(self._flow_setpoint.current_value - self._outside_temp.current_value)

        # Update the state counters
        self._defrost_counter.update(self._current_frame['Defrost Operation'])
        self._bh1_counter.update(self._current_frame['BUH Step1'])
        self._bh2_counter.update(self._current_frame['BUH Step2'])
        self._freeze_protection_counter.update(self._current_frame['Freeze Protection'])
        self._freeze_protection_water_piping_counter.update(self._current_frame['Freeze Protection For Water Piping'])
        self._low_noise_control_counter.update(self._current_frame['Low Noise Control'])
        self._silent_mode_counter.update(self._current_frame['Silent Mode'])

        # Update the energy rolling aggregates
        self._energy_in.update(self._current_frame['DateTime'], power_in)
        self._energy_out.update(self._current_frame['DateTime'], power_out)
        self._energy_immersion.update(self._current_frame['DateTime'], self._current_frame['Immersion Power'] / 1000.0)
        
        power_in_buh = 0.0
        if self._bh1_counter.state == 'ON' or self._bh2_counter.state == 'ON':
            power_in_buh = power_in
        
        self._energy_buh.update(self._current_frame['DateTime'], power_in_buh)

        # Why is this here? It should be in the session duration, no?
        power_in_ch = 0.0
        power_in_dhw = 0.0
        power_in_standby = 0.0
        power_out_ch = 0.0
        power_out_dhw = 0.0

        if friendly_operation_mode == 'CH':
            power_in_ch = power_in
            power_out_ch = power_out
        elif friendly_operation_mode == 'DHW':
            power_in_dhw = power_in
            power_out_dhw = power_out
        else:
            power_in_standby = power_in

        self._energy_ch_in.update(self._current_frame['DateTime'], power_in_ch)
        self._energy_ch_out.update(self._current_frame['DateTime'], power_out_ch)
        self._energy_dhw_in.update(self._current_frame['DateTime'], power_in_dhw)
        self._energy_dhw_out.update(self._current_frame['DateTime'], power_out_dhw)
        self._energy_standby.update(self._current_frame['DateTime'], power_in_standby)

        # Calculate the cops
        self._cop_average = cop(self._energy_in, self._energy_out) 
        self._cop_ch = cop(self._energy_ch_in, self._energy_ch_out) 
        self._cop_dhw = cop(self._energy_dhw_in, self._energy_dhw_out) 
        self._cop_dhw_inc_immersion = cop(self._energy_dhw_in + self._energy_immersion, self._energy_dhw_out) 
        self._cop_average_inc_immersion = cop(self._energy_in + self._energy_immersion, self._energy_out)

    def get_title(self):
        return "Duration"
    
    def get_duration_type(self):
        return self._duration_type
    
    def get_first_frame(self):
        return self._first_frame
      
    def get_last_frame(self):
        return self._current_frame
   
    def get_first_time(self):
        return self._first_frame['DateTime']
    
    def get_last_time(self):
        return self._current_frame['DateTime']
    
    def get_duration(self):
        return self.get_last_time() - self.get_first_time()
        
    def get_current_operation_mode(self):
        return self._current_operation_mode
    
    def get_current_three_way_valve(self):
        return self._current_three_way_valve
    
    def get_current_thermostat(self):
        return self._current_frame['Thermostat']

    def get_current_defrost_operation(self):
        return self._current_frame['Defrost Operation']
    
    def get_current_friendly_operation_mode(self):
        return Duration.unfriendly_to_friendly_operation_mode(self._current_operation_mode, self._current_three_way_valve)
    
    @staticmethod
    def get_friendly_operation_mode(data_frame):
        return Duration.unfriendly_to_friendly_operation_mode(data_frame['Operation Mode'], data_frame['Three Way Valve'])
    
    @staticmethod
    def unfriendly_to_friendly_operation_mode(operation_mode, three_way_valve):
        friendly_operation_mode = 'Standby';

        if operation_mode == 'Heating':
            if three_way_valve == 'ON':
                friendly_operation_mode = 'DHW'
            else:
                friendly_operation_mode = 'CH'

        return friendly_operation_mode

    def to_json(self):
        return \
            {
                'title': self.get_title(),
                'start_time': self.get_first_time().astimezone().strftime('%Y:%m:%d %H:%M:%S'),
                'end_time': self.get_last_time().astimezone().strftime('%Y:%m:%d %H:%M:%S'),
                'duration': str(self.get_duration()),
                'defrost_count': self._defrost_counter.get_count(),
                'bh1_count': self._bh1_counter.get_count(),
                'bh2_count': self._bh2_counter.get_count(),
                'freeze_protection_count': self._freeze_protection_counter.get_count(),
                'freeze_protection_water_piping_count': self._freeze_protection_water_piping_counter.get_count(),
                'low_noise_control_count': self._low_noise_control_counter.get_count(),
                'silent_mode_count': self._silent_mode_counter.get_count(),
                'outside_temp': self._outside_temp.to_json(),
                'delta_t': self._delta_t.to_json(),
                'flow_setpoint': self._flow_setpoint.to_json(),
                'wc_offset': self._wc_offset.to_json(),
                'energy_out': float(self._energy_out),
                'energy_in': float(self._energy_in),
                'energy_ch_in': float(self._energy_ch_in),
                'energy_ch_out': float(self._energy_ch_out),
                'energy_dhw_in': float(self._energy_dhw_in),
                'energy_dhw_out': float(self._energy_dhw_out),
                'energy_standby': float(self._energy_standby),
                'energy_immersion': float(self._energy_immersion),
                'cop_average': float(self._cop_average),
                'cop_ch': self._cop_ch,
                'cop_dhw': self._cop_dhw,
                'cop_dhw_inc_immersion': self._cop_dhw_inc_immersion,
                'cop_average_inc_immersion': self._cop_average_inc_immersion
            }

    def __str__(self):
        if self.get_duration() == timedelta(0):
            return ''
              
        result = \
            '-' * 20 + \
            f'{self.get_title()}, Start: {self.get_first_time().astimezone().strftime('%Y:%m:%d %H:%M:%S')}, End: {self.get_last_time().astimezone().strftime('%Y:%m:%d %H:%M:%S')}, Duration: {self.get_duration()}' + \
            '-' * 20 + '\n' + \
            f"Defrosts: {self._defrost_counter.get_count()}, " + \
            f"BUH1: {self._bh1_counter.get_count()}, " + \
            f"BUH2: {self._bh2_counter.get_count()}, " + \
            f"Freeze Protection: {self._freeze_protection_counter.get_count()}, " + \
            f"Freeze Protection(Pipes): {self._freeze_protection_water_piping_counter.get_count()}, " + \
            f"Low Noise: {self._low_noise_control_counter.get_count()}, " + \
            f"Silent Mode: {self._silent_mode_counter.get_count()}\n" + \
            f"Outside Temp: {str(self._outside_temp)}\n" + \
            f"Heating Energy Out: {self._energy_out}, Energy In: {self._energy_in}, Standby Energy: {self._energy_standby}, Immersion Energy: {self._energy_immersion}, BUH Energy: {self._energy_buh}\n" 

        result += self._on_to_str()

        return result
    
    def _on_to_str(self):
        # Override if you want to print a header before the durations are represented as strings
        return ''
    

    