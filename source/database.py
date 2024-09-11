import sqlite3

def createDatabase():
    try:
        connection = sqlite3.connect("pepperDatabase.db")
        cursor = connection.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            age INTEGER NOT NULL,
            testType TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()
    except Exception as e:
        print("Error during the database creation [%s]", e)

def insertUser(name, surname, age , testType):
    try:
        connection = sqlite3.connect("pepperDatabase.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user (name, surname, age, testType) VALUES (?, ?, ?, ?)", (name, surname, age, testType))
        connection.commit()
        connection.close()
    except Exception as e:
        print("Error inserting user into the database.")
        print(e)

