from datetime import datetime
from pprint import pprint
from datasource.data_loader import DataLoader
from durations_manager import DurationsManager
from argparse import ArgumentParser
from dotenv import load_dotenv
from duration_factory import DurationFactory
from os import environ
from tzlocal import get_localzone
from heat_pump_data_types import HeatPumpDataTypes

"""
This script creates a summary of the heat pump data. 
"""
if __name__ == "__main__":
    # Load the environment variables
    load_dotenv()
    load_dotenv(dotenv_path='.env.testing')
    load_dotenv(dotenv_path='.env.influx')

    local_timezone = get_localzone()

    # Parse the command line arguments
    parser = ArgumentParser(description="Re-run the data analysis.")
    parser.add_argument("--from_pickle", 
                        help="Load data from pickle file that is saves the data from the last influx run.  Leave out to load from influx.", 
                        action="store_true")
    parser.add_argument("--start_time", 
                        help="The start time for the data analysis (format: YYYY-MM-DDTHH:MM:SS).", 
                        type=lambda datetime_str: datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S"), 
                        default=datetime(year=2024, month=9, day=6, tzinfo=local_timezone))
    parser.add_argument("--end_time", 
                        help="The end time for the data analysis (format: YYYY-MM-DDTHH:MM:SS)., leave out to run to 'now'.", 
                        type=lambda datetime_str: datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S"), 
                        default=datetime.now(local_timezone))
    parser.add_argument("--output_format", 
                        help="The output format for the data analysis.", 
                        default="text", 
                        choices=["text", "json"])
    parser.add_argument("--duration_types", 
                        help="Duration types that you want to display.", 
                        nargs='+', 
                        choices=DurationFactory.get_top_level_duration_names(),
                        default=["session", "all_time"])

    args = parser.parse_args()

    # What period of data do we want to analyze?
    the_first_date = args.start_time.replace(tzinfo=local_timezone)
    the_last_date = args.end_time.replace(tzinfo=local_timezone)

    # this defines the data types that we are interested in loading from the data sounrce
    heat_pump_data_types = HeatPumpDataTypes()

    # Load the data (if from file then it will be whatever dates were used last time with influx)
    # make sure the dates specified align with or are within the data in the pickle file
    heat_pump_data = DataLoader(the_first_date, the_last_date, heat_pump_data_types, from_pickle='data.pickle' if args.from_pickle else None)

    durations = DurationsManager.from_data(heat_pump_data, the_first_date, the_last_date, args.duration_types)

    if args.output_format == "json":
        pprint(durations.to_json())
    else:
        print(durations)
