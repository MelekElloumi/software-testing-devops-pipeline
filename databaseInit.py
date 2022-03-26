import sqlite3

connection = sqlite3.connect('database.db')
connection.execute(
    "CREATE TABLE User (ID INTEGER PRIMARY KEY, USERNAME TEXT NOT NULL, PASSWORD TEXT NOT NULL);")
connection.execute(
    "INSERT INTO User (USERNAME,PASSWORD) VALUES ('admin','admin'),('root','root'),('melek','elloumi');")
connection.execute(
    "CREATE TABLE Product (ID INTEGER PRIMARY KEY, NAME TEXT NOT NULL, PRICE DOUBLE NOT NULL, QUANTITY INT NOT NULL);")
connection.execute(
    "INSERT INTO Product (NAME,PRICE,QUANTITY) VALUES ('CD',2.0,5),('DVD',3.5,1),('Flash',10.0,2),('Pen',1.0,0);")
connection.commit()
print("Done")
connection.close()