#!/bin/bash

# Create a virtual environment in the project directory based on python 3.12

# Install python 3.12 (or newer but requirements.txt should be compatible with 3.12)
# create a file called .env with the following content like:
# PYTHON_BIN=/usr/local/bin/python3.12

# Load environment variables from .env file  
source .env

# Get the Python executable path from the loaded variables
PYTHON_BIN=$PYTHON_BIN

echo "Value of PYTHON_BIN:" $PYTHON_BIN

# Create virtual environment (using the path)
$PYTHON_BIN -m venv venv 

# Activate virtual environment
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt -v

echo "Virtual environment created and activated!"