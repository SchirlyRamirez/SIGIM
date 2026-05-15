from django.urls import path
from inventario.views import dashboard

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name='home'),
]
