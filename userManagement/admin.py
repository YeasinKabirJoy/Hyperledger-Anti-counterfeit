from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Manufacturer,Distributor,DeliveryPerson,Admin
from cryptography.hazmat.primitives.asymmetric import ec

class UserAdminConfig(UserAdmin):
    ordering = ('join_date',)
    list_display = ('username','is_active','is_staff')
    readonly_fields = ('id',)
    fieldsets = (
        (None, {'fields': ('id','username', 'join_date','password','name','type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser','groups',"user_permissions")}),
    )
admin.site.register(User,UserAdminConfig)
admin.site.register(Manufacturer,UserAdminConfig)
admin.site.register(Distributor,UserAdminConfig)
admin.site.register(DeliveryPerson,UserAdminConfig)
admin.site.register(Admin,UserAdminConfig)
