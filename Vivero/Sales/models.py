from django.db import models
from Authentication.models import User
from Inventory.models import Plant

# Create your models here.
class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True, verbose_name="Id")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    total_price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")

    def __str__(self):
        return self.sale_id + ' - ' + self.date

class Sales_Detail(models.Model):
    sale_detail = models.AutoField(primary_key=True, verbose_name="Id")
    sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Sale')
    plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name='Plant')
    amount = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.sale_id + ' - ' + self.plant_id.plant_name

# Modelo de Carrito (Persistencia de productos agregados por el usuario)
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True, verbose_name="Id")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")  # Un usuario tiene un solo carrito
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Cart {self.cart_id} - User {self.user.username}"

# Modelo de Items dentro del Carrito
class Cart_Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Cart")  # Un carrito puede tener muchos items
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="Plant")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")  # Cantidad de la planta en el carrito
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Added At")

    def __str__(self):
        return f"{self.quantity} x {self.plant.name} in Cart {self.cart.cart_id}"