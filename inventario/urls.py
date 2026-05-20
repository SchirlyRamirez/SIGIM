from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.producto_lista, name='producto_lista'),
    path('<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('nuevo/', views.producto_crear, name='producto_crear'),
    path('<int:pk>/editar/', views.producto_editar, name='producto_editar'),
    path('entrada/', views.registrar_entrada, name='entrada'),
    path('entrada/<int:pk>/', views.registrar_entrada, name='entrada_producto'),
    path('salida/', views.registrar_salida, name='salida'),
    path('salida/<int:pk>/', views.registrar_salida, name='salida_producto'),
    path('alertas/', views.alertas_lista, name='alertas'),
    path('alertas/<int:pk>/atender/', views.atender_alerta, name='atender_alerta'),
    path('ordenes/', views.ordenes_lista, name='ordenes'),
    path('ordenes/<int:pk>/aprobar/', views.aprobar_orden, name='aprobar_orden'),
    path('historial/', views.historial_movimientos, name='historial'),
    path('busqueda/', views.busqueda_global, name='busqueda'),
]
