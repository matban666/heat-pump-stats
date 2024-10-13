from datetime import datetime
from pprint import pprint
from datasource.data_loader import DataLoader
from durations_manager import DurationsManager
from datasource.data_types import DataTypes
from argparse import ArgumentParser
from dotenv import load_dotenv
from duration_factory import DurationFactory
from os import environ
from tzlocal import get_localzone
from heat_pump_data_types import HeatPumpDataTypes


def analyse_data(heat_pump_data, heat_pump_data_types, the_first_date, the_last_date, duration_types=['session', 'all_time']):
    """
    Create the period manager, this processes the data into time periods.
    Time periods can be sessions or calendar durations.
    A session is a period of time where the heat pump was was idle or being asked to heat for
    either DHW or CH

    Parameters:
    - heat_pump_data (DataLoader): The data to analyze.
    - heat_pump_data_types (HeatPumpDataTypes): The data types to analyze.
    - the_first_date (datetime): The start date for the data analysis.
    - the_last_date (datetime): The end date for the data analysis.
    - duration_types (list): The duration types to analyze.
    """

    periods = DurationsManager(duration_types)

    # current_data has all the data types as keys and their default values as values
    current_data = {data_type.get_name(): data_type.get_default_value() for data_type in heat_pump_data_types.get_data_types()}

    for date_time, data_frame in heat_pump_data.data_by_time(the_first_date, the_last_date):
        # Each incomimg data frame will have one or more keys depending on the 
        # data available for the timestamp. Therefore, we keep track of all 
        # values in current_data and update the values as they come in.  This
        # way we always have a full set of values to send to the period manager

        for k, v, in data_frame.items():
            current_data[k] = v

        current_data['DateTime'] = date_time

        periods.update_periods(current_data)

    return periods


def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")


"""
This script creates a summary of the heat pump data. 
"""
if __name__ == "__main__":
    # Load the environment variables
    load_dotenv()
    load_dotenv(dotenv_path='.env.testing')

    local_timezone = get_localzone()

    # Parse the command line arguments
    parser = ArgumentParser(description="Re-run the data analysis.")
    parser.add_argument("--from_pickle", 
                        help="Load data from pickle file that is saves the data from the last influx run.  Leave out to load from influx.", 
                        action="store_true")
    parser.add_argument("--start_time", 
                        help="The start time for the data analysis (format: YYYY-MM-DDTHH:MM:SS).", 
                        type=parse_datetime, 
                        default=datetime(year=2024, month=9, day=6, tzinfo=local_timezone))
    parser.add_argument("--end_time", 
                        help="The end time for the data analysis (format: YYYY-MM-DDTHH:MM:SS)., leave out to run to 'now'.", 
                        type=parse_datetime, default=datetime.now(local_timezone))
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
    heat_pump_data = DataLoader(the_first_date, the_last_date, heat_pump_data_types, from_pickle='heat_pump_data.pickle' if args.from_pickle else None)

    durations = analyse_data(heat_pump_data, heat_pump_data_types, the_first_date, the_last_date, args.duration_types)

    if args.output_format == "json":
        pprint(durations.to_json())
    else:
        print(durations)
