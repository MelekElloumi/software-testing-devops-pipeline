import sqlite3
import os

def create_db(database_filename):
    connection = sqlite3.connect(database_filename)
    cur = connection.cursor()
    cur.execute("DROP TABLE IF EXISTS User")
    cur.execute("DROP TABLE IF EXISTS Product")
    cur.execute(
        "CREATE TABLE User (ID INTEGER PRIMARY KEY, USERNAME TEXT NOT NULL, PASSWORD TEXT NOT NULL);")
    cur.execute(
        "INSERT INTO User (USERNAME,PASSWORD) VALUES ('admin','admin'),('root','root'),('melek','elloumi');")
    cur.execute(
        "CREATE TABLE Product (ID INTEGER PRIMARY KEY, NAME TEXT NOT NULL, PRICE DOUBLE NOT NULL, QUANTITY INT NOT NULL);")
    cur.execute(
        "INSERT INTO Product (NAME,PRICE,QUANTITY) VALUES ('CD',2.0,5),('DVD',3.5,1),('Flash',10.0,2),('Pen',1.0,0);")
    connection.commit()
    print("Done")
    connection.close()

# if __name__ == '__main__':
#     database_filename = os.environ.get('DATABASE_FILENAME', 'database.db')
#     create_db(database_filename)