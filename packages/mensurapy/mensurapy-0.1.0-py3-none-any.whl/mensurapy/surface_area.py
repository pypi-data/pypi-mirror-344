from .param_parser_surface_area import *  # Module to analyze and break down input data into a structured, usable format
from .calculate_surface_area import * # Module to calculate surface area of different polygons

def surface_area(*args):
    # First check if arguments are having values else display error
    if not args:  # Check if args is empty
        return "Error: No arguments were passed"
    else:
        dimensions, shape = param_parser(args) # Call param_parser method to recieve parsed users inputs for calculation
        
        if shape == "cube":
            result = cube(dimensions)
            return result
        
        if shape == "cuboid":
            result = cuboid(dimensions)
            return result
        
        if shape == "sphere":
            result = sphere(dimensions)
            return result
        
        if shape == "cylinder":
            result = cylinder(dimensions)
            return result
        
        if shape == "cone":
            result = cone(dimensions)
            return result
        
        if shape == "pyramid":
            result = pyramid(dimensions)
            return result
        
        if shape == "hemisphere":
            result = hemisphere(dimensions)
            return result