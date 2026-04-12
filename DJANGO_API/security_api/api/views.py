from rest_framework import viewsets, serializers, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsAdminOrSelf  # tu permiso personalizado

from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from .serializers import PasswordChangeSerializer

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
    

#nuevo
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSelf]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    # NUEVO ENDPOINT: cambiar contraseña
    @action(detail=True, methods=['put'], url_path='password')
    def change_password(self, request, pk=None):
        user = self.get_object()
        current_user = request.user

        # CONTROL DE ACCESO (OWASP)
        if current_user.id != user.id and not current_user.is_staff:
            return Response({"error": "No autorizado"}, status=403)

        serializer = PasswordChangeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")

        # Usuario normal → validar contraseña actual
        if not current_user.is_staff:
            if not check_password(old_password, user.password):
                return Response({"error": "Contraseña actual incorrecta"}, status=400)

        # Cambiar contraseña
        user.set_password(new_password)
        user.save()

        return Response({"msg": "Contraseña actualizada correctamente"})