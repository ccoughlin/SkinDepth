__author__ = 'Chris'
'''Tests the basic controller'''
import unittest
from platform import SkinDepthController
from material import Material

class TestSkinDepthController(unittest.TestCase):
    '''Tests the basic controller for SkinDepth'''

    def setUp(self):
        self.testctrl = SkinDepthController.SkinDepthController(":memory:")
        self.testctrl.open()

    def test_addone(self):
        '''Testing addition of a material to the database'''
        testmaterial_dict={"name":"Iron",
                           "notes":"Pure Iron",
                           "iacs":18,
                           "mu_r":150}
        self.testctrl.add(testmaterial_dict)
        retrieved_material = self.testctrl.db.retrieve("Iron")
        self.assertEqual(testmaterial_dict["name"], retrieved_material.name)
        self.assertEqual(testmaterial_dict["notes"], retrieved_material.notes)
        self.assertAlmostEqual(testmaterial_dict["iacs"] , retrieved_material.iacs, delta=0.01)
        self.assertAlmostEqual(testmaterial_dict["mu_r"], retrieved_material.mu_r, delta=0.01)

    def test_fetchone(self):
        '''Testing retrieval of one material from the database'''
        testmaterial = Material.Material(name="Iron", sigma_iacs = 18, mu_rel = 150, notes = "Pure Iron")
        self.testctrl.db.add(testmaterial)
        retrieved_material = self.testctrl.fetch("Iron")
        self.assertEqual(testmaterial.name, retrieved_material["name"])
        self.assertEqual(testmaterial.notes, retrieved_material["notes"])
        self.assertAlmostEqual(testmaterial.iacs , retrieved_material["iacs"], delta = 0.01)
        self.assertAlmostEqual(testmaterial.mu_r, retrieved_material["mu_r"], delta = 0.01)

    def test_fetchlist(self):
        '''Testing retrieval of the complete list of materials from the database'''
        iron = Material.Material(name="Iron", sigma_iacs = 18, mu_rel = 150, notes = "Pure Iron")
        copper = Material.Material(name="Copper", sigma_iacs = 100, mu_rel = 1, notes = "Pure Annealed Copper")
        aluminum = Material.Material(name="Aluminum", sigma_iacs = 61, mu_rel = 1, notes = "Unalloyed Pure Aluminum")
        cobalt = Material.Material(name="Cobalt", sigma_iacs = 27.6, mu_rel = 70, notes ="Relative permeability can range between 70-250")
        water = Material.Material(name="Water", sigma_iacs = 4.353e-10, mu_rel = 1, notes ="Tap water")
        thematerials=[iron,copper,aluminum,cobalt,water]
        thematerialnames=[iron.name,copper.name,aluminum.name,cobalt.name,water.name]
        for amat in thematerials:
            self.testctrl.db.add(amat)
        materials_list = self.testctrl.fetchlist()
        self.assertEqual(len(thematerialnames),len(materials_list))
        self.assertItemsEqual(thematerialnames, materials_list)

    def test_deleteone(self):
        '''Testing deletion of one material from the database'''
        testmaterial = Material.Material(name="Iron", sigma_iacs = 18, mu_rel = 150, notes = "Pure Iron")
        self.testctrl.db.add(testmaterial)
        self.testctrl.remove("Iron")
        retrieved_material = self.testctrl.fetch("Iron")
        self.assertIsNone(retrieved_material)

    def test_undo(self):
        '''Testing database rollback'''
        testmaterial = Material.Material(name="Iron", sigma_iacs = 18, mu_rel = 150, notes = "Pure Iron")
        self.testctrl.db.add(testmaterial)
        self.testctrl.update()
        self.testctrl.remove("Iron")
        retrieved_material = self.testctrl.fetch("Iron")
        self.assertIsNone(retrieved_material)
        self.testctrl.undo()
        retrieved_material = self.testctrl.fetch("Iron")
        self.assertEqual(testmaterial.name, retrieved_material["name"])
        self.assertEqual(testmaterial.notes, retrieved_material["notes"])
        self.assertAlmostEqual(testmaterial.iacs , retrieved_material["iacs"], delta = 0.01)
        self.assertAlmostEqual(testmaterial.mu_r, retrieved_material["mu_r"], delta = 0.01)

    def test_calcdelta(self):
        '''Verifying attenuation depth calculation'''
        testmaterial = Material.Material(name="Iron", sigma_iacs = 18, mu_rel = 150, notes = "Pure Iron")
        self.testctrl.db.add(testmaterial)
        skindepth = self.testctrl.calcdelta(materialname="Iron",frequency = 1138)
        self.assertAlmostEqual(testmaterial.calc_skindepth(1138),skindepth, delta = 0.01)
        nomaterial = self.testctrl.calcdelta(materialname="Adamantium", frequency = 1)
        self.assertIsNone(nomaterial)

    def test_calcfrequency(self):
        '''Verifying excitation frequency calculation'''
        testmaterial = Material.Material(name="Iron", sigma_iacs = 18, mu_rel = 150, notes = "Pure Iron")
        self.testctrl.db.add(testmaterial)
        freq = self.testctrl.calcfrequency(materialname="Iron", skindepth=0.75)
        self.assertAlmostEqual(testmaterial.calc_frequency(attenuation=0.75), freq, delta = 0.01)

    def test_exportdb(self):
        '''Testing export of the database as a SQL script'''
        testmaterial_dict={"name":"Iron",
                           "notes":"Pure Iron",
                           "iacs":18,
                           "mu_r":150}
        self.testctrl.add(testmaterial_dict)
        self.testctrl.update()
        self.testctrl.exportsql("bert.sql")
        file_db = SkinDepthController.SkinDepthController(":memory:")
        file_db.importsql("bert.sql")
        retrieved_material = file_db.fetch("Iron")
        self.assertEqual(testmaterial_dict["name"], retrieved_material["name"])
        self.assertEqual(testmaterial_dict["notes"], retrieved_material["notes"])
        self.assertAlmostEqual(testmaterial_dict["iacs"] , retrieved_material["iacs"], delta = 0.01)
        self.assertAlmostEqual(testmaterial_dict["mu_r"], retrieved_material["mu_r"], delta = 0.01)

    def test_savecopyfromfile(self):
        '''Testing database file copies from storage'''
        dbfile_ctrl = SkinDepthController.SkinDepthController("test.db")
        dbfile_ctrl.open()
        iron = Material.Material(name="Iron", sigma_iacs = 18, mu_rel = 150, notes = "Pure Iron")
        iron_dict = {"name":iron.name,
                    "notes":iron.notes,
                    "iacs":iron.iacs,
                    "mu_r":iron.mu_r}
        dbfile_ctrl.add(iron_dict)
        dbfile_ctrl.update()
        dbfile_ctrl.savecopy("copyoftest.db")
        dbcopy_ctrl = SkinDepthController.SkinDepthController("copyoftest.db")
        dbcopy_ctrl.open()
        ironcopy_dict = dbcopy_ctrl.fetch("Iron")
        self.assertEqual(iron.name, ironcopy_dict["name"])
        self.assertEqual(iron.notes, ironcopy_dict["notes"])
        self.assertAlmostEqual(iron.iacs , ironcopy_dict["iacs"], delta = 0.01)
        self.assertAlmostEqual(iron.mu_r, ironcopy_dict["mu_r"], delta = 0.01)

    def test_savecopyfrommemory(self):
        '''Testing database file copies from :memory:'''
        dbfile_ctrl = SkinDepthController.SkinDepthController(":memory:")
        dbfile_ctrl.open()
        iron = Material.Material(name="Iron", sigma_iacs = 18, mu_rel = 150, notes = "Pure Iron")
        iron_dict = {"name":iron.name,
                    "notes":iron.notes,
                    "iacs":iron.iacs,
                    "mu_r":iron.mu_r}
        dbfile_ctrl.add(iron_dict)
        dbfile_ctrl.update()
        dbfile_ctrl.savecopy("copyoftest.db")
        dbcopy_ctrl = SkinDepthController.SkinDepthController("copyoftest.db")
        dbcopy_ctrl.open()
        ironcopy_dict = dbcopy_ctrl.fetch("Iron")
        self.assertEqual(iron.name, ironcopy_dict["name"])
        self.assertEqual(iron.notes, ironcopy_dict["notes"])
        self.assertAlmostEqual(iron.iacs , ironcopy_dict["iacs"], delta = 0.01)
        self.assertAlmostEqual(iron.mu_r, ironcopy_dict["mu_r"], delta = 0.01)

    def tearDown(self):
        pass

def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSkinDepthController)
    unittest.TextTestRunner(verbosity=2).run(suite)