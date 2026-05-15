from django.contrib import admin
from .models import Producto, Proveedor, MovimientoInventario, AlertaStock, OrdenCompra

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'contacto', 'telefono', 'email', 'activo']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo_unico', 'nombre', 'categoria', 'cantidad_disponible', 'stock_minimo', 'precio']
    list_filter = ['categoria', 'activo']
    search_fields = ['codigo_unico', 'nombre']

@admin.register(MovimientoInventario)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ['producto', 'tipo', 'cantidad', 'fecha', 'usuario_responsable']
    list_filter = ['tipo']

@admin.register(AlertaStock)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['producto', 'nivel_critico', 'estado', 'fecha']
    list_filter = ['estado']

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'producto', 'proveedor', 'cantidad_sugerida', 'estado', 'fecha']
    list_filter = ['estado']
