# -*- coding: utf-8 -*-
"""
Run PLEXOS model and parse log file for specific patterns

This script automates the process of running a PLEXOS model and parsing the log file for specific patterns.
The script performs several key functions:
- Model Execution: Runs the PLEXOS model using the specified dataset.
- Log Parsing: Parses the log file to extract relevant information based on a pattern.

Practical Use Cases
-------------------
1. Model Testing: Useful for running PLEXOS models and extracting specific log information for analysis.
2. Automation: Automates the process of running models and parsing logs, saving time and reducing potential errors.
3. Learning and Development: Serves as a learning tool for users new to the PLEXOS API.
4. Reporting: Can be integrated into larger workflows for generating and analyzing reports from PLEXOS models.

Example Usage
-------------
To run the script and perform the model execution and log parsing, ensure the required PLEXOS API assemblies are available and execute the script in your Python environment.

Updated by [Your Name] to incorporate best practices and enhancements.

"""

import sys
import os
import re
from shutil import copyfile
import subprocess as sp

def run_model(plexospath, filename, foldername, modelname):
    """
    Execute the PLEXOS model using the specified dataset.
    
    Args:
        plexospath (str): Path to the PLEXOS installation directory.
        filename (str): Name of the PLEXOS input file.
        foldername (str): Name of the folder to store the output.
        modelname (str): Name of the model to execute.
    
    Returns:
        None
    """
    sp.call([os.path.join(plexospath, 'PLEXOS64.exe'), filename, r'\n', r'\o', foldername, r'\m', modelname])

def parse_logfile(pattern, foldername, modelname, linecount=1):
    """
    Parse the PLEXOS log file to extract relevant information based on a pattern.
    
    Args:
        pattern (str): The regex pattern to search for in the log file.
        foldername (str): The folder where the log file is located.
        modelname (str): The name of the model whose log file is being parsed.
        linecount (int): The number of lines to extract after the pattern match.
    
    Yields:
        str: The extracted log lines.
    """
    currentlines = 0
    lines = []
    regex = re.compile(pattern)
    
    log_path = os.path.join(foldername, f'Model {modelname} Solution', f'Model ( {modelname} ) Log.txt')
    with open(log_path, 'r') as log_file:
        for line in log_file:
            if regex.findall(line):
                currentlines = linecount
            if currentlines > 0:
                lines.append(line.strip())
                currentlines -= 1
            if currentlines == 0 and lines:
                yield '\n'.join(lines)
                lines = []

def main():
    """
    Main function to execute the script.
    
    This function runs the PLEXOS model and parses the log file for specific patterns.
    
    Returns:
        None
    """
    plexospath = "C:\\Program Files\\Energy Exemplar\\PLEXOS 10.0"
    run_model(plexospath, 'test.xml', '.', 'Base')
    for res in parse_logfile('ST Schedule Completed', '.', 'Base', 25):
        print(res)

if __name__ == '__main__':
    main()
