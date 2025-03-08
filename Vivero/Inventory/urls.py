from django.urls import path
from . import views

urlpatterns = [
    path('plantas/', views.plantas, name='plantas'),

    path('catalogoPlantas/', views.catalogoPlantas, name='catalogoPlantas'),
    path('catalogoPlantas/plantas/categoria/<int:categoria_id>/', views.catalogoCategoria, name='catalogoCategoria'),
    path('catalogoPlantas/plantas/buscar/', views.catalogoBuscar, name='catalogoBuscar'),

]


