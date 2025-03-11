from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Categorie(models.Model):
    category_id = models.AutoField(primary_key=True, verbose_name="Id")
    category = models.CharField(max_length=30, verbose_name="Category")

    def __str__(self):
        return self.category
    
class Plant(models.Model):
    plant_id = models.AutoField(primary_key=True, verbose_name="Id")
    category_id = models.ForeignKey(Categorie, on_delete=models.CASCADE, verbose_name='Categorie')
    plant_name = models.CharField(max_length=30, verbose_name="Plant Name")
    care = models.CharField(max_length=1000, verbose_name="Care")
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Price")
    stock = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Stock")

    def __str__(self):
        return self.plant_name

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=20)

    def en_stock_bajo(self):
        return self.stock <= self.stock_minimo

    def __str__(self):
        return f"{self.nombre} - Stock: {self.stock}"
