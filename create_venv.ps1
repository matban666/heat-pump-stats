
# Create a virtual environment in the project directory based on python 3.11

# Install python 3.11 (or newer but requirements.txt should be compatible with 3.11)
# create a file called .env_windows_python with the following content something like this (USE FORWARD SLASHES IN PATHS):
# PYTHON_BIN=C:/Users/<YOU>/AppData/Local/Programs/Python/Python311/python.exe

# Load environment variables from .env_windows_python file  
$env_vars = Get-Content -Path '.env.windows_python' | ConvertFrom-StringData

#Get the Python executable path from the loaded variables
$PYTHON_BIN = $env_vars['PYTHON_BIN']

Write-Host "Value of PYTHON_BIN:" $PYTHON_BIN

# Create virtual environment (using the path)
& $PYTHON_BIN -m venv venv 

# Activate virtual environment (slightly different activation in PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies from requirements.txt
pip install -r requirements.txt

Write-Host "Virtual environment created and activated!"