import unittest
from mensurapy.perimeter import perimeter

class TestPerimeterFunction(unittest.TestCase):
    def test_empty_parameter(self):
        self.assertEqual(perimeter(), "Error: No arguments were passed")
        
    def test_1_perimeter_square(self):
        self.assertEqual(perimeter("square", "3m"), "Perimeter: 12.0 m")
        
    def test_2_perimeter_square(self):
        self.assertEqual(perimeter("square", "3cm"), "Perimeter: 0.12 m")
        
    def test_1_perimeter_rectangle(self):
        self.assertEqual(perimeter("rectangle", "3m", "4m"), "Perimeter: 14.0 m")

    def test_2_perimeter_rectangle(self):
        self.assertEqual(perimeter("rectangle", "3cm", "4m"), "Perimeter: 8.06 m")
        
    def test_1_perimeter_circle(self):
        self.assertEqual(perimeter("circle", "3m"), "Perimeter: 18.84955592153876 m")    

    def test_2_perimeter_circle(self):
        self.assertEqual(perimeter("circle", "3mm"), "Perimeter: 0.01884955592153876 m")
        
    def test_1_perimeter_triangle(self):
        self.assertEqual(perimeter("triangle", "4m"), "Perimeter: 12.0 m")
        
    def test_2_perimeter_triangle(self):
        self.assertEqual(perimeter("triangle", "4m", "2cm", "4m"), "Perimeter: 8.02 m")
        
    def test_3_perimeter_triangle(self):
        self.assertEqual(perimeter("triangle", "4m", "2m"), "Perimeter: 10.0 m")
    
    def test_4_perimeter_triangle(self):
        self.assertEqual(perimeter("triangle", "4m", "2cm"), "Perimeter: 8.02 m")
        
    def test_perimeter_parallelogram(self):
        self.assertEqual(perimeter("parallelogram", "4cm", "2m"), "Perimeter: 4.08 m")
    
    def test_perimeter_rhombus(self):
        self.assertEqual(perimeter("rhombus", "4m"), "Perimeter: 16.0 m")
        
    def test_perimeter_trapezium(self):
        self.assertEqual(perimeter("trapezium", "4m", "2m", "4m", "3m"), "Perimeter: 13.0 m")
        
    def test_perimeter_ellipse(self):
        self.assertEqual(perimeter("triangle", "4m", "3m"), "Perimeter: 11.0 m")
        
    def test_1_perimeter_cube(self):
        self.assertEqual(perimeter("cube", "3m"), "Perimeter: 36.0 m")
        
    def test_2_perimeter_cube(self):
        self.assertEqual(perimeter("cube", "3cm"), "Perimeter: 0.36 m")
        
    def test_1_perimeter_cuboid(self):
        self.assertEqual(perimeter("cuboid", "5m", "3m", "2m"), "Perimeter: 40.0 m")
        
    def test_2_perimeter_cuboid(self):
        self.assertEqual(perimeter("cuboid", "5cm", "3cm", "2cm"), "Perimeter: 0.4 m")
        
    #def test_perimeter_sphere(self):
        #self.assertEqual(perimeter("sphere", "5m"), "AssertionError: None != 'Error: Perimeter not defined for sphere'")
        
    def test_1_perimeter_cylinder(self):
        self.assertEqual(perimeter("cylinder", "3m"), "Base Perimeter: 18.84955592153876 m")
        
    def test_2_perimeter_cylinder(self):
        self.assertEqual(perimeter("cylinder", "3m", "4m"), "Total linear boundary: 45.69911184307752 m")
        
    def test_3_perimeter_cylinder(self):
        self.assertEqual(perimeter("cylinder", "3cm", "10cm"), "Total linear boundary: 0.5769911184307752 m")
        
    def test_1_perimeter_cone(self):
        self.assertEqual(perimeter("cone", "4m"), "Base perimeter: 25.132741228718345 m")
        
    def test_2_perimeter_cone(self):
        self.assertEqual(perimeter("cone", "4m", "6m"), "Total boundary- 31.132741228718345 m")
        
    def test_perimeter_cone(self):
        self.assertEqual(perimeter("pyramid", "6m", "5m"), "Total boundary- 44.0 m")
        
    def test_perimeter_hemisphere(self):
        self.assertEqual(perimeter("hemisphere", "5m"), "Perimeter: 31.41592653589793 m")
        
if __name__ == '__main__':
    unittest.main()