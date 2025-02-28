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