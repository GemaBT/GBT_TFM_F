"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers  
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
# urls.py
"""
ESTE FUNCIONA
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import UserViewSet, UserRegisterAPIView

# Router para UserViewSet
router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuarios')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registro/', UserRegisterAPIView.as_view(), name='user-register'),  # registro público
    path('', include(router.urls)),  # CRUD de usuarios autenticado
]
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import UserViewSet, UserRegisterAPIView

# Router para UserViewSet
router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuarios')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registro/', UserRegisterAPIView.as_view(), name='user-register'),  # registro público
    path('', include(router.urls)),  # CRUD de usuarios autenticado
]