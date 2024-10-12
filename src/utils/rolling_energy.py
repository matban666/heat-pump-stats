from datetime import datetime

class RollingEnergy():
    """
    A class to calculate the rolling energy consumption of a device.  Power values come in kW and
    converted into kWh. This is done by dividing the power by the number of frames per hour.
    """

    def __init__(self, granularity: int):
        """
        Initialize the RollingEnergy object.
        Parameters:
        - granularity (int): The granularity of the energy calculation.
        """
        self._energy = 0
        self._frames_per_hour = 60 * (60 / granularity) 

    def update(self, new_power_value):
        """
        Update the energy calculation with a new power value.

        Calculate on the way in so that it can be read out at any time and frequency

        Parameters:
        - new_power_value (float): The new power value in kW.
        """
        self._energy += new_power_value / self._frames_per_hour if self._frames_per_hour > 0 else 0

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