"""
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def inicio(request):
    return Response({"mensaje": "Hola, esta es mi primera API con Django"})

@api_view(['GET'])
def usuarios(request):
    return Response([
        {"id": 1, "nombre": "Ana"},
        {"id": 2, "nombre": "Carlos"}
    ])

"""
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def inicio(request):
    return Response({"mensaje": "Hola, esta es mi primera API con Django"})

@api_view(['GET'])
def usuarios(request):
    return Response([
        {"id": 1, "nombre": "Ana"},
        {"id": 2, "nombre": "Carlos"}
    ])
"""
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializers import UsuarioSerializer

# GET (todos) + POST
@api_view(['GET', 'POST'])
def usuarios(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET uno + PUT + DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def usuario_detalle(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario, Rol, Permiso
from .serializers import UsuarioSerializer  # luego puedes crear RolSerializer y PermisoSerializer


# ========================
# USUARIOS
# ========================

# GET (todos) + POST
@api_view(['GET', 'POST'])
def usuarios(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET uno + PUT + DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def usuario_detalle(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ========================
# ROLES (ejemplo)
# ========================
# Puedes expandir de manera similar a usuarios
@api_view(['GET', 'POST'])
def roles(request):
    if request.method == 'GET':
        roles = Rol.objects.all()
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = RolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def rol_detalle(request, pk):
    try:
        rol = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RolSerializer(rol)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RolSerializer(rol, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        rol.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ========================
# PERMISOS (ejemplo)
# ========================
@api_view(['GET', 'POST'])
def permisos(request):
    if request.method == 'GET':
        permisos = Permiso.objects.all()
        serializer = PermisoSerializer(permisos, many=True)
        return Response(serializer.data)
    
    elif request.method == ['POST']:
        serializer = PermisoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario, Rol, Permiso
from .serializers import UsuarioSerializer, RolSerializer, PermisoSerializer

# ========================
# USUARIOS
# ========================

# Listar todos los usuarios
@api_view(['GET'])
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)


# Crear un usuario
@api_view(['POST'])
def crear_usuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Obtener un usuario por ID
@api_view(['GET'])
def obtener_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)


# Actualizar un usuario por ID
@api_view(['PUT'])
def actualizar_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UsuarioSerializer(usuario, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Eliminar un usuario por ID
@api_view(['DELETE'])
def eliminar_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    usuario.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ========================
# ROLES
# ========================

@api_view(['GET'])
def listar_roles(request):
    roles = Rol.objects.all()
    serializer = RolSerializer(roles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def crear_rol(request):
    serializer = RolSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def obtener_rol(request, pk):
    try:
        rol = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RolSerializer(rol)
    return Response(serializer.data)


@api_view(['PUT'])
def actualizar_rol(request, pk):
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
def eliminar_rol(request, pk):
    try:
        rol = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    rol.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ========================
# PERMISOS
# ========================

@api_view(['GET'])
def listar_permisos(request):
    permisos = Permiso.objects.all()
    serializer = PermisoSerializer(permisos, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def crear_permiso(request):
    serializer = PermisoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def obtener_permiso(request, pk):
    try:
        permiso = Permiso.objects.get(pk=pk)
    except Permiso.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PermisoSerializer(permiso)
    return Response(serializer.data)


@api_view(['PUT'])
def actualizar_permiso(request, pk):
    try:
        permiso = Permiso.objects.get(pk=pk)
    except Permiso.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PermisoSerializer(permiso, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminar_permiso(request, pk):
    try:
        permiso = Permiso.objects.get(pk=pk)
    except Permiso.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    permiso.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

from .models import UserSession, AuthLog
from .serializers import UserSessionSerializer, AuthLogSerializer

# ========================
# USER SESSIONS
# ========================

@api_view(['GET'])
def listar_sesiones(request):
    sesiones = UserSession.objects.all()
    serializer = UserSessionSerializer(sesiones, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def crear_sesion(request):
    serializer = UserSessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def obtener_sesion(request, pk):
    try:
        sesion = UserSession.objects.get(pk=pk)
    except UserSession.DoesNotExist:
        return Response(status=404)
    serializer = UserSessionSerializer(sesion)
    return Response(serializer.data)


@api_view(['PUT'])
def actualizar_sesion(request, pk):
    try:
        sesion = UserSession.objects.get(pk=pk)
    except UserSession.DoesNotExist:
        return Response(status=404)
    serializer = UserSessionSerializer(sesion, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def eliminar_sesion(request, pk):
    try:
        sesion = UserSession.objects.get(pk=pk)
    except UserSession.DoesNotExist:
        return Response(status=404)
    sesion.delete()
    return Response(status=204)



# ========================
# AUTH LOGS
# ========================

@api_view(['GET'])
def listar_logs(request):
    logs = AuthLog.objects.all()
    serializer = AuthLogSerializer(logs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def crear_log(request):
    serializer = AuthLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def obtener_log(request, pk):
    try:
        log = AuthLog.objects.get(pk=pk)
    except AuthLog.DoesNotExist:
        return Response(status=404)
    serializer = AuthLogSerializer(log)
    return Response(serializer.data)


@api_view(['PUT'])
def actualizar_log(request, pk):
    try:
        log = AuthLog.objects.get(pk=pk)
    except AuthLog.DoesNotExist:
        return Response(status=404)
    serializer = AuthLogSerializer(log, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def eliminar_log(request, pk):
    try:
        log = AuthLog.objects.get(pk=pk)
    except AuthLog.DoesNotExist:
        return Response(status=404)
    log.delete()
    return Response(status=204)