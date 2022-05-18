import sqlite3
import os

def addUser(username,password):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    cur = connection.cursor()
    cur.execute("INSERT INTO User(USERNAME,PASSWORD) VALUES(?, ?)", (username, password))
    connection.commit()

def verifyUser(username,password):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    cur = connection.cursor()
    data=cur.execute("SELECT PASSWORD FROM USER WHERE USERNAME=?;", (username,)).fetchone()
    connection.commit()
    if(data==None):
        error="User not registered in database"
        return False,error
    if(data[0]!=password):
        error="Wrong password"
        return False,error
    return True,""

#old

# def loginMenu():
#     loggedin=False
#     username=""
#     password=""
#     while not loggedin:
#         print("-------Login-------")
#         username=input("Enter your username:\n")
#         password=input("Enter your password:\n")
#         loggedin=verifyUser(username,password)
#     print(username+" is logged in\n-------------------")
#     return username,password