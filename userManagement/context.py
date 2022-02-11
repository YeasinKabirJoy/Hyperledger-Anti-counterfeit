from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Types

def user_information(request):

    usertype = ''
    name = ''
    if request.user.is_authenticated:
        if request.user.type == Types.Manufacturer:
            usertype = 'Manufacturer'
        elif request.user.type == Types.Distributor:
            usertype = 'Distributor'
        elif request.user.type == Types.DeliveryPerson:
            usertype = 'DeliveryPerson'
        else:
            usertype = 'Admin'
        name= request.user.name
    context = {
        'usertype' : usertype,
        'name': name
    }
    return context
