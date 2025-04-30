from .param_parser_area import *  # Module to analyze and break down input data into a structured, usable format
from .calculate_area import * # Module to calculate area of different polygons

def area(*args):
    try:
        
        # First check if arguments are having values else display error
        if not args:  # Check if args is empty
            return("Error: No arguments were passed")
        
        # Parse arguments
        try:
            dimensions, shape = param_parser(args) # Call param_parser method to recieve parsed users inputs for calculation
        except Exception as e:
            return f"Error in parameter parsing: {e}"
        
        # Calculate area based on shape
        try:
            if shape == "square":
                result = square(dimensions)
                return result
            
            elif shape == "rectangle":
                result = rectangle(dimensions)
                return result
            
            elif shape == "circle":
                result = circle(dimensions)
                return result
            
            elif shape == "triangle":
                result = triangle(dimensions)
                return result
            
            elif shape == "parallelogram":
                result = parallelogram(dimensions)
                return result

            elif shape == "rhombus":
                result = rhombus(dimensions)
                return result
            
            elif shape == "trapezium":
                result = trapezium(dimensions)
                return result
            
            elif shape == "ellipse":
                result = ellipse(dimensions)
                return result
            
            else:
                return f"Error: Unsupported shape '{shape}'" 
            
        except Exception as e:
            return f"Error during area calculation for shape '{shape}': {e}"       
    
    except Exception as e:
        return f"Unexpected error: {e}"