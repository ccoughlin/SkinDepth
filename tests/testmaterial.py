'''Tests the Material class'''
import unittest
from material import Material

class TestMaterial(unittest.TestCase):
    def setUp(self):
        self.testmaterial = Material.Material(name="Pure Copper (Annealed)")

    def test_init(self):
        '''Verify Material initialization'''
        self.assertEqual(self.testmaterial.notes,None)
        self.assertAlmostEqual(self.testmaterial.iacs,0.0,delta=0.01)
        self.assertAlmostEqual(self.testmaterial.mu_r,1.0,delta=0.01)

    '''The next few tests verify setting members in Materials'''
    def test_name(self):
        matname = "Mithril"
        self.testmaterial.name = matname
        self.assertEqual(self.testmaterial.name, matname)

    def test_iacs(self):
        pct_iacs = 10.0
        self.testmaterial.iacs = pct_iacs
        self.assertAlmostEqual(self.testmaterial.iacs,pct_iacs,delta=0.01)

    def test_conductivity(self):
        conductivity = 58.0e6
        self.testmaterial.conductivity = conductivity
        self.assertAlmostEqual(self.testmaterial.conductivity,conductivity,delta=0.01)

    def test_mur(self):
        mur = 111
        self.testmaterial.mu_r = mur
        self.assertAlmostEqual(self.testmaterial.mu_r,mur,delta=0.01)

    def test_permeability(self):
        perm = 1.57079632679E-4
        self.testmaterial.permeability = perm
        self.assertAlmostEqual(self.testmaterial.permeability,perm,delta=0.01)

    def test_skindepth(self):
        '''Verify skin depth is approx. 2.09mm for IACS Copper Standard @ 1kHz'''
        freq = 1.0E3
        self.testmaterial.iacs = 100.0
        self.testmaterial.mu_r = 1
        self.assertAlmostEqual(self.testmaterial.calc_skindepth(freq),2.09e-3,delta=0.01)

    def test_frequency(self):
        '''Verify 100Hz creates a depth of attenuation of 1.272mm in Iron (18% IACS mu_r = 150)'''
        skindepth = 1.272e-3
        self.testmaterial.iacs = 18
        self.testmaterial.mu_r = 150
        self.assertAlmostEqual(self.testmaterial.calc_frequency(skindepth), 100, delta = 1)

def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMaterial)
    unittest.TextTestRunner(verbosity=2).run(suite)