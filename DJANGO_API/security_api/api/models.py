from django.db import models
from django.contrib.auth.models import User


# ========================
# ROLES
# ========================
class Rol(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'roles'
        managed = True

    def __str__(self):
        return self.name


# ========================
# PERMISOS
# ========================
class Permiso(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'permissions'
        managed = True

    def __str__(self):
        return self.name


# ========================
# ROLE_PERMISSIONS
# ========================
class RolPermiso(models.Model):
    role = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='permisos')
    permission = models.ForeignKey(Permiso, on_delete=models.CASCADE, related_name='roles')

    class Meta:
        db_table = 'role_permissions'
        managed = True
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.name} -> {self.permission.name}"


# ========================
# USUARIO (perfil extendido)
# ========================
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    role = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name='usuarios')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        managed = True

    def __str__(self):
        return f"{self.user.username} - Rol {self.role.name}"