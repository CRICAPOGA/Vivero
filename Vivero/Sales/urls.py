from django.urls import path
from . import views

urlpatterns = [
    path('cart/<int:plant_id>/', views.cart, name='cart'),
    path('cart/', views.show_cart, name='show_cart'),
    path("cart/update/<int:plant_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:plant_id>/", views.remove_from_cart, name="remove_from_cart"),
]