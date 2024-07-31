# -*- coding: utf-8 -*-
"""
Explore the DatabaseCore class

The PLEXOS API provides a class called DatabaseCore that
contains methods to interact with the PLEXOS database.
This script explores the methods of the DatabaseCore
class using the PLEXOS API and writes the details to a
text file.

Created on Sat Sep 09 20:11:21 2017
Updated on Tue Jul 30 09:30:16 2024 by Alejandro Elenes

@author: Steven
"""

import os
import sys
import clr

def initialize_plexos_api(version='9.0'):
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

    Args:
        version (str): The version of the PLEXOS API to initialize.

    Returns:
        None
    """
    api_path = f'C:/Program Files/Energy Exemplar/PLEXOS {version} API/'
    sys.path.append(api_path)
    clr.AddReference('PLEXOS_NET.Core')
    clr.AddReference('EEUTILITY')
    clr.AddReference('EnergyExemplar.PLEXOS.Utility')

def list_method(method):
    """
    List the details of a method from the DatabaseCore class.

    Args:
        method (MethodInfo): The method information object.

    Returns:
        str: A formatted string representing the method details.
    """
    text = '{} {}('.format(method.ReturnType.Name, method.Name)
    isFirst = True
    for param in method.GetParameters():
        if isFirst:
            isFirst = False
            text += '\n\t{} {}'.format(param.ParameterType.Name, param.Name)
        else:
            text += ',\n\t{} {}'.format(param.ParameterType.Name, param.Name)
        if param.HasDefaultValue:
            text += '[ = {}]'.format(param.DefaultValue)
    text += '\n\t)\n\n'
    return text

def explore_database_core_methods(output_file='DatabaseCoreMethods.txt'):
    """
    Explore the methods of the DatabaseCore class and write them to a file.

    Args:
        output_file (str): The path to the output text file.

    Returns:
        None
    """
    from PLEXOS_NET.Core import DatabaseCore
    with open(output_file, 'w') as fout:
        for method in clr.GetClrType(DatabaseCore).GetMethods():
            fout.write(list_method(method))

def main():
    """
    Main function to execute the script.

    This script explores the methods of the DatabaseCore
    class using the PLEXOS API and writes the details to a
    text file.

    Returns:
        None
    """
    initialize_plexos_api('9.0')
    explore_database_core_methods()

if __name__ == "__main__":
    main()
