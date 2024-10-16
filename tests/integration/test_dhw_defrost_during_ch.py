import pytz
from datetime import datetime
from datasource.data_loader import DataLoader
from heat_pump_duration_model.heat_pump_data_types import HeatPumpDataTypes
from pprint import pprint
from heat_pump_duration_model.durations_manager import DurationsManager


def test_defrost_during_ch():
    the_first_date = datetime(year=2024, month=10, day=11, hour=4, tzinfo=pytz.timezone('Europe/London'))
    the_last_date = datetime(year=2024, month=10, day=11, hour=9, tzinfo=pytz.timezone('Europe/London'))

    heat_pump_data_types = HeatPumpDataTypes()
    #Load the data (if from file then it will be whatever dates were used last time with influx)
    heat_pump_data = DataLoader(the_first_date, the_last_date, heat_pump_data_types, from_pickle='tests/integration/heat_pump_data_defrost_during_ch.pickle')

    periods = DurationsManager.from_data(heat_pump_data, the_first_date, the_last_date)

    json = periods.to_json()

    assert('session_durations' in json)
    assert('all_time_durations' in json)
    assert(len(json['session_durations']) == 3)
    assert(len(json['session_durations'][1]['cycles']) == 3)

    # pprint(json)


def test_dhw_defrost_during_ch():
    the_first_date = datetime(year=2024, month=10, day=10, hour=4, tzinfo=pytz.timezone('Europe/London'))
    the_last_date = datetime(year=2024, month=10, day=10, hour=9, tzinfo=pytz.timezone('Europe/London'))

    heat_pump_data_types = HeatPumpDataTypes()

    #Load the data (if from file then it will be whatever dates were used last time with influx)
    heat_pump_data = DataLoader(the_first_date, the_last_date, heat_pump_data_types, from_pickle='tests/integration/heat_pump_data_dhw_defrost_during_ch.pickle')

    periods = DurationsManager.from_data(heat_pump_data, the_first_date, the_last_date)

    json = periods.to_json()

    assert('session_durations' in json)
    assert('all_time_durations' in json)
    assert(len(json['session_durations']) == 3)
    assert(len(json['session_durations'][1]['cycles']) == 7)

    # pprint(json)


# TODO:
# Test heat_pump_data_dhw_before_defrost_in_ch.pickle
# This is a case where the DHW is called for before the defrost in a CH session
# It results in the CH session being splut into two parts
# It would be nicer to show this as a single CH session but not sure now to do that without making the code more complex
# the_first_date = datetime(year=2024, month=10, day=13, hour=5, tzinfo=pytz.timezone('Europe/London'))
# the_last_date = datetime(year=2024, month=10, day=13, hour=10, tzinfo=pytz.timezone('Europe/London'))