'''MaterialDB.py - defines a SQLITE3 backend for Material I/O

Chris Coughlin
'''
import sqlite3
import Material

class MaterialDB(object):
    def __init__(self,dbfile):
        '''Required parameter - filename of database to use.  Can use ':memory:' as per sqlite3
          module to keep database in memory only.'''
        self.dbfilename = dbfile

    def connect(self):
        '''Connects to the instance's database and creates the database cursor.
          Raises sqlite3.OperationalError if unable to open the database.
          '''
        self.dbconnection = sqlite3.connect(self.dbfilename)
        self.dbcursor = self.dbconnection.cursor()

    def create(self):
        '''Creates the materials table in the database'''
        self.dbcursor.execute(
                '''create table if not exists materials(name text unique, notes text, conductivity_iacs real,
                 rel_permeability real)'''
                )
        self.update()

    def update(self):
        '''Commits the changes to the database'''
        self.dbconnection.commit()

    def add(self,newmaterial,update=False):
        '''Adds / replaces (if material of same name already exists in database) a material
          to the database.  If update is True, the changes are commited to the database after
          execution (default is False).
        '''
        if isinstance(newmaterial,Material.Material):
            self.dbcursor.execute('insert or replace into materials values (?,?,?,?)', (
            newmaterial.name,
            newmaterial.notes,
            newmaterial.iacs,
            newmaterial.mu_r
            ))
            if update:
                self.update()

    def retrieve(self,materialname):
        '''Retrieves the material of the given name from the database, or None if not found.'''
        self.dbcursor.execute('select * from materials where name=?', (materialname,))
        row = self.dbcursor.fetchone()
        if row is None:
            return row
        else:
            return Material.Material(
                    name = row[0],
                    notes = row[1],
                    sigma_iacs = row[2],
                    mu_rel = row[3]
                    )

    def retrieveall(self):
        '''Retrieves all the materials currently in the database'''
        allmaterials=[]
        self.dbcursor.execute('select * from materials order by name asc')
        alldata = self.dbcursor.fetchall()
        if alldata is not None:
            for row in alldata:
                allmaterials.append(
                        Material.Material(
                                name = row[0],
                                notes = row[1],
                                sigma_iacs = row[2],
                                mu_rel = row[3]
                                )
                        )
        return allmaterials

    def delete(self,materialname,update=False):
        '''Deletes the material of the given name from the database.  If update is True,
          the changes are commited to the database after execution (default is False).
          '''
        self.dbcursor.execute("delete from materials where name=?", (materialname,))
        if update:
            self.update()

    def undo(self):
        '''Rollback the changes to the database since the last commit.'''
        self.dbconnection.rollback()

    def close(self,update=False):
        '''Closes the connection to the database.  If update is True, changes are
        commited to the database prior to close (default is False).
        '''
        if update:
            self.update()
        self.dbconnection.close()

    def exportsql(self,export_file):
        '''Wrapper for dumping database to SQL script text file'''
        with open(export_file,'w') as fidout:
            for row in self.dbconnection.iterdump():
                fidout.write('%s\n' % row)

    def importsql(self,import_file):
        '''Imports a SQL script and executes, returning the total number of changes made.'''
        self.connect()
        self.create()
        dbwalker = MaterialDB(":memory:")
        dbwalker.connect()
        with open(import_file,'r') as fidin:
            dbwalker.dbconnection.executescript(fidin.read())
        imported_records = dbwalker.retrieveall()
        for amaterial in imported_records:
            self.add(amaterial)
        return self.dbconnection.total_changes

    def importdb(self, import_file):
        '''Attempts to import a SQLite database into the current.  Only materials not already in the database are imported.
        Returns the total number of additions made to the database.
        '''
        try:
            otherdb = MaterialDB(import_file)
            otherdb.connect()
            otherdb.dbcursor.execute('select * from materials order by name asc')
            import_materials = otherdb.dbcursor.fetchall()
            if import_materials is not None:
                for newmaterial in import_materials:
                    self.dbcursor.execute('insert or ignore into materials values (?,?,?,?)', newmaterial)
                materials_added = self.dbconnection.total_changes
                self.update()
            otherdb.close()
            return materials_added
        except sqlite3.OperationalError:
            '''Unable to read the import database'''
            raise