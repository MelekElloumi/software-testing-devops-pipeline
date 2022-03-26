import sqlite3

def verifyUser(username,password):
    connection = sqlite3.connect('database.db')
    data=connection.execute("SELECT PASSWORD FROM USER WHERE USERNAME=?;", (username,)).fetchone()

    if(data==None):
        print("User not registered in database")
        connection.close()
        return False
    if(data[0]!=password):
        print("Wrong password")
        connection.close()
        return False
    connection.close()
    return True

def loginMenu():
    loggedin=False
    username=""
    password=""
    while not loggedin:
        print("-------Login-------")
        username=input("Enter your username:\n")
        password=input("Enter your password:\n")
        loggedin=verifyUser(username,password)
    print(username+" is logged in\n-------------------")
    return username,password