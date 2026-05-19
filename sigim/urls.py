from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls', namespace='usuarios')),
    path('dashboard/', include('inventario.urls_dashboard', namespace='dashboard')),
    path('inventario/', include('inventario.urls', namespace='inventario')),
    path('proveedores/', include('proveedores.urls', namespace='proveedores')),
    path('', lambda request: redirect('dashboard:home')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
