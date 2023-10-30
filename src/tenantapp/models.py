from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

# Create your models here.


class Client(TenantMixin):
    name = models.CharField(max_length=225)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=15)

    auto_create_schema = True


class Domain(DomainMixin):
    pass


class PlanName(models.Model):
    plan_name = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
