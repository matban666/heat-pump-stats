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
        self._state = None
        self._count = 0
        self._on = False

    def update(self, state):
        if self._state is None:
            # First state we just want to know what it is and store it
            # We are interested in transitions from 0 to > 0 so if it comes in
            # as > 0 we don't want to count it
            self._state = state

            if state > 0:
                self._on = True
            return

        if self._on == False and state > 0:
            self._count += 1
            self._on = True
        elif self._on and state == 0:
            self._on = False

    def get_count(self):
        return self._count
    
    @property
    def state(self):
        return self._state 
    
