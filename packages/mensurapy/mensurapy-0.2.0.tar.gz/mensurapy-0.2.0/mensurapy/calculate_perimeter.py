import math
from .unit_converter import * # Module to convert dimensions to base unit 'm'

def square(dictionary, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for key, values in dictionary.items() for item in [key] + values]
    side_value = flat_list[1]
    side_unit = flat_list[0]
    
    # Convert side to target unit (default is meters)
    side = convert_to_base_unit(side_value, side_unit, target_unit)
    
    # Compute perimeter of a square in the target unit
    perimeter = 4 * side
    result = f"Perimeter: {perimeter} {target_unit}"
    # Returns the perimeter of a square.
    return result

def rectangle(list, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
    # '1' and '3' i.e. odd numbers have values and even numbers have keys (units)
    length_value = flat_list[1]
    length_unit = flat_list[0]
    breadth_value = flat_list[3]
    breadth_unit = flat_list[2]
    
    # Convert both to target unit (default is meters)
    length = convert_to_base_unit(length_value, length_unit, target_unit)
    breadth = convert_to_base_unit(breadth_value, breadth_unit, target_unit)
    
    # Compute perimeter in rectangle of the target unit
    perimeter = 2 * (length + breadth)
    result = f"Perimeter: {perimeter} {target_unit}"
    # Returns the perimeter of a rectangle
    return result

def circle(dictionary, target_unit = 'm'):
    
    flat_list = [item for key, values in dictionary.items() for item in [key] + values]
    radius_value = flat_list[1]
    radius_unit = flat_list[0]
    
    # Convert radius to target unit (default is meters)
    radius = convert_to_base_unit(radius_value, radius_unit, target_unit)
    
    # Compute perimeter in square of the target unit
    perimeter = 2 * math.pi * radius
    result = f"Perimeter: {perimeter} {target_unit}"
    # Returns the perimeter of a circle.
    return result

def triangle(list, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
    # '1' and '3' i.e. odd numbers have values and even numbers have keys (units)
    l = len(flat_list)
    
    if l == 2:
        unit = flat_list[0]
        side = convert_to_base_unit(flat_list[1], unit, target_unit)
        perimeter = 3 * side
        result = f"Perimeter: {perimeter} {target_unit}"
        return result
    
    elif l == 4:
        unit_1 = flat_list[0]
        side_1 = convert_to_base_unit(flat_list[1], unit_1, target_unit)
        unit_2 = flat_list[2]
        side_2 = convert_to_base_unit(flat_list[3], unit_2, target_unit)
        perimeter = (2 * side_1) + side_2
        result = f"Perimeter: {perimeter} {target_unit}"
        return result
    
    elif l == 6:
        unit_1 = flat_list[0]
        side_1 = convert_to_base_unit(flat_list[1], unit_1, target_unit)
        unit_2 = flat_list[2]
        side_2 = convert_to_base_unit(flat_list[3], unit_2, target_unit)
        unit_3 = flat_list[4]
        side_3 = convert_to_base_unit(flat_list[5], unit_3, target_unit)
        perimeter = side_1 + side_2 + side_3
        result = f"Perimeter: {perimeter} {target_unit}"
        return result
    
def parallelogram(list, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
    # '1' and '3' i.e. odd numbers have values and even numbers have keys (units)
    length_value = flat_list[1]
    length_unit = flat_list[0]
    breadth_value = flat_list[3]
    breadth_unit = flat_list[2]
    
    # Convert both to target unit (default is meters)
    a = convert_to_base_unit(length_value, length_unit, target_unit)
    b = convert_to_base_unit(breadth_value, breadth_unit, target_unit)
    
    # Compute perimeter in parallelogram of the target unit
    perimeter = 2 * (a + b)
    result = f"Perimeter: {perimeter} {target_unit}"
    # Returns the perimeter of a parallelogram
    return result

def rhombus(dictionary, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for key, values in dictionary.items() for item in [key] + values]
    side_value = flat_list[1]
    side_unit = flat_list[0]
    
    # Convert side to target unit (default is meters)
    side = convert_to_base_unit(side_value, side_unit, target_unit)
    
    # Compute perimeter of a rhombus in the target unit
    perimeter = 4 * side
    result = f"Perimeter: {perimeter} {target_unit}"
    # Returns the perimeter of a rhombus.
    return result

def trapezium(list, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
    # '1' and '3' i.e. odd numbers have values and even numbers have keys (units)
    value_1 = flat_list[1]
    unit_1 = flat_list[0]
    value_2 = flat_list[3]
    unit_2 = flat_list[2]
    value_3 = flat_list[5]
    unit_3 = flat_list[4]
    value_4 = flat_list[7]
    unit_4 = flat_list[6]
    
    # Convert both to target unit (default is meters)
    a = convert_to_base_unit(value_1, unit_1, target_unit)
    b = convert_to_base_unit(value_2, unit_2, target_unit)
    c = convert_to_base_unit(value_3, unit_3, target_unit)
    d = convert_to_base_unit(value_4, unit_4, target_unit)
    
    # Compute perimeter in trapezium of the target unit
    perimeter = a + b + c + d
    result = f"Perimeter: {perimeter} {target_unit}"
    # Returns the perimeter of a trapezium
    return result

def ellipse(list, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
    # '1' and '3' i.e. odd numbers have values and even numbers have keys (units)
    semi_major_axis_value = flat_list[1]
    semi_major_axis_unit = flat_list[0]
    semi_minor_axis_value = flat_list[3]
    semi_minor_axis_unit = flat_list[2]
    
    # Convert both to target unit (default is meters)
    a = convert_to_base_unit(semi_major_axis_value, semi_major_axis_unit, target_unit)
    b = convert_to_base_unit(semi_minor_axis_value, semi_minor_axis_unit, target_unit)
    
    # Compute perimeter in rectangle of the target unit
    perimeter = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))
    result = f"Perimeter: {perimeter} {target_unit}"
    # Returns the perimeter of a rectangle
    return result

def cube(dictionary, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for key, values in dictionary.items() for item in [key] + values]
    side_value = flat_list[1]
    side_unit = flat_list[0]
    
    # Convert side to target unit (default is meters)
    side = convert_to_base_unit(side_value, side_unit, target_unit)
    
    # Compute perimeter of a cube in the target unit
    perimeter = 12 * side
    result = f"Perimeter: {perimeter} {target_unit}"
    # Returns the perimeter of a cube.
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
    
    # Compute perimeter in cuboid of the target unit
    perimeter = 4 * (l + b + h)
    result = f"Perimeter: {perimeter} {target_unit}"
    # Returns the perimeter of a cuboid
    return result

def sphere(dictionary, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for key, values in dictionary.items() for item in [key] + values]
    radius = flat_list[1]
    radius_unit = flat_list[0]
    result = " "
    # Returns the empty string
    return result

def cylinder(list, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
    # '1' and '3' i.e. odd numbers have values and even numbers have keys (units)
    l = len(flat_list)
    
    if l == 2:
        unit = flat_list[0]
        r = convert_to_base_unit(flat_list[1], unit, target_unit)
        perimeter = 2 * math.pi * r
        result = f"Base Perimeter: {perimeter} {target_unit}"
        return result
    
    elif l == 4:
        r_unit = flat_list[0]
        r = convert_to_base_unit(flat_list[1], r_unit, target_unit)
        h_unit = flat_list[2]
        h = convert_to_base_unit(flat_list[3], h_unit, target_unit)
        perimeter = 2 * ((2 * math.pi * r) + h)
        result = f"Total linear boundary: {perimeter} {target_unit}"
        return result
    
def cone(list, target_unit = 'm'):
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
    # '1' and '3' i.e. odd numbers have values and even numbers have keys (units)
    l = len(flat_list)
    
    if l == 2:
        unit = flat_list[0]
        r = convert_to_base_unit(flat_list[1], unit, target_unit)
        perimeter = 2 * math.pi * r
        result = f"Base perimeter: {perimeter} {target_unit}"
        return result
    
    elif l == 4:
        r_unit = flat_list[0]
        r = convert_to_base_unit(flat_list[1], r_unit, target_unit)
        l_unit = flat_list[2]
        l = convert_to_base_unit(flat_list[3], l_unit, target_unit)
        perimeter = 2 * math.pi * r + l
        result = f"Total boundary- {perimeter} {target_unit}"
        return result
    
def pyramid(list, target_unit = 'm'):
    
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for d in list for key, values in d.items() for item in [key] + values]
    # '1' and '3' i.e. odd numbers have values and even numbers have keys (units)
    l = len(flat_list)
    
    if l == 2:
        unit = flat_list[0]
        side = convert_to_base_unit(flat_list[1], unit, target_unit)
        perimeter = 2 * math.pi * side
        result = f"Base perimeter: {perimeter} {target_unit}"
        return result
    
    elif l == 4:
        side_unit = flat_list[0]
        side = convert_to_base_unit(flat_list[1], side_unit, target_unit)
        l_unit = flat_list[2]
        l = convert_to_base_unit(flat_list[3], l_unit, target_unit)
        perimeter = 4 * side + 4 * l
        result = f"Total boundary- {perimeter} {target_unit}"
        return result

def hemisphere(dictionary, target_unit = 'm'):
    # Structure the recieved data in a flattened list displaying keys and values
    flat_list = [item for key, values in dictionary.items() for item in [key] + values]
    radius_value = flat_list[1]
    radius_unit = flat_list[0]
    
    # Convert side to target unit (default is meters)
    r = convert_to_base_unit(radius_value, radius_unit, target_unit)
    
    # Compute perimeter of a hemisphere in the target unit
    perimeter = 2 * math.pi * r
    result = f"Perimeter: {perimeter} {target_unit}"
    # Returns the perimeter of a hemisphere.
    return result
    






