# -*- coding: utf-8 -*-
"""
Create multiple PLEXOS XML files with different generator configurations

This script creates multiple PLEXOS XML files with different generator configurations.
The script performs the following key functions:
- Connect to a PLEXOS dataset and update it.
- Loop over different generator configurations, creating a new XML file for each configuration.
- Add generator objects with different properties to the dataset.
- Save the updated dataset to a new XML file for each generator configuration.

This script was developed to generate multiple PLEXOS XML files with different generator configurations for a hackathon challenge.
It is partially successful as it creates the XML files with the specified generator configurations but does not handle the case where adding properties fails.

P10 Tested

v0 - Created on 2024-07-31 at 11:20:00 by Alejandro Elenes
what it does well:
- create an XML per generator category requested
what it does not so well:
- check if properties are enabled, if not, it will fail to add them
- critical properties are not added to the generator objects (e.g., 'Units')
- check if the fuel category exists before adding a new fuel

this is expected, as this is PLEXOS model-building specific knowledge
and that can only come with 'experience' with the PLEXOS API
i.e., we need to train the model builder to know what properties are critical,
to check if they are enabled, teach it how to enable them, etc.

but this is a good start, even if incomplete, as the XML files were created
and the enabled properties were successfully added to the generator objects
this is good enough for the Hackathon demo

"""

import os
import sys
import clr
from datetime import datetime
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

def connect_to_database(file_path):
    db = DatabaseCore()
    db.DisplayAlerts = False
    db.Connection(file_path)
    return db

def close_database(db):
    db.Close()

def add_category_if_not_exists(db, class_name, category_name):
    classes = db.FetchAllClassIds()
    category_exists = db.CategoryExists(classes[class_name], category_name)
    if not category_exists:
        db.AddCategory(classes[class_name], category_name)

def add_object(db, name, class_name, add_system_membership=True, category=None, description=None):
    classes = db.FetchAllClassIds()
    db.AddObject(name, classes[class_name], add_system_membership, category, description)

def add_membership(db, collection_name, parent_name, child_name):
    collections = db.FetchAllCollectionIds()
    db.AddMembership(collections[collection_name], parent_name, child_name)

def add_property(db, membership_id, enum_id, band_id, value, date_from=None, date_to=None, variable=None, data_file=None, pattern=None, scenario=None, action=None, period_type=PeriodEnum.Interval):
    db.AddProperty(membership_id, enum_id, band_id, value, date_from, date_to, variable, data_file, pattern, scenario, action, period_type)

def add_generator(db, generator_name, generator_type, properties):
    add_category_if_not_exists(db, "Generator", generator_type.capitalize())
    add_object(db, generator_name, "Generator", True, generator_type.capitalize(), f'{generator_name} {generator_type.capitalize()} Generator')
    add_membership(db, "GeneratorNodes", generator_name, "101")
    add_membership(db, "GeneratorFuels", generator_name, properties['fuel'])
    add_membership(db, "ReserveGenerators", "Spin Up", generator_name)
    
    mem_id = db.GetMembershipID(db.FetchAllCollectionIds()["SystemGenerators"], 'System', generator_name)
    for prop, value in properties['properties'].items():
        add_property(db, mem_id, db.FetchAllPropertyEnums()[prop], 1, value)

def main():
    file_path = r"C:\Users\alejandro.elenes\Documents\GitHub\Python-PLEXOS-API\blank_PLEXOS_model_for_GPT.xml"
    generator_properties = {
        'nuclear': {
            'fuel': 'Uranium',
            'properties': {
                'SystemGenerators.MaxCapacity': 1000.0,
                'SystemGenerators.MinStableLevel': 900.0,
                'SystemGenerators.HeatRate': 10.0,
                'SystemGenerators.StartCost': 500000.0,
                'SystemGenerators.MinUpTime': 48.0,
                'SystemGenerators.MinDownTime': 24.0,
            }
        },
        'gas': {
            'fuel': 'Natural Gas',
            'properties': {
                'SystemGenerators.MaxCapacity': 500.0,
                'SystemGenerators.MinStableLevel': 100.0,
                'SystemGenerators.HeatRate': 8.0,
                'SystemGenerators.StartCost': 100000.0,
                'SystemGenerators.MinUpTime': 4.0,
                'SystemGenerators.MinDownTime': 2.0,
            }
        },
        'coal': {
            'fuel': 'Coal',
            'properties': {
                'SystemGenerators.MaxCapacity': 800.0,
                'SystemGenerators.MinStableLevel': 200.0,
                'SystemGenerators.HeatRate': 11.0,
                'SystemGenerators.StartCost': 300000.0,
                'SystemGenerators.MinUpTime': 12.0,
                'SystemGenerators.MinDownTime': 8.0,
            }
        },
        'solar': {
            'fuel': 'None',
            'properties': {
                'SystemGenerators.MaxCapacity': 50.0,
                'SystemGenerators.MinStableLevel': 0.0,
                'SystemGenerators.HeatRate': 0.0,
                'SystemGenerators.StartCost': 0.0,
                'SystemGenerators.MinUpTime': 0.0,
                'SystemGenerators.MinDownTime': 0.0,
            }
        },
        'wind': {
            'fuel': 'None',
            'properties': {
                'SystemGenerators.MaxCapacity': 100.0,
                'SystemGenerators.MinStableLevel': 0.0,
                'SystemGenerators.HeatRate': 0.0,
                'SystemGenerators.StartCost': 0.0,
                'SystemGenerators.MinUpTime': 0.0,
                'SystemGenerators.MinDownTime': 0.0,
            }
        },
        'oil': {
            'fuel': 'Oil',
            'properties': {
                'SystemGenerators.MaxCapacity': 600.0,
                'SystemGenerators.MinStableLevel': 100.0,
                'SystemGenerators.HeatRate': 9.0,
                'SystemGenerators.StartCost': 200000.0,
                'SystemGenerators.MinUpTime': 6.0,
                'SystemGenerators.MinDownTime': 4.0,
            }
        },
        'geothermal': {
            'fuel': 'Geothermal',
            'properties': {
                'SystemGenerators.MaxCapacity': 70.0,
                'SystemGenerators.MinStableLevel': 50.0,
                'SystemGenerators.HeatRate': 0.0,
                'SystemGenerators.StartCost': 100000.0,
                'SystemGenerators.MinUpTime': 10.0,
                'SystemGenerators.MinDownTime': 5.0,
            }
        }
    }

    for gen_type, properties in generator_properties.items():
        modified_file_path = f'{file_path[:-4]}_{gen_type}.xml'
        copyfile(file_path, modified_file_path)
        db = connect_to_database(modified_file_path)
        add_generator(db, f'API_{gen_type.capitalize()}Gen', gen_type, properties)
        close_database(db)

if __name__ == '__main__':
    main()