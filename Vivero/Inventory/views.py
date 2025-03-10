import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Categorie, Plant
from django.core.files.storage import default_storage

class Vista_subir_excel(View):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No se ha subido ningún archivo'}, status=400)

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

            return JsonResponse({'message': 'Stock actualizado correctamente'})
        except Exception as e:
            message = {'error': f'Ocurrió un error: {str(e)}'}

        finally:
            # Eliminar el archivo después de procesarlo
            if default_storage.exists(file_path):
                default_storage.delete(file_path)

        return JsonResponse(message)

def ejemplo(request):
    return render(request, 'ejemplo.html')