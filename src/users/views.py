from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, UserLoginSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            print(username)
            password = serializer.validated_data['password']
            print(password)

            user = User.objects.filter(username=username).first()
            print("user", user)

            if user is None or not user.check_password(password):
                return Response({'detail': 'Invalid credentials'},
                                status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({'access_token': access_token}, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        print(email)
        password = request.data.get('password')
        print(password)

        if email is None or password is None:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        TenantModel = get_tenant_model()
        tenants = TenantModel.objects.all()
        schemas = [tenant.schema_name for tenant in tenants]
        schemas.remove('public')
        print("All schemas=", schemas)
        for schema_name in schemas:
            print("Current schema=", schema_name)
            with schema_context(schema_name):
                try:
                    all = Employee.objects.all()
                    print("all users", all)
                    # employee = get_object_or_404(Employee, email=email, password=password)
                    employee = Employee.objects.get(email=email, password=password)
                    client_tenant = Client.objects.get(schema_name=schema_name)
                    plan = PlanName.objects.get(client=client_tenant)
                    domain = get_object_or_404(Domain, tenant=client_tenant)
                    print("client tenant name", client_tenant)
                    print("client plan", plan)
                    print("Domain", domain)
                    print("Employee", employee)
                    print("redirect url", f'http://{domain}:8000/login/')
                    # return redirect(f'http://{domain}:8000/login/')
                    return Response({'message': 'Login successful for employee.',
                                     'redirect_url': f'http://{domain}:8000/login/'}, status=status.HTTP_200_OK)
                except Employee.DoesNotExist:
                    print(f'Employee not found in schema {schema_name}')
                    continue

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
