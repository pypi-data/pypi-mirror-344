# Validate 
def cube_param_validator(args):
    if len(args) == 2:
        return True
    else:
        return False
    
def cuboid_param_validator(args):
    if len(args) == 4:
        return True 
    else:
        return False
    
def sphere_param_validator(args):
    if len(args) == 2:
        return True
    else:
        return False
    
def cylinder_param_validator(args):
    if len(args) == 3:
        return True
    else:
        return False
    
def cone_param_validator(args):
    if len(args) == 3:
        return True
    else:
        return False
    
def pyramid_param_validator(args):
    if len(args) == 4:
        return True  
    elif len(args) == 2:
        return True 
    else:
        return False
    
def hemisphere_param_validator(args):
    if len(args) == 2:
        return True
    else:
        return False