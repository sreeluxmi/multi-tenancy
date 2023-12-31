from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django_tenants.utils import schema_context
from django_tenants.utils import get_tenant_model

from .models import Client, Domain, PlanName
from users.models import User
from users.serializers import UserSerializer
# Create your views here.


class UserLoginAPIView(APIView):

    def post(self, request):
        email = request.data.get('email')
        print(email)
        password = request.data.get('password')
        print(password)
        if email is None or password is None:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
  
        cache_key = f'user:{email}:{password}'
        print("cashed key", cache_key)
        cached_user = cache.get(cache_key)
        print(cached_user)

        if cached_user:
            user = cached_user
        else:
            TenantModel = get_tenant_model()
            tenants = TenantModel.objects.all()
            schemas = [tenant.schema_name for tenant in tenants]
            schemas.remove('public')
            schemas.remove('permissionPublic')
            print("All schemas=", schemas)
            for schema_name in schemas:
                print("Current schema=", schema_name)
                with schema_context(schema_name):
                    try:
                        all = User.objects.all()
                        print("all users", all)
                        user = User.objects.filter(email=email).first()
                        print("user", user)
                        if user is not None and user.check_password(password):
                            refresh = RefreshToken.for_user(user)
                            access_token = str(refresh.access_token)


                            client_tenant = Client.objects.get(schema_name=schema_name)
                            plan = PlanName.objects.get(client=client_tenant)
                            domain = get_object_or_404(Domain, tenant=client_tenant)
                            print("client tenant name", client_tenant)
                            print("client plan", plan)
                            print("Domain", domain)
                            print("User", user)
                            print("redirect url", f'http://{domain}:8000/api/login/')
                            return Response({'message': 'Login successful for employee.', 'access_token': access_token,
                                            'redirect_url': f'http://{domain}:8000/api/login/'}, status=status.HTTP_200_OK)
                    except User.DoesNotExist:
                        print(f'User not found in schema {schema_name}')
                    continue
                
                            
                        # if user is None or not user.check_password(password):
                    #         return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
                    #     refresh = RefreshToken.for_user(user)
                    #     access_token = str(refresh.access_token)
                    #     client_tenant = Client.objects.get(schema_name=schema_name)
                    #     plan = PlanName.objects.get(client=client_tenant)
                    #     domain = get_object_or_404(Domain, tenant=client_tenant)
                    #     print("client tenant name", client_tenant)
                    #     print("client plan", plan)
                    #     print("Domain", domain)
                    #     print("User", user)
                    #     print("redirect url", f'http://{domain}:8000/login/')
                    #     return Response({'message': 'Login successful for employee.', 'access_token': access_token,
                    #                     'redirect_url': f'http://{domain}:8000/login/'}, status=status.HTTP_200_OK)
                    # except User.DoesNotExist:
                    #     print(f'User not found in schema {schema_name}')
                    # continue
        try:
            client = get_object_or_404(Client, email=email, password=password)
            print("client returned", client)
            client_schema_name = client.schema_name
            print("client_schema", client_schema_name)
            domain = get_object_or_404(Domain, tenant=client)
            print("domain", domain)

            return Response({'message': 'Login successful.',
                             'redirect_url': f'http://{domain}:8000/login/'}, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
