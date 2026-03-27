# api/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from .models import Usuario, Rol, Permiso, RolPermiso
from .serializers import (
    UsuarioSerializer,
    RolSerializer,
    PermisoSerializer,
)

# ========================
# UTILIDADES DE PERMISOS
# ========================
def check_role_permission(user, permiso_id):
    """Verifica si el usuario tiene el permiso según su rol"""
    try:
        usuario = Usuario.objects.get(user=user)
        return RolPermiso.objects.filter(role_id=usuario.role_id, permission_id=permiso_id).exists()
    except Usuario.DoesNotExist:
        return False

# ========================
# CRUD USUARIOS
# ========================

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UsuarioSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])  # <-- aquí
def registrar_usuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
#poner por defecto el idRole a 2

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_usuarios(request):
    if not check_role_permission(request.user, permiso_id=1):  # ID permiso: listar usuarios
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_usuario(request):
    if not check_role_permission(request.user, permiso_id=2):  # ID permiso: crear usuario
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_usuario(request, pk):
    if not check_role_permission(request.user, permiso_id=3):  # ID permiso: ver usuario
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_usuario(request, pk):
    if not check_role_permission(request.user, permiso_id=4):  # ID permiso: editar usuario
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UsuarioSerializer(usuario, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_usuario(request, pk):
    if not check_role_permission(request.user, permiso_id=5):  # ID permiso: eliminar usuario
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    usuario.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# ========================
# CRUD ROLES
# ========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_roles(request):
    if not check_role_permission(request.user, permiso_id=6):
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
    roles = Rol.objects.all()
    serializer = RolSerializer(roles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_rol(request, pk):
    if not check_role_permission(request.user, permiso_id=6):  # Puedes usar el mismo permiso que listar roles
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        rol = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response({"error": "Rol no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = RolSerializer(rol)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_rol(request):
    if not check_role_permission(request.user, permiso_id=7):
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
    serializer = RolSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_rol(request, pk):
    if not check_role_permission(request.user, permiso_id=8):
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
    try:
        rol = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RolSerializer(rol, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_rol(request, pk):
    if not check_role_permission(request.user, permiso_id=9):
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
    try:
        rol = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    rol.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# ========================
# CRUD PERMISOS
# ========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_permisos(request):
    permisos = Permiso.objects.all()
    serializer = PermisoSerializer(permisos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_permiso(request):
    serializer = PermisoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_permiso(request, permiso_id):
    try:
        permiso = Permiso.objects.get(id=permiso_id)
        serializer = PermisoSerializer(permiso)
        return Response(serializer.data)
    except Permiso.DoesNotExist:
        return Response({"error": "Permiso no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_permiso(request, permiso_id):
    try:
        permiso = Permiso.objects.get(id=permiso_id)
    except Permiso.DoesNotExist:
        return Response({"error": "Permiso no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = PermisoSerializer(permiso, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_permiso(request, permiso_id):
    try:
        permiso = Permiso.objects.get(id=permiso_id)
        permiso.delete()
        return Response({"message": "Permiso eliminado"}, status=status.HTTP_200_OK)
    except Permiso.DoesNotExist:
        return Response({"error": "Permiso no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# ========================
# CRUD USER SESSIONS
# ========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_sesiones(request):
    sesiones = UserSession.objects.all()
    serializer = UserSessionSerializer(sesiones, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_sesion(request):
    serializer = UserSessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_sesion(request, sesion_id):
    try:
        sesion = UserSession.objects.get(id=sesion_id)
        serializer = UserSessionSerializer(sesion)
        return Response(serializer.data)
    except UserSession.DoesNotExist:
        return Response({"error": "Sesión no encontrada"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_sesion(request, sesion_id):
    try:
        sesion = UserSession.objects.get(id=sesion_id)
    except UserSession.DoesNotExist:
        return Response({"error": "Sesión no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSessionSerializer(sesion, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_sesion(request, sesion_id):
    try:
        sesion = UserSession.objects.get(id=sesion_id)
        sesion.delete()
        return Response({"message": "Sesión eliminada"}, status=status.HTTP_200_OK)
    except UserSession.DoesNotExist:
        return Response({"error": "Sesión no encontrada"}, status=status.HTTP_404_NOT_FOUND)

# ========================
# CRUD AUTH LOGS
# ========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_logs(request):
    logs = AuthLog.objects.all()
    serializer = AuthLogSerializer(logs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_log(request):
    serializer = AuthLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_log(request, log_id):
    try:
        log = AuthLog.objects.get(id=log_id)
        serializer = AuthLogSerializer(log)
        return Response(serializer.data)
    except AuthLog.DoesNotExist:
        return Response({"error": "Log no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_log(request, log_id):
    try:
        log = AuthLog.objects.get(id=log_id)
    except AuthLog.DoesNotExist:
        return Response({"error": "Log no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    serializer = AuthLogSerializer(log, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_log(request, log_id):
    try:
        log = AuthLog.objects.get(id=log_id)
        log.delete()
        return Response({"message": "Log eliminado"}, status=status.HTTP_200_OK)
    except AuthLog.DoesNotExist:
        return Response({"error": "Log no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
# ========================
# LISTAR SESIONES
# ========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_sesiones(request):
    if not check_role_permission(request.user, permiso_id=10):  # crea un permiso "listar sesiones"
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

    sesiones = UserSession.objects.all()
    serializer = UserSessionSerializer(sesiones, many=True)
    return Response(serializer.data)


# ========================
# CREAR SESIÓN
# ========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_sesion(request):
    if not check_role_permission(request.user, permiso_id=11):  # permiso "crear sesión"
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserSessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================
# OBTENER SESIÓN POR ID
# ========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_sesion(request, sesion_id):
    if not check_role_permission(request.user, permiso_id=10):
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

    try:
        sesion = UserSession.objects.get(pk=sesion_id)
    except UserSession.DoesNotExist:
        return Response({"error": "Sesión no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSessionSerializer(sesion)
    return Response(serializer.data)


# ========================
# ACTUALIZAR SESIÓN
# ========================
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_sesion(request, sesion_id):
    if not check_role_permission(request.user, permiso_id=12):  # permiso "actualizar sesión"
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

    try:
        sesion = UserSession.objects.get(pk=sesion_id)
    except UserSession.DoesNotExist:
        return Response({"error": "Sesión no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSessionSerializer(sesion, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================
# ELIMINAR SESIÓN
# ========================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_sesion(request, sesion_id):
    if not check_role_permission(request.user, permiso_id=13):  # permiso "eliminar sesión"
        return Response({"detail": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

    try:
        sesion = UserSession.objects.get(pk=sesion_id)
    except UserSession.DoesNotExist:
        return Response({"error": "Sesión no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    sesion.delete()
    return Response({"message": "Sesión eliminada"}, status=status.HTTP_200_OK)