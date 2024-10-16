from heat_pump_duration_model.duration import Duration
import heat_pump_duration_model.cycles

class SessionDuration(Duration):
    """
    A SessionDuration is a time duration where the heat pump was in a single operation mode of either CH or DHW or Standby
    CH or DHW will be if the shedule AND thermostat is asking for heat or hot water
    Confusingly, the Themostat propery will be 'Off' when the heat pump is cycling but the above conditions are met

    The functionality of SessionDuration is mostly handled in the base class, This class is just for creation and display
    """

    def __init__(self, name, data_frame):   
        self._cycles = heat_pump_duration_model.cycles.Cycles()

        super().__init__(name, data_frame)

        
    def _update_duration(self, data_frame):
        self._cycles.update_cycle(data_frame)

        super()._update_duration(data_frame)

    def get_title(self):
        return f"{self.get_current_friendly_operation_mode()}"

    def to_json(self):
        result = super().to_json()

        result['cycles'] = self._cycles.to_json()
        return result

    def _on_to_str(self):
        friendly_operation_mode = self.get_current_friendly_operation_mode()

        if friendly_operation_mode in ['CH', 'DHW'] and self._cycles.get_count() == 0:
            return ''

        result = ''

        if friendly_operation_mode == 'CH':
            result += f'Flow Setpoint: {self._flow_setpoint}\n'
            result += f'Flow Temp: {self._flow_temp}\n'
            result += f'WC Offset: {self._wc_offset}\n'
            result += f'Delta T Target: {self.get_last_frame()["Target Delta T"]:.1f}\n'

        if friendly_operation_mode in ['CH', 'DHW']:
            result += f'Delta T: {str(self._delta_t)}\n'

        if friendly_operation_mode == 'DHW':
            result += f'Start Temp: {self.get_first_frame()["DHW Temp"]:.1f}, '
            result += f'End Temp: {self.get_last_frame()["DHW Temp"]:.1f}\n'

        if friendly_operation_mode in ['CH', 'DHW']:
            result += str(self._cycles) 

        if friendly_operation_mode == 'DHW':
            result += f"DHW COP: {self._cop_average:.1f}\n"
            result += f"DHW COP (Inc Immersion): {self._cop_dhw_inc_immersion:.1f}\n"       
            
        if friendly_operation_mode == 'CH':
            result += f"CH COP: {self._cop_average:.2f}\n"

        return result
    
    

