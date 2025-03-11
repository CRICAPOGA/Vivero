from django.urls import path
from . import views
from .views import Vista_subir_excel
from .views import dashboard

urlpatterns = [
    path('plantas/', views.plantas, name='plantas'),
    path('plantas/categoria/<int:categoria_id>/', views.plantasPorCategoria, name='plantasPorCategoria'),
    path('plantas/crear/', views.crearPlanta, name='crearPlanta'),
    path('plantas/editar/<int:planta_id>/', views.editarPlanta, name='editarPlanta'),
    path('plantas/eliminar/<int:planta_id>/', views.eliminarPlanta, name='eliminarPlanta'),
    path('plantas/buscar/', views.buscarPlanta, name='buscarPlanta'),

    path('catalogoPlantas/', views.catalogoPlantas, name='catalogoPlantas'),
    path('catalogoPlantas/buscar/', views.catalogoBuscar, name='catalogoBuscar'),
    path('catalogoPlantas/categoria/<int:categoria_id>/', views.catalogoCategoria, name='catalogoCategoria'),

    path('subir-excel/', Vista_subir_excel.as_view(), name='subir_excel'),

    path('dashboard/', dashboard, name='dashboard'),
]