# -*- coding: utf-8 -*-
"""
Retrieve and process report properties from a PLEXOS input dataset

This script automates the retrieval and processing of report properties from a PLEXOS input dataset using the PLEXOS API. 
The script performs several key functions:
- Database Setup: Establishes a connection to a PLEXOS dataset.
- Data Retrieval: Fetches and processes report properties for a given model.
- Data Transformation: Converts the retrieved data into a Pandas DataFrame and saves it as a CSV file.

Differences from other scripts:
- Focus on Reporting: Unlike the other scripts, which primarily focus on creating scenarios, updating attributes, or manipulating objects within the PLEXOS model, this script specifically focuses on extracting and processing report properties. It is tailored towards generating reports and analyzing specific aspects of the PLEXOS dataset.
- Use of pandas: This script integrates the Pandas library for data manipulation and transformation. Pandas is used to create DataFrames, filter data, and save the processed data into a CSV file. This is a key difference as the other scripts did not involve such extensive data transformation using Pandas.
- Data conversion: The script includes a function (recordset_to_list) to convert PLEXOS recordsets into lists of rows. This is necessary to transform the data into a format that can be easily processed by Pandas, highlighting a different aspect of data handling compared to other scripts.
- Output generation: The script generates a CSV file as its final output, which is intended for further analysis or reporting. Other scripts focused more on modifying the PLEXOS model or its attributes and did not generate standalone output files for reporting purposes.

Practical Use Cases
-------------------
1. Data Analysis: Useful for analyzing and extracting specific report properties from a PLEXOS model.
2. Automation: Automates the process of data retrieval and transformation, saving time and reducing potential errors compared to manual data extraction.
3. Learning and Development: Serves as a learning tool for users new to the PLEXOS API.
4. Reporting: Can be integrated into larger workflows for generating reports from PLEXOS datasets.

Example Usage
-------------
To run the script and retrieve report properties from a PLEXOS input dataset, ensure the required PLEXOS API assemblies are available and execute the script in your Python environment.

Updated by [Your Name] to incorporate best practices and enhancements.

P9 Tested

TODO: P9 Failed

"""

import os
import sys
import clr
import pandas as pd

# Load PLEXOS assemblies
sys.path.append('C:/Program Files/Energy Exemplar/PLEXOS 10.0 API')
clr.AddReference('PLEXOS_NET.Core')
clr.AddReference('EEUTILITY')
clr.AddReference('EnergyExemplar.PLEXOS.Utility')

# .NET related imports
from PLEXOS_NET.Core import DatabaseCore
from EnergyExemplar.PLEXOS.Utility.Enums import *
from EEUTILITY.Enums import *

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

def recordset_to_list(rs):
    """
    Convert a PLEXOS recordset to a list of rows.
    
    Args:
        rs (Recordset): The PLEXOS recordset object.
    
    Returns:
        list: A list of rows, where each row is a list of field values.
    """
    result = []
    while not rs.EOF:
        row = [rs[f.Name] for f in rs.Fields]
        result.append(row)
        rs.MoveNext()
    return result

def get_report_properties(model_name):
    """
    Retrieve and process report properties for a given model in the PLEXOS dataset.
    
    Args:
        model_name (str): The name of the model.
    
    Returns:
        DataFrame: A Pandas DataFrame containing the processed report properties.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'rts_PLEXOS.xml')
    db = setup_database_connection(file_path)

    classes = db.FetchAllClassIds()
    collections = db.FetchAllCollectionIds()

    report_names = db.GetChildMembers(collections["ModelReport"], model_name)
    report_ids = [db.ObjectName2Id(classes["Report"], name) for name in report_names]

    rs, _ = db.GetData('t_report', [])
    report_data = recordset_to_list(rs)
    report_df = pd.DataFrame(report_data, columns=[f.Name for f in rs.Fields])
    rs.Close()

    report_df['filtered_report'] = report_df['object_id'].apply(lambda x: x in report_ids)
    report_df = report_df[report_df['filtered_report']]

    rs, _ = db.GetData('t_property_report', [])
    report_prop_data = recordset_to_list(rs)
    report_prop_df = pd.DataFrame(report_prop_data, columns=[f.Name for f in rs.Fields])
    rs.Close()

    report_prop_df = report_prop_df.set_index('property_id')
    df = report_df.join(report_prop_df, on='property_id', rsuffix='_prop')
    
    db.Close()
    return df

def main():
    """
    Main function to execute the script.
    
    This function retrieves and processes report properties for a given model and saves the result as a CSV file.
    
    Returns:
        None
    """
    report_properties_df = get_report_properties('Q3 DA')
    output_file_path = os.path.join(os.path.dirname(__file__), 'q3dareport.csv')
    report_properties_df.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    main()
