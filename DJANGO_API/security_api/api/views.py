from rest_framework import viewsets, serializers, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsAdminOrSelf  # tu permiso personalizado

from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from .serializers import PasswordChangeSerializer
from .utils.logging import log_event


from django.contrib.auth import authenticate
#from rest_framework.views import APIView
#from rest_framework.response import Response
#from api.utils.logging import log_event

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from api.utils.logging import log_event

#https
from rest_framework_simplejwt.tokens import RefreshToken
#from django.http import Response
from rest_framework.response import Response

"""
class CustomTokenObtainPairView(TokenObtainPairView):http

    def post(self, request, *args, **kwargs):

        username = request.data.get("username")
        password = request.data.get("password")
        print("DATA:", request.data)
        print("USERNAME:", username)

        ip = request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT")

        try:
            if username and password:
                user = authenticate(username=username, password=password)
            else:
                user = None

            if user:
                log_event(user, "login_success", "200", request)
            else:
                log_event(None, "login_failed", "401", request)

        except Exception as e:
            print("ERROR LOGIN:", e)
            log_event(None, "login_error", "500", request)

        return super().post(request, *args, **kwargs)
"""

#https
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api.utils.logging import log_event


class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Credenciales inválidas"}, status=401)

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        response = Response({"message": "Login correcto"})

        # ACCESS TOKEN (correcto)
        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        # REFRESH TOKEN
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        log_event(user, "login_success", "200", request)

        return response

#-----------
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

# Endpoint público para registro
class UserRegisterAPIView(APIView):
    permission_classes = [] 

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            
            log_event(
                user,
                "user_created",
                "201",
                request
            )
        
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }, status=status.HTTP_201_CREATED
            )
        
        log_event(
            user,
            "user_create_failed",
            "400",
            request
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Tus APIViews de prueba (opcionales)
class UsuarioList(APIView):
    def get(self, request):
        return Response({"mensaje": "Lista de usuarios"})

class UsuarioDetail(APIView):
    def get(self, request, pk):
        return Response({"mensaje": f"Detalle del usuario {pk}"})
    
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

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        # 🔹 LOG antes de borrar
        log_event(
            request.user,
            "delete_user",
            "200",
            request
        )

        # 🔹 borrar usuario
        self.perform_destroy(user)
        print("usuario eliminado")

        return Response(
            {"msg": "Usuario eliminado"},
            status=status.HTTP_200_OK
        )




    # NUEVO ENDPOINT: cambiar contraseña
    @action(detail=True, methods=['put'], url_path='password')
    def change_password(self, request, pk=None):
        user = self.get_object()
        current_user = request.user

        # CONTROL DE ACCESO (OWASP)
        if current_user.id != user.id and not current_user.is_staff:
            log_event(user, "forbidden_access", "403", request)
            return Response({"error": "No autorizado"}, status=403)

        serializer = PasswordChangeSerializer(data=request.data)
        if not serializer.is_valid():
            log_event(user, "password_change_failed", "400", request)
            return Response(serializer.errors, status=400)

        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")

        # Usuario normal → validar contraseña actual
        if not current_user.is_staff:
            if not check_password(old_password, user.password):
                return Response({"error": "Contraseña actual incorrecta"}, status=400)

        # Cambiar contraseña
        log_event(user, "password_change", "200", request)
        user.set_password(new_password)
        user.save()

        return Response({"msg": "Contraseña actualizada correctamente"})