'''testmaterial.py- Tests the Material class'''
import unittest
import math
from material import Material

class TestMaterial(unittest.TestCase):
    '''Tests the basic Material class'''
    def setUp(self):
        self.testmaterial = Material.Material(name="Pure Copper (Annealed)")

    def test_init(self):
        '''Verify Material initialization'''
        self.assertEqual(self.testmaterial.notes, None)
        try:
            self.assertAlmostEqual(self.testmaterial.iacs, 0.0, delta=0.01)
            self.assertAlmostEqual(self.testmaterial.mu_r, 1.0, delta=0.01)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(self.testmaterial.iacs, 0.0, places=1)
            self.assertAlmostEqual(self.testmaterial.mu_r, 1.0, places=1)

    def test_name(self):
        '''Verify setting name of material'''
        matname = "Mithril"
        self.testmaterial.name = matname
        self.assertEqual(self.testmaterial.name, matname)

    def test_iacs(self):
        '''Verify setting conductivity in %IACS of material'''
        pct_iacs = 10.0
        self.testmaterial.iacs = pct_iacs
        try:
            self.assertAlmostEqual(self.testmaterial.iacs, pct_iacs, delta=0.01*pct_iacs)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(self.testmaterial.iacs, pct_iacs, places=1)

    def test_conductivity(self):
        '''Verify setting conductivity in S/m of material'''
        conductivity = 58.0e6
        self.testmaterial.conductivity = conductivity
        try:
            self.assertAlmostEqual(self.testmaterial.conductivity, conductivity, delta=0.01*conductivity)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(self.testmaterial.conductivity, conductivity, places=1)

    def test_mur(self):
        '''Verify setting relative magnetic permeability of material'''
        mur = 111
        self.testmaterial.mu_r = mur
        try:
            self.assertAlmostEqual(self.testmaterial.mu_r, mur, delta=0.01*mur)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(self.testmaterial.mu_r, mur, places=1)

    def test_permeability(self):
        '''Verify setting magnetic permeability of material'''
        perm = 1.57079632679E-4
        self.testmaterial.permeability = perm
        try:
            self.assertAlmostEqual(self.testmaterial.permeability, perm, delta=0.01*perm)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(self.testmaterial.permeability, perm, places=1)

    def test_skindepth(self):
        '''Verify skin depth is approx. 2.09mm for IACS Copper Standard @ 1kHz'''
        freq = 1.0E3
        self.testmaterial.iacs = 100.0
        self.testmaterial.mu_r = 1
        try:
            self.assertAlmostEqual(self.testmaterial.calc_skindepth(freq), 2.09e-3, delta=2.09e-5)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(self.testmaterial.calc_skindepth(freq), 2.09e-3, places=1)

    def test_skindepth_perfect_insulator(self):
        '''Verify that a material with 0 conductivity returns infinite skin depth'''
        freq = 1.03E3
        self.testmaterial.iacs = 0.
        self.testmaterial.mu_r = 1
        self.assertEqual(self.testmaterial.calc_skindepth(freq), float('inf'))

    def test_skindepth_dc_field(self):
        '''Verify that a DC field returns infinite skin depth'''
        freq = 0.
        self.testmaterial.iacs = 0.
        self.testmaterial.mu_r = 1
        self.assertEqual(self.testmaterial.calc_skindepth(freq), float('inf'))

    def test_skindepth_neg_freq(self):
        '''Verify that a negative frequency returns NaN'''
        freq = -11.
        self.testmaterial.iacs = 100.
        self.testmaterial.mu_r = 1
        self.assertTrue(math.isnan(self.testmaterial.calc_skindepth(freq)))

    def test_skindepth_zero_permeability(self):
        '''Verify that a material with 0 permeability returns infinite skin depth'''
        freq = 0.
        self.testmaterial.iacs = 0.
        self.testmaterial.mu_r = 0
        self.assertEqual(self.testmaterial.calc_skindepth(freq), float('inf'))

    def test_frequency(self):
        '''Verify 100Hz creates a depth of attenuation of 1.272mm in Iron (18% IACS mu_r = 150)'''
        skindepth = 1.272e-3
        self.testmaterial.iacs = 18
        self.testmaterial.mu_r = 150
        try:
            self.assertAlmostEqual(self.testmaterial.calc_frequency(skindepth), 100, delta=1)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(self.testmaterial.calc_frequency(skindepth), 100, places=1)

    def test_frequency_zero_delta(self):
        '''Verify that an attenuation depth of zero returns an infinite excitation frequency'''
        skindepth = 0
        self.testmaterial.iacs = 18
        self.testmaterial.mu_r = 150
        self.assertEqual(self.testmaterial.calc_frequency(skindepth), float('inf'))

    def test_frequency_neg_delta(self):
        '''Verify a negative attenuation depth returns NaN for excitation frequency'''
        skindepth = -0.21
        self.testmaterial.iacs = 18
        self.testmaterial.mu_r = 150
        self.assertTrue(math.isnan(self.testmaterial.calc_frequency(skindepth)))

def run():
    '''Runs the suite of tests'''
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMaterial)
    unittest.TextTestRunner(verbosity=2).run(suite)