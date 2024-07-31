Prompt:

I attached the enhanced version of the "DatabaseCoreMethods.txt" file produced by one of the PLEXOS scripts. Based on the PLEXOS API functions used in all the python scripts you've helped improve so far, and contrasting with the methods described in the "DatabaseCoreMethods.txt"; can you identify which python function is linked to which method in the text file?

Response:

To identify which Python function is linked to which method in the `DatabaseCoreMethods.txt` file, we'll match the method signatures and descriptions from the text file with the corresponding function calls in the Python scripts. Here is the analysis:

### Python Functions and Corresponding `DatabaseCore` Methods

1. **`db.Connection(file_path)`**
   - **Method:** `Void Connection(String strFile)`
   - **Description:** Establishes a connection to the specified database file.

2. **`db.Close()`**
   - **Method:** `Void Close()`
   - **Description:** Closes the current database connection.

3. **`db.FetchAllClassIds()`**
   - **Method:** Not explicitly listed in the provided methods, but typically part of the DatabaseCore API for fetching class IDs.
   - **Description:** Fetches all class IDs from the database.

4. **`db.FetchAllCollectionIds()`**
   - **Method:** Not explicitly listed in the provided methods, but typically part of the DatabaseCore API for fetching collection IDs.
   - **Description:** Fetches all collection IDs from the database.

5. **`db.FetchAllPropertyEnums()`**
   - **Method:** Not explicitly listed in the provided methods, but typically part of the DatabaseCore API for fetching property enums.
   - **Description:** Fetches all property enums from the database.

6. **`db.FetchAllAttributeEnums()`**
   - **Method:** Not explicitly listed in the provided methods, but typically part of the DatabaseCore API for fetching attribute enums.
   - **Description:** Fetches all attribute enums from the database.

7. **`db.GetChildMembers(collections["ModelHorizon"], modelname)`**
   - **Method:** `String[] GetChildMembers(CollectionEnum nCollectionId, String strParent)`
   - **Description:** Retrieves child members for a parent object.

8. **`db.GetParentMembers(collections["SystemRegions"], 'System')`**
   - **Method:** `String[] GetParentMembers(CollectionEnum nCollectionId, String strChild)`
   - **Description:** Retrieves parent members for a child object.

9. **`db.AddObject('ApiGen', classes["Generator"], True, 'API', 'Testing the API')`**
   - **Method:** `Int32 AddObject(String strName, ClassEnum nClassId, Boolean bAddSystemMembership, String strCategory = None, String strDescription = None)`
   - **Description:** Adds a new object to the specified class.

10. **`db.RemoveObject('Q1 DA', classes["Model"])`**
    - **Method:** `Int32 RemoveObject(String strName, ClassEnum nClassId)`
    - **Description:** Removes an object from the specified class.

11. **`db.UpdateObjectDescription(classes["Horizon"], hor, 'New Description')`**
    - **Method:** `Int32 UpdateObjectDescription(ClassEnum nClassId, String strObjectName, String strNewDescription)`
    - **Description:** Updates the description of an object.

12. **`db.AddCategory(classes["Generator"], 'API')`**
    - **Method:** `Int32 AddCategory(ClassEnum nClassId, String strCategory)`
    - **Description:** Adds a new category to the specified class.

13. **`db.RemoveCategory(classes["Generator"], 'API', True)`**
    - **Method:** `Int32 RemoveCategory(ClassEnum nClassId, String strCategory, Boolean bRemoveObjects = True)`
    - **Description:** Removes a category and optionally its objects.

14. **`db.AddMembership(collections["GeneratorNodes"], 'ApiGen', '101')`**
    - **Method:** `Int32 AddMembership(CollectionEnum nCollectionId, String strParent, String strChild)`
    - **Description:** Adds a membership between parent and child objects.

15. **`db.RemoveMembership(collections["ModelHorizon"], 'Q1 DA', 'APIHorizon')`**
    - **Method:** `Int32 RemoveMembership(CollectionEnum nCollectionId, String strParent, String strChild)`
    - **Description:** Removes a membership between parent and child objects.

16. **`db.GetMembershipID(collections["SystemGenerators"], 'System', 'ApiGen')`**
    - **Method:** `Int32 GetMembershipID(CollectionEnum nCollectionId, String strParent, String strChild)`
    - **Description:** Gets the ID of a membership.

17. **`db.AddAttribute(classes["Horizon"], 'APIHorizon', attributes["Horizon.DateFrom"], DateTime(2024,1,1).ToOADate())`**
    - **Method:** `Int32 AddAttribute(ClassEnum nClassId, String strObjectName, Int32 nAttributeEnum, Double dValue)`
    - **Description:** Adds an attribute to an object.

18. **`db.RemoveAttribute(classes["Horizon"], 'APIHorizon', attributes["Horizon.DateFrom"])`**
    - **Method:** `Int32 RemoveAttribute(ClassEnum nClassId, String strObjectName, Int32 nAttributeEnum)`
    - **Description:** Removes an attribute from an object.

19. **`db.UpdateAttribute(classes["Horizon"], hor, int(attributes["Horizon.DateFrom"]), DateTime(start.Year, 1, 1).ToOADate())`**
    - **Method:** `Boolean UpdateAttribute(ClassEnum nClassId, String strObjectName, Int32 nAttributeEnum, Double dNewValue)`
    - **Description:** Updates the value of an attribute.

20. **`db.AddProperty(mem_id, properties["SystemGenerators.Units"], 1, 0.0, None, None, None, None, None, None, 0, PeriodEnum.Interval)`**
    - **Method:** `Int32 AddProperty(Int32 MembershipId, Int32 EnumId, Int32 BandId, Double Value, Object DateFrom, Object DateTo, Object Variable, Object DataFile, Object Pattern, Object Scenario, Object Action, PeriodEnum PeriodTypeId)`
    - **Description:** Adds a property to a membership.

21. **`db.RemoveProperty(mem_id, enum_id, 1, None, None, None, None, None, None, '=', PeriodEnum.Interval)`**
    - **Method:** `Int32 RemoveProperty(Int32 MembershipId, Int32 EnumId, Int32 BandId, Object DateFrom, Object DateTo, Object Variable, Object DataFile, Object Pattern, Object Scenario, Object Action, PeriodEnum PeriodTypeId)`
    - **Description:** Removes a property from a membership.

22. **`db.GetPropertiesTable(collections["SystemGenerators"], '', '101_1')`**
    - **Method:** `Recordset GetPropertiesTable(CollectionEnum CollectionId, String ParentNameList = None, String ChildNameList = None, String TimesliceList = None, String ScenarioList = None, String CategoryList = None)`
    - **Description:** Retrieves a table of properties.

23. **`db.GetData('t_report',[])`**
    - **Method:** `Recordset GetData(String TableName, String[]& strFields)`
    - **Description:** Retrieves data from the specified table and fields.

### Summary

The enhanced `DatabaseCoreMethods.txt` file and the improved Python scripts help in mapping the API methods to their corresponding functions. This structured and documented approach enhances the usability of the code and makes it more intuitive for an LLM to learn and generate accurate code for building toy PLEXOS models.


Prompt:

for the functions that we do have python code examples for: does the way those methods are described in the text file, show with precision the way they are called in python scripts i.e., without previous knowledge about how these methods are used in a python script, would I be able to write python code to use these methods just by looking at their description in the text file? 

if not; is there a pattern implied in how these methods are described in the text file, and how they are actually used in a python script, that you can extrapolate to figure out how the rest of the methods described in the text file would be used in an actual python script? 

Response:

### Analysis of Method Descriptions and Usage

1. **Method Descriptions:**
   - The descriptions in the `DatabaseCoreMethods.txt` file are concise and list the method signatures, including parameter types and return types.
   - They don't include detailed usage examples or context, which can make it challenging to write Python code directly from the descriptions without prior knowledge.

2. **Python Code Usage:**
   - The Python code examples provide context and show how to use these methods in a real script.
   - They often include specific values and additional logic that is not evident from the method signatures alone.

### Identified Patterns

1. **Parameter Types and Order:**
   - The order and types of parameters in the method descriptions match those in the Python code.

2. **Conversions and Adjustments:**
   - Some methods require conversions or adjustments (e.g., `DateTime` to `Double` using `ToOADate()`).
   - Enumerations are converted to integers using their corresponding enumeration names.

3. **Object and Membership IDs:**
   - Methods involving object and membership IDs (`AddMembership`, `RemoveMembership`, `AddProperty`, etc.) use IDs fetched from other methods (`FetchAllClassIds`, `FetchAllCollectionIds`, `GetMembershipID`).

### Extrapolated Usage Patterns

Here is how the methods would be used in actual Python scripts based on the patterns identified from existing code:

1. **Connection and Closing:**
   ```python
   db = DatabaseCore()
   db.Connection('path_to_file.xml')
   db.Close()
   ```

2. **Adding Objects:**
   ```python
   classes = db.FetchAllClassIds()
   db.AddObject('NewObjectName', classes["ClassName"], True, 'CategoryName', 'Description')
   ```

3. **Adding Categories:**
   ```python
   classes = db.FetchAllClassIds()
   db.AddCategory(classes["ClassName"], 'CategoryName')
   ```

4. **Adding Memberships:**
   ```python
   collections = db.FetchAllCollectionIds()
   db.AddMembership(collections["CollectionName"], 'ParentName', 'ChildName')
   ```

5. **Adding Properties:**
   ```python
   properties = db.FetchAllPropertyEnums()
   mem_id = db.GetMembershipID(collections["CollectionName"], 'ParentName', 'ChildName')
   db.AddProperty(mem_id, properties["PropertyName"], 1, 0.0, None, None, None, None, None, None, None, PeriodEnum.Interval)
   ```

6. **Updating Attributes:**
   ```python
   attributes = db.FetchAllAttributeEnums()
   db.UpdateAttribute(classes["ClassName"], 'ObjectName', attributes["AttributeName"], DateTime(2024,1,1).ToOADate())
   ```

### Mapping Example

Here’s a mapping of methods from the text file to their corresponding usage in Python code:

1. **Void Connection(String strFile)**
   ```python
   db.Connection('path_to_file.xml')
   ```

2. **Void Close()**
   ```python
   db.Close()
   ```

3. **Int32 AddObject(String strName, ClassEnum nClassId, Boolean bAddSystemMembership, String strCategory = None, String strDescription = None)**
   ```python
   classes = db.FetchAllClassIds()
   db.AddObject('NewObjectName', classes["ClassName"], True, 'CategoryName', 'Description')
   ```

4. **Int32 AddCategory(ClassEnum nClassId, String strCategory)**
   ```python
   classes = db.FetchAllClassIds()
   db.AddCategory(classes["ClassName"], 'CategoryName')
   ```

5. **Int32 AddMembership(CollectionEnum nCollectionId, String strParent, String strChild)**
   ```python
   collections = db.FetchAllCollectionIds()
   db.AddMembership(collections["CollectionName"], 'ParentName', 'ChildName')
   ```

6. **Int32 AddProperty(Int32 MembershipId, Int32 EnumId, Int32 BandId, Double Value, Object DateFrom, Object DateTo, Object Variable, Object DataFile, Object Pattern, Object Scenario, Object Action, PeriodEnum PeriodTypeId)**
   ```python
   properties = db.FetchAllPropertyEnums()
   mem_id = db.GetMembershipID(collections["CollectionName"], 'ParentName', 'ChildName')
   db.AddProperty(mem_id, properties["PropertyName"], 1, 0.0, None, None, None, None, None, None, None, PeriodEnum.Interval)
   ```

### Summary

The descriptions in the `DatabaseCoreMethods.txt` file provide the necessary method signatures but lack detailed usage context. The pattern identified from the Python code examples can be extrapolated to infer the usage of other methods. This pattern involves fetching necessary IDs and enumerations, using appropriate data types, and ensuring correct parameter order. 

Enhancing the `DatabaseCoreMethods.txt` file with examples and detailed explanations, as shown above, would make it more intuitive and useful for writing Python code directly from the descriptions.


Prompt:

I would like to do that: I think feeding this enhanced version of the DatabaseCoreMethods to an LLM would maximize its ability to leverage PLEXOS API to build PLEXOS models. Given you mention there is a pattern that you can extrapolate as to how python functions from PLEXOS API scripts leverage methods from the DatabaseCoreMethods text file, I think you should create a text file or script where you write the python equivalent version of each method described in the text files. You could include some tag to describe which python functions have been tried and tested (i.e., used in the PLEXOS API scripts you've helped me improved), and another tag to describe which functions are extrapolations. The intention is not to run this script, but to keep as documentation that can be consulted. Although having them in a script with docstrings might make them easier to deploy by copy-pasting. Do you agree that this is a good idea? Can you do that?

Response:

Yes, I agree that creating a detailed script with the Python equivalents of each method described in the `DatabaseCoreMethods.txt` file, including annotations for tested and extrapolated methods, is an excellent idea. This will serve as a comprehensive reference for leveraging the PLEXOS API and building PLEXOS models. Here's how we can structure it:

1. **Organize the methods into logical groups (e.g., Connection Management, Object Management).**
2. **Include docstrings with detailed descriptions and usage examples.**
3. **Tag methods that have been tried and tested in the provided scripts.**
4. **Tag methods that are extrapolated based on the identified patterns.**

Here's a sample of how this could be structured in a Python script format:

```python
# -*- coding: utf-8 -*-
"""
DatabaseCore Methods - Python Equivalents

This script provides Python equivalents for the methods described in the DatabaseCoreMethods.txt file.
Each method includes detailed descriptions, usage examples, and tags indicating whether the method
has been tested or extrapolated.

Tags:
    @tested: Method has been tried and tested in the provided PLEXOS API scripts.
    @extrapolated: Method is an extrapolation based on identified patterns.

Author: [Your Name]
Created on: [Today's Date]
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

# Connection Management
def connect_to_database(file_path):
    """
    Establishes a connection to the specified database file.

    Args:
        file_path (str): Path to the PLEXOS input file.

    Returns:
        DatabaseCore: An instance of the DatabaseCore class with an open connection.

    Example:
        db = connect_to_database('path_to_file.xml')
    @tested
    """
    db = DatabaseCore()
    db.DisplayAlerts = False
    db.Connection(file_path)
    return db

def close_database(db):
    """
    Closes the current database connection.

    Args:
        db (DatabaseCore): The database connection object.

    Example:
        close_database(db)
    @tested
    """
    db.Close()

# Object Management
def add_object(db, name, class_name, add_system_membership=True, category=None, description=None):
    """
    Adds a new object to the specified class.

    Args:
        db (DatabaseCore): The database connection object.
        name (str): Name of the new object.
        class_name (str): Class name to which the object belongs.
        add_system_membership (bool): Whether to add system membership.
        category (str, optional): Category of the object.
        description (str, optional): Description of the object.

    Example:
        add_object(db, 'ApiGen', 'Generator', True, 'API', 'Testing the API')
    @tested
    """
    classes = db.FetchAllClassIds()
    db.AddObject(name, classes[class_name], add_system_membership, category, description)

def remove_object(db, name, class_name):
    """
    Removes an object from the specified class.

    Args:
        db (DatabaseCore): The database connection object.
        name (str): Name of the object to remove.
        class_name (str): Class name from which the object will be removed.

    Example:
        remove_object(db, 'ApiGen', 'Generator')
    @extrapolated
    """
    classes = db.FetchAllClassIds()
    db.RemoveObject(name, classes[class_name])

# Membership Management
def add_membership(db, collection_name, parent_name, child_name):
    """
    Adds a membership between parent and child objects.

    Args:
        db (DatabaseCore): The database connection object.
        collection_name (str): Name of the collection.
        parent_name (str): Name of the parent object.
        child_name (str): Name of the child object.

    Example:
        add_membership(db, 'GeneratorNodes', 'ApiGen', '101')
    @tested
    """
    collections = db.FetchAllCollectionIds()
    db.AddMembership(collections[collection_name], parent_name, child_name)

def remove_membership(db, collection_name, parent_name, child_name):
    """
    Removes a membership between parent and child objects.

    Args:
        db (DatabaseCore): The database connection object.
        collection_name (str): Name of the collection.
        parent_name (str): Name of the parent object.
        child_name (str): Name of the child object.

    Example:
        remove_membership(db, 'GeneratorNodes', 'ApiGen', '101')
    @tested
    """
    collections = db.FetchAllCollectionIds()
    db.RemoveMembership(collections[collection_name], parent_name, child_name)

# Property Management
def add_property(db, membership_id, enum_id, band_id, value, date_from=None, date_to=None, variable=None, data_file=None, pattern=None, scenario=None, action=None, period_type=PeriodEnum.Interval):
    """
    Adds a property to a membership.

    Args:
        db (DatabaseCore): The database connection object.
        membership_id (int): ID of the membership.
        enum_id (int): ID of the property enum.
        band_id (int): ID of the band.
        value (float): Value of the property.
        date_from (DateTime, optional): Start date of the property.
        date_to (DateTime, optional): End date of the property.
        variable (object, optional): Variable associated with the property.
        data_file (object, optional): Data file associated with the property.
        pattern (object, optional): Pattern associated with the property.
        scenario (object, optional): Scenario associated with the property.
        action (object, optional): Action associated with the property.
        period_type (PeriodEnum, optional): Period type of the property.

    Example:
        add_property(db, mem_id, properties["SystemGenerators.Units"], 1, 0.0)
    @tested
    """
    db.AddProperty(membership_id, enum_id, band_id, value, date_from, date_to, variable, data_file, pattern, scenario, action, period_type)

def remove_property(db, membership_id, enum_id, band_id, date_from=None, date_to=None, variable=None, data_file=None, pattern=None, scenario=None, action=None, period_type=PeriodEnum.Interval):
    """
    Removes a property from a membership.

    Args:
        db (DatabaseCore): The database connection object.
        membership_id (int): ID of the membership.
        enum_id (int): ID of the property enum.
        band_id (int): ID of the band.
        date_from (DateTime, optional): Start date of the property.
        date_to (DateTime, optional): End date of the property.
        variable (object, optional): Variable associated with the property.
        data_file (object, optional): Data file associated with the property.
        pattern (object, optional): Pattern associated with the property.
        scenario (object, optional): Scenario associated with the property.
        action (object, optional): Action associated with the property.
        period_type (PeriodEnum, optional): Period type of the property.

    Example:
        remove_property(db, mem_id, properties["SystemGenerators.Units"], 1, None, None, None, None, None, None, PeriodEnum.Interval)
    @extrapolated
    """
    db.RemoveProperty(membership_id, enum_id, band_id, date_from, date_to, variable, data_file, pattern, scenario, action, period_type)

# Data Retrieval
def get_properties_table(db, collection_name, parent_name='', child_name=''):
    """
    Retrieves a table of properties.

    Args:
        db (DatabaseCore): The database connection object.
        collection_name (str): Name of the collection.
        parent_name (str, optional): Name of the parent object.
        child_name (str, optional): Name of the child object.

    Returns:
        Recordset: A recordset containing the properties table.

    Example:
        rs = get_properties_table(db, 'SystemGenerators', '', '101_1')
    @tested
    """
    collections = db.FetchAllCollectionIds()
    return db.GetPropertiesTable(collections[collection_name], parent_name, child_name)

# Example of usage for creating a PLEXOS model
def create_plexos_model():
    """
    Example function to create a PLEXOS model using the PLEXOS API.
    """
    plexosfile = 'path_to_plexosfile.xml'
    db = connect_to_database(plexosfile)
    
    # Add an object
    add_object(db, 'ApiGen', 'Generator', True, 'API', 'Testing the API')
    
    # Add a category
    add_category(db, 'Generator', 'API')
    
    # Add a membership
    add_membership(db, 'GeneratorNodes', 'ApiGen', '101')
    
    # Fetch properties
    properties = db.FetchAllPropertyEnums()
    mem_id = db.GetMembershipID(collections["SystemGenerators"], 'System', 'ApiGen')
    
    # Add a property
    add_property(db, mem_id, properties["SystemGenerators.Units"], 1, 0.0)
    
    # Close the database
    close_database(db)

if __name__ == '__main__':
    create

Prompt:

this looks excellent; you mention this is a sample, can you extend it to cover as many methods from the DatabaseCoreMethods.txt?

Response:

Sure, let's extend the sample to cover as many methods as possible from the `DatabaseCoreMethods.txt` file. I'll provide Python equivalents, with docstrings and tags indicating whether each method has been tested or is extrapolated.

```python
# -*- coding: utf-8 -*-
"""
DatabaseCore Methods - Python Equivalents

This script provides Python equivalents for the methods described in the DatabaseCoreMethods.txt file.
Each method includes detailed descriptions, usage examples, and tags indicating whether the method
has been tested or extrapolated.

Tags:
    @tested: Method has been tried and tested in the provided PLEXOS API scripts.
    @extrapolated: Method is an extrapolation based on identified patterns.

Author: [Your Name]
Created on: [Today's Date]
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
from System import DateTime, String, Int32, Double

# Connection Management
def connect_to_database(file_path):
    """
    Establishes a connection to the specified database file.

    Args:
        file_path (str): Path to the PLEXOS input file.

    Returns:
        DatabaseCore: An instance of the DatabaseCore class with an open connection.

    Example:
        db = connect_to_database('path_to_file.xml')
    @tested
    """
    db = DatabaseCore()
    db.DisplayAlerts = False
    db.Connection(file_path)
    return db

def close_database(db):
    """
    Closes the current database connection.

    Args:
        db (DatabaseCore): The database connection object.

    Example:
        close_database(db)
    @tested
    """
    db.Close()

# Database Creation
def create_empty_database(file_path, overwrite=False):
    """
    Creates a new empty database at the specified file path.

    Args:
        file_path (str): Path to create the new database file.
        overwrite (bool, optional): Whether to overwrite if the file already exists.

    Returns:
        bool: True if the database is created successfully, False otherwise.

    Example:
        success = create_empty_database('new_database.xml', overwrite=True)
    @extrapolated
    """
    db = DatabaseCore()
    return db.NewEmptyDatabase(file_path, overwrite)

# Object Management
def add_object(db, name, class_name, add_system_membership=True, category=None, description=None):
    """
    Adds a new object to the specified class.

    Args:
        db (DatabaseCore): The database connection object.
        name (str): Name of the new object.
        class_name (str): Class name to which the object belongs.
        add_system_membership (bool): Whether to add system membership.
        category (str, optional): Category of the object.
        description (str, optional): Description of the object.

    Example:
        add_object(db, 'ApiGen', 'Generator', True, 'API', 'Testing the API')
    @tested
    """
    classes = db.FetchAllClassIds()
    db.AddObject(name, classes[class_name], add_system_membership, category, description)

def remove_object(db, name, class_name):
    """
    Removes an object from the specified class.

    Args:
        db (DatabaseCore): The database connection object.
        name (str): Name of the object to remove.
        class_name (str): Class name from which the object will be removed.

    Example:
        remove_object(db, 'ApiGen', 'Generator')
    @extrapolated
    """
    classes = db.FetchAllClassIds()
    db.RemoveObject(name, classes[class_name])

def update_object_description(db, class_name, object_name, new_description):
    """
    Updates the description of an object.

    Args:
        db (DatabaseCore): The database connection object.
        class_name (str): Class name to which the object belongs.
        object_name (str): Name of the object to update.
        new_description (str): New description for the object.

    Example:
        update_object_description(db, 'Generator', 'ApiGen', 'Updated description')
    @extrapolated
    """
    classes = db.FetchAllClassIds()
    db.UpdateObjectDescription(classes[class_name], object_name, new_description)

# Category Management
def add_category(db, class_name, category_name):
    """
    Adds a new category to the specified class.

    Args:
        db (DatabaseCore): The database connection object.
        class_name (str): Class name to which the category belongs.
        category_name (str): Name of the new category.

    Example:
        add_category(db, 'Generator', 'API')
    @tested
    """
    classes = db.FetchAllClassIds()
    db.AddCategory(classes[class_name], category_name)

def remove_category(db, class_name, category_name, remove_objects=True):
    """
    Removes a category and optionally its objects.

    Args:
        db (DatabaseCore): The database connection object.
        class_name (str): Class name to which the category belongs.
        category_name (str): Name of the category to remove.
        remove_objects (bool, optional): Whether to remove objects in the category.

    Example:
        remove_category(db, 'Generator', 'API', True)
    @extrapolated
    """
    classes = db.FetchAllClassIds()
    db.RemoveCategory(classes[class_name], category_name, remove_objects)

# Membership Management
def add_membership(db, collection_name, parent_name, child_name):
    """
    Adds a membership between parent and child objects.

    Args:
        db (DatabaseCore): The database connection object.
        collection_name (str): Name of the collection.
        parent_name (str): Name of the parent object.
        child_name (str): Name of the child object.

    Example:
        add_membership(db, 'GeneratorNodes', 'ApiGen', '101')
    @tested
    """
    collections = db.FetchAllCollectionIds()
    db.AddMembership(collections[collection_name], parent_name, child_name)

def remove_membership(db, collection_name, parent_name, child_name):
    """
    Removes a membership between parent and child objects.

    Args:
        db (DatabaseCore): The database connection object.
        collection_name (str): Name of the collection.
        parent_name (str): Name of the parent object.
        child_name (str): Name of the child object.

    Example:
        remove_membership(db, 'GeneratorNodes', 'ApiGen', '101')
    @tested
    """
    collections = db.FetchAllCollectionIds()
    db.RemoveMembership(collections[collection_name], parent_name, child_name)

# Attribute Management
def add_attribute(db, class_name, object_name, attribute_name, value):
    """
    Adds an attribute to an object.

    Args:
        db (DatabaseCore): The database connection object.
        class_name (str): Class name to which the object belongs.
        object_name (str): Name of the object to add the attribute to.
        attribute_name (str): Name of the attribute to add.
        value (float): Value of the attribute.

    Example:
        add_attribute(db, 'Generator', 'ApiGen', 'MaxCapacity', 100.0)
    @extrapolated
    """
    classes = db.FetchAllClassIds()
    attributes = db.FetchAllAttributeEnums()
    db.AddAttribute(classes[class_name], object_name, attributes[attribute_name], value)

def remove_attribute(db, class_name, object_name, attribute_name):
    """
    Removes an attribute from an object.

    Args:
        db (DatabaseCore): The database connection object.
        class_name (str): Class name to which the object belongs.
        object_name (str): Name of the object to remove the attribute from.
        attribute_name (str): Name of the attribute to remove.

    Example:
        remove_attribute(db, 'Generator', 'ApiGen', 'MaxCapacity')
    @extrapolated
    """
    classes = db.FetchAllClassIds()
    attributes = db.FetchAllAttributeEnums()
    db.RemoveAttribute(classes[class_name], object_name, attributes[attribute_name])

def update_attribute(db, class_name, object_name, attribute_name, new_value):
    """
    Updates the value of an attribute.

    Args:
        db (DatabaseCore): The database connection object.
        class_name (str): Class name to which the object belongs.
        object_name (str): Name of the object to update the attribute for.
        attribute_name (str): Name of the attribute to update.
        new_value (float): New value of the attribute.

    Example:
        update_attribute(db, 'Generator', 'ApiGen', 'MaxCapacity', 150.0)
    @tested
    """
    classes = db.FetchAllClassIds()
    attributes = db.FetchAllAttributeEnums()
    db.UpdateAttribute(classes[class_name], object_name, attributes[attribute_name], new_value)

# Property Management
def add_property(db, membership_id, enum_id, band_id, value, date_from=None, date_to=None, variable=None, data_file=None, pattern=None, scenario=None, action=None, period_type=PeriodEnum.Interval):
    """
    Adds a property to a membership.

    Args:
        db (DatabaseCore): The database connection object.
        membership_id (int): ID of the membership.
        enum_id (int): ID of the property enum.
        band_id (int): ID of the band.
        value