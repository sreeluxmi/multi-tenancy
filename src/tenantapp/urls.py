from django.urls import path
from django.contrib import admin
# from rest_framework.routers import DefaultRouter
from .views import UserLoginAPIView

# router = DefaultRouter()
# router.register(r'login', UserLoginAPIView, basename='login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', UserLoginAPIView.as_view(), name="login"),
]
