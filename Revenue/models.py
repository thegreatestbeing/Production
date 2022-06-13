from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from Inventory.models import Business, Coupen, Inventory
from Products.models import Product


class Sales(models.Model):
    sales       = models.IntegerField()
    revenue     = models.IntegerField()
    business    = models.ForeignKey(Business, on_delete=models.CASCADE)
    timestamp   = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name        = _('sale')
        verbose_name_plural = _('sales')


class Invoice(models.Model):
    buyer       = models.CharField(max_length=64, null=False)
    saler       = models.ForeignKey(Business, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    discount    = models.ForeignKey(Coupen, on_delete=models.SET_NULL, null=True, blank=True)
    tax         = models.CharField(max_length=32, null=True, blank=True, default=None)
    total       = models.CharField(max_length=32, null=False, default=None)
    timestamp   = models.DateTimeField(auto_now_add=True)


class Return(models.Model):
    sold        = models.ForeignKey(Sales, on_delete=models.CASCADE)
    cash        = models.CharField(max_length=32, )
    timestamp   = models.DateTimeField(auto_now_add=True)