import os

from datetime import date, datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save, pre_save
from django.utils.translation import ugettext_lazy as _
from io import BytesIO
from os import path
from django.core.files import File
from PIL import Image, ImageDraw
from barcode.writer import ImageWriter

import qrcode
import barcode


# Imports from application
from Business.extras import ROLE, WEEKDAYS
from Business.utils import GenerateUniqueNumber

# Model Imports 
from Inventory.models import Inventory
from Products.models import Product

from Business.utils import product_code_directory_path, product_directory_path


User    = get_user_model()
EAN     = barcode.get_barcode_class('code128')

# Stock Keeping Unit
class SKU(models.Model):
    code            = models.CharField(max_length=14, unique=True, blank=True)
    barcodeimage    = models.ImageField(upload_to=product_code_directory_path, blank=True) 
    qrcodeimage     = models.ImageField(upload_to=product_code_directory_path, blank=True) 
    product         = models.OneToOneField(Product, on_delete=models.CASCADE)


    # Generate or update barcode and qrcode
    def GenerateSKU(self):
        pass

# Implimentation required Generate SKU Code ( Stock Keeping Unit )
def GenerateSKU(sender, instance, created, *args, **kwargs):
    if created:
        # Generate barcode and qrcode image
        barcode = GenerateUniqueNumber()
        
        # check if directory exists
        qrdir   = path.isdir('media/{0}/product/qrcode/'.format(instance.inventory.id))
        bardir  = path.isdir('media/{0}/product/barcode/'.format(instance.inventory.id))
        
        if not qrdir and not bardir:
            os.makedirs('media/{0}/product/qrcode/'.format(instance.inventory.id))
            os.makedirs('media/{0}/product/barcode/'.format(instance.inventory.id))
        elif not bardir:
            os.makedirs('media/{0}/product/barcode/'.format(instance.inventory.id))
        elif not qrdir:
            os.makedirs('media/{0}/product/qrcode/'.format(instance.inventory.id))
        else: 
            print('both directory exists')


        # add a watermark



        # create QRCode image
        image       = qrcode.make(barcode)
        canvas      = Image.new('RGB', (image.pixel_size, image.pixel_size), 'white')
        canvas.paste(image)


        # create the file and save
        filename    = f'{barcode}.png'
        upload      = 'media/{0}/product/qrcode/{1}'.format(instance.inventory.id, filename)
        canvas.save(upload)


        # create the barcode image
        barimage            = EAN(barcode, writer=ImageWriter())
        buffer              = BytesIO()
        barimage.write(buffer)

        # load it in memmory and retrive the size [width, height] of the file 
        barfile             = File(buffer)
        barcodeimage        = Image.open(barfile)

        # copy image in new image
        barcanvas           = Image.new('RGB', barcodeimage.size, 'white')
        barcanvas.paste(barcodeimage)
        
        # save file to upload directory
        barfilename         = f'{barcode}.png'
        barupload           = 'media/{0}/product/barcode/{1}'.format(instance.inventory.id, barfilename)
        

        barcanvas.save(barupload)


        SKU.objects.create(
            code            = barcode, 
            qrcodeimage     = '{0}/product/qrcode/{1}'.format(instance.inventory.id, filename),
            barcodeimage    = '{0}/product/barcode/{1}'.format(instance.inventory.id, barfilename),
            product         = instance,
            )

post_save.connect(GenerateSKU, sender=Product)


# Universal Product code
class UPC(models.Model):
    code            = models.CharField(max_length=14, unique=True, blank=True)
    barcodeimage    = models.ImageField(upload_to=product_code_directory_path, blank=True) 
    qrcodeimage     = models.ImageField(upload_to=product_code_directory_path, blank=True) 
    product         = models.OneToOneField(Product, on_delete=models.CASCADE)


    # Generate or update barcode and qrcode
    def GenerateUPC(self):
        pass

# Implimentation required Generate UPC Code ( Universal Product Code )

# def GenerateUPC(sender, instance, created, *args, **kwargs):
#     if created:
#         # Generate barcode and qrcode image
#         barcode = GenerateUniqueNumber()
        
#         # check if directory exists
#         qrdir   = path.isdir('media/{0}/product/qrcode/'.format(instance.inventory.id))
#         bardir  = path.isdir('media/{0}/product/barcode/'.format(instance.inventory.id))
        
#         if not qrdir and not bardir:
#             os.makedirs('media/{0}/product/qrcode/'.format(instance.inventory.id))
#             os.makedirs('media/{0}/product/barcode/'.format(instance.inventory.id))
#         elif not bardir:
#             os.makedirs('media/{0}/product/barcode/'.format(instance.inventory.id))
#         elif not qrdir:
#             os.makedirs('media/{0}/product/qrcode/'.format(instance.inventory.id))
#         else: 
#             print('both directory exists')


#         # add a watermark



#         # create QRCode image
#         image       = qrcode.make(barcode)
#         canvas      = Image.new('RGB', (image.pixel_size, image.pixel_size), 'white')
#         canvas.paste(image)


#         # create the file and save
#         filename    = f'{barcode}.png'
#         upload      = 'media/{0}/product/qrcode/{1}'.format(instance.inventory.id, filename)
#         canvas.save(upload)


#         # create the barcode image
#         barimage            = EAN(barcode, writer=ImageWriter())
#         buffer              = BytesIO()
#         barimage.write(buffer)

#         # load it in memmory and retrive the size [width, height] of the file 
#         barfile             = File(buffer)
#         barcodeimage        = Image.open(barfile)

#         # copy image in new image
#         barcanvas           = Image.new('RGB', barcodeimage.size, 'white')
#         barcanvas.paste(barcodeimage)
        
#         # save file to upload directory
#         barfilename         = f'{barcode}.png'
#         barupload           = 'media/{0}/product/barcode/{1}'.format(instance.inventory.id, barfilename)
        

#         barcanvas.save(barupload)


#         UPC.objects.create(
#             code            = barcode, 
#             qrcodeimage     = '{0}/product/qrcode/{1}'.format(instance.inventory.id, filename),
#             barcodeimage    = '{0}/product/barcode/{1}'.format(instance.inventory.id, barfilename),
#             product         = instance,
#             )

# post_save.connect(GenerateUPC, sender=Product)