import database as db
db.createDatabase()
name = raw_input("Insert user name: ")
surname = raw_input("Insert user surname: ")
age = raw_input("Insert user age: ")
db.insertUser(name, surname, age, "Human")


