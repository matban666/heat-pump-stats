from datetime import datetime
from pprint import pprint
from datasource.data_loader import DataLoader
from heat_pump_duration_model.durations_manager import DurationsManager
from argparse import ArgumentParser
from dotenv import load_dotenv
from heat_pump_duration_model.duration_factory import DurationFactory
from tzlocal import get_localzone
from heat_pump_duration_model.heat_pump_data_types import HeatPumpDataTypes

"""
This script creates a summary of CH cycles. 
"""
if __name__ == "__main__":
    # Load the environment variables if they are in files
    load_dotenv()
    load_dotenv(dotenv_path='.env.testing')
    load_dotenv(dotenv_path='.env.influx')

    # Get the local timezone
    local_timezone = get_localzone()

    # Parse the command line arguments
    parser = ArgumentParser(description="Re-run the data analysis.")
    parser.add_argument("--from_pickle", 
                        help="Load data from pickle file that is saves the data from the last influx run.  Leave out to load from influx.", 
                        action="store_true")
    parser.add_argument("--start_time", 
                        help="The start time for the data analysis (format: YYYY-MM-DDTHH:MM:SS).", 
                        type=lambda datetime_str: datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=local_timezone), 
                        default=datetime(year=2024, month=9, day=6, tzinfo=local_timezone))
    parser.add_argument("--end_time", 
                        help="The end time for the data analysis (format: YYYY-MM-DDTHH:MM:SS)., leave out to run to 'now'.", 
                        type=lambda datetime_str: datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=local_timezone), 
                        default=datetime.now(local_timezone))

    args = parser.parse_args()

    # this defines the data types that we are interested in loading from the data sounrce
    heat_pump_data_types = HeatPumpDataTypes()

    # Load the data (if from file then it will be whatever dates were used last time with influx)
    # make sure the dates specified align with or are within the data in the pickle file
    heat_pump_data = DataLoader(args.start_time, args.end_time, heat_pump_data_types, from_pickle='data.pickle' if args.from_pickle else None)

    # Create a DuratonManager object by reading the data in and processing it into the required durations
    durations = DurationsManager.from_data(heat_pump_data, args.start_time, args.end_time, ['session'])

    # Output the data in the required format
    sessions = durations.to_json()['session_durations']

    for session in filter(lambda x: x['title'] == 'CH', sessions):
        # pprint(session)
        # break
        for cycle in filter(lambda x: x['state'] == 'ON' and x['duration'] != "0:00:00", session['cycles']):
            print(f"Cycle: {cycle['start_time']}, Length: {cycle['duration']}, OUT: {cycle['outside_temp']['last']:.1f}, IN: {cycle['inside_temp']['last']:.1f}, Flow SP: {cycle['flow_setpoint']['last']:.1f}, Flow: {cycle['flow_temp']['last']:.1f}, WC Off: {cycle['wc_offset']['last']:.1f}, Elec: {cycle['energy_ch_in']:.1f}, Heat: {cycle['energy_ch_out']:.1f}, Flow Over: {cycle['flow_temp']['last'] - cycle['flow_setpoint']['last']:.1f}, Room Over: {cycle['inside_temp']['last'] - cycle['room_setpoint']['last']:.1f}, COP {cycle['cop_ch']:.1f}")
            # pprint(cycle)
