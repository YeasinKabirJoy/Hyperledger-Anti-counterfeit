# import nacl.utils
# from nacl.public import PrivateKey, Box
# from Crypto.Util.Padding import pad, unpad
# import base64
# import qrcode


# ECC  Curve25519 public key and private key.
# encrypt_private_key = PrivateKey.generate()
# print(encrypt_private_key)
# decrypt_public_key = encrypt_private_key.public_key
# print(decrypt_public_key)
# decrypt_private_key = PrivateKey.generate()
# print(decrypt_private_key)
# encrypt_public_key = decrypt_private_key.public_key
# print(encrypt_public_key)
#
#
#
# text = base64.b32encode(encrypt_private_key.encode()).decode("ascii")
# with open('encrypt_private_key.txt', 'w') as f:
#     f.write(text)
#
# text = base64.b32encode(decrypt_public_key.encode()).decode("ascii")
# with open('decrypt_public_key.txt', 'w') as f:
#     f.write(text)
#
# text = base64.b32encode(decrypt_private_key.encode()).decode("ascii")
# with open('decrypt_private_key.txt', 'w') as f:
#     f.write(text)
#
# text = base64.b32encode(encrypt_public_key.encode()).decode("ascii")
# with open('encrypt_public_key.txt', 'w') as f:
#     f.write(text)

#
# with open('encrypt_private_key.txt', 'r') as f:
#     content = f.read()
#     encrypted = base64.b32decode(content)
#
# print(PrivateKey(encrypted))



# encrypt_box = Box(encrypt_private_key, encrypt_public_key)
# decrypt_box = Box(decrypt_private_key, decrypt_public_key)


# message= 'c001'
# encrypt_message = encrypt_box.encrypt(message.encode()).hex()
# print(encrypt_message)
# decrypt_message = decrypt_box.decrypt(bytes.fromhex(encrypt_message)).decode()
# print(decrypt_message)
#
# message= 'c001p001'
# encrypt_message = encrypt_box.encrypt(message.encode()).hex()
# print(encrypt_message)
# decrypt_message = decrypt_box.decrypt(bytes.fromhex(encrypt_message)).decode()
# print(decrypt_message)
#


#
# message= 'c001'
# encrypt_message = encrypt_box.encrypt(pad(message.encode(),10,style='pkcs7')).hex()
# print(encrypt_message)
# decrypt_message = unpad(decrypt_box.decrypt(bytes.fromhex(encrypt_message)),10,style='pkcs7').decode()
# print(decrypt_message)
#
# message= 'c001p001'
# encrypt_message = encrypt_box.encrypt(pad(message.encode(),10,style='pkcs7')).hex()
# print(encrypt_message)
# decrypt_message = unpad(decrypt_box.decrypt(bytes.fromhex(encrypt_message)),10,style='pkcs7').decode()
# print(decrypt_message)



# url = 'http://192.168.0.101:8000/check/kjlkfdldj'
# qr = qrcode.QRCode(
#                 version=5,
#                 error_correction=qrcode.constants.ERROR_CORRECT_M,
#                 box_size=10,
#                 border=4,
#             )
# qr.add_data(url)
# qr.make(fit=True)
# img = qr.make_image(fill_color="red", back_color="black")
# img.save('test.png')
