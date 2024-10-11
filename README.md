# heat-pump-stats
Utility to load ESPAltherma heat pump metrics from Home Assistant Influx and summarise

# Pre Requisites
- ESP Altherma 
- Home Assistant with Influxdb

# Quick Start

## Python
Create a venv (optional method)
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
