'''Tests the sqlite3 interface'''
import tempfile
import unittest
from material import MaterialDB
from material import Material

class TestMaterialDB(unittest.TestCase):
    '''Tests the SQLITE3 database for SkinDepth'''

    def setUp(self):
        self.testdb = MaterialDB.MaterialDB(":memory:")
        self.testdb.connect()
        self.testdb.create()

    def test_badconnection(self):
        '''Verify throws OperationalError if unable to connect to database'''
        import sqlite3

        atestdb = MaterialDB.MaterialDB("x:/werd/test.db")
        with self.assertRaises(sqlite3.OperationalError):
            atestdb.connect()
            atestdb.create()

    def test_add(self):
        '''Verify adding / revising materials'''
        testmaterial = Material.Material(name="Iron", sigma_iacs=18, mu_rel=150, notes="Pure Iron")
        self.testdb.add(testmaterial)
        retrieved_material = self.testdb.retrieve("Iron")
        self.assertEqual(testmaterial.name, retrieved_material.name)
        self.assertEqual(testmaterial.notes, retrieved_material.notes)
        self.assertAlmostEqual(testmaterial.iacs, retrieved_material.iacs, delta=0.01)
        self.assertAlmostEqual(testmaterial.mu_r, retrieved_material.mu_r, delta=0.01)

        #Verify adding material w. existing material's name updates the existing entry
        newiron = Material.Material(name="Iron", sigma_iacs=18, mu_rel=5000,
                                    notes="Relative Permeability can range anywhere between 150 to 5000")
        self.testdb.add(newiron)
        revised_material = self.testdb.retrieve("Iron")
        self.assertEqual(newiron.name, revised_material.name)
        self.assertEqual(newiron.notes, revised_material.notes)
        self.assertAlmostEqual(newiron.iacs, revised_material.iacs, delta=0.01)
        self.assertAlmostEqual(newiron.mu_r, revised_material.mu_r, delta=0.01)

    def test_retrieve(self):
        '''Verify retrieving materials'''
        copper = Material.Material(name="Copper", sigma_iacs=100, mu_rel=1, notes="IACS Copper Standard")
        self.testdb.add(copper)
        retrieved = self.testdb.retrieve("Copper")
        self.assertEqual(copper.name, retrieved.name)
        self.assertEqual(copper.notes, retrieved.notes)
        self.assertAlmostEqual(copper.iacs, retrieved.iacs, delta=0.01)
        self.assertAlmostEqual(copper.mu_r, retrieved.mu_r, delta=0.01)

    def test_retrieveall(self):
        '''Verify retrieving complete material list'''
        copper = Material.Material(name="Copper", sigma_iacs=100, mu_rel=1, notes="IACS Copper Standard")
        self.testdb.add(copper)
        iron = Material.Material(name="Iron", sigma_iacs=18, mu_rel=150, notes="Pure Iron")
        self.testdb.add(iron)
        aluminum = Material.Material(name="Aluminum", sigma_iacs = 61, mu_rel = 1, notes = "Unalloyed Pure Aluminum")
        self.testdb.add(aluminum)
        cobalt = Material.Material(name="Cobalt", sigma_iacs = 27.6, mu_rel = 70, notes ="Relative permeability can range between 70-250")
        self.testdb.add(cobalt)
        water = Material.Material(name="Water", sigma_iacs = 4.353e-10, mu_rel = 1, notes ="Tap water")
        self.testdb.add(water)
        input_materials = [copper,iron,aluminum,cobalt,water]
        retrieved_materials = self.testdb.retrieveall()
        self.assertEqual(len(input_materials),len(retrieved_materials))
        for im in input_materials:
            for rm in retrieved_materials:
                if im.name == rm.name:
                    #print("Retrieved %s matches input %s" % (im.name,rm.name))
                    self.assertEqual(im.notes, rm.notes)
                    self.assertAlmostEqual(im.iacs, rm.iacs, delta=0.01)
                    self.assertAlmostEqual(im.mu_r, rm.mu_r, delta=0.01)

    def test_noentry(self):
        '''Verifying retrieve returns None when no entry found'''
        self.assertEqual(None, self.testdb.retrieve("Adamantium"))

    def test_delete(self):
        '''Verify deletion of an existing entry'''
        testmaterial = Material.Material(name="Iron", sigma_iacs=18, mu_rel=150, notes="Pure Iron")
        self.testdb.add(testmaterial)
        self.testdb.delete(testmaterial.name)
        retrieved = self.testdb.retrieve(testmaterial.name)
        self.assertEqual(None, retrieved)

    def test_undo(self):
        '''Verify rollback of last operation'''
        origmaterial = Material.Material(name="Iron", sigma_iacs=18, mu_rel=150, notes="Pure Iron")
        self.testdb.add(origmaterial, update=True)
        newiron = Material.Material(name="Iron", sigma_iacs=18, mu_rel=5000,
                                    notes="Relative Permeability can range anywhere between 150 to 5000")
        self.testdb.add(newiron)
        self.testdb.undo()
        revised_material = self.testdb.retrieve("Iron")
        self.assertEqual(origmaterial.name, revised_material.name)
        self.assertEqual(origmaterial.notes, revised_material.notes)
        self.assertAlmostEqual(origmaterial.iacs, revised_material.iacs, delta=0.01)
        self.assertAlmostEqual(origmaterial.mu_r, revised_material.mu_r, delta=0.01)

    def test_exportimportsql(self):
        '''Verifying export and import of SQL'''
        testmaterial=Material.Material(name="Iron", sigma_iacs=18, mu_rel=150, notes="Pure Iron")
        self.testdb.add(testmaterial)
        self.testdb.update()
        self.testdb.exportsql("bert.sql")
        file_db = MaterialDB.MaterialDB(":memory:")
        file_db.importsql("bert.sql")
        retrieved_material = file_db.retrieve("Iron")
        self.assertEqual(testmaterial.name, retrieved_material.name)
        self.assertEqual(testmaterial.notes, retrieved_material.notes)
        self.assertAlmostEqual(testmaterial.iacs , retrieved_material.iacs, delta = 0.01)
        self.assertAlmostEqual(testmaterial.mu_r, retrieved_material.mu_r, delta = 0.01)

    def test_importdb(self):
        '''Verify importing another database'''
        copper = Material.Material(name="Copper", sigma_iacs=100, mu_rel=1, notes="IACS Copper Standard")
        self.testdb.add(copper)
        iron = Material.Material(name="Iron", sigma_iacs=18, mu_rel=150, notes="Pure Iron")
        self.testdb.add(iron)
        aluminum = Material.Material(name="Aluminum", sigma_iacs = 61, mu_rel = 1, notes = "Unalloyed Pure Aluminum")
        self.testdb.add(aluminum)
        cobalt = Material.Material(name="Cobalt", sigma_iacs = 27.6, mu_rel = 70, notes ="Relative permeability can range between 70-250")
        self.testdb.add(cobalt)
        water = Material.Material(name="Water", sigma_iacs = 4.353e-10, mu_rel = 1, notes ="Tap water")
        self.testdb.add(water)
        # Create another database for import
        another_db_fn = tempfile.NamedTemporaryFile(delete=False)
        another_db = MaterialDB.MaterialDB(another_db_fn.name)
        another_db.connect()
        another_db.create()
        # Create another Cobalt, make sure it doesn't overwrite the existing
        fake_cobalt = Material.Material(name="Cobalt", sigma_iacs = 1000, mu_rel = 7e10, notes ="Relative permeability can range between 70-250")
        another_db.add(fake_cobalt)
        another_db.add(water)
        # Create a couple of new materials for import
        unobtanium = Material.Material(name="Unobtanium", sigma_iacs = 1.0, mu_rel = 1.0, notes ="Not a real material, sorry.")
        vibranium = Material.Material(name="Vibranium", sigma_iacs = 1.0, mu_rel = 1.0, notes ="Captain America's shield")
        another_db.add(unobtanium)
        another_db.add(vibranium)
        another_db.close(update=True)
        # Import the new database, and check the results
        self.testdb.importdb(another_db_fn.name)
        # Verify we didn't overwrite the good Cobalt entry
        cobalt_entry = self.testdb.retrieve("Cobalt")
        self.assertEqual(cobalt_entry.name, cobalt.name)
        self.assertEqual(cobalt_entry.notes, cobalt.notes)
        self.assertAlmostEqual(cobalt_entry.iacs , cobalt.iacs, delta = 0.01)
        self.assertAlmostEqual(cobalt_entry.mu_r, cobalt.mu_r, delta = 0.01)
        # Now verify we did import the other two materials that were unique
        unobtanium_entry = self.testdb.retrieve("Unobtanium")
        self.assertEqual(unobtanium_entry.name, unobtanium.name)
        self.assertEqual(unobtanium_entry.notes, unobtanium.notes)
        self.assertAlmostEqual(unobtanium_entry.iacs , unobtanium.iacs, delta = 0.01)
        self.assertAlmostEqual(unobtanium_entry.mu_r, unobtanium.mu_r, delta = 0.01)
        vibranium_entry = self.testdb.retrieve("Vibranium")
        self.assertEqual(vibranium_entry.name, vibranium.name)
        self.assertEqual(vibranium_entry.notes, vibranium.notes)
        self.assertAlmostEqual(vibranium_entry.iacs , vibranium.iacs, delta = 0.01)
        self.assertAlmostEqual(vibranium_entry.mu_r, vibranium.mu_r, delta = 0.01)
        another_db_fn.close()

    def test_importbaddb(self):
        '''Verify that attempting to import a bad SQLite3 database raises an exception'''
        import sqlite3
        with self.assertRaises(sqlite3.OperationalError):
            self.testdb.importdb("x:/werd/test.db")

    def tearDown(self):
        self.testdb.close()

def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMaterialDB)
    unittest.TextTestRunner(verbosity=2).run(suite)