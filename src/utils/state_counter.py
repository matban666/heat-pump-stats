class StateCounter():
    def __init__(self, state_to_count="ON"):
        self._state_to_count = state_to_count
        self._state = None
        self._count = 0

    def update(self, state):
        if state == self._state:
            return
        
        if state == self._state_to_count:
            self._count += 1    

        self._state = state

    def get_count(self):
        return self._count
    
    @property
    def state(self):
        return self._state
    

class AboveZeroStateCounter():
    def __init__(self):
        self._state = 0
        self._count = 0
        self._on = False

    def update(self, state):
        if self._on == False and state > 0:
            self._count += 1
            self._firendly_state = 'ON'
        elif self._on and state == 0:
            self._firendly_state = 'OFF'

    def get_count(self):
        return self._count
    
    @property
    def state(self):
        return self._state 
    
