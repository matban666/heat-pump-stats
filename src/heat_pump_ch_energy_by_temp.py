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
This script creates a summary input and output energy by temperature 
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
    durations = DurationsManager.from_data(heat_pump_data, args.start_time, args.end_time, ['day'])

    # Output the data in the required format
    day_durations = durations.to_json()['day_durations']

    for day in sorted(day_durations, key=lambda x: x['outside_temp']['mean']):
        # pprint(day)
        print(f"Day: {day['start_time']}, mean outside temp: {day['outside_temp']['mean']:.1f}, mean inside temp: {day['inside_temp']['mean']:.1f}, flow setpoint mean: {day['flow_setpoint']['mean']:.1f}, wc offset mean: {day['wc_offset']['mean']:.1f}, input energy: {day['energy_ch_in']:.1f}, output energy: {day['energy_ch_out']:.1f}, cop {day['cop_ch']:.2f}")

