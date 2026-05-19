from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.proveedor_lista, name='lista'),
    path('<int:pk>/', views.proveedor_detalle, name='detalle'),
    path('nuevo/', views.proveedor_crear, name='crear'),
    path('<int:pk>/editar/', views.proveedor_editar, name='editar'),
    path('<int:pk>/desactivar/', views.proveedor_desactivar, name='desactivar'),
]