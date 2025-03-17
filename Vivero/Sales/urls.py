from django.urls import path
from . import views

urlpatterns = [
    # Carrito
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/<int:plant_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    # Pedidos
    path("register-sale/", views.register_sale, name="register_sale"),
    path("sales-history/", views.sales_history, name="sales_history"),
]
