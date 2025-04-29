def convert_to_base_unit(value, from_unit, base_unit='m'):
    conversion_factors = {
        'm': 1,
        'cm': 0.01,
        'mm': 0.001,
        'km': 1000,
        'inch': 0.0254,
        'foot': 0.3048,
        'yard': 0.9144
    }

    if from_unit not in conversion_factors or base_unit not in conversion_factors:
        raise ValueError(f"Unsupported unit: {from_unit} or {base_unit}")

    # Convert from 'from_unit' to meters
    value_in_meters = value * conversion_factors[from_unit]

    # Convert from meters to the desired 'base_unit'
    return value_in_meters / conversion_factors[base_unit]
