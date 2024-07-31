# -*- coding: utf-8 -*-
"""
Update PLEXOS dataset, run model, and query results

Created on Sat Sep 09 19:19:57 2017
Updated on [Today's Date] by [Your Name]

This script automates the process of updating a PLEXOS dataset, running a PLEXOS model, 
and querying the results using the PLEXOS API. The script performs several key functions:
- Database Setup: Establishes a connection to a PLEXOS dataset and updates it.
- Model Execution: Runs the PLEXOS model using the updated dataset.
- Log Parsing: Parses the log file to extract relevant information.
- Results Querying: Queries the results from the PLEXOS solution file and saves them to a CSV and Excel file.

Practical Use Cases
-------------------
1. Model Testing: Useful for testing different configurations within a PLEXOS model.
2. Automation: Automates the process of updating datasets, running models, and querying results, saving time and reducing potential errors.
3. Learning and Development: Serves as a learning tool for users new to the PLEXOS API.
4. Reporting: Can be integrated into larger workflows for generating and analyzing reports from PLEXOS datasets.

Example Usage
-------------
To run the script and perform the update, execution, and querying process, ensure the required PLEXOS API assemblies are available and execute the script in your Python environment.

Updated by [Your Name] to incorporate best practices and enhancements.

P9 Tested

TODO: P9 Failed

"""

import os
import sys
import re
import clr
import subprocess as sp
import pandas as pd
from datetime import datetime
from shutil import copyfile

# Load PLEXOS assemblies
plexospath = 'C:/Program Files/Energy Exemplar/PLEXOS 10.0'
sys.path.append('C:/Program Files/Energy Exemplar/PLEXOS 10.0 API')
clr.AddReference('PLEXOS_NET.Core')
clr.AddReference('EEUTILITY')
clr.AddReference('EnergyExemplar.PLEXOS.Utility')

# .NET related imports
from PLEXOS_NET.Core import DatabaseCore, Solution, PLEXOSConnect
from EEUTILITY.Enums import *
from EnergyExemplar.PLEXOS.Utility.Enums import *

def setup_database_connection(file_path):
    """
    Set up the database connection to the PLEXOS dataset.
    
    Args:
        file_path (str): Path to the PLEXOS input file.
    
    Returns:
        DatabaseCore: An instance of the DatabaseCore class with an open connection.
    """
    db = DatabaseCore()
    db.DisplayAlerts = False
    db.Connection(file_path)
    return db

def update_dataset(original_ds, new_ds):
    """
    Update the PLEXOS dataset by copying the original dataset and adding new data.
    
    Args:
        original_ds (str): Path to the original PLEXOS dataset.
        new_ds (str): Path to the new PLEXOS dataset.
    
    Returns:
        None
    """
    if os.path.exists(original_ds):
        if os.path.exists(new_ds):
            os.remove(new_ds)
        copyfile(original_ds, new_ds)
        
        db = setup_database_connection(new_ds)
        
        classes = db.FetchAllClassIds()
        collections = db.FetchAllCollectionIds()
        properties = db.FetchAllPropertyEnums()
        
        db.AddCategory(classes["Generator"], 'API')
        db.AddObject('ApiGen', classes["Generator"], True, 'API', 'Testing the API')
        db.AddMembership(collections["GeneratorNodes"], 'ApiGen', '101')
        db.AddMembership(collections["GeneratorFuels"], 'ApiGen', 'Coal/Steam')
        db.AddMembership(collections["ReserveGenerators"], 'Spin Up', 'ApiGen')
        
        mem_id = db.GetMembershipID(collections["SystemGenerators"], 'System', 'ApiGen')
        db.AddProperty(mem_id, properties["SystemGenerators.Units"], 1, 0.0, None, None, None, None, None, None, 0, PeriodEnum.Interval)
        
        db.Close()

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
                lines.append(line)
                currentlines -= 1
            if currentlines == 0 and lines:
                yield '\n'.join(lines)
                lines = []

def query_results(sol_file, csv_file):
    """
    Query results from the PLEXOS solution file and save them to a CSV and Excel file.
    
    Args:
        sol_file (str): Path to the PLEXOS solution file.
        csv_file (str): Path to the output CSV file.
    
    Returns:
        None
    """
    if not os.path.exists(sol_file):
        print('No such file')
        return
        
    sol = Solution()
    sol.Connection(sol_file)
    sol.DisplayAlerts = False

    collections = sol.FetchAllCollectionIds()
    sol.QueryToCSV(
        csv_file, False,
        SimulationPhaseEnum.STSchedule,
        collections["SystemGenerators"],
        '', '', PeriodEnum.Interval,
        SeriesTypeEnum.Names, '1'
    )
               
    df = pd.read_csv(csv_file)
    with pd.ExcelWriter(re.sub(r'\.csv$', '.xlsx', csv_file)) as writer:
        df.to_excel(writer, 'Query')

def main():
    """
    Main function to execute the script.
    
    This function updates the PLEXOS dataset, runs the PLEXOS model, parses the log file,
    and queries the results from the PLEXOS solution file.
    
    Returns:
        None
    """
    update_dataset('rts_PLEXOS.xml', 'rts2.xml')
    run_model(plexospath, 'rts2.xml', '.', 'Base')
    for res in parse_logfile('ST Schedule Completed', '.', 'Base', 25):
        print(res)
    query_results('Model Base Solution/Model Base Solution.zip', 'Gens.csv')

if __name__ == "__main__":
    main()
