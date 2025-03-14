import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Categorie, Plant
from django.core.files.storage import default_storage
from .models import Plant, Categorie
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class Vista_subir_excel(View):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            messages.error(request, 'No se ha subido ningún archivo')
            return redirect('plantas')

        # Guardar temporalmente el archivo
        file_path = default_storage.save(file.name, file)
        try:
            # Leer el archivo Excel
            df = pd.read_excel(file_path)

            for _, row in df.iterrows():
                category_name = row['category']
                plant_name = row['plant_name']
                care = row['care']
                price = row['price']
                stock = row['stock']

                # Buscar o crear la categoría
                category, _ = Categorie.objects.get_or_create(category=category_name)

                # Buscar la planta, si existe actualiza el stock, si no, créala
                plant, created = Plant.objects.get_or_create(
                    plant_name=plant_name,
                    category_id=category,
                    defaults={'care': care, 'price': price, 'stock': stock}
                )

                if not created:
                    plant.stock += stock  # Sumar stock existente
                    plant.save()
            verificar_stock(request)
            messages.success(request, 'Stock actualizado correctamente')
            return redirect('plantas')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')
            return redirect('plantas')

        finally:
            # Eliminar el archivo después de procesarlo
            if default_storage.exists(file_path):
                default_storage.delete(file_path)

        return redirect('plantas')


############## CRUD PLANTAS ##############
@login_required
def plantas(request):
    plants = Plant.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'CRUD Planta/plantas.html', {'plants': plants, 'categories': categories})

@login_required
def plantasPorCategoria(request, categoria_id):
    categoria = get_object_or_404(Categorie, category_id=categoria_id)
    plants = Plant.objects.filter(category_id=categoria)
    categories = Categorie.objects.all()
    return render(request, 'CRUD Planta/plantas.html', {'categories': categories, 'plants': plants, 'categoria': categoria})

@login_required
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
        verificar_stock(request)
        return redirect('plantas')
    
    return render(request, 'CRUD Planta/editarPlanta.html', {'plants': plants, 'categories': categories})

@login_required
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
        verificar_stock(request)
        return redirect('plantas')
    
    return render(request, 'CRUD Planta/crearPlanta.html', {'categories': categories})

@login_required
def eliminarPlanta(request, planta_id):
    plants = get_object_or_404(Plant, plant_id=planta_id)
    if request.method == 'POST':
        plants.delete()
        messages.success(request, f'La planta "{plants.plant_name}" ha sido eliminado exitosamente.')
        return redirect('plantas')
    return render(request, 'CRUD Planta/eliminarPlanta.html', {'plants': plants})

@login_required
def buscarPlanta(request):
    query = request.GET.get('buscarPlanta', '').strip()
    plants = Plant.objects.filter(plant_name__icontains=query) if query else Plant.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'CRUD Planta/plantas.html', {'plants': plants, 'categories': categories, 'query': query})

#######CATALOGO PLANTAS##########
@login_required
def catalogoPlantas(request):
    plants = Plant.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'Catalogo/catalogoPlantas.html', {'plants': plants, 'categories': categories})

@login_required
def catalogoCategoria(request, categoria_id):
    categoria = get_object_or_404(Categorie, category_id=categoria_id) 
    plants = Plant.objects.filter(category_id=categoria)
    categories = Categorie.objects.all()
    return render(request, 'Catalogo/catalogoPlantas.html', {'plants': plants, 'categories': categories, 'categoria': categoria})

@login_required
def catalogoBuscar(request):
    query = request.GET.get('buscarPlanta')
    plants = Plant.objects.filter(plant_name__icontains=query) if query else Plant.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'Catalogo/catalogoPlantas.html', {'plants': plants, 'categories': categories, 'query': query})

############## STOCK BAJO ##############
def verificar_stock(request):
    plants = Plant.objects.all()
    for plant in plants:
        if plant.stock <= 5:
            messages.warning(request, f'!STOCK BAJO de {plant.plant_name}¡')
