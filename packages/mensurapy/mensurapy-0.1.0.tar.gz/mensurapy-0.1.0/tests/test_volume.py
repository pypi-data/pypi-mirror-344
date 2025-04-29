import unittest
from mensurapy.volume import volume

class TestVolumeFunction(unittest.TestCase):

    def test_volume_cube(self):
        self.assertEqual(volume("cube", "3m"), "Volume: 27.0 m³")
        self.assertEqual(volume("cube", "300cm"), "Volume: 27.0 m³")
        self.assertEqual(volume("cube", "3000mm"), "Volume: 27.0 m³")

    def test_volume_cuboid(self):
        self.assertEqual(volume("cuboid", "2m", "3m", "4m"), "Volume: 24.0 m³")
        self.assertEqual(volume("cuboid", "200cm", "300cm", "400cm"), "Volume: 24.0 m³")
        self.assertEqual(volume("cuboid", "2000mm", "3000mm", "4000mm"), "Volume: 24.0 m³")

    def test_volume_sphere(self):
        self.assertEqual(volume("sphere", "3m"), "Volume: 113.09733552923254 m³")
        self.assertEqual(volume("sphere", "300cm"), "Volume: 113.09733552923254 m³")
        self.assertEqual(volume("sphere", "3000mm"), "Volume: 113.09733552923254 m³")

    def test_volume_cylinder(self):
        self.assertEqual(volume("cylinder", "2m", "3m"), "Volume: 37.69911184307752 m³")
        self.assertEqual(volume("cylinder", "200cm", "300cm"), "Volume: 37.69911184307752 m³")
        self.assertEqual(volume("cylinder", "2000mm", "3000mm"), "Volume: 37.69911184307752 m³")

    def test_volume_cone(self):
        self.assertEqual(volume("cone", "2m", "3m"), "Volume: 12.566370614359172 m³")
        self.assertEqual(volume("cone", "200cm", "300cm"), "Volume: 12.566370614359172 m³")
        self.assertEqual(volume("cone", "2000mm", "3000mm"), "Volume: 12.566370614359172 m³")

    def test_volume_hemisphere(self):
        self.assertEqual(volume("hemisphere", "3m"), "Volume: 56.54866776461627 m³")
        self.assertEqual(volume("hemisphere", "300cm"), "Volume: 56.54866776461627 m³")
        self.assertEqual(volume("hemisphere", "3000mm"), "Volume: 56.54866776461627 m³")

    def test_volume_pyramid(self):
        self.assertEqual(volume("pyramid", "3m", "4m", "5m"), "Volume: 20.0 m³")
        self.assertEqual(volume("pyramid", "300cm", "400cm", "500cm"), "Volume: 20.0 m³")
        self.assertEqual(volume("pyramid", "3000mm", "4000mm", "5000mm"), "Volume: 20.0 m³")

    def test_volume_prism(self):
        self.assertEqual(volume("prism", "3m", "4m", "10m" ), "Volume: 60.0 m³")
        self.assertEqual(volume("prism", "300cm", "400cm", "1000cm"), "Volume: 60.0 m³")
        self.assertEqual(volume("prism", "3000mm", "4000mm", "10000mm"), "Volume: 60.0 m³")

    def test_volume_ellipsoid(self):
        self.assertEqual(volume("ellipsoid", "2m", "3m", "4m"), "Volume: 100.53096491487338 m³")
        self.assertEqual(volume("ellipsoid", "200cm", "300cm", "400cm"), "Volume: 100.53096491487338 m³")
        self.assertEqual(volume("ellipsoid", "2000mm", "3000mm", "4000mm"), "Volume: 100.53096491487338 m³")

    def test_invalid_shape(self):
        self.assertEqual(volume("invalidshape", "3m"), "Error: Error in param_parser: Invalid shape 'invalidshape' provided.")

    def test_no_arguments(self):
        self.assertEqual(volume(), "ValueError: No arguments were passed.")

if __name__ == "__main__":
    unittest.main()
