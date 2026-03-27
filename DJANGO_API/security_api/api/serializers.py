# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Usuario, Rol, Permiso

# ========================
# USUARIO
# ========================
class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'role_id', 'is_active']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=validated_data.pop('password')
        )
        usuario = Usuario.objects.create(user=user, **validated_data)
        return usuario

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        if 'username' in user_data:
            user.username = user_data['username']
        if 'email' in user_data:
            user.email = user_data['email']
        if 'password' in validated_data:
            user.set_password(validated_data.pop('password'))
        user.save()
        return super().update(instance, validated_data)

# ========================
# ROLES
# ========================
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'name', 'description']

# ========================
# PERMISOS
# ========================
class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = ['id', 'name', 'description']


