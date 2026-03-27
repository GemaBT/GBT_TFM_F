from rest_framework import permissions
from .models import RolPermiso, Usuario, Permiso

class RolPermisoPermission(permissions.BasePermission):
    """
    Permite acceso solo si el usuario tiene permiso según su rol.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Obtener rol del usuario
        try:
            usuario = Usuario.objects.get(user=user)
            rol = usuario.role
        except Usuario.DoesNotExist:
            return False

        # Verificar si la vista tiene permiso_name definido
        permiso_name = getattr(view, 'permission_name', None)
        if not permiso_name:
            return True  # Si no hay permiso definido, acceso permitido

        # Buscar el permiso por nombre
        try:
            permiso = Permiso.objects.get(name=permiso_name)
        except Permiso.DoesNotExist:
            return False

        # Verificar si el rol tiene ese permiso
        return RolPermiso.objects.filter(role=rol, permission=permiso).exists()