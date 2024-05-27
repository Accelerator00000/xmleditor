'''
Steps to Implement the Function
Read the XML File: Load the target XML file.
Read the Template: Load the XML template for a new sector.
Get User Input: Prompt the user for information according to the template.
Add New Sector: Insert the new sector into the target XML file.
Save the File: Save the modified XML file.
'''

import xml.etree.ElementTree as ET

def add_sector_to_xml(target_file, template_file):
    """
    Adds a new sector to the target XML file based on a template.

    Args:
        target_file (str): The path to the target XML file.
        template_file (str): The path to the XML template file.
    """
    # Parse the target XML file
    tree = ET.parse(target_file)
    root = tree.getroot()
    
    # Parse the template XML file
    template_tree = ET.parse(template_file)
    template_root = template_tree.getroot()
    
    # Function to recursively get user input for each element
    def get_user_input(element):
        for child in element:
            if child.text.strip():  # if the element has text, prompt for input
                user_input = input(f"Enter value for {child.tag} (default: {child.text}): ")
                child.text = user_input if user_input else child.text
            # Recurse for child elements
            get_user_input(child)
    
    # Make a copy of the template's root element to modify
    new_sector = ET.fromstring(ET.tostring(template_root))
    
    # Get user input for the new sector
    get_user_input(new_sector)
    
    # Add the new sector to the target XML root
    root.append(new_sector)
    
    # Save the modified XML back to the file
    tree.write(target_file, encoding='utf-8', xml_declaration=True)
    print(f"New sector added and saved to {target_file}")

# Example usage
target_file = 'target.xml'
template_file = 'template.xml'

add_sector_to_xml(target_file, template_file)



'''
Step-by-Step Guide
Read the XML File: Load the target XML file.
List Child Elements: Return a list of child element names for each sector.
Search for Specific Sector(s): Allow the user to define the sector they want to edit by specifying a field and its value.
Display Matching Sectors: Show all sectors that match the search criteria.
Edit Sector(s): Allow the user to input the new values for the specified elements.
Confirm Changes: Display the changes and ask for confirmation.
Save or Repeat: Save the changes or go back for further editing.
'''

import xml.etree.ElementTree as ET

def list_sector_children(file_name):
    """
    Lists the child element names of each sector in the XML file.

    Args:
        file_name (str): The path to the XML file.

    Returns:
        list: A list of child element names for the first sector.
    """
    tree = ET.parse(file_name)
    root = tree.getroot()
    sectors = root.findall('.//sector')
    
    if not sectors:
        print("No sectors found in the XML file.")
        return []

    # Assuming all sectors have the same structure, get child element names from the first sector
    first_sector = sectors[0]
    child_element_names = [child.tag for child in first_sector]
    
    return child_element_names

def edit_existing_sectors(file_name):
    """
    Edits existing sectors in the XML file based on user input.

    Args:
        file_name (str): The path to the XML file.
    """
    tree = ET.parse(file_name)
    root = tree.getroot()
    sectors = root.findall('.//sector')

    if not sectors:
        print("No sectors found in the XML file.")
        return

    # List child element names
    child_element_names = list_sector_children(file_name)
    print("Child element names:", child_element_names)
    
    # Get search criteria from user
    search_field = input("Enter the search field name: ")
    search_value = input(f"Enter the value for {search_field}: ")
    
    # Find matching sectors
    matching_sectors = [sector for sector in sectors if sector.find(search_field) is not None and sector.find(search_field).text == search_value]
    
    if not matching_sectors:
        print("No sectors found with the specified search criteria.")
        return

    print("Matching sectors found:")
    for idx, sector in enumerate(matching_sectors):
        print(f"Sector {idx + 1}:")
        for child in sector:
            print(f"  {child.tag}: {child.text}")
    
    # Get edit details from user
    edits = {}
    for child_name in child_element_names:
        edit_value = input(f"Enter new value for {child_name} (or NA to skip): ")
        if edit_value != 'NA':
            if child_name in edits:
                edits[child_name].append(edit_value)
            else:
                edits[child_name] = [edit_value]

    # Apply edits
    for sector in matching_sectors:
        for child_name, new_values in edits.items():
            if len(new_values) == 1:
                sector.find(child_name).text = new_values[0]
            else:
                for i, new_value in enumerate(new_values):
                    if i < len(sectors):
                        sectors[i].find(child_name).text = new_value

    # Confirm changes
    print("Edited sectors:")
    for idx, sector in enumerate(matching_sectors):
        print(f"Sector {idx + 1}:")
        for child in sector:
            print(f"  {child.tag}: {child.text}")
    
    confirm = input("Do you want to save these changes? (yes/no): ")
    if confirm.lower() == 'yes':
        tree.write(file_name, encoding='utf-8', xml_declaration=True)
        print("Changes saved.")
    else:
        print("Changes discarded.")

# Example usage
file_name = 'target.xml'
edit_existing_sectors(file_name)



'''
Steps to Implement the Delete Function
Read the XML File: Load the target XML file.
List Child Elements: Return a list of child element names for each sector.
Search for Specific Sector(s): Allow the user to define the sector they want to delete by specifying a field and its value.
Display Matching Sectors: Show all sectors that match the search criteria.
Delete Sector(s): Allow the user to confirm deletion of the specified sectors.
Save Changes: Save the modified XML file.
'''
import xml.etree.ElementTree as ET

def list_sector_children(file_name):
    """
    Lists the child element names of each sector in the XML file.

    Args:
        file_name (str): The path to the XML file.

    Returns:
        list: A list of child element names for the first sector.
    """
    tree = ET.parse(file_name)
    root = tree.getroot()
    sectors = root.findall('.//sector')
    
    if not sectors:
        print("No sectors found in the XML file.")
        return []

    # Assuming all sectors have the same structure, get child element names from the first sector
    first_sector = sectors[0]
    child_element_names = [child.tag for child in first_sector]
    
    return child_element_names

def delete_existing_sector(file_name):
    """
    Deletes existing sectors in the XML file based on user input.

    Args:
        file_name (str): The path to the XML file.
    """
    tree = ET.parse(file_name)
    root = tree.getroot()
    sectors = root.findall('.//sector')

    if not sectors:
        print("No sectors found in the XML file.")
        return

    # List child element names
    child_element_names = list_sector_children(file_name)
    print("Child element names:", child_element_names)
    
    # Get search criteria from user
    search_field = input("Enter the search field name: ")
    search_value = input(f"Enter the value for {search_field}: ")
    
    # Find matching sectors
    matching_sectors = [sector for sector in sectors if sector.find(search_field) is not None and sector.find(search_field).text == search_value]
    
    if not matching_sectors:
        print("No sectors found with the specified search criteria.")
        return

    print("Matching sectors found:")
    for idx, sector in enumerate(matching_sectors):
        print(f"Sector {idx + 1}:")
        for child in sector:
            print(f"  {child.tag}: {child.text}")

    # Confirm deletion
    confirm = input("Do you want to delete these sectors? (yes/no): ")
    if confirm.lower() == 'yes':
        for sector in matching_sectors:
            root.remove(sector)
        tree.write(file_name, encoding='utf-8', xml_declaration=True)
        print("Sectors deleted and changes saved.")
    else:
        print("No changes made.")

# Example usage
file_name = 'target.xml'
delete_existing_sector(file_name)

'''
xml_editor/
│
├── __init__.py
├── list_sector_children.py
├── edit_sector.py
├── delete_sector.py
└── text_to_dict_converter.py


'''


# __init__.py
from .list_sector_children import list_sector_children
from .edit_sector import edit_existing_sectors
from .delete_sector import delete_existing_sector
from .text_to_dict_converter import TextToDictConverter

__all__ = ['list_sector_children', 'edit_existing_sectors', 'delete_existing_sector', 'TextToDictConverter']




# list_sector_children.py

import xml.etree.ElementTree as ET

def list_sector_children(file_name):
    """
    Lists the child element names of each sector in the XML file.

    Args:
        file_name (str): The path to the XML file.

    Returns:
        list: A list of child element names for the first sector.
    """
    tree = ET.parse(file_name)
    root = tree.getroot()
    sectors = root.findall('.//sector')
    
    if not sectors:
        print("No sectors found in the XML file.")
        return []

    # Assuming all sectors have the same structure, get child element names from the first sector
    first_sector = sectors[0]
    child_element_names = [child.tag for child in first_sector]
    
    return child_element_names


# edit_sector.py

import xml.etree.ElementTree as ET

def edit_existing_sectors(file_name):
    """
    Edits existing sectors in the XML file based on user input.

    Args:
        file_name (str): The path to the XML file.
    """
    tree = ET.parse(file_name)
    root = tree.getroot()
    sectors = root.findall('.//sector')

    if not sectors:
        print("No sectors found in the XML file.")
        return

    # List child element names
    child_element_names = list_sector_children(file_name)
    print("Child element names:", child_element_names)
    
    # Get search criteria from user
    search_field = input("Enter the search field name: ")
    search_value = input(f"Enter the value for {search_field}: ")
    
    # Find matching sectors
    matching_sectors = [sector for sector in sectors if sector.find(search_field) is not None and sector.find(search_field).text == search_value]
    
    if not matching_sectors:
        print("No sectors found with the specified search criteria.")
        return

    print("Matching sectors found:")
    for idx, sector in enumerate(matching_sectors):
        print(f"Sector {idx + 1}:")
        for child in sector:
            print(f"  {child.tag}: {child.text}")
    
    # Get edit details from user
    edits = {}
    for child_name in child_element_names:
        edit_value = input(f"Enter new value for {child_name} (or NA to skip): ")
        if edit_value != 'NA':
            if child_name in edits:
                edits[child_name].append(edit_value)
            else:
                edits[child_name] = [edit_value]

    # Apply edits
    for sector in matching_sectors:
        for child_name, new_values in edits.items():
            if len(new_values) == 1:
                sector.find(child_name).text = new_values[0]
            else:
                for i, new_value in enumerate(new_values):
                    if i < len(matching_sectors):
                        matching_sectors[i].find(child_name).text = new_value

    # Confirm changes
    print("Edited sectors:")
    for idx, sector in enumerate(matching_sectors):
        print(f"Sector {idx + 1}:")
        for child in sector:
            print(f"  {child.tag}: {child.text}")
    
    confirm = input("Do you want to save these changes? (yes/no): ")
    if confirm.lower() == 'yes':
        tree.write(file_name, encoding='utf-8', xml_declaration=True)
        print("Changes saved.")
    else:
        print("Changes discarded.")


# delete_sector.py

import xml.etree.ElementTree as ET

def delete_existing_sector(file_name):
    """
    Deletes existing sectors in the XML file based on user input.

    Args:
        file_name (str): The path to the XML file.
    """
    tree = ET.parse(file_name)
    root = tree.getroot()
    sectors = root.findall('.//sector')

    if not sectors:
        print("No sectors found in the XML file.")
        return

    # List child element names
    child_element_names = list_sector_children(file_name)
    print("Child element names:", child_element_names)
    
    # Get search criteria from user
    search_field = input("Enter the search field name: ")
    search_value = input(f"Enter the value for {search_field}: ")
    
    # Find matching sectors
    matching_sectors = [sector for sector in sectors if sector.find(search_field) is not None and sector.find(search_field).text == search_value]
    
    if not matching_sectors:
        print("No sectors found with the specified search criteria.")
        return

    print("Matching sectors found:")
    for idx, sector in enumerate(matching_sectors):
        print(f"Sector {idx + 1}:")
        for child in sector:
            print(f"  {child.tag}: {child.text}")

    # Confirm deletion
    confirm = input("Do you want to delete these sectors? (yes/no): ")
    if confirm.lower() == 'yes':
        for sector in matching_sectors:
            root.remove(sector)
        tree.write(file_name, encoding='utf-8', xml_declaration=True)
        print("Sectors deleted and changes saved.")
    else:
        print("No changes made.")


# text_to_dict_converter.py

class TextToDictConverter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_dict = self._convert_to_dict()

    def _convert_to_dict(self):
        """
        Converts the text file into a dictionary.
        
        Returns:
            dict: A dictionary where keys are element names and values are lists of element values.
        """
        data_dict = {}
        
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                if ':' not in line:
                    print(f"Skipping invalid line: {line}")
                    continue
                
                element, value = line.split(':', 1)
                element = element.strip()
                value = value.strip()
                
                if element in data_dict:
                    if isinstance(data_dict[element], list):
                        data_dict[element].append(value)
                    else:
                        data_dict[element] = [data_dict[element], value]
                else:
                    data_dict[element] = value
        
        # Convert single values to lists to align with the requirement
        for key in data_dict:
            if not isinstance(data_dict[key], list):
                data_dict[key] = [data_dict[key]]
        
        return data_dict

    def get_dict(self):
        """
        Returns the dictionary representation of the text file.
        
        Returns:
            dict: The converted dictionary.
        """
        return self.data_dict
