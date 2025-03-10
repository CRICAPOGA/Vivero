from django.urls import path
from .views import Vista_subir_excel
from . import views

urlpatterns = [
    path('ejemplo/', views.ejemplo, name='ejemplo'),
    path('subir-excel/', Vista_subir_excel.as_view(), name='subir_excel'),
]