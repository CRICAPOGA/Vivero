from django.shortcuts import render
from Inventory.models import Plant, Categorie
from Authentication.models import User

def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        low_stock_plants = Plant.objects.filter(stock__lt=5)  # Plantas con stock bajo
        total_plants = Plant.objects.count()
        total_users = User.objects.count()
        return render(request, 'index.html', {
            'low_stock_plants': low_stock_plants,
            'total_plants': total_plants,
            'total_users': total_users
        })

    return render(request, 'index.html')