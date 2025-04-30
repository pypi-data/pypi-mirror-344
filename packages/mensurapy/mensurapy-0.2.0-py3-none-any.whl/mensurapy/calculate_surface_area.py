import math
from .unit_converter import * # Module to convert dimensions to base unit 'm'

def cube(dictionary, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for key, values in dictionary.items() for item in [key] + values]
    side_value = flat_list[1]
    side_unit = flat_list[0]
    
    # Convert side to target unit (default is meters)
    side = convert_to_base_unit(side_value, side_unit, target_unit)
    
    # Compute surface area in cube of the target unit
    TSA = 6 * side * side
    LSA = 4 * side * side
    BA = side * side
    result = f" \n Total Surface Area: {TSA} {target_unit}² \n Lateral Surface Area: {LSA} {target_unit}² \n Base Area: {BA} {target_unit}²"
    # Returns the surface area of a cube
    return result

def cuboid(list, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
    # '1' and '3' i.e. odd numbers have values and even numbers have keys (units)
    length_value = flat_list[1]
    length_unit = flat_list[0]
    breadth_value = flat_list[3]
    breadth_unit = flat_list[2]
    height_value = flat_list[5]
    height_unit = flat_list[4]
    
    # Convert both to target unit (default is meters)
    l = convert_to_base_unit(length_value, length_unit, target_unit)
    b = convert_to_base_unit(breadth_value, breadth_unit, target_unit)
    h = convert_to_base_unit(height_value, height_unit, target_unit)
    
    # Compute surface area in cuboid of the target unit
    TSA = 2 * ((l * b) + (b * h) + (h * l))
    LSA = 2 * h * (l + b)
    BA = l * b
    result = f" \n Total Surface Area: {TSA} {target_unit}² \n Lateral Surface Area: {LSA} {target_unit}² \n Base Area: {BA} {target_unit}²"
    # Returns the surface area of a cuboid
    return result

def sphere(dictionary, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for key, values in dictionary.items() for item in [key] + values]
    radius_value = flat_list[1]
    radius_unit = flat_list[0]
    
    # Convert side to target unit (default is meters)
    r = convert_to_base_unit(radius_value, radius_unit, target_unit)
    
    # Compute surface area in sphere of the target unit
    TSA = 4 * math.pi * r * r
    CSA = 4 * math.pi * r * r
    result = f" \n Total Surface Area: {TSA} {target_unit}² \n Curved Surface Area: {CSA} {target_unit}²"
    # Returns the surface area of a sphere
    return result

def cylinder(list, target_unit = 'm'):

    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
    # '1' and '3' i.e. odd numbers have values and even numbers have keys (units)
    radius_value = flat_list[1]
    radius_unit = flat_list[0]
    height_value = flat_list[3]
    height_unit = flat_list[2]
    
    # Convert both to target unit (default is meters)
    r = convert_to_base_unit(radius_value, radius_unit, target_unit)
    h = convert_to_base_unit(height_value, height_unit, target_unit)
    
    # Compute surface area in cylinder of the target unit
    TSA = 2 * math.pi * r * (r + h)
    CSA = 2 * math.pi * r * h
    BA = math.pi * r * r
    result = f" \n Total Surface Area: {TSA} {target_unit}² \n Lateral Surface Area: {CSA} {target_unit}² \n Base Area: {BA} {target_unit}²"
    # Returns the surface area of a cylinder
    return result

def cone(list, target_unit = 'm'):

    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
    # '1' and '3' i.e. odd numbers have values and even numbers have keys (units)
    radius_value = flat_list[1]
    radius_unit = flat_list[0]
    height_value = flat_list[3]
    height_unit = flat_list[2]
    
    # Convert both to target unit (default is meters)
    r = convert_to_base_unit(radius_value, radius_unit, target_unit)
    h = convert_to_base_unit(height_value, height_unit, target_unit)
    # slant height
    l = math.sqrt((r * r) + (h * h))
    
    # Compute surface area in cone of the target unit
    TSA = math.pi * r * (l + r) 
    CSA = math.pi * r * l
    BA = math.pi * r * r
    result = f" \n Total Surface Area: {TSA} {target_unit}² \n Curved Surface Area: {CSA} {target_unit}² \n Base Area: {BA} {target_unit}²"
    # Returns the surface area of a cone
    return result

def pyramid(list, target_unit = 'm'):

    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
    # '1' and '3' i.e. odd numbers have values and even numbers have keys (units)
    l = len(flat_list)
    
    if l == 2:
        unit = flat_list[0]
        side = convert_to_base_unit(flat_list[1], unit, target_unit)
        TSA = math.sqrt(3) * side ** 2
        BA = (math.sqrt(3) / 4) * side ** 2
        result = f" \n Total Surface Area: {TSA} {target_unit}² \n Base Area: {BA} {target_unit}²"
        return result
        
    elif l == 6:
        side_unit, side_value = flat_list[0], flat_list[1]
        slant_height_unit, slant_height_value = flat_list[2], flat_list[3]
        height_unit, height_value = flat_list[4], flat_list[5]
        s = convert_to_base_unit(side_value, side_unit, target_unit)
        l = convert_to_base_unit(slant_height_value, slant_height_unit, target_unit)
        h = convert_to_base_unit(height_value, height_unit, target_unit)
        TSA = (2 * s * l) + (s * s)
        LSA = 2 * s * l
        BA = s * s
        result = f" \n Total Surface Area: {TSA} {target_unit}² \n Lateral Surface Area: {LSA} {target_unit}² \n Base Area: {BA} {target_unit}²"
        return result
    
def hemisphere(dictionary, target_unit = 'm'):
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for key, values in dictionary.items() for item in [key] + values]
    radius_value = flat_list[1]
    radius_unit = flat_list[0]
    
    # Convert side to target unit (default is meters)
    r = convert_to_base_unit(radius_value, radius_unit, target_unit)
    
    # Compute surface area of hemisphere of the target unit
    TSA = 3 * math.pi * r * r
    CSA = 3 * math.pi * r * r
    result = f" \n Total Surface Area: {TSA} {target_unit}² \n Curved Surface Area: {CSA} {target_unit}²"
    # Returns the surface area of a hemisphere
    return result
    