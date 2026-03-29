from django.contrib import admin
from django.urls import path, include
from rest_framework import routers  # <- Esto faltaba
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet  # asegúrate de importar tu ViewSet

router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]



"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

# ----------------------------
# SERIALIZER
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active']

# ----------------------------
# VIEWSET
# ----------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # requiere JWT

# ----------------------------
# ROUTER
# ----------------------------
router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet)

# ----------------------------
# URLS PRINCIPALES
# ----------------------------
urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # Endpoints de usuarios
    path('api/', router.urls),  # /api/usuarios/

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       # login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),      # refresh token
]
"""