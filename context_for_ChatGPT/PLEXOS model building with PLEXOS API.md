### Comprehensive Guide for Building, Modifying, and Running PLEXOS Models using the PLEXOS API in Python

#### Introduction

This document serves as a comprehensive guide to using the PLEXOS API to build, modify, and run PLEXOS models using Python. It encapsulates the knowledge gained from various Python scripts and provides a structured approach to handling PLEXOS models. This guide will cover the fundamental tasks, essential actions, and best practices for working with the PLEXOS API.

#### Fundamental Tasks and Building Blocks

##### Atoms (Basic Tasks)
1. **Connect to a Database**:
   - Establish a connection to a PLEXOS database using the `DatabaseCore` class.
   ```python
   def connect_to_database(file_path):
       db = DatabaseCore()
       db.DisplayAlerts = False
       db.Connection(file_path)
       return db
   ```

2. **Add Category**:
   - Add a new category to a specified class if it does not already exist.
   ```python
   def add_category_if_not_exists(db, class_name, category_name):
       classes = db.FetchAllClassIds()
       category_exists = db.CategoryExists(classes[class_name], category_name)
       if not category_exists:
           db.AddCategory(classes[class_name], category_name)
   ```

3. **Add Object**:
   - Add a new object to a specified class with optional category and description.
   ```python
   def add_object(db, name, class_name, add_system_membership=True, category=None, description=None):
       classes = db.FetchAllClassIds()
       db.AddObject(name, classes[class_name], add_system_membership, category, description)
   ```

4. **Add Membership**:
   - Establish a membership relationship between two objects.
   ```python
   def add_membership(db, collection_name, parent_name, child_name):
       collections = db.FetchAllCollectionIds()
       db.AddMembership(collections[collection_name], parent_name, child_name)
   ```

5. **Add Property**:
   - Add a property to a specified membership.
   ```python
   def add_property(db, membership_id, enum_id, band_id, value, date_from=None, date_to=None, variable=None, data_file=None, pattern=None, scenario=None, action=None, period_type=PeriodEnum.Interval):
       db.AddProperty(membership_id, enum_id, band_id, value, date_from, date_to, variable, data_file, pattern, scenario, action, period_type)
   ```

##### Molecules (Composite Tasks)
1. **Add Generator**:
   - Add a new generator with specified properties and memberships.
   ```python
   def add_generator(db, generator_name, generator_type, properties):
       add_category_if_not_exists(db, "Generator", generator_type.capitalize())
       add_object(db, generator_name, "Generator", True, generator_type.capitalize(), f'{generator_name} {generator_type.capitalize()} Generator')
       add_membership(db, "GeneratorNodes", generator_name, "101")
       add_membership(db, "GeneratorFuels", generator_name, properties['fuel'])
       add_membership(db, "ReserveGenerators", "Spin Up", generator_name)
       
       mem_id = db.GetMembershipID(db.FetchAllCollectionIds()["SystemGenerators"], 'System', generator_name)
       for prop, value in properties['properties'].items():
           add_property(db, mem_id, db.FetchAllPropertyEnums()[prop], 1, value)
   ```

#### Essential Actions for PLEXOS API

1. **Load PLEXOS Assemblies**:
   - Ensure the necessary PLEXOS assemblies are loaded.
   ```python
   plexos_path = 'C:/Program Files/Energy Exemplar/PLEXOS 10.0 API'
   sys.path.append(plexos_path)
   clr.AddReference('PLEXOS_NET.Core')
   clr.AddReference('EEUTILITY')
   clr.AddReference('EnergyExemplar.PLEXOS.Utility')
   ```

2. **Handle Database Connection**:
   - Properly manage opening and closing database connections.
   ```python
   def connect_to_database(file_path):
       db = DatabaseCore()
       db.DisplayAlerts = False
       db.Connection(file_path)
       return db
   
   def close_database(db):
       db.Close()
   ```

#### Best Practices

1. **Error Handling**:
   - Implement robust error handling to manage potential issues with database connections and property additions.
   ```python
   try:
       db.Connection(file_path)
   except Exception as e:
       print(f"Error connecting to database: {e}")
   ```

2. **Debugging**:
   - Use print statements to debug and verify the data being fetched and manipulated.
   ```python
   print(f"Classes fetched: {classes}")
   print(f"Collections fetched: {collections}")
   ```

3. **Documentation**:
   - Document each function with docstrings to explain its purpose, arguments, and return values.
   ```python
   def connect_to_database(file_path):
       """
       Connect to a PLEXOS database.
       
       Args:
           file_path (str): Path to the PLEXOS database file.
       
       Returns:
           DatabaseCore: Connected PLEXOS database object.
       """
       db = DatabaseCore()
       db.DisplayAlerts = False
       db.Connection(file_path)
       return db
   ```

4. **Modularity**:
   - Break down tasks into smaller, reusable functions to improve readability and maintainability.

#### Example Script

Here is the latest version of the script that successfully creates multiple PLEXOS XML files with different generator configurations.

```python
# -*- coding: utf-8 -*-
"""
Create multiple PLEXOS XML files with different generator configurations

This script creates multiple PLEXOS XML files with different generator configurations.
The script performs the following key functions:
- Connect to a PLEXOS dataset and update it.
- Loop over different generator configurations, creating a new XML file for each configuration.
- Add generator objects with different properties to the dataset.
- Save the updated dataset to a new XML file for each generator configuration.

P10 Tested

v0 - Created on 2024-07-31 at 11:20:00 by Alejandro Elenes
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
    file_path = 'C:/Users/alejandro.elenes/Documents/GitHub/Python-PLEXOS-API/new.xml'
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
```

### Summary of What Was Learned

1. **Connecting to PLEXOS Database**:
   - Learned how to connect to a PLEXOS database and handle the connection lifecycle.
   - Importance of closing the database connection to avoid memory leaks.

2. **Adding Categories, Objects, and Memberships**:
   - How to check if a category exists and add it if it doesn't.
   - Adding objects to a database and creating system memberships.
   - Adding memberships between objects.

3. **Adding Properties to Generators**:
   - Adding properties to objects and handling potential issues like missing properties or unsupported property types.
   - Importance of critical properties like 'Units' for generators.

4. **Generating Multiple PLEXOS XML Files**:
   - Looping through different generator configurations and creating a new XML file for each configuration.
   - Ensuring the generated files are correctly modified and saved.

5. **Debugging and Error Handling**:
   - Importance of debugging print statements to verify the fetched data.
   - Implementing error handling to manage issues like missing classes or properties.

This comprehensive guide and the script provide a solid foundation for building, modifying, and running PLEXOS models using the PLEXOS API in Python. It ensures that the process is repeatable, maintainable, and understandable for both humans and an LLM being fine-tuned to work with PLEXOS API.