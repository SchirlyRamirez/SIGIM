from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from inventario.models import Proveedor, Producto
from inventario.forms import ProveedorForm

@login_required
def proveedor_lista(request):
    query = request.GET.get('q', '')
    proveedores = Proveedor.objects.annotate(
        total_productos=Count('productos')
    ).order_by('nombre')
    if query:
        proveedores = proveedores.filter(
            Q(nombre__icontains=query) |
            Q(contacto__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, 'proveedores/lista.html', {
        'proveedores': proveedores, 'query': query, 'titulo': 'Proveedores'
    })

@login_required
def proveedor_detalle(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    productos = proveedor.productos.filter(activo=True).order_by('nombre')
    return render(request, 'proveedores/detalle.html', {
        'proveedor': proveedor, 'productos': productos,
        'titulo': f'Proveedor: {proveedor.nombre}'
    })

@login_required
def proveedor_crear(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor = form.save()
            messages.success(request, f'Proveedor "{proveedor.nombre}" creado exitosamente.')
            return redirect('proveedores:detalle', pk=proveedor.pk)
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/form.html', {
        'form': form, 'titulo': 'Nuevo proveedor', 'accion': 'Registrar'
    })

@login_required
def proveedor_editar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Proveedor "{proveedor.nombre}" actualizado.')
            return redirect('proveedores:detalle', pk=proveedor.pk)
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/form.html', {
        'form': form, 'titulo': 'Editar proveedor',
        'accion': 'Guardar cambios', 'proveedor': proveedor
    })

@login_required
def proveedor_desactivar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.activo = not proveedor.activo
        proveedor.save()
        estado = 'activado' if proveedor.activo else 'desactivado'
        messages.success(request, f'Proveedor "{proveedor.nombre}" {estado}.')
        return redirect('proveedores:lista')
    return render(request, 'proveedores/confirmar_desactivar.html', {
        'proveedor': proveedor, 'titulo': 'Confirmar accion'
    })