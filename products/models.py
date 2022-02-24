from django.db import models
from userManagement.models import Manufacturer,Distributor,DeliveryPerson

# Create your models here.

class Carton(models.Model):
    carton_id = models.CharField(primary_key=True,max_length=20)
    manufacturer_id = models.ForeignKey(Manufacturer,on_delete=models.DO_NOTHING)
    product_name = models.CharField(max_length=50,blank=True,null=True)
    product_quantity = models.IntegerField()
    product_price = models.IntegerField()
    production_date= models.DateField()
    expiry_date = models.DateField()
    distributor = models.ForeignKey(Distributor,blank=True,null=True,on_delete=models.DO_NOTHING,related_name='distributor')
    distributor_scan_date = models.DateField(blank=True,null=True)
    delivery_person = models.ForeignKey(DeliveryPerson,blank=True,null=True,on_delete=models.DO_NOTHING,related_name='delivery')
    delivery_date = models.DateField(blank=True,null=True)
    pharmacist_details = models.CharField(max_length=100,blank=True,null=True)
    number_of_scan = models.IntegerField(blank=True,null=True,default=0)
    is_blocked = models.BooleanField(default=False)


class Product(models.Model):
    product_id = models.CharField(primary_key=True,max_length=20)
    carton_id = models.ForeignKey(Carton,on_delete=models.CASCADE)
    number_of_scan = models.IntegerField(blank=True,null=True,default=0)
    is_blocked = models.BooleanField(default=False)

