from django.shortcuts import render, redirect, get_object_or_404
from .models import Sale, Sales_Detail
from Inventory.models import Plant 
from django.contrib.auth.decorators import login_required
from django.contrib import messages


############## CARRITO ##############
def cart(request):
    plants = Plant.objects.all()
    print(plants)  # Verifica en la terminal si hay datos
    return render(request, 'cart.html', {'plants': plants})
