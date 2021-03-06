# TutoringDB

## Usage
```py
from operations import student, language

student = student.create(language.french, "Luis", "Chaparro", "Venezuelan", "Venezuela")
student.update_payment(20.4) #Student paid 20.4 US dollars
student.update_payment(54.2) #Student paid 54.2 US dollars
print(student.total_payed)
# Output: 74.6

student = student.get(language.french, "Alfonso", "Gutierrez")
print(student.nationality)
# Venezuelan
print(student.total_payed)
# 65.4 USD
```

## SQL Table
```sql
CREATE TABLE FrenchClass (
  StudentFirstName TEXT NOT NULL,
  StudentLastName TEXT NOT NULL,
  ResidenceCountry TEXT NOT NULL,
  Nationality TEXT NOT NULL,
  DateLastPayment TEXT,
  AmountLastPayment REAL,
  TotalPayed REAL,
  Debt REAL ,
  ID TEXT NOT NULL UNIQUE
);

CREATE TABLE PaymentHistory (
  FirstName TEXT NOT NULL, 
  LastName TEXT NOT NULL, 
  DatePayment TEXT NOT NULL,
  Amount REAL NOT NULL,
  ID TEXT NOT NULL
);
```
