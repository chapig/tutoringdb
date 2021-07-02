# tutoringdb

```py
from .operations import student

student = student.create("fr", "Luis", "Chaparro", "Venezuelan", "Venezuela")
student.update_payment(20.4) #Student paid 20.4 US dollars
student.update_payment(54.2) #Student paid 54.2 US dollars
print(student.total_payed)
# Output: 74.6

student = student.get("fr", "Alfonso", "Gutierrez")
print(student.nationality)
# Colombian
print(student.total_payed)
# 65.4 USD
```
