from abc import ABC, abstractmethod
from duration import Duration

class CycleDuration(Duration, ABC):
    def __init__(self, duration_type, data_frame):
        super().__init__(duration_type, data_frame)

    def __str__(self):
        result = f' {self.state}: duration: {self.get_duration()}, COP: {self._cop_average:.1f}'
        result += self._on_to_str()
        return result
    
    def to_json(self):
        result = super().to_json()  

        result['state'] = self.state

        return result

    @abstractmethod
    def _on_to_str(self):
        raise NotImplementedError
    

class CycleOnDuration(CycleDuration):
    def __init__(self, duration_type, data_frame):
        super().__init__(duration_type, data_frame)

    def _on_to_str(self):
        result = f''

        return result
    
    @property
    def state(self):
        return 'ON'


class CycleOffDuration(CycleDuration):
    def __init__(self, duration_type, data_frame):
        super().__init__(duration_type, data_frame)

    def _on_to_str(self):
        result = ''
        return result
    
    @property
    def state(self):
        return 'OFF'