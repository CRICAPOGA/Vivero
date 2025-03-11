#Lógica del carrito de compras
class Cart:
    # Constructor: inicializa el carrito y lo almacena en la sesión
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    # Método para agregar una planta al carrito
    def add(self, plant):
        if str(plant.plant_id) not in self.cart.keys():
            self.cart[plant.plant_id] = {
                "plant_id": plant.plant_id,
                "name": plant.plant_name,
                "quantity": 1,
                "price": str(plant.price),
            }
        else:
            # Si la planta ya está en el carrito, incrementa su cantidad
            for key, value in self.cart.items():
                if key == str(plant.plant_id):
                    value["quantity"] = value["quantity"] + 1
                    break  
        self.save()   
    
    # Método para incrementar la cantidad de una planta en el carrito
    def increment(self, plant):
        if str(plant.plant_id) not in self.cart.keys():
            self.cart[plant.plant_id] = {
                "plant_id": plant.plant_id,
                "name": plant.plant_name,
                "quantity": 1,
                "price": str(plant.price)
            }
        else:
            for key, value in self.cart.items():
                if key == str(plant.plant_id):
                    value["quantity"] = value["quantity"] + 1
                    break  
        self.save()   

    # Método para guardar la sesión actualizada y persistir los datos
    def save(self):
        self.session["cart"] = self.cart # Actualiza la sesión con el carrito modificado
        self.session.modified = True # Marca la sesión como modificada para que se guarde

    # Método para eliminar una planta completamente del carrito
    def remove(self, plant):
        plant_id = str(plant.plant_id)
        if plant_id in self.cart: # Verifica si la planta está en el carrito
            del self.cart[plant_id]
            self.save()
    
     # Método para disminuir la cantidad de una planta en el carrito
    def decrement(self, plant):
        for key, value in self.cart.items():
                if key == str(plant.plant_id):
                    value["quantity"] = value["quantity"] - 1
                    if value["quantity"] < 1:
                        self.remove(plant)
                    else:
                        self.save()
                    break
                else:
                    print("El producto no existe en el carrito")
    
    # Método para vaciar el carrito
    def clean(self):
        self.session["cart"] = {}
        self.session.modified = True
        
    # Método para calcular el total del carrito
    def get_total(self):
        return sum(float(item["price"]) * item["quantity"] for item in self.cart.values())
    