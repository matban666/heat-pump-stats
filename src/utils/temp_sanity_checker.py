class TempSanityChecker:
    """
    Sometimes spurious temperature readings of zero are received.  This class
    checks for these and replaces them with the last good value.
    """
    def __init__(self, tolerance=2.0):
        self.current_value = None
        self.tolerance = tolerance

    def sanity_check(self, new_value):
        if self.current_value is None:
            # if this is the first value then we blindly trust
            self.current_value = new_value
        elif new_value != 0.0:
            # if the value isn't zero then we trust it
            self.current_value = new_value
        elif abs(new_value - self.current_value) < self.tolerance:
            # if the value isn't but is with tolerance of the last value then we trust it
            self.current_value = new_value
        else:
            # none of the above conditions were met so ignore the new value
            pass

        return self.current_value