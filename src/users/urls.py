from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserLoginAPIView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'login', UserLoginAPIView, basename='login')

urlpatterns = [
    path('api/', include(router.urls)),
    # path('login/', UserLoginAPIView.as_view(), name='login')
]
