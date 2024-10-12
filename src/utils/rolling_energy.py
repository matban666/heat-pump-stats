class RollingEnergy():
    def __init__(self, granularity, start_time):
        self._start_time = start_time
        self._last_time = start_time
        self._power_sum = 0
        self._energy = 0
        self._frames_per_hour = 60 * (60 / granularity) 

    def update(self, current_time, new_power_value):
        # Calculate on the way in so that it can be read out at any time and frequency
        self._power_sum += new_power_value / self._frames_per_hour if self._frames_per_hour > 0 else 0
        self._last_time = current_time

        self._energy = self._power_sum 

    def get_energy(self):
        return float(self._energy)
    
    def __str__(self) -> str:
        return f'{self.get_energy():.2f} kWh'
    
    def __float__(self):
        return self.get_energy()
    
    def __truediv__(self, other):
        if isinstance(other, RollingEnergy):
            return float(self) / float(other)
        return NotImplemented
    
    def __add__(self, other):
        if isinstance(other, RollingEnergy):
            return float(self) + float(other)
        return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __repr__(self):
        return f"RollingEnergy(energy={self._energy})"