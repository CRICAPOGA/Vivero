from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login_auth/', views.login_auth, name='login_auth'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    # path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    # path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    # path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    # path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]
