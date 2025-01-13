'''
To gain better understand for PyDentic library
what we are expect and what we get
PyDentic is necessary for data control and
'''

example_json = {
    'type':'cellphone',
    'price': '999',
    'in_stock': 'True'
}

class exampleClass:
    def __init__(self, type: str , price: int ,in_stock: bool): # Type Notation of class`s values
        self.type = type
        self.price = price
        self.in_stock = in_stock

if __name__ == '__main__':

    item1 = exampleClass(
        type = example_json.get('type'),
        price = example_json.get('price'), #Expected as int, gave warnings
        in_stock = example_json.get('in_stock') #Expected as bool, gave warnings
    )
    print(item1.type, type(item1.type),'\n',
          item1.price, type(item1.price), '\n', #Python can`t evaluate value to int
          item1.in_stock, type(item1.in_stock)) #Python can`t evaluate value to bool