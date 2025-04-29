import math
from .unit_converter import *  # Module to convert dimensions to base unit 'm'

def cube(dictionary, target_unit='m'):
    try:
        flat_list = [item for key, values in dictionary.items() for item in [key] + values]
        side_value = flat_list[1]
        side_unit = flat_list[0]
        side = convert_to_base_unit(side_value, side_unit, target_unit)
        vol = side ** 3
        return f"Volume: {vol} {target_unit}³"
    except Exception as e:
        raise ValueError(f"Error calculating cube volume: {e}")

def cuboid(list, target_unit='m'):
    try:
        flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
        length_value = flat_list[1]
        length_unit = flat_list[0]
        breadth_value = flat_list[3]
        breadth_unit = flat_list[2]
        height_value = flat_list[5]
        height_unit = flat_list[4]
        l = convert_to_base_unit(length_value, length_unit, target_unit)
        b = convert_to_base_unit(breadth_value, breadth_unit, target_unit)
        h = convert_to_base_unit(height_value, height_unit, target_unit)
        vol = l * b * h
        return f"Volume: {vol} {target_unit}³"
    except Exception as e:
        raise ValueError(f"Error calculating cuboid volume: {e}")

def sphere(dictionary, target_unit='m'):
    try:
        flat_list = [item for key, values in dictionary.items() for item in [key] + values]
        radius_value = flat_list[1]
        radius_unit = flat_list[0]
        r = convert_to_base_unit(radius_value, radius_unit, target_unit)
        vol = (4/3) * math.pi * r ** 3
        return f"Volume: {vol} {target_unit}³"
    except Exception as e:
        raise ValueError(f"Error calculating sphere volume: {e}")

def cylinder(list, target_unit='m'):
    try:
        flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
        radius_value = flat_list[1]
        radius_unit = flat_list[0]
        height_value = flat_list[3]
        height_unit = flat_list[2]
        r = convert_to_base_unit(radius_value, radius_unit, target_unit)
        h = convert_to_base_unit(height_value, height_unit, target_unit)
        vol = math.pi * r ** 2 * h
        return f"Volume: {vol} {target_unit}³"
    except Exception as e:
        raise ValueError(f"Error calculating cylinder volume: {e}")

def cone(list, target_unit='m'):
    try:
        flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
        l = len(flat_list)
        if l == 4:
            radius_value = flat_list[1]
            radius_unit = flat_list[0]
            height_value = flat_list[3]
            height_unit = flat_list[2]
            r = convert_to_base_unit(radius_value, radius_unit, target_unit)
            h = convert_to_base_unit(height_value, height_unit, target_unit)
            vol = (1/3) * math.pi * r ** 2 * h
        elif l == 6:
            r1 = convert_to_base_unit(flat_list[1], flat_list[0], target_unit)
            r2 = convert_to_base_unit(flat_list[3], flat_list[2], target_unit)
            h = convert_to_base_unit(flat_list[5], flat_list[4], target_unit)
            vol = (1/3) * math.pi * h * (r1 ** 2 + r2 ** 2 + r1 * r2)
        else:
            raise ValueError("Invalid number of dimensions for cone")
        return f"Volume: {vol} {target_unit}³"
    except Exception as e:
        raise ValueError(f"Error calculating cone volume: {e}")

def pyramid(list, target_unit='m'):
    try:
        flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
        l = len(flat_list)
        if l == 4:
            b = convert_to_base_unit(flat_list[1], flat_list[0], target_unit)
            h = convert_to_base_unit(flat_list[3], flat_list[2], target_unit)
            vol = (1/3) * b ** 2 * h
        elif l == 6:
            l_val = convert_to_base_unit(flat_list[1], flat_list[0], target_unit)
            w = convert_to_base_unit(flat_list[3], flat_list[2], target_unit)
            h = convert_to_base_unit(flat_list[5], flat_list[4], target_unit)
            vol = (1/3) * l_val * w * h
        else:
            raise ValueError("Invalid number of dimensions for pyramid")
        return f"Volume: {vol} {target_unit}³"
    except Exception as e:
        raise ValueError(f"Error calculating pyramid volume: {e}")

def hemisphere(dictionary, target_unit='m'):
    try:
        flat_list = [item for key, values in dictionary.items() for item in [key] + values]
        r = convert_to_base_unit(flat_list[1], flat_list[0], target_unit)
        vol = (2/3) * math.pi * r ** 3
        return f"Volume: {vol} {target_unit}³"
    except Exception as e:
        raise ValueError(f"Error calculating hemisphere volume: {e}")

def prism(list, target_unit='m'):
    try:
        flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
        l = convert_to_base_unit(flat_list[1], flat_list[0], target_unit)
        b = convert_to_base_unit(flat_list[3], flat_list[2], target_unit)
        h = convert_to_base_unit(flat_list[5], flat_list[4], target_unit)
        vol = 0.5 * l * b * h
        return f"Volume: {vol} {target_unit}³"
    except Exception as e:
        raise ValueError(f"Error calculating prism volume: {e}")

def ellipsoid(list, target_unit='m'):
    try:
        flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
        a = convert_to_base_unit(flat_list[1], flat_list[0], target_unit)
        b = convert_to_base_unit(flat_list[3], flat_list[2], target_unit)
        c = convert_to_base_unit(flat_list[5], flat_list[4], target_unit)
        vol = (4/3) * math.pi * a * b * c
        return f"Volume: {vol} {target_unit}³"
    except Exception as e:
        raise ValueError(f"Error calculating ellipsoid volume: {e}")