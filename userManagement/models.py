import uuid

from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db.models.signals import post_save
from django.utils import timezone


# Create your models here.

class Types(models.TextChoices):
    Distributor = 'DISTRIBUTOR', 'Distributor'
    DeliveryPerson = 'DELIVERYPERSON', 'DeliveryPerson'
    Manufacturer = 'MANUFACTURER', 'Manufacturer'
    Admin = 'ADMIN', 'Admin'

class Gender(models.TextChoices):
    Male = 'MALE', 'Male'
    Female = 'FEMALE', 'Female'


class CustomUserManager(BaseUserManager):
    def crete_user(self,username,password,**other_fields):
        user = self.model(username=username,**other_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self,username,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('type', Types.Admin)
        return self.crete_user(username,password,**other_fields)


class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    username = models.CharField(max_length=50,unique=True)
    type = models.CharField(max_length=20,choices=Types.choices)
    name = models.CharField(max_length=50,blank=True,null=True)
    join_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class ManufacturerManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=Types.Manufacturer)


class Manufacturer(User):
    objects = ManufacturerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Types.Manufacturer
        return super().save(*args, **kwargs)


class DistributorManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=Types.Distributor)


class Distributor(User):
    objects = DistributorManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Types.Distributor
        return super().save(*args, **kwargs)


class DeliveryPersonManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=Types.DeliveryPerson)


class DeliveryPerson(User):
    objects = DeliveryPersonManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Types.DeliveryPerson
        return super().save(*args, **kwargs)


class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Types.Admin)


class Admin(User):
    objects = AdminManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Types.Admin
        self.is_active = True
        self.is_superuser = True
        self.is_staff = True
        return super().save(*args, **kwargs)



