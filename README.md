# heat-pump-stats
Utilities to load ESPAltherma heat pump metrics from Home Assistant Influx and summarise

# Pre Requisites
- ESP Altherma https://raomin.github.io/ESPAltherma/
- Home Assistant with Influxdb https://www.home-assistant.io/integrations/influxdb/

# Quick Start

## Python
Create a venv with dependencies in requirements.txt (
    
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
You will probably have to edit src/heat_pump_data_types.py content in create_data_types to match your friendly entity names in influx
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
- Possible Bug: energy for defrosts in CH where DHW is used are counted against DHW, is that correct
- If a defrost in CH requires DHW, this can happen before the defrost state is entered and the CH sesssion is split - see comments in integration tests
- If datatype objects were used to store the values and moved through the pipeline then they could be used for unit display and sanity checking
- HeatPumpState class to take complxity out of Duration
- HeatPumpLogic class to collect the state change logic from the DurationFactory
- Influx queries can probably be done as two queries, one for string and one for value instead of a seperate query for every metric
- Adapt for continual streaming from influx and streaming out to somewhere else so that a web app can consume the stats
