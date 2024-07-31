# -*- coding: utf-8 -*-
"""
Update PLEXOS attributes in an input dataset

Created on Sat Sep 09 19:19:57 2017

This script automates the process of updating attributes in a PLEXOS input dataset using the PLEXOS API. 
The script performs several key functions:
- Database Setup: Establishes a connection to a PLEXOS dataset by copying an existing PLEXOS input XML file.
- Object Manipulation: Copies and removes objects within the PLEXOS dataset.
- Membership Management: Adds and removes memberships between objects.
- Attribute Management: Updates or adds attributes to objects within the dataset.

Practical Use Cases
-------------------
1. Model Testing: Useful for testing different configurations within a PLEXOS model without altering the original dataset.
2. Automation: Automates the process of updating attributes, saving time and reducing potential errors compared to manual entry.
3. Learning and Development: Serves as a learning tool for users new to the PLEXOS API.
4. Batch Processing: Can be integrated into larger automation workflows for scenarios requiring repetitive modifications to multiple datasets.

Example Usage
-------------
To run the script and update attributes in a PLEXOS input dataset, ensure the required PLEXOS API assemblies are available and execute the script in your Python environment.

TODO: P9 Failed

Updated to incorporate best practices and enhancements.

@author:
    - Steven (Original Author)
    - Alejandro Elenes (Updated by)
"""

import os
import sys
import clr
from shutil import copyfile

# Load PLEXOS assemblies
sys.path.append('C:/Program Files/Energy Exemplar/PLEXOS 10.0 API')
clr.AddReference('PLEXOS_NET.Core')
clr.AddReference('EEUTILITY')
clr.AddReference('EnergyExemplar.PLEXOS.Utility')

# .NET related imports
from PLEXOS_NET.Core import DatabaseCore
from EEUTILITY.Enums import ClassEnum, CollectionEnum
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
        db.Connection(output_file)
        return db
    else:
        raise FileNotFoundError(f"Base file not found at {input_file}")

def copy_and_remove_objects(db, classes):
    """
    Copy and remove objects within the PLEXOS dataset.
    
    Args:
        db (DatabaseCore): The database connection object.
        classes (dict): Dictionary of class IDs.
    
    Returns:
        None
    """
    db.CopyObject('Q1 DA', 'APIModel', classes["Model"])
    db.CopyObject('Q1 DA', 'APIHorizon', classes["Horizon"])
    
    collections = db.FetchAllCollectionIds()
    
    db.RemoveMembership(collections["ModelHorizon"], 'Q1 DA', 'APIHorizon')
    db.RemoveMembership(collections["ModelHorizon"], 'APIModel', 'Q1 DA')

def update_or_add_attributes(db, attributes):
    """
    Update or add attributes to objects within the PLEXOS dataset.
    
    Args:
        db (DatabaseCore): The database connection object.
        attributes (list): List of tuples representing attributes to update or add.
    
    Returns:
        None
    """
    for param in attributes:
        if not db.UpdateAttribute(*param):
            db.AddAttribute(*param)

def main():
    """
    Main function to execute the script.
    
    This function sets up the database connection, copies and removes objects,
    manages memberships, and updates or adds attributes in a PLEXOS input dataset.
    
    Returns:
        None
    """
    # Define file paths
    folder = os.path.dirname(__file__)
    input_file = os.path.join(folder, 'rts_PLEXOS.xml')
    output_file = os.path.join(folder, 'rts3.xml')

    # Set up the database connection
    db = setup_database_connection(input_file, output_file)

    # Fetch required IDs
    classes = db.FetchAllClassIds()
    attribute_ids = db.FetchAllAttributeEnums()

    # Copy and remove objects
    copy_and_remove_objects(db, classes)
    
    # Define attributes to update or add
    attributes = [
        (classes["Horizon"], 'APIHorizon', attribute_ids["Horizon.DateFrom"], DateTime(2024, 1, 1).ToOADate()),
        (classes["Horizon"], 'APIHorizon', attribute_ids["Horizon.StepType"], 4.0),
        (classes["Horizon"], 'APIHorizon', attribute_ids["Horizon.StepCount"], 1.0),
        (classes["Horizon"], 'APIHorizon', attribute_ids["Horizon.ChronoDateFrom"], DateTime(2024, 2, 15).ToOADate()),
        (classes["Horizon"], 'APIHorizon', attribute_ids["Horizon.ChronoStepType"], 2.0),
        (classes["Horizon"], 'APIHorizon', attribute_ids["Horizon.ChronoAtaTime"], 3.0),
        (classes["Horizon"], 'APIHorizon', attribute_ids["Horizon.ChronoStepCount"], 4.0)
    ]

    # Update or add attributes
    update_or_add_attributes(db, attributes)

    # Close the database connection
    db.Close()

if __name__ == "__main__":
    main()
