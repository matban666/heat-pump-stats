from heat_pump_duration_model.duration import Duration
from heat_pump_duration_model.new_session_subscriber import NewSessionSubscriber
from collections import defaultdict

class CalendarDuration(Duration, NewSessionSubscriber):
    """
    A duration of time that is based on a calendar period such as a day, week, month or year, the heat pump can be in any state during this time
    Calendar durations may include SessionDurations so that Session stats per Duration can be calculated

    The functionality of SessionDuration is all handled in Duration, This class is just for creation, diplay and subscription management
    """

    def __init__(self, name, data_frame):
        Duration.__init__(self, name, data_frame)

        self._sessions = []

    def _on_to_str(self) -> str:
        return \
            f"CH: Sessions:{self.get_ch_session_count()} Energy in:{self._energy_ch_in} Energy out: {self._energy_ch_out} COP: {self._cop_ch:.1f}\n" + \
            f"DHW: Sessions:{self.get_dhw_session_count()} Energy in:{self._energy_dhw_in} Energy out: {self._energy_dhw_out} COP: {self._cop_dhw:.1f} COP Inc Immersion: {self._cop_dhw_inc_immersion:.1f}\n"  + \
            f"SCOP: {self._cop_average:.2f}\n" + \
            f"SCOP Inc Immersion: {self._cop_average_inc_immersion:.2f}\n" 

    def new_session_update(self, session):
        # This is making the assumption that calendar durations and session durations are in lock step for every data frame 
        # and ordeded with the calendar durations first
        # it would be more robust to check that the datetime of the session is within the calendar duration  
        self._sessions.append(session)

    def get_ch_session_count(self):
        return len([session for session in self._sessions if session.get_current_friendly_operation_mode() == 'CH'])
    
    def get_dhw_session_count(self):
        return len([session for session in self._sessions if session.get_current_friendly_operation_mode() == 'DHW'])
    
    def to_json(self):
        result = super().to_json()

        session_type_count = defaultdict(int)

        for session in self._sessions:
            session_type_count[session.get_title()] += 1

        result['sessions'] = dict(session_type_count)

        return result
    
    def get_title(self):
        return f"{self._duration_type.value} Duration"