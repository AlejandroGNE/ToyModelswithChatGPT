# -*- coding: utf-8 -*-
"""
Create scenarios and add data overlays to a PLEXOS input dataset

Created on Sat Sep 09 19:19:57 2017

This script automates the process of creating scenarios and adding data overlays in a PLEXOS input dataset using the PLEXOS API. 
The script performs several key functions:
- Database Setup: Establishes a connection to a PLEXOS dataset by copying an existing PLEXOS input XML file.
- Scenario Management: Adds categories and scenarios to the PLEXOS dataset.
- Data Overlay: Adds properties tagged with the created scenario.
- Membership Management: Adds the scenario to a model.

Practical Use Cases
-------------------
1. Model Testing: Useful for testing different scenarios within a PLEXOS model without altering the original dataset.
2. Automation: Automates the process of creating scenarios and adding data overlays, saving time and reducing potential errors compared to manual entry.
3. Learning and Development: Serves as a learning tool for users new to the PLEXOS API.
4. Batch Processing: Can be integrated into larger automation workflows for scenarios requiring repetitive modifications to multiple datasets.

Example Usage
-------------
To run the script and create scenarios in a PLEXOS input dataset, ensure the required PLEXOS API assemblies are available and execute the script in your Python environment.

P9 Tested
@author:
    - Steven (Original Author)
    - Alejandro Elenes (Updated by)
"""

import os
import sys
import clr
from datetime import datetime
from shutil import copyfile

# Load PLEXOS assemblies
sys.path.append('C:/Program Files/Energy Exemplar/PLEXOS 10.0 API')
clr.AddReference('PLEXOS_NET.Core')
clr.AddReference('EEUTILITY')
clr.AddReference('EnergyExemplar.PLEXOS.Utility')

# .NET related imports
from PLEXOS_NET.Core import DatabaseCore
from EEUTILITY.Enums import ClassEnum, CollectionEnum, PeriodEnum
from EnergyExemplar.PLEXOS.Utility.Enums import *
from System import DateTime

def setup_database_connection(input_file, output_file):
    """
    Set up the database connection by copying the base file to a new location.
    Deletes the copied file if it already exists.
    
    Args:
        input_file (str): Path to the base PLEXOS input file.
        output_file (str): Path to the copied PLEXOS input file.
    
    Returns:
        DatabaseCore: An instance of the DatabaseCore class with an open connection.
    """
    if os.path.exists(input_file):
        if os.path.exists(output_file):
            os.remove(output_file)
        copyfile(input_file, output_file)

        db = DatabaseCore()
        db.DisplayAlerts = False
        db.Connection(output_file)
        return db
    else:
        raise FileNotFoundError(f"Base file not found at {input_file}")

def add_scenario_category(db, class_id, category_name):
    """
    Add a category of scenarios if it doesn't already exist.
    
    Args:
        db (DatabaseCore): The database connection object.
        class_id (int): The class ID for the Scenario class.
        category_name (str): The name of the category to add.
    
    Returns:
        None
    """
    if not db.CategoryExists(class_id, category_name):
        db.AddCategory(class_id, category_name)

def add_scenario(db, class_id, category_name):
    """
    Add a scenario to the PLEXOS dataset.
    
    Args:
        db (DatabaseCore): The database connection object.
        class_id (int): The class ID for the Scenario class.
        category_name (str): The category name for the scenario.
    
    Returns:
        str: The name of the newly added scenario.
    """
    scenario = 'API{:%Y%m%d%H%M}'.format(datetime.now())
    db.AddObject(scenario, class_id, True, category_name)
    return scenario

def add_data_overlay(db, collection_id, enum_id, scenario, params):
    """
    Create data and tag it with the scenario.
    
    Args:
        db (DatabaseCore): The database connection object.
        collection_id (int): The collection ID for the data overlay.
        enum_id (int): The enum ID for the property.
        scenario (str): The name of the scenario.
        params (list): List of tuples representing the parameters for the properties.
    
    Returns:
        None
    """
    for p in params:
        db.AddProperty(*p)

def add_scenario_to_model(db, collection_id, model_name, scenario_name):
    """
    Add the scenario to a model.
    
    Args:
        db (DatabaseCore): The database connection object.
        collection_id (int): The collection ID for the model scenarios.
        model_name (str): The name of the model.
        scenario_name (str): The name of the scenario.
    
    Returns:
        None
    """
    db.AddMembership(collection_id, model_name, scenario_name)

def main():
    """
    Main function to execute the script.
    
    This function sets up the database connection, adds scenario categories and scenarios,
    creates data overlays, and adds the scenario to a model in a PLEXOS input dataset.
    
    Returns:
        None
    """
    # Define file paths
    folder = os.path.dirname(__file__)
    input_file = os.path.join(folder, 'rts_PLEXOS.xml')
    output_file = os.path.join(folder, 'rts4.xml')

    # Set up the database connection
    db = setup_database_connection(input_file, output_file)

    # Fetch required IDs
    classes = db.FetchAllClassIds()
    collections = db.FetchAllCollectionIds()
    properties = db.FetchAllPropertyEnums()

    # Add scenario category if it doesn't exist
    add_scenario_category(db, classes["Scenario"], 'Added by API')

    # Add a scenario and get its name
    scenario_name = add_scenario(db, classes["Scenario"], 'Added by API')

    # Define parameters for data overlay (monthly gas prices for 3 months)
    mem_id = db.GetMembershipID(collections["SystemFuels"], 'System', 'NG/CT')
    enum_id = properties["SystemFuels.Price"]
    params = [
        (mem_id, enum_id, 1, 5.0, DateTime(2024, 1, 1), None, None, None, None, scenario_name, None, PeriodEnum.Interval),
        (mem_id, enum_id, 1, 5.1, DateTime(2024, 2, 1), None, None, None, None, scenario_name, None, PeriodEnum.Interval),
        (mem_id, enum_id, 1, 4.8, DateTime(2024, 3, 1), None, None, None, None, scenario_name, None, PeriodEnum.Interval)
    ]

    # Add data overlay
    add_data_overlay(db, collections["SystemFuels"], enum_id, scenario_name, params)

    # Add the scenario to a model
    add_scenario_to_model(db, collections["ModelScenarios"], 'Q1 DA', scenario_name)

    # Close the database connection
    db.Close()

if __name__ == "__main__":
    main()
