# heat-pump-stats
Utilities to load ESPAltherma heat pump metrics from Home Assistant Influx and summarise.  The initial intention was to just display the data in different groupings to get an understanding of the heat pump behaviour in how it transitions between states and get statistics for sessions and durations. 

## Nomenclature
- duration - A calendar/sesssion/cycle, see below.
- calendar duration - A period of time to gather stats for: year/month/week/day
- session duration - A period of time when the heat pump is in a single mode: Standby/CH/DHW. Calendar durtions know about sessions that start within them.
- cycle duration - A period of time during a DHW or CH session where the compressor is on or off. Cycles belong to sessions.

## Architecture
 It currently does a single read from the datasource (live influx or pickle file), passes the complete data set to the durations manager to identify the durations, then the durations manager is asked for text or json output.  Although it is not streaming, the duration transitions are based on differences between the current and previous data frame.  Therefore, it could be adapted to stream from the input data source and stream to an output data store.  One challenge for streaming is how to handle false state changes that are correctable with data a fram or two on (see: CH session sometimes split into two by defrost that uses DHW).


# Pre Requisites
- ESP Altherma https://raomin.github.io/ESPAltherma/
- Home Assistant with Influxdb https://www.home-assistant.io/integrations/influxdb/

# Quick Start

## Python
Create a venv with dependencies in requirements.txt
    
Ooptional method
1. Install a fairly new python - tested with 3.12
2. Add the path to .env file - e.g. PYTHON_BIN=/usr/local/bin/python3.12
3. Run source create_venv.sh

## Environment
The environment needs:
INFLUXDB_TOKEN=<YOUR_TOKEN>
INFLUXDB_ORG=<YOUR_ORG>
INFLUXDM_URI=<YOUR_INFLUX_URI>
For convience these can be added to a .env.influx file in the root of the project

## Datatypes and flux
You will probably have to edit src/heat_pump_duration_model/heat_pump_data_types.py content in create_data_types to match your friendly entity names in influx
You may also have to edit the flux queries in src/datasource/influx/influx_queries.py if your data is structured differently in influx

## Running
(venv) $ src/heatpump_summary.py
(venv) $ src/heat_pump_ch_energy_by_temp.py

## Help
(venv) $ src/heatpump_summary.py --help
(venv) $ src/heat_pump_ch_energy_by_temp.py --help

## Tests
(venv) $ pytest
Very Sparce
Tested with influx local instance v2.6.0 and cloud version 3

## ToDo

- Move datasource into its own project as it is re-usable - all it time-series-datasource (it's tied to influx but could be agnostic)
- Possible Bug: energy for defrosts in CH where DHW is used are counted against DHW, is that correct?
- CH session sometimes split into two by defrost that uses DHW.  If a defrost in CH requires DHW, the DHW state can start before the defrost state is entered resulting in the CH sesssion being split into two sessions - see comments in integration tests (1 minute on 2024-10-14 at 07:42). I wonder if we could quaranteen new sessions for a frame or three - If we get a succession of CH, DHW defrost single frame, CH then we append the data from the last two quaranteened sessions to the prior session, make that the current session and then dump the quaranteened sessions.  Rule for exiting quaranteen normally could be that the session has more than one frame or it is more than 2 or 3 frames old.  This puts a delay on the stream of 1 to 1.5 mins (at 30 second granularity).  We also need a mechanism to flush the quaranteen que when we have finished reading - nice if it was implicit rather than needing to call a 'flush' or 'close' from the outside.  Sessions and perhaps Cycles would need this but not Calendar durations so could manage as an extension for duration(s) rather than a modification. 
- If datatype objects were used to store the values and moved through the pipeline then they could be used for unit display and sanity checking
- HeatPumpState class to take complxity out of Duration
- HeatPumpLogic class to collect the state change logic from the DurationFactory
- Influx queries can probably be done as two queries, one for string and one for value instead of a seperate query for every metric
- Adapt for continual streaming from influx and streaming out to somewhere else so that a web app can consume the stats
