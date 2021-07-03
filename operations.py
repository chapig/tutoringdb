#Importing class Database from database.py file
#Written by Luis Alfredo Chaparro Gómez
from database import Database, ALIASES
import random

class Languages:
    
    english = "EN"
    french = "FR"

class HiddenMeta:
    
    def generate_id(self, fname, lname, residence, nationality):
    
        return fname[0:1].upper() + lname[0:1].upper() + \
                            residence.replace(" ", "").upper()[0:1] + \
                            nationality.replace(" ", "").upper()[0:1] + \
                            str(random.choice(range(len(fname) + len(lname))))
                            
class Result:

    def __init__(self, table, database, firstname, lastname, residence, nationality, date_lastpayment, amount_lastpayment, total_payed, debt, identification):
        
        self.table = table
        self.database = database
        self.firstname = firstname
        self.lastname = lastname
        self.residence = residence
        self.nationality = nationality
        self.date_lastpayment = date_lastpayment
        self.amount_lastpayment = amount_lastpayment
        self.total_payed = total_payed
        self.debt = debt
        self.identification = identification
        
    def update_payment(self, payment: float = 0.0):
        """Update payment in Database"""
        
        if payment > 0.0:
            
            #Update date of payment, amount of the last payment and update the total payed.
            #Insert into payment history
            with self.database.conn:
                self.database.cursor.executescript(f"""
                                                
                                                UPDATE {self.table}
                                                    SET DateLastPayment = date('now'),
                                                        AmountLastPayment = {payment},
                                                        TotalPayed = TotalPayed + {payment}
                                                WHERE ID = "{self.identification}";
                                                
                                                INSERT INTO PaymentHistory (FirstName, LastName, DatePayment, Amount, ID)
                                                VALUES ("{self.firstname}", "{self.lastname}", date('now'), {payment}, "{self.identification}");
                                                
                                            """)
                self.database.conn.commit()

            #Update attributes
            self.fetch_attributes()
            return True
        
    def fetch_attributes(self):
        
        with self.database.conn:
            
            self.database.cursor.execute(f"""SELECT * FROM {self.table} WHERE ID = "{self.identification}";""")
                    
            student_results = self.database.cursor.fetchall()[0]
            self.date_lastpayment = student_results[4]
            self.amount_lastpayment = student_results[5]
            self.total_payed = student_results[6]
            self.debt = student_results[7]
        
        return Result(
                        self.table, self.database,
                        self.firstname, self.lastname,
                        self.residence, self.nationality,
                        self.date_lastpayment, self.amount_lastpayment,
                        self.total_payed, self.debt, self.identification
                    )

class Course:
    
    def get(self, language: str, student_firstname: str = None, student_lastname: str = None, student_id: str = None):
        
        self.language = language.upper()   
        if self.language is not None and self.language in ALIASES:
            self.database = Database(language)
            self.table = ALIASES[self.language]
        self.student_id = student_id
        self.student_firstname = student_firstname
        self.student_lastname = student_lastname
        
        new_id = None
        success = False
        
        if student_id is not None:
            
            with self.database.conn:
                self.database.cursor.execute(f"""SELECT EXISTS(SELECT 1 FROM {self.table} WHERE ID = "{self.student_id}");""")
                if self.database.cursor.fetchone()[0]:
                    self.database.cursor.execute(f"""SELECT * FROM {self.table} WHERE ID = "{self.student_id}"; """)
                    student_results = self.database.cursor.fetchall()[0]
                    success = True
                else:
                    print("Student was not found using ID, try using their name instead or add a new one")
                    return None
        else:
            
            #Check if students exists
            with self.database.conn:
                
                self.database.cursor.execute(f"""
                                        SELECT EXISTS(SELECT 1 FROM {self.table} WHERE StudentFirstName = "{self.student_firstname}" 
                                        AND StudentLastName = "{self.student_lastname}");""")
            
                if self.database.cursor.fetchone()[0]:
                    
                    self.database.cursor.execute(f"""SELECT * FROM {self.table} WHERE StudentFirstName = "{self.student_firstname}" 
                                            AND StudentLastName = "{self.student_lastname}"; """)
                    
                    student_results = self.database.cursor.fetchall()[0]
                    success = True
                    
                    #Create an ID for student
                    if student_results[-1] is None:
                        new_id =    student_firstname[0:1].upper() + student_lastname[0:1].upper() + \
                                    student_results[2].replace(" ", "").upper()[0:1] + \
                                    student_results[3].replace(" ", "").upper()[0:1] + \
                                    str(random.choice(range(len(student_firstname) + len(student_lastname))))
                    
                        self.database.cursor.execute(f"""UPDATE {self.table} SET ID = "{new_id}" WHERE StudentFirstName = "{self.student_firstname}" 
                                            AND StudentLastName = "{self.student_lastname}"; """)
                        self.database.conn.commit()
                        success = True
            
                elif student_firstname is not None and student_lastname is not None:
                    print(f"Student {student_firstname} {student_lastname} is not in the database, try using their ID instead")
                    return None
            
        #Adding attributes.
        if success:
                
            self.firstname = student_results[0]
            self.lastname = student_results[1]
            self.residence = student_results[2]
            self.nationality = student_results[3]
            self.date_lastpayment = student_results[4]
            self.amount_lastpayment = student_results[5]
            self.total_payed = student_results[6]
            self.debt = student_results[7]
            self.id = new_id if new_id is not None else student_results[8]
            return Result(  self.table, self.database,
                            self.firstname, self.lastname, 
                            self.residence, self.nationality, 
                            self.date_lastpayment, self.amount_lastpayment, 
                            self.total_payed, self.debt, self.id
                        )
            
    def create(self, language, fname, lname, nationality, residence):
    
        language = language.upper()
    
        self.fname = fname
        self.lname = lname
        self.nationality = nationality
        self.residence = residence
        self.table = ALIASES[language]
        self.created_id = HiddenMeta().generate_id(self.fname, self.lname, self.residence, self.nationality)

        database = Database(language)
        
        with database.conn:
            database.cursor.execute(f"""
                                    INSERT INTO {self.table} (StudentFirstName, StudentLastName, Nationality, ResidenceCountry, ID, TotalPayed)
                                    VALUES ("{fname}", "{lname}", "{nationality}", "{residence}", "{self.created_id}", 0);
                                    """)
            database.conn.commit()       
        
        return Result(  self.table, Database(language),
                        self.fname, self.lname, 
                        self.residence, self.nationality, 
                        None, 0, 0, 0, self.created_id)

student = Course()
language = Languages()
