from django.db import models
from django.db.models.deletion import SET_NULL


from Products.models import Product

# Create your models here.
class Cart(models.Model):
    item        = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity    = models.IntegerField()

