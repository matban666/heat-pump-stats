class RollingMinMaxMean():
    def __init__(self):
        self._sum = 0
        self._count = 0
        self._min = float('inf')
        self._max = float('-inf')
        self._mean = 0
        self._current_value = None
        self._first_value = None

    def update(self, new_value):
        if self._first_value is None:
            self._first_value = new_value

        self._current_value = new_value
        self._count += 1
        self._sum += new_value

        # Calculate on the way in so that it can be read out at any time and frequency
        self._min = min(new_value, self._min)
        self._max = max(new_value, self._max)
        self._mean = self._sum / self._count if self._count > 0 else 0

    @property
    def mean(self):
        return self._mean
    
    @property
    def min(self):
        return self._min
    
    @property
    def max(self):
        return self._max
    
    @property
    def first(self):
        return self._first_value
    
    @property
    def last(self):
        return self._current_value
    
    @property
    def current_value(self):
        return self._current_value
    
    def to_json(self):
        return {
            "min": self.min,
            "max": self.max,
            "mean": self.mean,
            "last": self._current_value,
            "first": self._first_value
        }
    
    def __str__(self):
        return f'Min: {self.min:.1f}, Max: {self.max:.1f}, Mean: {self.mean:.1f}, First: {self._first_value:.1f}, Last: {self._current_value:.1f}'