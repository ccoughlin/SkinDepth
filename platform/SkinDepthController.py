__author__ = 'Chris'
import os.path
import sys
from material import Material
from material import MaterialDB
import FetchFile

'''Handles the interface between UI and the backend for SkinDepth'''

class SkinDepthController(object):
    def __init__(self,dbfilename):
        self.db = MaterialDB.MaterialDB(dbfilename)

    def open(self):
        '''Opens/creates the database @ dbfilename'''
        self.db.connect()
        self.db.create()

    def importdb(self, import_fn):
        '''Imports another SQLite3 database into the current, returning the number of additions made.'''
        return self.db.importdb(import_fn)

    def import_remotedb(self, db_url = 'http://www.chriscoughlin.com/dnlds/skindepth2_materials.db'):
        '''Fetches the remote copy of the database, returning the number of additions made.'''
        try:
            dest_path = os.path.join(sys.path[0],'materials_update.db')
            fetcher = FetchFile.FetchFile(db_url, dst = dest_path, overwrite=True)
            fetcher.fetch()
            return self.importdb(dest_path)
        except Exception:
            raise

    def exportsql(self,export_fn):
        '''Exports the current database as a SQL script'''
        self.db.exportsql(export_fn)

    def importsql(self,import_fn):
        '''Creates and populates the database using an ASCII text SQL script, returning the number of changes made.'''
        return self.db.importsql(import_fn)

    def savecopy(self,copy_fn):
        '''Saves a copy of the current list of materials to the new file copy_fn,
        closes the current database connection and reopens at the new location.'''
        if os.path.exists(copy_fn):
            os.remove(copy_fn)
        tempdb = MaterialDB.MaterialDB(copy_fn)
        tempdb.connect()
        tempdb.create()
        materials = self.db.retrieveall()
        for material in materials:
            tempdb.add(material)
        tempdb.update()
        self.db.close()
        self.db = MaterialDB.MaterialDB(copy_fn)
        self.open()

    def add(self,material_dict):
        '''Adds a new material to the database'''
        newmat = Material.Material(name=material_dict["name"],
                                   notes=material_dict["notes"],
                                   sigma_iacs=material_dict["iacs"],
                                   mu_rel=material_dict["mu_r"])
        self.db.add(newmat)

    def fetch(self,materialname):
        '''Returns the selected material as a dict'''
        foundmat = self.db.retrieve(materialname)
        if foundmat is None:
            foundmat_dict = None
        else:
            foundmat_dict = {"name":foundmat.name,
                             "notes":foundmat.notes,
                             "iacs":foundmat.iacs,
                             "mu_r":foundmat.mu_r}
        return foundmat_dict

    def remove(self,materialname):
        '''Removes the given material from the database'''
        self.db.delete(materialname)

    def calcdelta(self,materialname,frequency):
        '''Returns the skin depth in mm at the given frequency in Hz for the material materialname'''
        thematerial = self.db.retrieve(materialname)
        if thematerial is None:
            return None
        else:
            return thematerial.calc_skindepth(frequency)

    def calcfrequency(self, materialname, skindepth):
        '''Returns the excitation frequency in Hz that would induce the given skin depth'''
        thematerial = self.db.retrieve(materialname)
        if thematerial is None:
            return None
        else:
            return thematerial.calc_frequency(skindepth)

    def update(self):
        '''Commits the changes to the database'''
        self.db.update()

    def undo(self):
        '''Drops the changes to the database made since last update'''
        self.db.undo()

    def fetchlist(self):
        '''Returns a list of the materials (names) currently in the database'''
        thematerials = self.db.retrieveall()
        materialnames = [material.name for material in thematerials]
        return materialnames