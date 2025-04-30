from .param_validator_surface_area import * # Module to validate arguments
import re # Module used to extract the user input values into values and units
def param_parser(args):
    
    # Recieving arguments
    # Based on the shape of polygon call the relevant method to split the arguments & list them
    try:
        match args[0]:
            case 'cube':
                return cube_param_parser(args), args[0]
            case 'cuboid':
                return cuboid_param_parser(args), args[0]
            case 'sphere':
                return sphere_param_parser(args), args[0]
            case 'cylinder':
                return cylinder_param_parser(args), args[0]
            case 'cone':
                return cone_param_parser(args), args[0]
            case 'pyramid':
                return pyramid_param_parser(args), args[0]
            case 'hemisphere':
                return hemisphere_param_parser(args), args[0]    
            case _:
                return("Error: Invalid shape")
    except IndexError:
        print("Something went wrong- Index not in range!")
            
# Regex operation to determine the 'unit' and 'value' of the args recieved from method 'square_param_parser'
def extract_value_and_unit(value_string):
    # Regular expression to match the numeric value followed by a unit
    match = re.match(r"(\d+\.?\d*)\s*(\w+)", value_string)
    
    if match:
        value = float(match.group(1))  # Extract the value as a float
        unit = match.group(2)          # Extract the unit
        return value, unit
    else:
        return None, None  # If no match is found
    
# Packing the extracted parameters from method 'extract_value_and_unit'
def pack_value_and_unit(value, unit):
    # Initialise an empty dict
    data = {}

    # Adding multiple values under the same key manually
    data.setdefault(unit, []).append(value)
    return data    
            
def cube_param_parser(args):
    
    """Call param_validator to check if the arguments are suitable for the calculation
    and if it returns True"""
    if cube_param_validator(args):
        # extract argument 1 and send to extractor and recieve the 'value' and 'unit' splitted and made suitable for calculation
        side = args[1]
        value, unit = extract_value_and_unit(side)
    
        # Pack 'value' and 'unit' in 'data' to be used for calculation in area program
        data = pack_value_and_unit(value, unit)
        # Return extracted and packed 'value' and 'unit' to Module 'area'
        return data
    else:
        return {}
    
def cuboid_param_parser(args):
    # Initialising a list to append the extracted 'unit' and 'values' as there are more unit and value pairs
    data_packer = []
    """Call param_validator to check if the arguments are suitable for the calculation
    and if it returns True"""    
    if cuboid_param_validator(args):
        # extract arguments and send to extractor
        for i in range(len(args)-1):
            dimension = args[i+1]
            value, unit = extract_value_and_unit(dimension)
            data = pack_value_and_unit(value, unit)
            # Inserting the extracted value and unit in the initialised list
            data_packer.append(data)
        # Return extracted and packed 'value' and 'unit' to Module 'area'
        return data_packer
    else:
        return data_packer
    
def sphere_param_parser(args):
    
    """Call param_validator to check if the arguments are suitable for the calculation
    and if it returns True"""
    if sphere_param_validator(args):
        # extract argument 1 and send to extractor and recieve the 'value' and 'unit' splitted and made suitable for calculation
        side = args[1]
        value, unit = extract_value_and_unit(side)
    
        # Pack 'value' and 'unit' in 'data' to be used for calculation in area program
        data = pack_value_and_unit(value, unit)
        # Return extracted and packed 'value' and 'unit' to Module 'area'
        return data
    else:
        return {}
    
def cylinder_param_parser(args):
    # Initialising a list to append the extracted 'unit' and 'values' as there are more unit and value pairs
    data_packer = []
    """Call param_validator to check if the arguments are suitable for the calculation
    and if it returns True"""    
    if cylinder_param_validator(args):
        # extract arguments and send to extractor
        for i in range(len(args)-1):
            dimension = args[i+1]
            value, unit = extract_value_and_unit(dimension)
            data = pack_value_and_unit(value, unit)
            # Inserting the extracted value and unit in the initialised list
            data_packer.append(data)
        # Return extracted and packed 'value' and 'unit' to Module 'area'
        return data_packer
    else:
        return data_packer
    
def cone_param_parser(args):
    # Initialising a list to append the extracted 'unit' and 'values' as there are more unit and value pairs
    data_packer = []
    """Call param_validator to check if the arguments are suitable for the calculation
    and if it returns True"""    
    if cone_param_validator(args):
        # extract arguments and send to extractor
        for i in range(len(args)-1):
            dimension = args[i+1]
            value, unit = extract_value_and_unit(dimension)
            data = pack_value_and_unit(value, unit)
            # Inserting the extracted value and unit in the initialised list
            data_packer.append(data)
        # Return extracted and packed 'value' and 'unit' to Module 'area'
        return data_packer
    else:
        return data_packer
    
def pyramid_param_parser(args):
    # Initialising a list to append the extracted 'unit' and 'values' as there are more unit and value pairs
    data_packer = []
    """Call param_validator to check if the arguments are suitable for the calculation
    and if it returns True"""    
    if pyramid_param_validator(args):
        # extract arguments and send to extractor
        for i in range(len(args)-1):
            dimension = args[i+1]
            value, unit = extract_value_and_unit(dimension)
            data = pack_value_and_unit(value, unit)
            # Inserting the extracted value and unit in the initialised list
            data_packer.append(data)
        # Return extracted and packed 'value' and 'unit' to Module 'area'
        return data_packer
    else:
        return data_packer
    
def hemisphere_param_parser(args):
    
    """Call param_validator to check if the arguments are suitable for the calculation
    and if it returns True"""
    if hemisphere_param_validator(args):
        # extract argument 1 and send to extractor and recieve the 'value' and 'unit' splitted and made suitable for calculation
        side = args[1]
        value, unit = extract_value_and_unit(side)
    
        # Pack 'value' and 'unit' in 'data' to be used for calculation in area program
        data = pack_value_and_unit(value, unit)
        # Return extracted and packed 'value' and 'unit' to Module 'area'
        return data
    else:
        return {}