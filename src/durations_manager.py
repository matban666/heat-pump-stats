from durations import Durations
from duration_factory import DurationFactory, DurationTypes


class DurationsManager():
    """
    Owns all the different types of durations and passes each data frame to them
    """

    def __init__(self):
        all_time = Durations(DurationFactory(DurationTypes.ALL_TIME))
        # week = Durations(DurationFactory(DurationTypes.WEEK))
        # day = Durations(DurationFactory(DurationTypes.DAY))
        month = Durations(DurationFactory(DurationTypes.MONTH))
        sessions = Durations(DurationFactory(DurationTypes.SESSION), subscribers=[all_time, month])

        # only one of each type of duration
        self._durations = [
            all_time,
            # month,
            # week,
            # days,
            sessions
        ]

    def __str__(self):
        result = f''
        for duration in reversed(self._durations):
            result += str(duration)
        return result
    
    def to_json(self):
        result = {}
        for duration in self._durations:
            duration_type = duration.get_current_duration_type().lower().replace(' ', '_')
            result[f'{duration_type}_durations'] = duration.to_json()
        return result

    def update_periods(self, data_frame):
        for duration in self._durations:
            duration.update_duration(data_frame)

