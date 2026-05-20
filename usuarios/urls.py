from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.usuario_lista, name='lista'),
    path('nuevo/', views.usuario_crear, name='crear'),
    path('<int:pk>/editar/', views.usuario_editar, name='editar'),
    path('<int:pk>/desactivar/', views.usuario_desactivar, name='desactivar'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/password/', views.cambiar_password, name='cambiar_password'),
]