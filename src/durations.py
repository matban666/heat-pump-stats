from new_session_subscriber import NewSessionSubscriber
import duration_factory 

class Durations(NewSessionSubscriber):
    """
    Each instance of this will contain a list of durations if the same type
    Multiple instances of this can be used to track different types of durations
    """

    def __init__(self, duration_factory: duration_factory.DurationFactory, subscribers=[]):
        self._duration_factory = duration_factory
        self._durations = []
        self._subscribers = subscribers
        self._duration_factory_func = duration_factory.get_factory_func()

    def update_duration(self, data_frame):
        new_duration = self._duration_factory_func(data_frame, self.get_current_durtation())

        if new_duration is not None:
            self._durations.append(new_duration)
            self.on_new_duration(new_duration)
        else:
            self._update_duration(data_frame)

    def on_new_duration(self, new_duration):
        for subscriber in self._subscribers:
            subscriber.new_session_update(new_duration)

    def get_current_durtation(self):
        if len(self._durations) == 0:
            return None
        
        return self._durations[-1]
    
    def get_current_duration_type(self):
        current_durtation = self.get_current_durtation()

        if current_durtation is None:
            return None

        return current_durtation.get_duration_type().value
    
    def get_current_duration_type_snake(self):
        return self.get_current_duration_type().lower().replace(' ', '_')
    
    def _update_duration(self, data_frame):
        if len(self._durations) == 0:
            raise Exception('No duration to update')

        self._durations[-1]._update_duration(data_frame)

    
    def new_session_update(self, session):
        current_duration = self.get_current_durtation()

        if current_duration is not None:
            current_duration.new_session_update(session)

    def to_json(self):
        return [duration.to_json() for duration in self._durations]

    def __str__(self):

        result = '=' * 80 + '\n' 

        result += f'{self.get_current_duration_type()}: Durations {len(self._durations)}\n'

        for duration in self._durations:
            result += str(duration)

        return result
