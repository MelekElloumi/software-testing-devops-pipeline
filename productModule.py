import sqlite3
import os

def fetch_by_id(id):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    cur = connection.cursor()
    product= cur.execute("SELECT * FROM PRODUCT WHERE ID=?;", (id,)).fetchone()
    connection.close()
    return product

def fetch_all():
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    cur = connection.cursor()
    products = cur.execute("SELECT * FROM PRODUCT;").fetchall()
    connection.close()
    return products

def average(list):
    if(len(list)==0):
        raise ValueError
    avg=0
    for i in list:
        avg+=i
    return avg/len(list)

def price_average():
    products = fetch_all()
    prices=[]
    for product in products:
        prices.append(product[2])
    return average(prices)

def add_product(name,price,quantity):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    connection.execute(
        "INSERT INTO Product (NAME,PRICE,QUANTITY) VALUES (?,?,?);", (name,price,quantity,))
    connection.commit()

def update_product(id,name,price,quantity):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    connection.execute(
        "UPDATE PRODUCT SET NAME=?, PRICE=?, QUANTITY=? WHERE ID=?;", (name,price,quantity,id,))
    connection.commit()

def delete_product(id):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    connection.execute(
        "DELETE FROM PRODUCT WHERE ID=?;",(id,))
    connection.commit()

def buy_product(id):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(
        "UPDATE PRODUCT SET QUANTITY=QUANTITY-1 WHERE ID=? AND QUANTITY>0;",(id,))
    connection.commit()
    if cursor.rowcount < 1:
        return False
    else:
        return True

#Old

# def productMenu():
#     choice='0'
#     while choice!='8':
#         print("\n-------Product Menu-------")
#         print("1-Fetch product by name")
#         print("2-Fetch all products")
#         print("3-Add product")
#         print("4-Update product")
#         print("5-Delete product")
#         print("6-Average price of all products")
#         print("7-Buy product")
#         print("8-Exit")
#         print("--------------------------")
#         choice=input("Enter your choice number: ")
# # ---------------------------------------------------------------------------------------
#         if (choice=='1'):
#             name=input("Enter the product's name: ")
#             found,product=fetch_by_id(name)
#             if not found:
#                 print("Product not found")
#             else:
#                 print("Product found:")
#                 product.show()
# # ---------------------------------------------------------------------------------------
#         if (choice=='2'):
#             products=fetch_all()
#             print(str(len(products))+" products found: ")
#             for i in range(0,len(products)):
#                 print(str(i+1)+"- ", end='')
#                 products[i].show()
# # ---------------------------------------------------------------------------------------
#         if (choice=='3'):
#             found=True
#             product=Product(0,'',0,0)
#             while found:
#                 product.name=input("Enter the product's name: ")
#                 found, p = fetch_by_id(product.name)
#                 if found:
#                     print("Product name exists")
#             negative=True
#             while negative:
#                 product.price = float(input("Enter the product's price: "))
#                 negative = product.price <= 0
#                 if negative:
#                     print("Product's price must be strictly positive")
#             negative=True
#             while negative:
#                 product.quantity = int(input("Enter the product's quantity: "))
#                 negative = product.price < 0
#                 if negative:
#                     print("Product's quantity must be positive")
#             add_product(product)
#             print(product.name+" added")
# #---------------------------------------------------------------------------------------
#         if (choice=='4'):
#             name = input("Enter the existing product's name: ")
#             found, product = fetch_by_id(name)
#             if not found :
#                 print("Product not found")
#                 continue
#             found = True
#             while found:
#                 product.name = input("Enter the product's new name: ")
#                 found, p = fetch_by_id(product.name)
#                 found=found and product.name!=name
#                 if found:
#                     print("Product name exists")
#             negative = True
#             while negative:
#                 product.price = float(input("Enter the product's new price: "))
#                 negative = product.price <= 0
#                 if negative:
#                     print("Product's price must be strictly positive")
#             negative = True
#             while negative:
#                 product.quantity = int(input("Enter the product's new quantity: "))
#                 negative = product.price < 0
#                 if negative:
#                     print("Product's quantity must be positive")
#             update_product(product)
#             print(name+" updated")
# # ---------------------------------------------------------------------------------------
#         if (choice=='5'):
#             name = input("Enter the product's name to delete: ")
#             found, product = fetch_by_id(name)
#             if not found:
#                 print("Product not found")
#                 continue
#             delete_product(product.id)
#             print(name+" deleted")
# # ---------------------------------------------------------------------------------------
#         if (choice=='6'):
#             price=price_average()
#             print("The average price of all products is: "+str(price))
# # ---------------------------------------------------------------------------------------
#         if (choice=='7'):
#             name = input("Enter the product's name to buy: ")
#             found, product = fetch_by_id(name)
#             if not found:
#                 print("Product not found")
#                 continue
#             bought=buy_product(product.id)
#             if bought:
#                 print(name + " bought")
#             else:
#                 print(name +"'s stock is depleted")


