from .param_parser_volume import *  # Module to analyze and break down input data into a structured, usable format
from .calculate_volume import *     # Module to calculate volume of different 3D shapes

def volume(*args):
    try:
        # Check if arguments are passed
        if not args:
            raise ValueError("No arguments were passed.")

        # Parse the input arguments
        dimensions, shape = param_parser(args)

        # Map shape names to their respective functions
        shape_functions = {
            "cube": cube,
            "cuboid": cuboid,
            "sphere": sphere,
            "cylinder": cylinder,
            "cone": cone,
            "pyramid": pyramid,
            "hemisphere": hemisphere,
            "prism": prism,
            "ellipsoid": ellipsoid,
        }

        # Get the appropriate function for the shape
        if shape not in shape_functions:
            raise ValueError(f"Unsupported shape: '{shape}'")

        # Call the shape-specific function
        result = shape_functions[shape](dimensions)
        return result

    except ValueError as ve:
        return f"ValueError: {ve}"

    except Exception as e:
        return f"Error: {str(e)}"
