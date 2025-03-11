from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/<int:plant_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:plant_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/increment/<int:plant_id>/", views.increment_from_cart, name="increment_from_cart"),
    path("cart/decrement/<int:plant_id>/", views.decrement_from_cart, name="decrement_from_cart"),
    path("cart/clean/", views.clean_cart, name="clean_cart"),
    path("register-sale/", views.register_sale, name="register_sale"),
    path("sales-history/", views.sales_history, name="sales_history"),
]
