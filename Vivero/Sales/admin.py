from django.contrib import admin
from .models import Sale, Sales_Detail, Cart, Cart_Item

# Register your models here.
admin.site.register(Sale)
admin.site.register(Sales_Detail)
admin.site.register(Cart)
admin.site.register(Cart_Item)