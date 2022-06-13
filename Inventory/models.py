from django.conf import settings as appsettings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils.translation import ugettext_lazy as _


from Business.extras import ROLE, WEEKDAYS
from Business.utils import product_code_directory_path

User    = get_user_model()


# Create your models here.
class Business(models.Model):
    name        = models.CharField(max_length=64, blank=False, null=False)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    slug        = models.SlugField(max_length=256, unique=True)
    timestamp   = models.DateTimeField(auto_now_add=True)


# Removing that 
class Inventory(models.Model):
    business    = models.OneToOneField(Business, on_delete=models.CASCADE)
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = _('inventory')
        verbose_name_plural = _('inventories')


class Detail(models.Model):
    address     = models.CharField(max_length=512, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    business    = models.OneToOneField(Business, on_delete=models.CASCADE)


class Contact(models.Model):
    email       = models.EmailField(unique=True, null=True, blank=True)
    contact     = models.CharField(max_length=10, null=True, blank=True)
    business    = models.ForeignKey(Business, on_delete=models.CASCADE)


class Event(models.Model):
    event       = models.CharField(max_length=512, blank=False, null=False)
    scheduled   = models.DateField()
    user        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    business    = models.ForeignKey(Business, on_delete=models.CASCADE)
    timestamp   = models.DateTimeField(auto_now_add=True)


class Timing(models.Model):
    business    = models.ForeignKey(Business, on_delete=models.CASCADE)
    weekday     = models.IntegerField(choices=WEEKDAYS)
    opening     = models.TimeField()
    closing     = models.TimeField()
    timestamp   = models.DateTimeField(auto_now_add=True)


    # class Meta:
    #     unique_together = (weekday, opening, closing)


class Relation(models.Model):
    business    = models.ForeignKey(Business, on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    role        = models.CharField(max_length=1, blank=True, choices=ROLE)
    timestamp   = models.DateTimeField(auto_now_add=True)


class Classification(models.Model):
    business        = models.OneToOneField(Business, on_delete=models.CASCADE)
    classification  = models.CharField(max_length=256)


class Coupen(models.Model):
    discount    = models.CharField(max_length=64, null=True, blank=True)
    coupen      = models.CharField(max_length=64, null=True, blank=True)
    barcode     = models.CharField(max_length=256)
    code        = models.ImageField(upload_to=product_code_directory_path)
    valid       = models.DateTimeField(auto_now=True, null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
# Model Import










