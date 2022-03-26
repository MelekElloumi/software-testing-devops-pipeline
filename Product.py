class Product:

    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

    def show(self):
        print("Id = "+str(self.id)+ \
              ", Name = "+self.name+ \
              ", Price = "+str(self.price)+ \
              ", Quantity = "+str(self.quantity))

    def __eq__(self, other):
        return self.id == other.id and \
               self.name == other.name and \
               self.price == other.price and \
               self.quantity == other.quantity