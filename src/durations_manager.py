from durations import Durations
from duration_factory import DurationFactory, DurationTypes


class DurationsManager():
    """
    Owns all the different types of durations and passes each data frame to them
    """

    def __init__(self, duration_types):
        subscribers = []
        self._durations = []
        self._duration_types = duration_types

        if 'all_time' in duration_types:
            all_time = Durations(DurationFactory(DurationTypes.ALL_TIME))   
            subscribers.append(all_time)
            self._durations.append(all_time)

        if 'week' in duration_types:
            week = Durations(DurationFactory(DurationTypes.WEEK))
            subscribers.append(week)
            self._durations.append(week)

        if 'day' in duration_types:
            day = Durations(DurationFactory(DurationTypes.DAY))
            subscribers.append(day)
            self._durations.append(day)

        if 'month' in duration_types:
            month = Durations(DurationFactory(DurationTypes.MONTH))
            subscribers.append(month)
            self._durations.append(month)

        # Always add the session duration as it is used by the other durations
        sessions = Durations(DurationFactory(DurationTypes.SESSION), subscribers=subscribers)
        self._durations.append(sessions)

    def __str__(self):
        result = f''
        for duration in reversed(self._durations):
            duration_type = duration.get_current_duration_type_snake()
            if duration_type in self._duration_types:
                result += str(duration)
        return result
    
    def to_json(self):
        result = {}
        for duration in self._durations:
            duration_type = duration.get_current_duration_type_snake()
            if duration_type in self._duration_types:
                result[f'{duration_type}_durations'] = duration.to_json()
        return result

    def update_periods(self, data_frame):
        for duration in self._durations:
            duration.update_duration(data_frame)

