from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Sale, Sales_Detail
from Inventory.models import Plant
from Authentication.models import User
from datetime import datetime
from Sales.cart import Cart

#Vistas que manejan las peticiones HTTP

# Vista del carrito, incluyendo plantas añadidas y el total a pagar
#@login_required
def cart_view(request):
    cart = Cart(request) # Se obtiene el carrito de la sesión
    total = cart.get_total() 

    # Agregar subtotal a cada ítem del carrito
    for item in cart.cart.values():
        item["subtotal"] = float(item["price"]) * item["quantity"]

    return render(request, "cart.html", {"cart": cart.cart, "total": total})

# Agrega una planta al carrito de compras (Llama función)
#@login_required
def add_to_cart(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id) # Busca la planta
    cart = Cart(request)
    cart.add(plant)
    return redirect("catalogoPlantas")

# Incrementa la cantidad de una planta en el carrito de compras (Llama función)
#@login_required
def increment_from_cart(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id) 
    cart = Cart(request)
    cart.add(plant)
    return redirect("cart_view")

# Elimina una planta del carrito de compras (Llama función)
#@login_required
def remove_from_cart(request, plant_id):
    plant = Plant.objects.get(pk=plant_id)
    cart = Cart(request)
    cart.remove(plant)
    return redirect("cart_view")

# Reduce la cantidad de una planta en el carrito de compras (Llama función)
#@login_required
def decrement_from_cart(request, plant_id):
    plant = Plant.objects.get(pk=plant_id)
    cart = Cart(request)
    cart.decrement(plant)
    return redirect("cart_view")

# Vacía completamente el carrito de compras (Llama función)
#@login_required
def clean_cart(request):
    cart = Cart(request)
    cart.clean()
    return redirect("cart_view")

############## PEDIDO ###############

# Restringir la vista solo para administradores
#@staff_member_required
def order_list(request):
    user_id = request.user.id if request.user.is_authenticated else None
    orders = Sale.objects.all().order_by('-date')  # Obtener todos los pedidos ordenados por fecha descendente
    return render(request, 'order_list.html', {'orders':orders})
