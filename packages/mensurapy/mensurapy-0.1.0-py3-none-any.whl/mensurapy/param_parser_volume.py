from .param_validator_volume import *  # Module to validate arguments
import re  # Module used to extract the user input values into values and units

def param_parser(args):
    try:
        shape = args[0]
        match shape:
            case 'cube':
                return cube_param_parser(args), shape
            case 'cuboid':
                return cuboid_param_parser(args), shape
            case 'sphere':
                return sphere_param_parser(args), shape
            case 'cylinder':
                return cylinder_param_parser(args), shape
            case 'cone':
                return cone_param_parser(args), shape
            case 'pyramid':
                return pyramid_param_parser(args), shape
            case 'hemisphere':
                return hemisphere_param_parser(args), shape
            case 'prism':
                return prism_param_parser(args), shape
            case 'ellipsoid':
                return ellipsoid_param_parser(args), shape
            case _:
                raise ValueError(f"Invalid shape '{shape}' provided.")
    except IndexError:
        raise IndexError("Shape not provided. Please pass at least one argument.")
    except Exception as e:
        raise Exception(f"Error in param_parser: {e}")

def extract_value_and_unit(value_string):
    try:
        match = re.match(r"(\d+\.?\d*)\s*(\w+)", value_string)
        if match:
            value = float(match.group(1))
            unit = match.group(2)
            return value, unit
        else:
            raise ValueError(f"Input '{value_string}' is not in the expected format like '5m' or '3 kg'")
    except Exception as e:
        raise Exception(f"Error in extract_value_and_unit: {e}")

def pack_value_and_unit(value, unit):
    try:
        data = {}
        data.setdefault(unit, []).append(value)
        return data
    except Exception as e:
        raise Exception(f"Error in pack_value_and_unit: {e}")

def cube_param_parser(args):
    try:
        if cube_param_validator(args):
            side = args[1]
            value, unit = extract_value_and_unit(side)
            data = pack_value_and_unit(value, unit)
            return data
        else:
            raise ValueError("Invalid arguments for cube.")
    except IndexError:
        raise IndexError("Missing dimension for cube.")
    except Exception as e:
        raise Exception(f"cube_param_parser error: {e}")

def cuboid_param_parser(args):
    data_packer = []
    try:
        if cuboid_param_validator(args):
            for dimension in args[1:]:
                value, unit = extract_value_and_unit(dimension)
                data = pack_value_and_unit(value, unit)
                data_packer.append(data)
            return data_packer
        else:
            raise ValueError("Invalid arguments for cuboid.")
    except Exception as e:
        raise Exception(f"cuboid_param_parser error: {e}")

def sphere_param_parser(args):
    try:
        if sphere_param_validator(args):
            side = args[1]
            value, unit = extract_value_and_unit(side)
            data = pack_value_and_unit(value, unit)
            return data
        else:
            raise ValueError("Invalid arguments for sphere.")
    except Exception as e:
        raise Exception(f"sphere_param_parser error: {e}")

def cylinder_param_parser(args):
    data_packer = []
    try:
        if cylinder_param_validator(args):
            for dimension in args[1:]:
                value, unit = extract_value_and_unit(dimension)
                data = pack_value_and_unit(value, unit)
                data_packer.append(data)
            return data_packer
        else:
            raise ValueError("Invalid arguments for cylinder.")
    except Exception as e:
        raise Exception(f"cylinder_param_parser error: {e}")

def cone_param_parser(args):
    data_packer = []
    try:
        if cone_param_validator(args):
            for dimension in args[1:]:
                value, unit = extract_value_and_unit(dimension)
                data = pack_value_and_unit(value, unit)
                data_packer.append(data)
            return data_packer
        else:
            raise ValueError("Invalid arguments for cone.")
    except Exception as e:
        raise Exception(f"cone_param_parser error: {e}")

def pyramid_param_parser(args):
    data_packer = []
    try:
        if pyramid_param_validator(args):
            for dimension in args[1:]:
                value, unit = extract_value_and_unit(dimension)
                data = pack_value_and_unit(value, unit)
                data_packer.append(data)
            return data_packer
        else:
            raise ValueError("Invalid arguments for pyramid.")
    except Exception as e:
        raise Exception(f"pyramid_param_parser error: {e}")

def hemisphere_param_parser(args):
    try:
        if hemisphere_param_validator(args):
            side = args[1]
            value, unit = extract_value_and_unit(side)
            data = pack_value_and_unit(value, unit)
            return data
        else:
            raise ValueError("Invalid arguments for hemisphere.")
    except Exception as e:
        raise Exception(f"hemisphere_param_parser error: {e}")

def prism_param_parser(args):
    data_packer = []
    try:
        if prism_param_validator(args):
            for dimension in args[1:]:
                value, unit = extract_value_and_unit(dimension)
                data = pack_value_and_unit(value, unit)
                data_packer.append(data)
            return data_packer
        else:
            raise ValueError("Invalid arguments for prism.")
    except Exception as e:
        raise Exception(f"prism_param_parser error: {e}")

def ellipsoid_param_parser(args):
    data_packer = []
    try:
        if ellipsoid_param_validator(args):
            for dimension in args[1:]:
                value, unit = extract_value_and_unit(dimension)
                data = pack_value_and_unit(value, unit)
                data_packer.append(data)
            return data_packer
        else:
            raise ValueError("Invalid arguments for ellipsoid.")
    except Exception as e:
        raise Exception(f"ellipsoid_param_parser error: {e}")
