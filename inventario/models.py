from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    contacto = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    UNIDADES = [
        ('UND', 'Unidad'),
        ('KG', 'Kilogramo'),
        ('LT', 'Litro'),
        ('MT', 'Metro'),
        ('CJ', 'Caja'),
        ('PQ', 'Paquete'),
    ]

    codigo_unico = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    categoria = models.CharField(max_length=80)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad_disponible = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=10)
    unidad_medida = models.CharField(max_length=3, choices=UNIDADES, default='UND')
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='productos'
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo_unico} — {self.nombre}'

    @property
    def es_bajo_stock(self):
        return self.cantidad_disponible <= self.stock_minimo

    @property
    def estado_stock(self):
        if self.cantidad_disponible == 0:
            return 'sin_stock'
        elif self.es_bajo_stock:
            return 'bajo'
        return 'normal'


class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(default=timezone.now)
    descripcion = models.CharField(max_length=300, blank=True)
    usuario_responsable = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='movimientos'
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='movimientos'
    )
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='movimientos'
    )

    class Meta:
        verbose_name = 'Movimiento de inventario'
        verbose_name_plural = 'Movimientos de inventario'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.tipo} — {self.producto.nombre} ({self.cantidad})'


class AlertaStock(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('ATENDIDA', 'Atendida'),
        ('IGNORADA', 'Ignorada'),
    ]

    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='alertas'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    mensaje = models.CharField(max_length=300)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVA')
    nivel_critico = models.IntegerField()

    class Meta:
        verbose_name = 'Alerta de stock'
        verbose_name_plural = 'Alertas de stock'
        ordering = ['-fecha']

    def __str__(self):
        return f'Alerta: {self.producto.nombre} — {self.estado}'


class OrdenCompra(models.Model):
    ESTADO_CHOICES = [
        ('SUGERIDA', 'Sugerida'),
        ('APROBADA', 'Aprobada'),
        ('ENVIADA', 'Enviada'),
        ('RECIBIDA', 'Recibida'),
        ('CANCELADA', 'Cancelada'),
    ]

    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='ordenes'
    )
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, related_name='ordenes'
    )
    alerta = models.ForeignKey(
        AlertaStock, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='ordenes'
    )
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='ordenes'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='SUGERIDA')
    cantidad_sugerida = models.IntegerField()
    observaciones = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = 'Orden de compra'
        verbose_name_plural = 'Órdenes de compra'
        ordering = ['-fecha']

    def __str__(self):
        return f'OC-{self.pk} — {self.producto.nombre} ({self.estado})'
