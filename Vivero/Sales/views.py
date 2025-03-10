from django.shortcuts import render, redirect, get_object_or_404
from .models import Sale, Sales_Detail
from Inventory.models import Plant 
from django.contrib.auth.decorators import login_required
from django.contrib import messages


############## CARRITO ##############
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Inventory.models import Plant

# Agregar planta al carrito
def cart(request, plant_id):
    plant = get_object_or_404(Plant, plant_id=plant_id)

    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']

    if str(plant_id) in cart:
        cart[str(plant_id)]['quantity'] += 1
    else:
        cart[str(plant_id)] = {
            'name': plant.plant_name,
            'price': plant.price,
            'quantity': 1
        }

    request.session.modified = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Verifica si es una solicitud AJAX
        return JsonResponse({'success': True, 'name': plant.plant_name, 'quantity': cart[str(plant_id)]['quantity']})

    messages.success(request, f"{plant.plant_name} ha sido agregado al carrito.")
    return redirect('catalogoPlantas')  # Regresa al catálogo

# Mostrar carrito
def show_cart(request):
    cart = request.session.get("cart", {})
    total = 0  # Inicializar el total

    for key, item in cart.items():
        item["subtotal"] = float(item["price"]) * int(item["quantity"])  # Calcular subtotal
        total += item["subtotal"]  # Sumar al total

    return render(request, "cart.html", {"cart": cart, "total": total})

# Modificar la cantidad de una planta en el carrito
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

def update_cart(request, plant_id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart = request.session.get("cart", {})

        if str(plant_id) in cart:
            if quantity > 0:
                cart[str(plant_id)]["quantity"] = quantity
                subtotal = float(cart[str(plant_id)]["price"]) * quantity
                cart[str(plant_id)]["subtotal"] = subtotal
                request.session["cart"] = cart
                request.session.modified = True

                return JsonResponse({"success": True, "subtotal": subtotal})

            else:
                del cart[str(plant_id)]
                request.session["cart"] = cart
                request.session.modified = True
                return JsonResponse({"success": True, "remove": True})

    return redirect("show_cart")


# Eliminar una planta del carrito
def remove_from_cart(request, plant_id):
    cart = request.session.get("cart", {})

    if str(plant_id) in cart:
        del cart[str(plant_id)]
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request, "Producto eliminado del carrito.")

    return redirect("show_cart")

############## COMPRA ##############