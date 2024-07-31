# -*- coding: utf-8 -*-
"""
Retrieve data from the PLEXOS input dataset 
and modify it using the PLEXOS API.

Created on Sat Sep 09 19:19:57 2017

@author: Steven
"""

import os
import sys
import clr
from shutil import copyfile

def initialize_plexos_api():
    """
    Initialize the PLEXOS API by adding the necessary 
    references and setting up the path.

    To call the PLEXOS API from Python, some libraries
    are always needed. We use the clr library which 
    provides access to the Common Language Runtime (CLR)
    of the .NET Framework. 
    
    The .NET Framework is a software framework developed
    by Microsoft that runs primarily on Microsoft Windows.
    It includes a large class library called Framework
    Class Library (FCL) and provides language
    interoperability across several programming languages.
    
    The PLEXOS assemblies are loaded using the sys library
    and the clr library. The sys.path.append() method is
    used to add the path to the PLEXOS API to the list of
    paths that the Python interpreter will search for
    modules. The clr.AddReference() method is used to add
    references to the PLEXOS .NET assemblies. The PLEXOS
    .NET assemblies are the .NET libraries that contain the
    classes and methods needed to interact with PLEXOS.

    These series of sys and clr commands, as well as the
    imports, are essential to interact with the PLEXOS API.
    There is no other method to interact with the PLEXOS API.

    Returns:
        None
    """
    sys.path.append('C:/Program Files/Energy Exemplar/PLEXOS 10.0 API')
    clr.AddReference('PLEXOS_NET.Core')
    clr.AddReference('EEUTILITY')
    clr.AddReference('EnergyExemplar.PLEXOS.Utility')

# Initialize PLEXOS API
initialize_plexos_api()

# .NET related imports; all four of them are essential for interacting with the PLEXOS API
from PLEXOS_NET.Core import DatabaseCore
from EEUTILITY.Enums import *
from EnergyExemplar.PLEXOS.Utility.Enums import *
from System import DateTime

def copy_plexos_file(src, dest):
    """
    Copy the PLEXOS input file to a new location.

    Args:
        src (str): Source file path.
        dest (str): Destination file path.

    Returns:
        None
    """
    if os.path.exists(dest):
        os.remove(dest)
    copyfile(src, dest)

def add_category(db, class_id, category):
    """
    Add a category to a specified class in the PLEXOS model.

    Args:
        db (DatabaseCore): The PLEXOS database core object.
        class_id (int): The ID of the class to which the category will be added.
        category (str): The name of the category to be added.

    Returns:
        None
    """
    db.AddCategory(class_id, category)

def add_object(db, name, class_id, add_system_membership, category, description):
    """
    Add an object to the PLEXOS model.

    Args:
        db (DatabaseCore): The PLEXOS database core object.
        name (str): The name of the object to be added.
        class_id (int): The ID of the class to which the object belongs.
        add_system_membership (bool): Whether to add the object to the system membership.
        category (str): The category of the object.
        description (str): The description of the object.

    Returns:
        None
    """
    db.AddObject(name, class_id, add_system_membership, category, description)

def add_system_membership(db, collection_id, parent, child):
    """
    Add a membership between the system and an object in the PLEXOS model.

    Args:
        db (DatabaseCore): The PLEXOS database core object.
        collection_id (int): The ID of the collection to which the membership will be added.
        parent (str): The name of the parent object.
        child (str): The name of the child object.

    Returns:
        None
    """
    db.AddMembership(collection_id, parent, child)

def add_membership(db, collection_id, parent, child):
    """
    Add a membership between two objects in the PLEXOS model.

    Args:
        db (DatabaseCore): The PLEXOS database core object.
        collection_id (int): The ID of the collection to which the membership will be added.
        parent (str): The name of the parent object.
        child (str): The name of the child object.

    Returns:
        None
    """
    db.AddMembership(collection_id, parent, child)

def add_property(db, membership_id, enum_id, band_id, value, date_from, date_to, variable, data_file, pattern, scenario, action, period_type):
    """
    Add a property to an object in the PLEXOS model.

    Args:
        db (DatabaseCore): The PLEXOS database core object.
        membership_id (int): The ID of the membership to which the property will be added.
        enum_id (int): The ID of the property enum.
        band_id (int): The ID of the band.
        value (float): The value of the property.
        date_from (DateTime): The start date of the property.
        date_to (DateTime): The end date of the property.
        variable (object): The variable of the property.
        data_file (object): The data file of the property.
        pattern (object): The pattern of the property.
        scenario (object): The scenario of the property.
        action (object): The action of the property.
        period_type (PeriodEnum): The period type of the property.

    Returns:
        None
    """
    db.AddProperty(membership_id, enum_id, band_id, value, date_from, date_to, variable, data_file, pattern, scenario, action, period_type)

def create_plexos_model(input_file):
    """
    Create and modify a PLEXOS model by adding categories, objects, memberships, and properties.

    Args:
        input_file (str): Path to the PLEXOS input file.

    Returns:
        None
    """

    db = DatabaseCore()
    db.DisplayAlerts = False
    db.Connection(input_file)
    
    # Fetch class, collection, and property enums
    classes = db.FetchAllClassIds()
    collections = db.FetchAllCollectionIds()
    properties = db.FetchAllPropertyEnums()
    
    # Add categories
    add_category(db, classes["Generator"], 'API')
    add_category(db, classes["GasPipeline"], 'API')
    
    # Add objects and system memberships
    add_object(db, 'ApiGen', classes["Generator"], True, 'API', 'Testing the API')
    add_object(db, 'ApiPipe', classes["GasPipeline"], True, 'API', 'Testing the API')

    # Add memberships
    add_membership(db, collections["GeneratorNodes"], 'ApiGen', '101')    
    add_membership(db, collections["GeneratorFuels"], 'ApiGen', 'Coal/Steam')
    add_membership(db, collections["ReserveGenerators"], 'Spin Up', 'ApiGen')
    
    # Get the System.Generators membership ID for the new generator
    gen_mem_id = db.GetMembershipID(collections["SystemGenerators"], 'System', 'ApiGen')
    
    # Add properties for the new generator
    add_property(db, gen_mem_id, properties["SystemGenerators.Units"], 1, 0.0, None, None, None, None, None, None, 0, PeriodEnum.Interval)

    # Get the System.GasPipelines membership ID for the new pipeline
    pipe_mem_id = db.GetMembershipID(collections["SystemGasPipelines"], 'System', 'ApiPipe')
    
    # Add properties for the new pipeline
    add_property(db, pipe_mem_id, properties["SystemGasPipelines.IsAvailable"], 1, 1, DateTime(2024, 1, 1), None, None, None, None, None, 0, PeriodEnum.Interval)
    
    # Save the modified dataset
    db.Close()

def main():
    """
    Main function to execute the script.

    This is an example script to demonstrate 
    how to modify a PLEXOS model using the PLEXOS API.
    'Fundamental tasks' are also defined in the script,
    which can be used as a template for other scripts.

    Returns:
        None
    """
    folder = os.path.dirname(__file__)
    base_file = os.path.join(folder, 'rts_PLEXOS.xml')
    copied_file = os.path.join(folder, 'rts2.xml')
    
    if os.path.exists(base_file):
        copy_plexos_file(base_file, copied_file)
        create_plexos_model(copied_file)
        print(f"Model created and saved to {copied_file}")

if __name__ == "__main__":
    main()
