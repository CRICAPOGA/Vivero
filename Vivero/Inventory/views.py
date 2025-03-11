from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Categorie
# from django.contrib.auth.decorators import login_required
from django.contrib import messages

############## CRUD PLANTAS ##############
def plantas(request):
    plants = Plant.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'CRUD Planta/plantas.html', {'plants': plants, 'categories': categories})

def plantasPorCategoria(request, categoria_id):
    categoria = get_object_or_404(Categorie, category_id=categoria_id)
    plants = Plant.objects.filter(category_id=categoria)
    categories = Categorie.objects.all()
    return render(request, 'CRUD Planta/plantas.html', {'categories': categories, 'plants': plants, 'categoria': categoria})

def editarPlanta(request, planta_id):
    plants = get_object_or_404(Plant, plant_id=planta_id)
    categories = Categorie.objects.all()
    
    if request.method == 'POST':
        plants.plant_name = request.POST.get('plant_name')
        plants.care = request.POST.get('care')
        plants.price = request.POST.get('price')
        plants.stock = request.POST.get('stock')
        
        category_id = request.POST.get('category') #Definir antes de usar
        if category_id:
            plants.category_id = get_object_or_404(Categorie, category_id=category_id)

        plants.save()
        messages.success(request, f'La planta "{plants.plant_name}" ha sido actualizado exitosamente.')
        return redirect('plantas')
    
    return render(request, 'CRUD Planta/editarPlanta.html', {'plants': plants, 'categories': categories})

def crearPlanta(request):
    categories = Categorie.objects.all()
    
    if request.method == 'POST':
        plant_name = request.POST.get('plant_name', '').strip() #Elimina espacios extra
        care = request.POST.get('care' ,'').strip()
        price = request.POST.get('price', '').strip()
        stock = request.POST.get('stock', '0')
        category_id = request.POST.get('category')

        #Validaciones
        if not plant_name:
            messages.error(request, 'El nombre de la planta es obligatorio.')
            return render(request, 'CRUD Planta/crearPlanta.html', {'categories': categories})
    
        if category_id:  # Verificamos que category_id no sea None o vacío
            category = get_object_or_404(Categorie, category_id=category_id)  # Convertimos el ID en instancia
        else:
            messages.error(request, 'Debe seleccionar una categoría.')
            return render(request, 'CRUD Planta/crearPlanta.html', {'categories': categories})

        # Creamos la planta con la instancia correcta de Categorie
        plant = Plant(plant_name=plant_name, care=care, price=price, stock=stock, category_id=category)
        plant.save()
        messages.success(request, f'La planta "{plant.plant_name}" ha sido creado exitosamente.')
        return redirect('plantas')
    
    return render(request, 'CRUD Planta/crearPlanta.html', {'categories': categories})


def eliminarPlanta(request, planta_id):
    plants = get_object_or_404(Plant, plant_id=planta_id)
    if request.method == 'POST':
        plants.delete()
        messages.success(request, f'La planta "{plants.plant_name}" ha sido eliminado exitosamente.')
        return redirect('plantas')
    return render(request, 'CRUD Planta/eliminarPlanta.html', {'plants': plants})

def buscarPlanta(request):
    query = request.GET.get('buscarPlanta', '').strip()
    plants = Plant.objects.filter(plant_name__icontains=query) if query else Plant.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'CRUD Planta/plantas.html', {'plants': plants, 'categories': categories, 'query': query})

#######CATALOGO PLANTAS##########
def catalogoPlantas(request):
    plants = Plant.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'Catalogo/catalogoPlantas.html', {'plants': plants, 'categories': categories})

def catalogoCategoria(request, categoria_id):
    categoria = get_object_or_404(Categorie, category_id=categoria_id) 
    plants = Plant.objects.filter(category_id=categoria)
    categories = Categorie.objects.all()
    return render(request, 'Catalogo/catalogoPlantas.html', {'plants': plants, 'categories': categories, 'categoria': categoria})

def catalogoBuscar(request):
    query = request.GET.get('buscarPlanta')
    plants = Plant.objects.filter(plant_name__icontains=query) if query else Plant.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'Catalogo/catalogoPlantas.html', {'plants': plants, 'categories': categories, 'query': query})