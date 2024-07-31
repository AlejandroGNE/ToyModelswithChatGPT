# -*- coding: utf-8 -*-
"""
Retrieve data from the PLEXOS input dataset

Created on Sat Sep 09 19:19:57 2017
Updated on [Today's Date] by [Your Name]

This script automates the retrieval of data from a PLEXOS input dataset using the PLEXOS API. 
The script performs several key functions:
- Database Setup: Establishes a connection to a PLEXOS dataset.
- Data Retrieval: Fetches and lists generators from the dataset.
- Property Query: Queries and writes properties of a specific generator to an output file.

Practical Use Cases
-------------------
1. Data Analysis: Useful for analyzing and extracting specific data from a PLEXOS model.
2. Automation: Automates the process of data retrieval, saving time and reducing potential errors compared to manual data extraction.
3. Learning and Development: Serves as a learning tool for users new to the PLEXOS API.
4. Reporting: Can be integrated into larger workflows for generating reports from PLEXOS datasets.

Example Usage
-------------
To run the script and retrieve data from a PLEXOS input dataset, ensure the required PLEXOS API assemblies are available and execute the script in your Python environment.

Updated by [Your Name] to incorporate best practices and enhancements.

P9 Tested

@author:
    - Steven (Original Author)
    - Alejandro Elenes (Updated by)
"""

import os
import sys
import clr

# Load PLEXOS assemblies
sys.path.append('C:/Program Files/Energy Exemplar/PLEXOS 10.0 API')
clr.AddReference('PLEXOS_NET.Core')
clr.AddReference('EEUTILITY')
clr.AddReference('EnergyExemplar.PLEXOS.Utility')

# .NET related imports
from PLEXOS_NET.Core import DatabaseCore
from EEUTILITY.Enums import ClassEnum, CollectionEnum
from EnergyExemplar.PLEXOS.Utility.Enums import *

def setup_database_connection(input_file):
    """
    Set up the database connection to the PLEXOS dataset.
    
    Args:
        input_file (str): Path to the PLEXOS input file.
    
    Returns:
        DatabaseCore: An instance of the DatabaseCore class with an open connection.
    """
    db = DatabaseCore()
    db.DisplayAlerts = False
    db.Connection(input_file)
    return db

def fetch_and_list_generators(db, class_id, output_file):
    """
    Fetch and list generators from the PLEXOS dataset.
    
    Args:
        db (DatabaseCore): The database connection object.
        class_id (int): The class ID for generators.
        output_file (file): The output file to write the list of generators.
    
    Returns:
        None
    """
    output_file.write('List of generators\n')
    for gen in db.GetObjects(class_id):
        output_file.write(gen + '\n')

def query_and_write_generator_properties(db, collection_id, parent_name, output_file):
    """
    Query and write properties of a specific generator to the output file.
    
    Args:
        db (DatabaseCore): The database connection object.
        collection_id (int): The collection ID for system generators.
        parent_name (str): The name of the parent generator.
        output_file (file): The output file to write the generator properties.
    
    Returns:
        None
    """
    rs = db.GetPropertiesTable(collection_id, parent_name, None)
    rs.MoveFirst()

    if not rs is None and not rs.EOF:
        output_file.write('\n\nProperties of generator {}\n'.format(parent_name) + ','.join([x.Name for x in rs.Fields]) + '\n')
        while not rs.EOF:
            output_file.write(','.join([str(x.Value) for x in rs.Fields]) + '\n')
            rs.MoveNext()
    rs.Close()

def main():
    """
    Main function to execute the script.
    
    This function sets up the database connection, fetches and lists generators,
    queries and writes properties of a specific generator to an output file.
    
    Returns:
        None
    """
    # Define file paths
    input_file = 'rts_PLEXOS.xml'
    output_file_path = 'rts_PLEXOS.txt'

    # Change to input files directory if it exists
    if os.path.exists('Input Files'):
        os.chdir('Input Files')

    # Set up the database connection
    db = setup_database_connection(input_file)

    # Fetch required IDs
    classes = db.FetchAllClassIds()
    collections = db.FetchAllCollectionIds()

    # Open the output file
    with open(output_file_path, 'w') as output_file:
        # Fetch and list generators
        fetch_and_list_generators(db, classes["Generator"], output_file)
        
        # Query and write properties of a specific generator
        query_and_write_generator_properties(db, collections["SystemGenerators"], '101_1', output_file)

    # Close the database connection
    db.Close()

if __name__ == "__main__":
    main()
