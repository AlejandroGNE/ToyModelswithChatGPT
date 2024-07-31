# -*- coding: utf-8 -*-
"""
Modify the horizon of a PLEXOS model

Created on Mon Dec 17 15:42:56 2018

This script automates the process of modifying the horizon of a PLEXOS model using the PLEXOS API. 
The script performs several key functions:
- Database Setup: Establishes a connection to a PLEXOS dataset.
- Horizon Modification: Updates the start date and step type for the model horizon.

Practical Use Cases
-------------------
1. Model Testing: Useful for testing different horizon configurations within a PLEXOS model.
2. Automation: Automates the process of updating model horizons, saving time and reducing potential errors.
3. Learning and Development: Serves as a learning tool for users new to the PLEXOS API.
4. Reporting: Can be integrated into larger workflows for generating and analyzing reports from PLEXOS models.

Example Usage
-------------
To run the script and modify the model horizon, ensure the required PLEXOS API assemblies are available and execute the script in your Python environment.

Updated by [Your Name] to incorporate best practices and enhancements.

"""

import os
import sys
import clr
import datetime as dt
from shutil import copyfile

# Load PLEXOS assemblies
plexos_path = 'C:/Program Files/Energy Exemplar/PLEXOS 10.0 API'
sys.path.append(plexos_path)
clr.AddReference('PLEXOS_NET.Core')
clr.AddReference('EEUTILITY')
clr.AddReference('EnergyExemplar.PLEXOS.Utility')

# .NET related imports
from PLEXOS_NET.Core import DatabaseCore
from EEUTILITY.Enums import *
from EnergyExemplar.PLEXOS.Utility.Enums import *
from System import DateTime

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

def copy_plexos_file(original_file, new_file):
    """
    Copy the PLEXOS input file to a new location.
    
    Args:
        original_file (str): Path to the original PLEXOS input file.
        new_file (str): Path to the new PLEXOS input file.
    
    Returns:
        None
    """
    if not os.path.exists(original_file):
        raise FileNotFoundError(f'"{original_file}" does not exist')

    if os.path.exists(new_file):
        os.remove(new_file)

    copyfile(original_file, new_file)

def modify_model_horizon(datafile, modelname, start):
    """
    Modify the horizon of a PLEXOS model by updating the start date and step type.
    
    Args:
        datafile (str): Path to the PLEXOS input file.
        modelname (str): Name of the model to modify.
        start (DateTime): The new start date for the model horizon.
    
    Returns:
        str: The path of the newly created PLEXOS input file.
    """
    tempfile = f'{datafile[:-4]}{dt.datetime.now():%m%d%Y%H%M%S}.xml'
    copy_plexos_file(datafile, tempfile)
    
    db = setup_database_connection(tempfile)
    classes = db.FetchAllClassIds()
    collections = db.FetchAllCollectionIds()
    attributes = db.FetchAllAttributeEnums()
    
    horizons = db.GetChildMembers(collections["ModelHorizon"], modelname)
    for hor in horizons:
        db.UpdateAttribute(classes["Horizon"], hor, int(attributes["Horizon.DateFrom"]), DateTime(start.Year, 1, 1).ToOADate())
        db.UpdateAttribute(classes["Horizon"], hor, int(attributes["Horizon.StepType"]), 4)
        db.UpdateAttribute(classes["Horizon"], hor, int(attributes["Horizon.ChronoDateFrom"]), start.ToOADate())
                    
    db.Close()
    return tempfile
    
def main():
    """
    Main function to execute the script.
    
    This function modifies the horizon of a specified PLEXOS model and updates the dataset.
    
    Returns:
        None
    """
    new_file = modify_model_horizon('test.xml', 'Base', DateTime.Today)
    print(f'Modified PLEXOS input file created: {new_file}')

if __name__ == '__main__':
    main()
