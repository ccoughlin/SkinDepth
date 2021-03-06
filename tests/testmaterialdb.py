'''testmaterialdb.py- Tests the sqlite3 interface'''

import os
import os.path
import sqlite3
import tempfile
import unittest
from material import MaterialDB
from material import Material

class TestMaterialDB(unittest.TestCase):
    '''Tests the SQLite3 database for SkinDepth'''

    def setUp(self):
        self.testdb = MaterialDB.MaterialDB(":memory:")
        self.testdb.connect()
        self.testdb.create()

    def test_badconnection(self):
        '''Verify throws OperationalError if unable to connect to database'''
        atestdb = MaterialDB.MaterialDB("x:/werd/test.db")
        try:
            with self.assertRaises(sqlite3.OperationalError):
                atestdb.connect()
                atestdb.create()
        except TypeError:
            # Handle assertRaises under 2.6
            self.assertRaises(sqlite3.OperationalError,atestdb.connect)

    def test_add(self):
        '''Verify adding / revising materials'''
        testmaterial = Material.Material(name="Iron", sigma_iacs=18, mu_rel=150, notes="Pure Iron")
        self.testdb.add(testmaterial)
        retrieved_material = self.testdb.retrieve("Iron")
        self.assertEqual(testmaterial.name, retrieved_material.name)
        self.assertEqual(testmaterial.notes, retrieved_material.notes)
        try:
            self.assertAlmostEqual(testmaterial.iacs, retrieved_material.iacs, delta=0.01*testmaterial.iacs)
            self.assertAlmostEqual(testmaterial.mu_r, retrieved_material.mu_r, delta=0.01*testmaterial.mu_r)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(testmaterial.iacs, retrieved_material.iacs, places=1)
            self.assertAlmostEqual(testmaterial.mu_r, retrieved_material.mu_r, places=1)

        #Verify adding material w. existing material's name updates the existing entry
        newiron = Material.Material(name="Iron", sigma_iacs=18, mu_rel=5000,
            notes="Relative Permeability can range anywhere between 150 to 5000")
        self.testdb.add(newiron)
        revised_material = self.testdb.retrieve("Iron")
        self.assertEqual(newiron.name, revised_material.name)
        self.assertEqual(newiron.notes, revised_material.notes)
        try:
            self.assertAlmostEqual(newiron.iacs, revised_material.iacs, delta=0.01*newiron.iacs)
            self.assertAlmostEqual(newiron.mu_r, revised_material.mu_r, delta=0.01*newiron.mu_r)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(newiron.iacs, revised_material.iacs, places=1)
            self.assertAlmostEqual(newiron.mu_r, revised_material.mu_r, places=1)

    def test_retrieve(self):
        '''Verify retrieving materials'''
        copper = Material.Material(name="Copper", sigma_iacs=100, mu_rel=1, notes="IACS Copper Standard")
        self.testdb.add(copper)
        retrieved = self.testdb.retrieve("Copper")
        self.assertEqual(copper.name, retrieved.name)
        self.assertEqual(copper.notes, retrieved.notes)
        try:
            self.assertAlmostEqual(copper.iacs, retrieved.iacs, delta=0.01*copper.iacs)
            self.assertAlmostEqual(copper.mu_r, retrieved.mu_r, delta=0.01*copper.mu_r)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(copper.iacs, retrieved.iacs, places=1)
            self.assertAlmostEqual(copper.mu_r, retrieved.mu_r, places=1)

    def test_retrieveall(self):
        '''Verify retrieving complete material list'''
        copper = Material.Material(name="Copper", sigma_iacs=100, mu_rel=1, notes="IACS Copper Standard")
        self.testdb.add(copper)
        iron = Material.Material(name="Iron", sigma_iacs=18, mu_rel=150, notes="Pure Iron")
        self.testdb.add(iron)
        aluminum = Material.Material(name="Aluminum", sigma_iacs=61, mu_rel=1, notes="Unalloyed Pure Aluminum")
        self.testdb.add(aluminum)
        cobalt = Material.Material(name="Cobalt", sigma_iacs=27.6, mu_rel=70, 
            notes="Relative permeability can range between 70-250")
        self.testdb.add(cobalt)
        water = Material.Material(name="Water", sigma_iacs=4.353e-10, mu_rel=1, notes="Tap water")
        self.testdb.add(water)
        input_materials = [copper, iron, aluminum, cobalt, water]
        retrieved_materials = self.testdb.retrieveall()
        self.assertEqual(len(input_materials), len(retrieved_materials))
        for im in input_materials:
            for rm in retrieved_materials:
                if im.name == rm.name:
                    self.assertEqual(im.notes, rm.notes)
                    try:
                        self.assertAlmostEqual(im.iacs, rm.iacs, delta=0.01*im.iacs)
                        self.assertAlmostEqual(im.mu_r, rm.mu_r, delta=0.01*im.mu_r)
                    except TypeError:
                        # Use places instead of delta for 2.6
                        self.assertAlmostEqual(im.iacs, rm.iacs, places=1)
                        self.assertAlmostEqual(im.mu_r, rm.mu_r, places=1)

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
        try:
            self.assertAlmostEqual(origmaterial.iacs, revised_material.iacs, delta=0.01*origmaterial.iacs)
            self.assertAlmostEqual(origmaterial.mu_r, revised_material.mu_r, delta=0.01*origmaterial.mu_r)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(origmaterial.iacs, revised_material.iacs, places=1)
            self.assertAlmostEqual(origmaterial.mu_r, revised_material.mu_r, places=1)

    def test_exportimportsql(self):
        '''Verifying export and import of SQL'''
        testmaterial = Material.Material(name="Iron", sigma_iacs=18, mu_rel=150, notes="Pure Iron")
        self.testdb.add(testmaterial)
        self.testdb.update()
        temp_sql_file = tempfile.NamedTemporaryFile(delete=False)
        self.testdb.exportsql(temp_sql_file.name)
        file_db = MaterialDB.MaterialDB(":memory:")
        file_db.importsql(temp_sql_file.name)
        retrieved_material = file_db.retrieve("Iron")
        temp_sql_file.close()
        if os.path.exists(temp_sql_file.name):
            os.remove(temp_sql_file.name)
        self.assertEqual(testmaterial.name, retrieved_material.name)
        self.assertEqual(testmaterial.notes, retrieved_material.notes)
        try:
            self.assertAlmostEqual(testmaterial.iacs , retrieved_material.iacs, delta=0.01*testmaterial.iacs)
            self.assertAlmostEqual(testmaterial.mu_r, retrieved_material.mu_r, delta=0.01*testmaterial.mu_r)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(testmaterial.iacs , retrieved_material.iacs, places=1)
            self.assertAlmostEqual(testmaterial.mu_r, retrieved_material.mu_r, places=1)

    def test_importdb(self):
        '''Verify importing another database'''
        copper = Material.Material(name="Copper", sigma_iacs=100, mu_rel=1, notes="IACS Copper Standard")
        self.testdb.add(copper)
        iron = Material.Material(name="Iron", sigma_iacs=18, mu_rel=150, notes="Pure Iron")
        self.testdb.add(iron)
        aluminum = Material.Material(name="Aluminum", sigma_iacs=61, mu_rel=1, notes="Unalloyed Pure Aluminum")
        self.testdb.add(aluminum)
        cobalt = Material.Material(name="Cobalt", sigma_iacs=27.6, mu_rel=70, 
            notes="Relative permeability can range between 70-250")
        self.testdb.add(cobalt)
        water = Material.Material(name="Water", sigma_iacs=4.353e-10, mu_rel=1, notes="Tap water")
        self.testdb.add(water)
        # Create another database for import
        another_db_fn = tempfile.NamedTemporaryFile(delete=False)
        another_db = MaterialDB.MaterialDB(another_db_fn.name)
        another_db.connect()
        another_db.create()
        # Create another Cobalt, make sure it doesn't overwrite the existing
        fake_cobalt = Material.Material(name="Cobalt", sigma_iacs=1000, mu_rel=7e10, 
            notes="Relative permeability can range between 70-250")
        another_db.add(fake_cobalt)
        another_db.add(water)
        # Create a couple of new materials for import
        unobtanium = Material.Material(name="Unobtanium", sigma_iacs=1.0, mu_rel=1.0, 
            notes="Not a real material, sorry.")
        vibranium = Material.Material(name="Vibranium", sigma_iacs=1.0, mu_rel=1.0, notes="Captain America's shield")
        another_db.add(unobtanium)
        another_db.add(vibranium)
        another_db.close(update=True)
        # Import the new database, and check the results
        self.testdb.importdb(another_db_fn.name)
        # Verify we didn't overwrite the good Cobalt entry
        cobalt_entry = self.testdb.retrieve("Cobalt")
        self.assertEqual(cobalt_entry.name, cobalt.name)
        self.assertEqual(cobalt_entry.notes, cobalt.notes)
        try:
            self.assertAlmostEqual(cobalt_entry.iacs, cobalt.iacs, delta=0.01*cobalt_entry.iacs)
            self.assertAlmostEqual(cobalt_entry.mu_r, cobalt.mu_r, delta=0.01*cobalt_entry.mu_r)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(cobalt_entry.iacs, cobalt.iacs, places=1)
            self.assertAlmostEqual(cobalt_entry.mu_r, cobalt.mu_r, places=1)
        # Now verify we did import the other two materials that were unique
        unobtanium_entry = self.testdb.retrieve("Unobtanium")
        self.assertEqual(unobtanium_entry.name, unobtanium.name)
        self.assertEqual(unobtanium_entry.notes, unobtanium.notes)
        try:
            self.assertAlmostEqual(unobtanium_entry.iacs, unobtanium.iacs, delta=0.01*unobtanium.iacs)
            self.assertAlmostEqual(unobtanium_entry.mu_r, unobtanium.mu_r, delta=0.01*unobtanium.mu_r)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(unobtanium_entry.iacs, unobtanium.iacs, places=1)
            self.assertAlmostEqual(unobtanium_entry.mu_r, unobtanium.mu_r, places=1)
        vibranium_entry = self.testdb.retrieve("Vibranium")
        self.assertEqual(vibranium_entry.name, vibranium.name)
        self.assertEqual(vibranium_entry.notes, vibranium.notes)
        try:
            self.assertAlmostEqual(vibranium_entry.iacs, vibranium.iacs, delta=0.01*vibranium.iacs)
            self.assertAlmostEqual(vibranium_entry.mu_r, vibranium.mu_r, delta=0.01*vibranium.mu_r)
        except TypeError:
            # Use places instead of delta for 2.6
            self.assertAlmostEqual(vibranium_entry.iacs, vibranium.iacs, places=1)
            self.assertAlmostEqual(vibranium_entry.mu_r, vibranium.mu_r, places=1)
        another_db_fn.close()

    def test_importbaddb(self):
        '''Verify that attempting to import a bad SQLite3 database raises an exception'''
        try:
            with self.assertRaises(sqlite3.OperationalError):
                self.testdb.importdb("x:/werd/test.db")
        except TypeError:
            # Handles assertRaises under 2.6
            self.assertRaises(sqlite3.OperationalError, self.testdb.importdb, "x:/werd/test.db")

    def tearDown(self):
        '''Closes the SQLite3 database in memory'''
        self.testdb.close()

def run():
    '''Runs the suite of tests'''
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMaterialDB)
    unittest.TextTestRunner(verbosity=2).run(suite)