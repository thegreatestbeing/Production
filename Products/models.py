from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils.translation import ugettext_lazy as _

from Business.utils import product_directory_path


# Import models from User, Inventory
from Inventory.models import Inventory


# Status
class Product(models.Model):
    name        = models.CharField(max_length=64, null=False, blank=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    inventory   = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    timestamp   = models.DateTimeField(auto_now_add=True)
    # updated   = models.DateTimeField(auto=True)

    class Meta:
        verbose_name        = _('product')
        verbose_name_plural = _('products')


class Category(models.Model):
    product     = models.OneToOneField(Product, on_delete=CASCADE)
    category    = models.CharField(max_length=32, unique=True)
    
    class Meta:
        verbose_name        = _('category')
        verbose_name_plural = _('categories')


# work around if has no variants than just create one 
class Variant(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE) 
    option      = models.CharField(max_length=2)
    variant     = models.CharField(max_length=256)


class Schedualed(models.Model):
    product     = models.ForeignKey(Variant, on_delete=models.CASCADE)
    available   = models.DateTimeField(auto_now=False)


# for each variant
class Quantity(models.Model):
    product     = models.ForeignKey(Variant, null=True, on_delete=SET_NULL)
    quantity    = models.IntegerField()


class Price(models.Model):
    product     = models.ForeignKey(Variant, on_delete=models.CASCADE)
    wholesale   = models.CharField(max_length=64, null=True, blank=True)
    retail      = models.CharField(max_length=64, null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag         = models.CharField(max_length=256)

    class Meta:
        verbose_name        = _('tag')
        verbose_name_plural = _('tags')


class Tax(models.Model):
    pass




