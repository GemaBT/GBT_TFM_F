from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    """
    Permite que los superusuarios accedan a todos los usuarios,
    y usuarios normales solo a su propio usuario.
    """

    def has_object_permission(self, request, view, obj):
        # Superusuario: acceso total
        if request.user.is_superuser:
            return True
        # Usuario normal: solo a su propio registro
        return obj == request.user