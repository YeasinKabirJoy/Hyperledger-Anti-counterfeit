from django.contrib import admin
from .models import Carton,Product

# Register your models here.

admin.site.register([Carton,Product])
