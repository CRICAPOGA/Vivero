from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Categorie
# from django.contrib.auth.decorators import login_required
from django.contrib import messages

############## CRUD PLANTAS ##############
def plantas(request):
    plants = Plant.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'CRUD Planta/plantas.html', {'plants': plants, 'categories': categories})

def plantasPorCategoria(request, category_id):
    categories = Categorie.objects.get(id=category_id)
    plants = Plant.objects.filter(category=categoria)
    categoria = Categorie.objects.all()
    return render(request, 'CRUD planta/plantas.html', {'categories': categories, 'plants': plants, 'categoria': categoria})

def eliminarPlanta(request, plant_id):
    Plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        Plant.delete()
        messages.success(request, f'La planta "{Plant.name}" ha sido eliminado exitosamente.')
        return redirect('plantas')
    return render(request, 'CRUD plantas/plantas.html', {'plant': Plant})

def buscarPlanta(request):
    query = request.GET.get('buscarPlanta')
    plants = Plant.objects.filter(name__icontains=query) if query else Plant.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'CRUD plantas/plantas.html', {'plants': plants, 'categories': categories, 'query': query})

#######CATALOGO PLANTAS##########
def catalogoPlantas(request):
    plants = Plant.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'Catalogo/catalogoPlantas.html', {'plants': plants, 'categories': categories})

def catalogoCategoria(request, categoria_id):
    categoria = Categorie.objects.get(id=categoria_id)
    plants = Plant.objects.filter(category=categoria)
    categories = Categorie.objects.all()
    return render(request, 'Catalogo/catalogoPlantas.html', {'plants': plants, 'categories': categories, 'categoria': categoria})

def catalogoBuscar(request):
    query = request.GET.get('buscarPlanta')
    plants = Plant.objects.filter(name__icontains=query) if query else Plant.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'Catalogo/catalogoPlantas.html', {'plants': plants, 'categories': categories, 'query': query})