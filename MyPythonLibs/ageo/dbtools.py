def add_vasp_structure(dbname, folder):
   """Add a VASP structure into a database.

   Keyword arguments:
   dbname -- database filename
   folder -- path with VASP outputs

   """
   import sys
   import os
   import re
   import ase.db
   from ase.io import read
   from ase.io.vasp import read_vasp_out


   start_dir = os.path.realpath(".")
   db = ase.db.connect(dbname)
   os.chdir(folder)

   structure = read_vasp_out("OUTCAR")

   fin = open("INCAR"); INCAR = fin.readlines(); fin.close()
   fin = open("KPOINTS"); KPOINTS = fin.readlines(); fin.close()
   fin = open("POTCAR");  POTCARf = fin.read();      fin.close();
   POTCAR = re.findall('TITEL  = (.*)',POTCARf)
   fin = open("CONTCAR"); CONTCAR= fin.readlines(); fin.close()

   datain = {"INCAR" : INCAR,
             "KPOINTS" : KPOINTS,
             "POTCAR_TITEL" : POTCAR,
             "CONTCAR" : CONTCAR}

   str_path = os.path.realpath(".")
   os.chdir(start_dir)

   row_id = db.write(structure,data=datain, structure_path=str_path)
   print ("Structure added with id:", row_id)
   return row_id


def db_read_row(dbname, id):
    """Reads a specific row in a ASE database.

    Keyword arguments:
    dbname -- database name.
    id -- id number of the row to read.

    """
    import ase.db

    db = ase.db.connect(dbname)

    # Read all information for one row in the database
    row = db.get(id=id)

    structure = row.toatoms()
    structure.row = row
    return structure
