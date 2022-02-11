import datetime
import os
import qrcode
from django.shortcuts import render

from .models import Carton,Product
from .addProductForm import AddCartonAndProductForm,PharmacistDetailsForm
from userManagement.models import Types
from nacl.public import PrivateKey,PublicKey, Box
from Crypto.Util.Padding import pad, unpad
from django.contrib.auth.decorators import login_required
import base64
import time
import nacl.exceptions as exc

# Create your views here.
@login_required
def add_carton(request):
    if request.user.type == Types.Manufacturer or request.user.type == Types.Manufacturer:
        start_time = time.time()
        form = AddCartonAndProductForm
        if request.method == 'POST':
            form = AddCartonAndProductForm(request.POST)
            if form.is_valid():
                carton=form.save(commit=False)
                carton.manufacturer_id=request.user

                quantity = request.POST['product_quantity']
                cid = request.POST['carton_id']

                with open('encrypt_private_key.txt', 'r') as f:
                    content = f.read()
                    encrypt_private_key = base64.b32decode(content)

                with open('encrypt_public_key.txt', 'r') as f:
                    content = f.read()
                    encrypt_public_key = base64.b32decode(content)

                encrypt_box = Box(PrivateKey(encrypt_private_key),PublicKey(encrypt_public_key))

                encrypted_carton_id = encrypt_box.encrypt(pad(cid.encode('utf-8'),10,style='pkcs7'))

                qr = qrcode.QRCode(
                    version=5,
                    error_correction=qrcode.constants.ERROR_CORRECT_M,
                    box_size=10,
                    border=4,
                )
                data = '192.168.131.1:8000/carton/'+str(encrypted_carton_id.hex())
                # qr.add_data(encrypted_carton_id.hex())
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="red", back_color="black")
                if not os.path.exists('QRcodes\{}'.format(cid)):
                    os.makedirs('QRcodes\{}'.format(cid))
                img.save('QRcodes\{}\{}.png'.format(cid,cid))

                for i in range(1,int(quantity)+1):
                    if i < 10:
                        pid = cid+'00'+str(i)
                    elif i > 9 and i < 100:
                        pid = cid + '0' + str(i)
                    else:
                        pid = cid + str(i)

                    encrypted_product_id = encrypt_box.encrypt(pad(pid.encode('utf-8'),10,style='pkcs7'))
                    product= Product(product_id=pid,carton_id=carton)
                    carton.save()
                    product.save()

                    qr = qrcode.QRCode(
                        version=5,
                        error_correction=qrcode.constants.ERROR_CORRECT_M,
                        box_size=10,
                        border=4,
                    )
                    data = '192.168.131.1:8000/product/' + str(encrypted_product_id.hex())
                    # qr.add_data(encrypted_product_id.hex())
                    qr.add_data(data)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="blue", back_color="black")
                    img.save('QRcodes\{}\{}.png'.format(cid,pid))

                    # img = qrcode.make(encrypted_product_id)
                    # img.save("{}.png".format(pid))
                form=AddCartonAndProductForm()
        context = {
            'form': form,
        }
        print("--- %s seconds ---" % (time.time() - start_time))
        return render(request, 'addCarton.html', context)
    else:
        context = {
            'message':'Not Allowed'
        }

    return render(request,'addCarton.html', context)


@login_required
def add_carton_details(request, cid):
    carton = ''
    message = ''
    if request.user.type == Types.Distributor:
        try:
            with open('decrypt_private_key.txt', 'r') as f:
                content = f.read()
                decrypt_private_key = base64.b32decode(content)

            with open('decrypt_public_key.txt', 'r') as f:
                content = f.read()
                decrypt_public_key = base64.b32decode(content)

            decrypt_box = Box(PrivateKey(decrypt_private_key), PublicKey(decrypt_public_key))
            decrypt_message = unpad(decrypt_box.decrypt(bytes.fromhex(cid)),10,style='pkcs7').decode()
        except(exc.CryptoError,ValueError):
            context = {
                'message': 'Invalid ID',
                'carton': carton
            }
            return render(request, 'addCartonSupplyChainInformation.html', context)

        try:
            carton = Carton.objects.get(carton_id=decrypt_message)
        except Carton.DoesNotExist:
            context = {
                'carton': carton,
                'message': 'Carton Not Found in The Database'
            }
            return render(request, 'addCartonSupplyChainInformation.html', context)
        if carton.number_of_scan == 0:
            carton.distributor = request.user
            carton.distributor_scan_date = datetime.date.today()
            carton.number_of_scan += 1
            carton.save()
            message= str(request.user.name) + " : " + "Your Information Has  Successfully Stored"
        else:
            message = 'Already Scanned'

        context={
            'carton':carton,
            'message':message
        }
        return render(request, 'addCartonSupplyChainInformation.html', context)

    elif request.user.type == Types.DeliveryPerson:

        try:
            with open('decrypt_private_key.txt', 'r') as f:
                content = f.read()
                decrypt_private_key = base64.b32decode(content)

            with open('decrypt_public_key.txt', 'r') as f:
                content = f.read()
                decrypt_public_key = base64.b32decode(content)

            decrypt_box = Box(PrivateKey(decrypt_private_key), PublicKey(decrypt_public_key))
            decrypt_message = unpad(decrypt_box.decrypt(bytes.fromhex(cid)), 10, style='pkcs7').decode()
        except(exc.CryptoError, ValueError):
            context = {
                'message': 'Invalid ID'
            }
            return render(request, 'addCartonSupplyChainInformation.html', context)

        try:
            carton = Carton.objects.get(carton_id=decrypt_message)
        except Carton.DoesNotExist:
            context = {
                'message': 'Carton Not Found in The Database'
            }
            return render(request, 'addCartonSupplyChainInformation.html', context)

        if carton.number_of_scan==1:
            form = PharmacistDetailsForm()
        elif carton.number_of_scan ==0:
            form = ''
            message = str(request.user.name) + " :  " + "You are not allowed to add information"
        else:
            form = ''
            message = str(request.user.name) + " :  " + "Already Scanned"

        if request.method == 'POST':
            form = PharmacistDetailsForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                details = data.get('details')

                if carton.number_of_scan == 1:
                    carton.delivery_person = request.user
                    carton.delivery_date = datetime.date.today()
                    carton.pharmacist_details=details
                    carton.number_of_scan += 1
                    carton.is_blocked = True
                    form = ''
                    carton.save()
                    message = str(request.user.name) + " : " + "The Informations  have successfully stored"
                else:
                    message = str(request.user.name) + " :  " + "you are not allowed to add information"
                    form = ''
                    carton = ''

        context={
            'name':request.user.name,
            'form':form,
            'carton':carton,
            'message':message
             }
        return render(request, 'addCartonSupplyChainInformation.html', context)
    else:
        context = {
            'message': 'you are not allowed to add information'
        }
        return render(request, 'addCartonSupplyChainInformation.html', context)


def product_details(request,pid):
    try:
        with open('decrypt_private_key.txt', 'r') as f:
            content = f.read()
            decrypt_private_key = base64.b32decode(content)

        with open('decrypt_public_key.txt', 'r') as f:
            content = f.read()
            decrypt_public_key = base64.b32decode(content)

        decrypt_box = Box(PrivateKey(decrypt_private_key), PublicKey(decrypt_public_key))
        decrypt_message = unpad(decrypt_box.decrypt(bytes.fromhex(pid)), 10, style='pkcs7').decode()
    except(exc.CryptoError, ValueError):
        context = {
            'message': 'Invalid ID'
        }
        return render(request, 'addCartonSupplyChainInformation.html', context)

    try:
        product = Product.objects.get(product_id=decrypt_message)
        cid = decrypt_message[:5]
        carton = Carton.objects.get(carton_id=cid)
    except (Product.DoesNotExist,Carton.DoesNotExist):
        context = {
            'message': 'No Information Available'
        }
        return render(request, 'productDetails.html', context)
    if product.number_of_scan == 0:
        message = '1st Scan. Please Check Other Information'
        product.number_of_scan += 1
        product.is_blocked=True
        product.save()
    else:
        message = 'This Product has scanned before.'
        product.number_of_scan += 1
        product.save()

    context = {
        'product':product,
        'carton':carton,
        'message':message

    }
    return render(request, 'productDetails.html', context)



