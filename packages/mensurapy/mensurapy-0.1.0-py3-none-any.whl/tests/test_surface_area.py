import unittest
from mensurapy.surface_area import surface_area

class TestSurfaceAreaFunction(unittest.TestCase):
    def test_empty_parameter(self):
        self.assertEqual(surface_area(), "Error: No arguments were passed")
        
    def test_surface_area_cube(self):
        self.assertEqual(surface_area("cube", "3m"), " \n Total Surface Area: 54.0 m² \n Lateral Surface Area: 36.0 m² \n Base Area: 9.0 m²")
    
    def test_1_surface_area_cuboid(self):
        self.assertEqual(surface_area("cuboid", "4m", "3m", "2m"), " \n Total Surface Area: 52.0 m² \n Lateral Surface Area: 28.0 m² \n Base Area: 12.0 m²")
    
    def test_2_surface_area_cuboid(self):
        self.assertEqual(surface_area("cuboid", "4cm", "3m", "2cm"), " \n Total Surface Area: 0.3616 m² \n Lateral Surface Area: 0.1216 m² \n Base Area: 0.12 m²")
    
    def test_surface_area_sphere(self):
        self.assertEqual(surface_area("sphere", "3m"), " \n Total Surface Area: 113.09733552923255 m² \n Curved Surface Area: 113.09733552923255 m²")
    
    def test_1_surface_area_cylinder(self):
        self.assertEqual(surface_area("cylinder", "5m", "10m"), " \n Total Surface Area: 471.23889803846896 m² \n Lateral Surface Area: 314.1592653589793 m² \n Base Area: 78.53981633974483 m²")
        
    def test_2_surface_area_cylinder(self):
        self.assertEqual(surface_area("cylinder", "5cm", "10m"), " \n Total Surface Area: 3.1573006168577424 m² \n Lateral Surface Area: 3.141592653589793 m² \n Base Area: 0.007853981633974483 m²")
    
    def test_1_surface_area_cone(self):
        self.assertEqual(surface_area("cone", "4m", "3m"), " \n Total Surface Area: 113.09733552923255 m² \n Curved Surface Area: 62.83185307179586 m² \n Base Area: 50.26548245743669 m²")
    
    def test_2_surface_area_cone(self):
        self.assertEqual(surface_area("cone", "4m", "3cm"), " \n Total Surface Area: 100.53237861168765 m² \n Curved Surface Area: 50.26689615425097 m² \n Base Area: 50.26548245743669 m²")
    
    def test_1_surface_area_cuboid(self):
        self.assertEqual(surface_area("pyramid", "6m", "5m", "4m"), " \n Total Surface Area: 96.0 m² \n Lateral Surface Area: 60.0 m² \n Base Area: 36.0 m²")
    
    def test_surface_area_hemisphere(self):
        self.assertEqual(surface_area("sphere", "3m"), " \n Total Surface Area: 113.09733552923255 m² \n Curved Surface Area: 113.09733552923255 m²")    

if __name__ == '__main__':
    unittest.main()