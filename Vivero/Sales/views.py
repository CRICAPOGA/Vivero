from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Sale, Sales_Detail, Cart, Cart_Item
from Inventory.models import Plant
from Authentication.models import User
from django.utils.timezone import now

#Vistas que manejan las peticiones HTTP

############## CARRITO ##############

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    # Agregar subtotales a cada ítem
    for item in items:
        item.subtotal = item.plant.price * item.quantity

    total_price = sum(item.plant.price * item.quantity for item in items)

    return render(request, 'cart.html', {'cart': cart, 'items': items, 'total_price': total_price})

# Agregar un producto al carrito
@login_required
def add_to_cart(request, plant_id):
    plant = get_object_or_404(Plant, plant_id=plant_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = Cart_Item.objects.get_or_create(cart=cart, plant=plant)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('catalogoPlantas')

# Incrementar la cantidad de un producto en el carrito
@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(Cart_Item, id=item_id)
    if item.cart.user == request.user:
        item.quantity += 1
        item.save()

    return redirect('cart_view')

# Disminuir la cantidad de un producto en el carrito
@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(Cart_Item, id=item_id)
    if item.cart.user == request.user:
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()  # Elimina el item si la cantidad es 0

    return redirect('cart_view')

# Eliminar un producto del carrito
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart_Item, id=item_id)
    if item.cart.user == request.user:
        item.delete()

    return redirect('cart_view')

############## PEDIDO ##############
@login_required
def register_sale(request):
    if request.method == "POST":
        cart = Cart.objects.filter(user=request.user).first()  
        if not cart or not cart.items.exists():
            return JsonResponse({"success": False, "message": "El carrito está vacío."})

        user = request.user  
        total_price = sum(item.plant.price * item.quantity for item in cart.items.all())

        # Registrar la venta
        sale = Sale.objects.create(user_id=user, total_price=total_price, date=now())

        for item in cart.items.all():
            plant = item.plant
            # Mensaje de stock bajo 
            if plant.stock < item.quantity:
                if request.user.is_staff:  # Si es un administrador
                    mensaje = f"No hay suficiente stock de {plant.plant_name}."
                else:  # Si es un cliente
                    mensaje = f"Lo sentimos, la planta {plant.plant_name} no esta disponible en este momento."

                return JsonResponse({"success": False, "message": mensaje})
            # Datos
            Sales_Detail.objects.create(
                sale_id=sale,
                plant_id=item.plant,
                amount=item.quantity,
                price=item.plant.price
            )

            # Reducir el stock
            plant.stock -= item.quantity
            plant.save()

        # Vaciar carrito después de la compra
        cart.items.all().delete()

        # Notificar al administrador
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