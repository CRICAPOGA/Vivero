from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from Inventory.models import Plant
from .models import User, Role

# Create your views here.
def login_view(request):
    return render(request, 'login.html')

def login_auth(request):
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['password']
        user = authenticate(request, username=username, password=contraseña)
        if user is not None:
            login(request, user)  # Inicia la sesión del usuario
            if request.user.is_authenticated and request.user.is_staff:
                low_stock_plants = Plant.objects.filter(stock__lt=5)  # Plantas con stock bajo
                total_plants = Plant.objects.count()
                total_users = User.objects.count()
                return render(request, 'index.html', {
                    'low_stock_plants': low_stock_plants,
                    'total_plants': total_plants,
                    'total_users': total_users
                })
            return render(request, 'index.html')
        else:
            messages.error(request,'Credenciales incorrectas')
            return render(request, 'login.html')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'login.html')

def register_view(request):
    roles = Role.objects.all()
    
    if request.method == 'POST':
        name = request.POST['name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role_id = 1

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.name = name
        user.last_name = last_name
        user.role_id = Role.objects.get(role_id=role_id) if role_id else None
        user.save()
        
        messages.success(request, 'Usuario registrado exitosamente')
        return redirect('login')
    
    return render(request, 'register.html', {'roles': roles})

############## CRUD USUARIOS #################
@staff_member_required(login_url='/')
@login_required
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'CRUD usuarios/usuarios.html', {'usuarios': usuarios})

@staff_member_required(login_url='/')
@login_required
def crear_usuario(request):
    roles = Role.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        role_id = request.POST["role_id"]
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
        else:
            role = get_object_or_404(Role, pk=role_id)
            usuario = User.objects.create_user(
                username=username, email=email, name=name,
                last_name=last_name, password=password, role_id=role
            )
            usuario.save()
            messages.success(request, "Usuario creado exitosamente.")
            return redirect("lista_usuarios")
    
    return render(request, "CRUD usuarios/crear_usuario.html", {"roles": roles})

@staff_member_required(login_url='/')
@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    roles = Role.objects.all()
    
    if request.method == "POST":
        usuario.username = request.POST["username"]
        usuario.email = request.POST["email"]
        usuario.name = request.POST["name"]
        usuario.last_name = request.POST["last_name"]
        role_id = request.POST["role_id"]
        usuario.role_id = get_object_or_404(Role, pk=role_id)
        
        if "password" in request.POST and request.POST["password"]:
            usuario.set_password(request.POST["password"])
        
        usuario.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect("lista_usuarios")
    
    return render(request, "CRUD usuarios/editar_usuario.html", {"usuario": usuario, "roles": roles})

@staff_member_required(login_url='/')
@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect("lista_usuarios")
