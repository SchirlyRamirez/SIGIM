from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.http import JsonResponse

from .models import Producto, Proveedor, MovimientoInventario, AlertaStock, OrdenCompra
from .forms import ProductoForm, MovimientoForm, ProveedorForm


# ─── DASHBOARD ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    from django.db.models import Count, Q
    import json

    total_productos = Producto.objects.filter(activo=True).count()
    sin_stock = Producto.objects.filter(activo=True, cantidad_disponible=0).count()
    bajo_stock = Producto.objects.filter(activo=True).extra(
        where=['cantidad_disponible > 0 AND cantidad_disponible <= stock_minimo']
    ).count()
    alertas_activas = AlertaStock.objects.filter(estado='ACTIVA').count()
    ordenes_pendientes = OrdenCompra.objects.filter(estado__in=['SUGERIDA', 'APROBADA']).count()
    ultimos_movimientos = MovimientoInventario.objects.select_related(
        'producto', 'usuario_responsable'
    ).order_by('-fecha')[:8]
    alertas = AlertaStock.objects.filter(estado='ACTIVA').select_related('producto')[:5]
    productos_criticos = Producto.objects.filter(activo=True).extra(
        where=['cantidad_disponible <= stock_minimo']
    ).order_by('cantidad_disponible')[:5]

    # Datos para graficas
    cats = Producto.objects.filter(activo=True).values_list('categoria', flat=True).distinct().order_by('categoria')
    categorias_labels = list(cats)
    categorias_data, stock_normal, stock_bajo, stock_sin = [], [], [], []

    for cat in categorias_labels:
        prods = Producto.objects.filter(activo=True, categoria=cat)
        categorias_data.append(prods.count())
        stock_normal.append(prods.extra(where=['cantidad_disponible > stock_minimo']).count())
        stock_bajo.append(prods.extra(where=['cantidad_disponible > 0 AND cantidad_disponible <= stock_minimo']).count())
        stock_sin.append(prods.filter(cantidad_disponible=0).count())

    context = {
        'total_productos': total_productos,
        'sin_stock': sin_stock,
        'bajo_stock': bajo_stock,
        'alertas_activas': alertas_activas,
        'ordenes_pendientes': ordenes_pendientes,
        'ultimos_movimientos': ultimos_movimientos,
        'alertas': alertas,
        'productos_criticos': productos_criticos,
        'categorias_labels': json.dumps(categorias_labels),
        'categorias_data': json.dumps(categorias_data),
        'stock_normal': json.dumps(stock_normal),
        'stock_bajo': json.dumps(stock_bajo),
        'stock_sin': json.dumps(stock_sin),
        'titulo': 'Dashboard',
    }
    return render(request, 'dashboard/home.html', context)

# ─── PRODUCTOS ────────────────────────────────────────────────────────────────

@login_required
def producto_lista(request):
    query = request.GET.get('q', '')
    categoria = request.GET.get('categoria', '')
    estado = request.GET.get('estado', '')

    productos = Producto.objects.filter(activo=True).select_related('proveedor')

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(codigo_unico__icontains=query) |
            Q(categoria__icontains=query)
        )
    if categoria:
        productos = productos.filter(categoria__icontains=categoria)
    if estado == 'bajo':
        productos = productos.extra(where=['cantidad_disponible <= stock_minimo AND cantidad_disponible > 0'])
    elif estado == 'sin_stock':
        productos = productos.filter(cantidad_disponible=0)
    elif estado == 'normal':
        productos = productos.extra(where=['cantidad_disponible > stock_minimo'])

    categorias = Producto.objects.filter(activo=True).values_list(
        'categoria', flat=True
    ).distinct().order_by('categoria')

    context = {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_sel': categoria,
        'estado_sel': estado,
        'titulo': 'Inventario de productos',
    }
    return render(request, 'inventario/producto_lista.html', context)


@login_required
def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    movimientos = producto.movimientos.select_related(
        'usuario_responsable', 'proveedor'
    ).order_by('-fecha')[:20]
    alertas = producto.alertas.order_by('-fecha')[:5]
    context = {
        'producto': producto,
        'movimientos': movimientos,
        'alertas': alertas,
        'titulo': f'Detalle — {producto.nombre}',
    }
    return render(request, 'inventario/producto_detalle.html', context)


@login_required
def producto_crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" registrado exitosamente.')
            return redirect('inventario:producto_detalle', pk=producto.pk)
    else:
        form = ProductoForm()
    return render(request, 'inventario/producto_form.html', {
        'form': form, 'titulo': 'Registrar producto', 'accion': 'Registrar'
    })


@login_required
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado.')
            return redirect('inventario:producto_detalle', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/producto_form.html', {
        'form': form, 'titulo': 'Editar producto',
        'accion': 'Guardar cambios', 'producto': producto
    })


# ─── MOVIMIENTOS ──────────────────────────────────────────────────────────────

@login_required
def registrar_entrada(request, pk=None):
    producto = get_object_or_404(Producto, pk=pk) if pk else None
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.tipo = 'ENTRADA'
            movimiento.usuario_responsable = request.user
            movimiento.save()

            # Actualizar stock
            prod = movimiento.producto
            prod.cantidad_disponible += movimiento.cantidad
            prod.save()

            # Cerrar alertas activas si el stock ya es suficiente
            if not prod.es_bajo_stock:
                prod.alertas.filter(estado='ACTIVA').update(estado='ATENDIDA')

            messages.success(
                request,
                f'Entrada de {movimiento.cantidad} unidades de "{prod.nombre}" registrada.'
            )
            return redirect('inventario:producto_detalle', pk=prod.pk)
    else:
        initial = {'producto': producto} if producto else {}
        form = MovimientoForm(initial=initial)
    return render(request, 'inventario/movimiento_form.html', {
        'form': form, 'titulo': 'Registrar entrada de inventario',
        'tipo': 'ENTRADA', 'producto': producto
    })


@login_required
def registrar_salida(request, pk=None):
    producto = get_object_or_404(Producto, pk=pk) if pk else None
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.tipo = 'SALIDA'
            movimiento.usuario_responsable = request.user
            prod = movimiento.producto

            if movimiento.cantidad > prod.cantidad_disponible:
                messages.error(request, 'No hay suficiente stock para esta salida.')
                return render(request, 'inventario/movimiento_form.html', {
                    'form': form, 'titulo': 'Registrar salida',
                    'tipo': 'SALIDA', 'producto': producto
                })

            movimiento.save()
            prod.cantidad_disponible -= movimiento.cantidad
            prod.save()

            # Generar alerta si cae bajo stock mínimo
            if prod.es_bajo_stock:
                alerta, creada = AlertaStock.objects.get_or_create(
                    producto=prod,
                    estado='ACTIVA',
                    defaults={
                        'mensaje': f'Stock de "{prod.nombre}" en nivel crítico: {prod.cantidad_disponible} unidades.',
                        'nivel_critico': prod.cantidad_disponible,
                    }
                )
                if creada:
                    # Generar sugerencia de orden de compra
                    if prod.proveedor:
                        OrdenCompra.objects.create(
                            producto=prod,
                            proveedor=prod.proveedor,
                            alerta=alerta,
                            usuario=request.user,
                            cantidad_sugerida=prod.stock_minimo * 3,
                            observaciones='Generada automáticamente por alerta de stock.',
                        )
                    messages.warning(
                        request,
                        f'⚠ Stock bajo detectado en "{prod.nombre}". Se generó una alerta y sugerencia de pedido.'
                    )

            messages.success(request, f'Salida de {movimiento.cantidad} unidades registrada.')
            return redirect('inventario:producto_detalle', pk=prod.pk)
    else:
        initial = {'producto': producto} if producto else {}
        form = MovimientoForm(initial=initial)
    return render(request, 'inventario/movimiento_form.html', {
        'form': form, 'titulo': 'Registrar salida de inventario',
        'tipo': 'SALIDA', 'producto': producto
    })


# ─── ALERTAS ──────────────────────────────────────────────────────────────────

@login_required
def alertas_lista(request):
    alertas = AlertaStock.objects.select_related('producto').order_by('-fecha')
    activas = alertas.filter(estado='ACTIVA')
    context = {
        'alertas': alertas,
        'activas_count': activas.count(),
        'titulo': 'Alertas de stock',
    }
    return render(request, 'inventario/alertas.html', context)


@login_required
def atender_alerta(request, pk):
    alerta = get_object_or_404(AlertaStock, pk=pk)
    alerta.estado = 'ATENDIDA'
    alerta.save()
    messages.success(request, 'Alerta marcada como atendida.')
    return redirect('inventario:alertas')


# ─── ÓRDENES DE COMPRA ────────────────────────────────────────────────────────

@login_required
def ordenes_lista(request):
    ordenes = OrdenCompra.objects.select_related(
        'producto', 'proveedor', 'usuario'
    ).order_by('-fecha')
    context = {'ordenes': ordenes, 'titulo': 'Órdenes de compra'}
    return render(request, 'inventario/ordenes.html', context)


@login_required
def aprobar_orden(request, pk):
    orden = get_object_or_404(OrdenCompra, pk=pk)
    orden.estado = 'APROBADA'
    orden.save()
    messages.success(request, f'Orden OC-{orden.pk} aprobada y enviada al proveedor.')
    return redirect('inventario:ordenes')
