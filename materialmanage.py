# My materials manager code, im using this to test stuff before adding it all to the main program 

import sqlite3

class materialmanage:
    def create_db(self):
        db = sqlite3.connect("materials.sqlite3")
        cursor = db.cursor()
        cursor.execute(""" CREATE TABLE materials(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, supplier TEXT, cat1 TEXT, cat2 TEXT, item TEXT, cost INT, description TEXT, notes TEXT) """)
        db.commit()
        db.close()
        print("creating materials db success")

    def read_db(self):
        results_format=" \n Supplier: {}\n Category: {}\n Subcategory 1:{}\n Item: {}\n Cost: {}\n Description: {}\n Notes: {}\n"
        db=sqlite3.connect("materials.sqlite3")
        cursor=db.cursor()
        cursor.execute("""SELECT * FROM materials""")

        
        print("\n\n\n\n\n############################ RESULTS START HERE ############################\n\n\n\n")
        
        for record in cursor:
            x = results_format.format( record[1], record [2], record[3], record[4], record[5], record[6], record[7])
            print (x)


material = materialmanage()
material.read_db()
#material.create_db()
