from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django_tenants.utils import schema_context
from django_tenants.utils import get_tenant_model

from .models import Client, Domain, PlanName
from users.models import User
# Create your views here.


class UserLoginAPIView(viewsets.ModelViewSet):
    def post(self, request):
        email = request.data.get('email')
        print(email)
        password = request.data.get('password')
        print(password)
