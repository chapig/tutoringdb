#Author Luis Alfredo Chaparro Gómez 29/06/2021 Venezuela

import sqlite3

#Name of databases for flexibility and usability

ALIASES = {"EN": "EnglishClass", "FR": "FrenchClass", "PAYH": "PaymentHistory"}

class Database:
    """Inticiate instance of DATABASE, arguments are: db_name which stands for the name of the database. They are part of a DICT in database.py"""
    def __init__(self, db_name: str):
        
        self.db_name = db_name 
        self.db_name = self.db_name.upper()
        
        if self.db_name not in ALIASES:
            print("Database does not exist")
        else:
            self.conn = sqlite3.connect(f'classes.sl3')
            self.cursor = self.conn.cursor()
