"""
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import serializers
from .permissions import IsAdminOrSelf

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]

    # Sobrescribimos get_queryset para que usuarios normales vean solo su usuario
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)
"""


"""
ESTE FUNCIONA
# views.py
from rest_framework import viewsets, serializers, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsAdminOrSelf

# Serializer para listar usuarios (sin password)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serializer para crear usuario con contraseña
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

# ViewSet para CRUD de usuarios autenticado
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSelf]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    # Solo los superusuarios ven todos los usuarios
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)

# Endpoint público para registro
class UserRegisterAPIView(APIView):
    permission_classes = []  # público

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Tus APIViews de prueba (opcional)
class UsuarioList(APIView):
    def get(self, request):
        return Response({"mensaje": "Lista de usuarios"})

class UsuarioDetail(APIView):
    def get(self, request, pk):
        return Response({"mensaje": f"Detalle del usuario {pk}"})
"""

from rest_framework import viewsets, serializers, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsAdminOrSelf  # tu permiso personalizado

# Serializer para listar usuarios
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serializer para crear usuario con contraseña y rol
class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[('user','User'), ('admin','Admin')], write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        # Asignar rol
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user

# ViewSet para CRUD de usuarios autenticado
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSelf]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    # Filtrar queryset según rol
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()  # Admin ve todos
        return User.objects.filter(id=user.id)  # Usuario normal ve solo su info

# Endpoint público para registro
class UserRegisterAPIView(APIView):
    permission_classes = []  # público

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Tus APIViews de prueba (opcionales)
class UsuarioList(APIView):
    def get(self, request):
        return Response({"mensaje": "Lista de usuarios"})

class UsuarioDetail(APIView):
    def get(self, request, pk):
        return Response({"mensaje": f"Detalle del usuario {pk}"})