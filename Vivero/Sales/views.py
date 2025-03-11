from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Sale, Sales_Detail
from Inventory.models import Plant
from Authentication.models import User
from datetime import datetime
from Sales.cart import Cart
from django.utils.timezone import now

#Vistas que manejan las peticiones HTTP

# Vista del carrito, incluyendo plantas añadidas y el total a pagar
@login_required
def cart_view(request):
    cart = Cart(request) # Se obtiene el carrito de la sesión
    total = cart.get_total() 

    # Agregar subtotal a cada ítem del carrito
    for item in cart.cart.values():
        item["subtotal"] = float(item["price"]) * item["quantity"]

    return render(request, "cart.html", {"cart": cart.cart, "total": total})

# Agrega una planta al carrito de compras (Llama función)
@login_required(login_url='login') 
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
@login_required
def remove_from_cart(request, plant_id):
    plant = Plant.objects.get(pk=plant_id)
    cart = Cart(request)
    cart.remove(plant)
    return redirect("cart_view")

# Reduce la cantidad de una planta en el carrito de compras (Llama función)
@login_required
def decrement_from_cart(request, plant_id):
    plant = Plant.objects.get(pk=plant_id)
    cart = Cart(request)
    cart.decrement(plant)
    return redirect("cart_view")

# Vacía completamente el carrito de compras (Llama función)
@login_required
def clean_cart(request):
    cart = Cart(request)
    cart.clean()
    return redirect("cart_view")

############## PEDIDO ##############
@login_required
def register_sale(request):
    if request.method == "POST":
        cart = Cart(request)  
        if not cart.cart:
            return JsonResponse({"success": False, "message": "El carrito está vacío."})

        user = request.user  
        total_price = cart.get_total()  

        sale = Sale.objects.create(user_id=user, total_price=total_price, date=now())

        for item in cart.cart.values():
            plant = Plant.objects.get(pk=item["plant_id"])

            if plant.stock < item["quantity"]:
                return JsonResponse({"success": False, "message": f"No hay suficiente stock de {plant.plant_name}."})

            Sales_Detail.objects.create(
                sale_id=sale,
                plant_id=plant,
                amount=item["quantity"],
                price=item["price"]
            )

            plant.stock -= item["quantity"]
            plant.save()

        cart.clean()  
        # Enviar notificación al administrador
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            messages.success(request, f"Nuevo pedido realizado por {user.username}. Total: ${total_price}")
            
        return JsonResponse({"success": True, "message": "¡Pedido realizado exitosamente!"})
    return JsonResponse({"success": False, "message": "Método no permitido."})

@login_required
def sales_history(request):
    sales = Sale.objects.all().order_by("-date")  # Obtener todas las ventas ordenadas por fecha descendente
    sales_details = Sales_Detail.objects.filter(sale_id__in=sales)  # Obtener los detalles de esas ventas

    context = {
        "sales": sales,
        "sales_details": sales_details,
    }
    
    return render(request, "sales_history.html", context)
