# heat-pump-stats
Utility to load ESPAltherma heat pump metrics from Home Assistant Influx and summarise

# Pre Requisites
- ESP Altherma https://raomin.github.io/ESPAltherma/
- Home Assistant with Influxdb https://www.home-assistant.io/integrations/influxdb/

# Quick Start

## Python
Create a venv with dependencies in requirements.txt (optional method)
1. Install a fairly new python - tested with 3.12
2. Add the path to .env file - e.g. PYTHON_BIN=/usr/local/bin/python3.12
3. Run source create_venv.sh

## Environment
The environment needs:
INFLUXDB_TOKEN=<YOUR_TOKEN>
INFLUXDB_ORG=<YOUR_ORG>
INFLUXDM_URI=<YOUR_INFLUX_URI>
For convience these can be added to a .env file in the root of the project

## Datatypes and flux
You will probably have to edit src/datasource/data_types.py data_source_names to match your friendly entity names in influx
You may also have to edit the flux queries in src/datasource/influx/influx_queries.py 

## Running
(venv) $ src/heatpump_summary.py

## Help
(venv) $ src/heatpump_summary.py --help

## ToDo

- Compressor starts count, use secondary inverter current
- HeatPumpState class to take complxity out of Duration
- HeatPumpLogic class to collect the state change logic from the DurationFactory
- Influx queries can probably be done as two queries, one for string and one for value instead of a seperate query for every metric
- Adapt for continual streaming from influx and streaming out to somewhere else so that a web app can consume the stats
