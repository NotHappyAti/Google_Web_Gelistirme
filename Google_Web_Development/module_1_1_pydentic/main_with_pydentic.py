from pydantic import BaseModel

class exampleClass(BaseModel):
    type: str
    price: int
    in_stock: bool

if __name__ == '__main__':

    example_json = {
        'type': 'cellphone',
        'price': '999',
        'in_stock': 'True'
    }

    item1 = exampleClass(
        type = example_json.get('type'),
        price = example_json.get('price'), #Expected as int, gave warnings
        in_stock = example_json.get('in_stock') #Expected as bool, gave warnings
    )
    print(item1.type, type(item1.type),'\n',
          item1.price, type(item1.price), '\n', #pydantic evaluate value to int
          item1.in_stock, type(item1.in_stock)) #pydantic evaluate value to bool