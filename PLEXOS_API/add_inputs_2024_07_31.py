# -*- coding: utf-8 -*-
"""
Retrieve data from the PLEXOS input dataset

This Python script automates the retrieval and 
modification of data from a PLEXOS input dataset,
leveraging the PLEXOS API. The script performs
several key functions:
- Database Setup: It establishes a connection to a
    PLEXOS dataset by copying an existing PLEXOS input
    XML file (rts_PLEXOS.xml) to a new file (rts2.xml).
    This step ensures that any modifications are made
    on a duplicate file, preserving the original data.
- Class and Collection Fetching: It retrieves all 
    class and collection IDs from the PLEXOS dataset.
    These IDs are used to identify the classes and
    collections to which new objects and properties
    will be added.
- Category Creation: It adds new categories ('API') to
    the 'Generator' and 'GasPipeline' classes. Categories
    help in organizing and grouping objects.
- Object Creation: It creates new objects ('ApiGen' and
    'ApiPipe') in the 'Generator' and 'GasPipeline'
    classes, respectively. These objects are also
    assigned to the 'API' category and provided with
    descriptions.
- Membership Creation: It establishes relationships
    (memberships) between the newly created objects and
    existing collections. For example, the script
    associates the 'ApiGen' object with specific
    generator nodes, fuels, and reserve generators.
- Property Addition: It adds properties to the newly
    created objects. For instance, it sets the 'Units'
    property for the 'ApiGen' generators, and the
    'IsAvailable' property for the 'ApiPipe' gas
    pipeline. These properties define the behavior and
    characteristics of the objects in the PLEXOS model.
- Error Handling: The script includes error handling
    to ensure that the PLEXOS input file is available
    before proceeding. It also handles the deletion of
    the copied file if it already exists, ensuring a
    clean slate for each run.
- Modularity and Maintainability: The script is organized
    into functions that encapsulate specific tasks
    (e.g., database setup, category creation). This
    modular approach enhances code readability,
    maintainability, and reusability of the code.

Practical Use Cases
-------------------
1. Model Testing: The script and/or its functions are
    particularly useful for users who need to test
    different configurations and modifications within
    a PLEXOS model without altering the original dataset.
2. Automation: By automating the process of adding new
    objects, categories, and properties, the script
    saves time and reduces the potential for human error
    compared to manual data entry.
3. Learning and Development: Users new to the PLEXOS API
    can use this script as a learning tool to interact
    with and manipulate PLEXOS datasets programmatically.
4. Batch Processing: For scenarios requiring repetitive
    modifications to multiple datasets, the script can
    be integrated into larger automation workflows to
    streamlining the process.

Created on Sat Sep 09 19:19:57 2017
Updated on Tue Jul 30 11:47:32 2024 by Alejandro Elenes

@author: Steven
"""

import os
import sys
from shutil import copyfile
import clr

# Load PLEXOS assemblies
sys.path.append('C:/Program Files/Energy Exemplar/PLEXOS 10.0 API')
clr.AddReference('PLEXOS_NET.Core')
clr.AddReference('EEUTILITY')
clr.AddReference('EnergyExemplar.PLEXOS.Utility')

# .NET related imports
from PLEXOS_NET.Core import DatabaseCore
from EEUTILITY.Enums import ClassEnum, CollectionEnum, PeriodEnum
from EnergyExemplar.PLEXOS.Utility.Enums import PropertyEnum
from System import DateTime

def setup_database_connection(basefile_path, copiedfile_path):
    """
    Set up the database connection by copying the base file to a new location.
    Deletes the copied file if it already exists.
    
    Args:
        basefile_path (str): Path to the base PLEXOS input file.
        copiedfile_path (str): Path to the copied PLEXOS input file.
    
    Returns:
        DatabaseCore: An instance of the DatabaseCore class with an open connection.
    """
    if os.path.exists(basefile_path):
        if os.path.exists(copiedfile_path):
            os.remove(copiedfile_path)
        copyfile(basefile_path, copiedfile_path)

        db = DatabaseCore()
        db.DisplayAlerts = False
        db.Connection(copiedfile_path)
        return db
    else:
        raise FileNotFoundError(f"Base file not found at {basefile_path}")

def add_categories(db, class_ids):
    """
    Add categories to the PLEXOS database.
    
    Args:
        db (DatabaseCore): The database connection object.
        class_ids (dict): Dictionary of class IDs.
    """
    db.AddCategory(class_ids["Generator"], 'API')
    db.AddCategory(class_ids["GasPipeline"], 'API')

def add_objects(db, class_ids):
    """
    Add objects to the PLEXOS database and assign them to a category.
    
    Args:
        db (DatabaseCore): The database connection object.
        class_ids (dict): Dictionary of class IDs.
    """
    db.AddObject('ApiGen', class_ids["Generator"], True, 'API', 'Testing the API')
    db.AddObject('ApiPipe', class_ids["GasPipeline"], True, 'API', 'Testing the API')

def add_memberships(db, collection_ids):
    """
    Add memberships between objects in the PLEXOS database.
    
    Args:
        db (DatabaseCore): The database connection object.
        collection_ids (dict): Dictionary of collection IDs.
    """
    db.AddMembership(collection_ids["GeneratorNodes"], 'ApiGen', '101')
    db.AddMembership(collection_ids["GeneratorFuels"], 'ApiGen', 'Coal/Steam')
    db.AddMembership(collection_ids["ReserveGenerators"], 'Spin Up', 'ApiGen')

def add_properties(db, collection_ids, property_ids):
    """
    Add properties to memberships in the PLEXOS database.
    
    Args:
        db (DatabaseCore): The database connection object.
        collection_ids (dict): Dictionary of collection IDs.
        property_ids (dict): Dictionary of property IDs.
    """
    # Get the System.Generators membership ID for the new generator
    generator_mem_id = db.GetMembershipID(collection_ids["SystemGenerators"], 'System', 'ApiGen')

    # Add units for the new generator
    db.AddProperty(
        generator_mem_id, 
        property_ids["SystemGenerators.Units"],
        1, 
        0.0, 
        None, 
        None, 
        None, 
        None, 
        None, 
        None, 
        0, 
        PeriodEnum.Interval
    )

    # Get the System.GasPipelines membership ID for the new pipeline
    pipeline_mem_id = db.GetMembershipID(collection_ids["SystemGasPipelines"], 'System', 'ApiPipe')

    # Add IsAvailable for the new pipeline
    db.AddProperty(
        pipeline_mem_id,
        property_ids["SystemGasPipelines.IsAvailable"], 
        1, 
        1, 
        DateTime(2024, 1, 1),
        None, 
        None, 
        None, 
        None, 
        None, 
        0, 
        PeriodEnum.Interval
    )

def main():
    # Define file paths
    folder = os.path.dirname(__file__)
    basefile_path = os.path.join(folder, 'rts_PLEXOS.xml')
    copiedfile_path = os.path.join(folder, 'rts2.xml')

    # Set up the database connection
    db = setup_database_connection(basefile_path, copiedfile_path)

    # Fetch required IDs
    class_ids = db.FetchAllClassIds()
    collection_ids = db.FetchAllCollectionIds()
    property_ids = db.FetchAllPropertyEnums()

    # Add categories, objects, memberships, and properties
    add_categories(db, class_ids)
    add_objects(db, class_ids)
    add_memberships(db, collection_ids)
    add_properties(db, collection_ids, property_ids)

    # Close the database connection
    db.Close()

if __name__ == "__main__":
    main()
