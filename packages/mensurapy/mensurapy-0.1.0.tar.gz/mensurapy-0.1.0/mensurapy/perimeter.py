from .param_parser_perimeter import *  # Module to analyze and break down input data into a structured, usable format
from .calculate_perimeter import * # Module to calculate perimeter of different polygons

def perimeter(*args):
    # First check if arguments are having values else display error
    if not args:  # Check if args is empty
        return "Error: No arguments were passed"
    else:
        dimensions, shape = param_parser(args) # Call param_parser method to recieve parsed users inputs for calculation
        
        if shape == "square":
            result = square(dimensions)
            return result
        
        if shape == "rectangle":
            result = rectangle(dimensions)
            return result
        
        if shape == "circle":
            result = circle(dimensions)
            return result
        
        if shape == "triangle":
            result = triangle(dimensions)
            return result
        
        if shape == "parallelogram":
            result = parallelogram(dimensions)
            return result
        
        if shape == "rhombus":
            result = rhombus(dimensions)
            return result
        
        if shape == "trapezium":
            result = trapezium(dimensions)
            return result
        
        if shape == "ellipse":
            result = ellipse(dimensions)
            return result
        
        if shape == "cube":
            result = cube(dimensions)
            return result
        
        if shape == "cuboid":
            result = cuboid(dimensions)
            return result
        
        if shape == "sphere":
            result = square(dimensions)
            
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