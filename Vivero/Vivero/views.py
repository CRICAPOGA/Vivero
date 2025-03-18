from django.shortcuts import render
from django.contrib import messages
from Inventory.models import Plant

def home(request):
    return render(request, 'index.html')

def verificar_stock():
    """Obtiene las plantas con stock bajo."""
    return Plant.objects.filter(stock__lte=5)  # Ajusta el umbral según necesidad

def admin_home(request):
    """Vista de inicio para el administrador."""
    if not request.user.is_staff:
        return redirect('login')  # Redirigir si no es admin
    
    productos_stock_bajo = verificar_stock()  # Obtener productos con stock bajo
    return render(request, 'admin_home.html', {'productos_stock_bajo': productos_stock_bajo})