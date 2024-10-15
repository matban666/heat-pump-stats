import heat_pump_duration_model.duration_factory

class Cycles:
    def __init__(self) -> None:
        self._cycles = []
        
    def update_cycle(self, data_frame):
        factory = heat_pump_duration_model.duration_factory.DurationFactory(heat_pump_duration_model.duration_factory.DurationTypes.CYCLE)

        new_cycle = factory.get_factory_func()(data_frame, self._cycles[-1] if len(self._cycles) > 0 else None)
        if new_cycle is not None:
            self._cycles.append(new_cycle)
        else:
            self._cycles[-1]._update_duration(data_frame)


    def on_cycle_count(self):
        return len([cycle for cycle in self._cycles if cycle.state == 'ON'])
    
    def off_cycle_count(self):
        return len([cycle for cycle in self._cycles if cycle.state == 'OFF'])
    
    def get_count(self):
        return len(self._cycles)

    def to_json(self):
        return [cycle.to_json() for cycle in self._cycles]

    def __str__(self):
        result = f'ON Cycles: {self.on_cycle_count()}\n'
        result += f'All Cycles:\n'
        for i, cycle in enumerate(self._cycles):
            result += str(cycle) + '\n'
        return result
    
