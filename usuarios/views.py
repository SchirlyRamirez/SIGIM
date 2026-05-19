from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UsuarioCrearForm, UsuarioEditarForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard:home'))
        else:
            messages.error(request, 'Usuario o contrasena incorrectos.')
    return render(request, 'auth/login.html', {'titulo': 'Iniciar sesion'})


def logout_view(request):
    logout(request)
    messages.info(request, 'Sesion cerrada correctamente.')
    return redirect('usuarios:login')


@login_required
def usuario_lista(request):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para acceder a esta seccion.')
        return redirect('dashboard:home')
    usuarios = User.objects.all().order_by('username')
    return render(request, 'usuarios/lista.html', {
        'usuarios': usuarios, 'titulo': 'Gestion de usuarios'
    })


@login_required
def usuario_crear(request):
    if not request.user.is_staff:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = UsuarioCrearForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            rol = form.cleaned_data['rol']
            if rol == 'admin':
                user.is_staff = True
            user.save()
            messages.success(request, f'Usuario "{user.username}" creado exitosamente.')
            return redirect('usuarios:lista')
    else:
        form = UsuarioCrearForm()
    return render(request, 'usuarios/form.html', {
        'form': form, 'titulo': 'Nuevo usuario', 'accion': 'Crear'
    })


@login_required
def usuario_editar(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard:home')
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            rol = form.cleaned_data['rol']
            user.is_staff = (rol == 'admin')
            user.save()
            messages.success(request, f'Usuario "{user.username}" actualizado.')
            return redirect('usuarios:lista')
    else:
        rol_inicial = 'admin' if usuario.is_staff else 'encargado'
        form = UsuarioEditarForm(instance=usuario, initial={'rol': rol_inicial})
    return render(request, 'usuarios/form.html', {
        'form': form, 'titulo': f'Editar: {usuario.username}',
        'accion': 'Guardar', 'usuario': usuario
    })


@login_required
def usuario_desactivar(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard:home')
    usuario = get_object_or_404(User, pk=pk)
    if usuario == request.user:
        messages.error(request, 'No puedes desactivarte a ti mismo.')
        return redirect('usuarios:lista')
    if request.method == 'POST':
        usuario.is_active = not usuario.is_active
        usuario.save()
        estado = 'activado' if usuario.is_active else 'desactivado'
        messages.success(request, f'Usuario "{usuario.username}" {estado}.')
        return redirect('usuarios:lista')
    return render(request, 'usuarios/confirmar_desactivar.html', {
        'usuario': usuario, 'titulo': 'Confirmar accion'
    })