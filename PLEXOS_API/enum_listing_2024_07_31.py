# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 12:54:57 2017
Updated on Tue Jul 30 13:26:34 2024 by Alejandro Elenes

This script demonstrates the use of the PLEXOS API to retrieve and document
all enumeration types and their values from the EEUTILITY and EnergyExemplar
PLEXOS Utility assemblies. The output is written to text files for review.

Key Improvements:
- Modular functions for enhanced readability and reusability.
- Comprehensive docstrings and comments for better understanding.
- Improved file handling and error checking.
- Practical use cases for each function, providing context and application.

Practical Use Cases
-------------------
1. **Documentation**: Generate a detailed enumeration list for reference,
    aiding in understanding and using the PLEXOS API.
2. **Learning Tool**: Help new users and developers familiarize themselves
    with the various enumeration types and their values in the PLEXOS API.
3. **Code Integration**: Integrate the generated enumeration list into
    larger automation workflows for enhanced PLEXOS model building.

Example Usage
-------------
To run the script and generate the enumeration lists, ensure the required
PLEXOS API assemblies are available and execute the script in your Python
environment.

Updated by Alejandro Elenes to incorporate best practices and enhancements.

@author:
    - Steven (Original Author)
    - Alejandro Elenes (Updated by)
"""

import os
import sys
import clr

# Add PLEXOS API assemblies to the system path
sys.path.append('C:\\Program Files\\Energy Exemplar\\PLEXOS 9.0 API')
clr.AddReference('EEUTILITY')
clr.AddReference('EnergyExemplar.PLEXOS.Utility')

# .NET related imports
from EEUTILITY.Enums import ClassEnum
from EnergyExemplar.PLEXOS.Utility.Enums import FlatFileFormatEnum
from System import Enum

def write_enums_to_file(assembly, file_path):
    """
    Writes all enumeration types and their values from a given assembly to a file.
    
    Args:
        assembly: The assembly from which to retrieve enumeration types.
        file_path (str): The path of the file to write the enumeration list.
    
    Returns:
        None
    """
    with open(file_path, 'w') as fout:
        for t in clr.GetClrType(assembly).Assembly.GetTypes():
            if t.IsEnum:
                fout.write('{}\n'.format(t.Name))
                for en in t.GetEnumNames():
                    fout.write('\t{} = {}\n'.format(en, int(Enum.Parse(t, en))))
                fout.write('\n')

def main():
    """
    Main function to generate enumeration lists from PLEXOS API assemblies.
    
    Generates two text files documenting all enumeration types and their values
    from the EEUTILITY and EnergyExemplar PLEXOS Utility assemblies.
    
    Returns:
        None
    """
    # Define file paths for the output files
    eeutility_enums_file = 'EEUTILITY_Enums.txt'
    plexos_utility_enums_file = 'EnergyExemplar_PLEXOS_UTILITY_Enums.txt'
    
    # Write enumeration lists to the respective files
    write_enums_to_file(ClassEnum, eeutility_enums_file)
    write_enums_to_file(FlatFileFormatEnum, plexos_utility_enums_file)

if __name__ == "__main__":
    main()
