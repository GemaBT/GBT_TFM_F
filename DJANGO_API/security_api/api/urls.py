from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ========================
    # JWT
    # ========================
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ========================
    # USUARIOS
    # ========================
    path('usuarios/registro/', views.registrar_usuario, name='registro_usuario'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:pk>/', views.obtener_usuario, name='obtener_usuario'),
    path('usuarios/<int:pk>/actualizar/', views.actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),

    # ========================
    # ROLES
    # ========================
    path('roles/', views.listar_roles, name='listar_roles'),
    path('roles/crear/', views.crear_rol, name='crear_rol'),
    path('roles/<int:pk>/', views.obtener_rol, name='obtener_rol'),
    path('roles/<int:pk>/actualizar/', views.actualizar_rol, name='actualizar_rol'),
    path('roles/<int:pk>/eliminar/', views.eliminar_rol, name='eliminar_rol'),

    # ========================
    # PERMISOS
    # ========================
    path('permisos/', views.listar_permisos, name='listar_permisos'),
    path('permisos/crear/', views.crear_permiso, name='crear_permiso'),
    path('permisos/<int:permiso_id>/', views.obtener_permiso, name='obtener_permiso'),
    path('permisos/<int:permiso_id>/actualizar/', views.actualizar_permiso, name='actualizar_permiso'),
    path('permisos/<int:permiso_id>/eliminar/', views.eliminar_permiso, name='eliminar_permiso'),


     
]