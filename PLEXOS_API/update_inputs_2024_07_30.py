# -*- coding: utf-8 -*-
"""
Create scenarios and add data overlays to a PLEXOS input dataset

Created on Tue Dec 18 07:12:40 2018
Updated on [Today's Date] by [Your Name]

This script automates the process of creating scenarios and adding data overlays in a PLEXOS input dataset using the PLEXOS API.
The script performs several key functions:
- Database Setup: Establishes a connection to a PLEXOS dataset.
- Scenario and Data Overlay: Adds scenarios and data overlays to the dataset.
- Data File Handling: Creates and attaches data files to objects within the PLEXOS dataset.

Practical Use Cases
-------------------
1. Model Testing: Useful for testing different data overlays within a PLEXOS model.
2. Automation: Automates the process of updating datasets and attaching data files, saving time and reducing potential errors.
3. Learning and Development: Serves as a learning tool for users new to the PLEXOS API.
4. Reporting: Can be integrated into larger workflows for generating and analyzing reports from PLEXOS models.

Example Usage
-------------
To run the script and create scenarios and data overlays, ensure the required PLEXOS API assemblies are available and execute the script in your Python environment.

Updated by [Your Name] to incorporate best practices and enhancements.

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

def create_datafile_object(plexosfile, datafilename, datafilepath, copyfileto=''):
    """
    Create a data file object in the PLEXOS dataset.
    
    Args:
        plexosfile (str): Path to the PLEXOS input file.
        datafilename (str): Name of the data file object.
        datafilepath (str): Path to the data file.
        copyfileto (str, optional): Path to copy the PLEXOS input file.
    
    Returns:
        str: Path to the PLEXOS input file (original or copied).
    """
    if not os.path.exists(plexosfile):
        raise FileNotFoundError(f'"{plexosfile}" does not exist')
        
    if copyfileto:
        copy_plexos_file(plexosfile, copyfileto)
        plexosfile = copyfileto
    
    db = setup_database_connection(plexosfile)
    classes = db.FetchAllClassIds()
    collections = db.FetchAllCollectionIds()
    properties = db.FetchAllPropertyEnums()
    
    db.AddObject(datafilename, classes["DataFile"], True)
    
    mem_id = db.GetMembershipID(collections["SystemDataFiles"], 'System', datafilename)
    enum_id = int(properties["SystemDataFiles.Filename"])
    
    params = [(mem_id, enum_id, 1, 0, None, None, None, datafilepath, None, None, None, PeriodEnum.Interval)]
    for p in params:
        db.AddProperty(*p)
    
    db.Close()
    return plexosfile

def attach_datafile_to_object(plexosfile, datafilename, collectionenum, propertyenum, objectname, parentname='System'):
    """
    Attach a data file to an object in the PLEXOS dataset.
    
    Args:
        plexosfile (str): Path to the PLEXOS input file.
        datafilename (str): Name of the data file to attach.
        collectionenum (str): Collection enum for the object.
        propertyenum (str): Property enum for the object.
        objectname (str): Name of the object to attach the data file to.
        parentname (str, optional): Parent name of the object.
    
    Returns:
        None
    """
    if not os.path.exists(plexosfile):
        raise FileNotFoundError(f'"{plexosfile}" does not exist')
        
    db = setup_database_connection(plexosfile)
    collections = db.FetchAllCollectionIds()
    properties = db.FetchAllPropertyEnums()
    
    res = db.GetPropertiesTable(collections[collectionenum], parentname, objectname)
    mem_id = db.GetMembershipID(collections[collectionenum], parentname, objectname)
    enum_id = properties[propertyenum]

    while not res.EOF:
        fields = {res.Fields[i].Name.replace('_x0020_', ''): res.Fields[i].Value for i in range(res.Fields.Count)}
        if fields['Property'] == str(propertyenum):
            db.RemoveProperty(
                mem_id, enum_id,
                1 if 'Band' not in fields else int(fields['Band']),
                None if 'DateFrom' not in fields else fields['DateFrom'],
                None if 'DateTo' not in fields else fields['DateTo'],
                None if 'Variable' not in fields else fields['Variable'],
                None if 'DataFile' not in fields else fields['DataFile'],
                None if 'Pattern' not in fields else fields['Pattern'],
                None if 'Scenario' not in fields else fields['Scenario'],
                '=' if 'Action' not in fields else fields['Action'],
                PeriodEnum.Interval
            )
        res.MoveNext()
    
    params = [(mem_id, enum_id, 1, 0, None, None, None, datafilename, None, None, None, PeriodEnum.Interval)]
    for p in params:
        db.AddProperty(*p)
    
    db.Close()

def update_load_csv_file(csv_file, start_date, data, minutes_per_interval=60):
    """
    Update the load CSV file with new data.
    
    Args:
        csv_file (str): Path to the CSV file.
        start_date (datetime): Start date for the data.
        data (list): List of data values to write to the CSV file.
        minutes_per_interval (int, optional): Number of minutes per interval.
    
    Returns:
        None
    """
    row_length = int(24 * 60 / minutes_per_interval)
    rows = (len(data) - 1) // row_length + 1
    with open(csv_file, 'w') as fout:
        fout.write('Year,Month,Day,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24\n')
        for i in range(rows):
            fout.write(f'{start_date.year},{start_date.month},{start_date.day},')
            fout.write(f'{",".join([str(val) for val in data[i * row_length:(i + 1) * row_length]])}\n')

def main():
    """
    Main function to execute the script.
    
    This function creates a data file object, attaches the data file to an object,
    and updates the load CSV file with new data.
    
    Returns:
        None
    """
    plexosfile = create_datafile_object('test.xml', 'Load File', r'CSV Files\load.csv', 'test2.xml')
    attach_datafile_to_object(plexosfile, 'Load File', "SystemRegions", "SystemRegions.Load", 'B')
    from random import random
    update_load_csv_file(r'CSV Files\load.csv', datetime.today(), [80 + int(40 * random()) for _ in range(168)])

if __name__ == '__main__':
    main()
