from enum import Enum
from session_duration import SessionDuration
from calendar_duration import CalendarDuration
from cycle_duration import CycleOffDuration, CycleOnDuration

class DurationTypes(Enum):
    DAY = 'Day'
    WEEK = 'Week'
    MONTH = 'Month'
    YEAR = 'Year'
    ALL_TIME = 'All Time'
    SESSION = 'Session'
    CYCLE = 'Cycle'

class DurationFactory():
    """
    This delegates the creation of new durations to the correct factory method so that the owner of the durations
    can be generic as it does not need to know how to create each type of duration

    I wonder if the logic in the factory methods should be in the durations themselves, this would make the durations
    the single source of understanding of how to create themselves.  Or, the logic in the factory methods could be moved
    to a HeatPumpModel class so that all heat pump state transition logic was in one place and the durations were just durations
    """
    def __init__(self, duration_type: DurationTypes):
        self._duration_type = duration_type

    def get_factory_func(self):
        if self._duration_type == DurationTypes.DAY:
            return self.day_factory
        elif self._duration_type == DurationTypes.WEEK:
            return self.week_factory
        elif self._duration_type == DurationTypes.MONTH:
            return self.month_factory
        elif self._duration_type == DurationTypes.YEAR:
            return self.year_factory
        elif self._duration_type == DurationTypes.ALL_TIME:
            return self.all_time_factory
        elif self._duration_type == DurationTypes.SESSION:
            return self.session_factory
        elif self._duration_type == DurationTypes.CYCLE:
            return self.cycle_factory
        else:
            raise Exception('Unknown duration type')
    
    @property
    def duration_type(self):
        return self._duration_type
    
    @staticmethod
    def get_top_level_duration_names():
        snake = lambda x: x.lower().replace(' ', '_')

        return [snake(duration_type.value) for duration_type in DurationTypes if duration_type not in [DurationTypes.CYCLE]]


    @staticmethod
    def session_factory(data_frame, current_duration):
        """
        Work out if a new session should be created and create it if necessary
        """
        duration_type = DurationTypes.SESSION

        if current_duration is None:
            # This is the first data frame so create a new duration
            return SessionDuration(duration_type, data_frame)
        
        # detect state change between On/Off CH and DHW
        if data_frame['Operation Mode'] != current_duration.get_current_operation_mode():
            # The operation mode has changed so create a new duration
            return SessionDuration(duration_type, data_frame)
        elif data_frame['Operation Mode'] == 'Heating':
            # We are in heatng mode so check if the three way valve has changed
            if data_frame['Three Way Valve'] != current_duration.get_current_three_way_valve():
                # Three way valve has changed

                # Check if this is a defrost
                if data_frame['Defrost Operation'] == 'ON':
                    # During a CH session and a defrost it might temporarily swich the three way valve to DHW
                    # in order to use some heat from the cylinder to defrost heatp pump, ignore this
                    return None

                # The three way valve has changed whilst in heating mode so create a new duration
                return SessionDuration(duration_type, data_frame)
        
        return None

    @staticmethod
    def cycle_factory(data_frame, current_duration):
        """
        Work out if a new cycle should be created and create it if necessary
        """
        duration_type = DurationTypes.CYCLE

        if current_duration is None or data_frame['Thermostat'] != current_duration.get_current_thermostat():
            # This is the first data frame so create a new duration
            if data_frame['Thermostat'] == 'ON':
                return CycleOnDuration(duration_type, data_frame)
            else:
                return CycleOffDuration(duration_type, data_frame)
            
        if current_duration.get_current_thermostat() == 'ON':
            if data_frame['Defrost Operation'] != current_duration.get_current_defrost_operation():
                if data_frame['Defrost Operation'] == 'ON':
                    return CycleOffDuration(duration_type, data_frame)
                elif data_frame['Defrost Operation'] == 'OFF':
                    return CycleOnDuration(duration_type, data_frame)
        
        return None

    @staticmethod
    def all_time_factory(data_frame, current_duration):
        duration_type = DurationTypes.ALL_TIME

        if current_duration is None:
            return CalendarDuration(duration_type, data_frame)
        
        return None
    
    @staticmethod
    def year_factory(data_frame, current_duration):
        duration_type = DurationTypes.YEAR

        if current_duration is None:
            return CalendarDuration(duration_type, data_frame)
        
        if data_frame['DateTime'].year != current_duration.get_last_time().year:
            return CalendarDuration(duration_type, data_frame)
        
        return None

    @staticmethod
    def month_factory(data_frame, current_duration):
        duration_type = DurationTypes.MONTH

        if current_duration is None:
            return CalendarDuration(duration_type, data_frame)
        
        if data_frame['DateTime'].month != current_duration.get_last_time().month:
            return CalendarDuration(duration_type, data_frame)
        
        return None
    
    @staticmethod
    def week_factory(data_frame, current_duration):
        duration_type = DurationTypes.WEEK

        if current_duration is None:
            return CalendarDuration(duration_type, data_frame)
        
        if data_frame['DateTime'].weekday() == 0 and current_duration.get_last_time().weekday() == 6:
            return CalendarDuration(duration_type, data_frame)
        
        return None
    
    @staticmethod
    def day_factory(data_frame, current_duration):
        duration_type = DurationTypes.DAY

        if current_duration is None:
            return CalendarDuration(duration_type, data_frame)

        if data_frame['DateTime'].day != current_duration.get_last_time().day:
            return CalendarDuration(duration_type, data_frame)
        
        return None

    