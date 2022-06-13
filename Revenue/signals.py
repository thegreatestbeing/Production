from datetime import date, datetime
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save, pre_save
from django.utils.translation import ugettext_lazy as _


from Inventory.models import Inventory
from Products.models import Product
from Revenue.models import Invoice, Sales

def Sold(sender, instance, created, *args, **kwargs):
    if created:
        # check last sale of today if exists update it
        today       = Sales.objects.filter(timestamp=date.today(), business=instance.saler)
        inventory   = Inventory.objects.filter(business=instance.saler)
        product     = Product.objects.filter(inventory=inventory)

        # Generate revenue 
        _revenue    = int(instance.total) - int(instance.product.price.wholesale)
        _earned     = int(_revenue) - int(instance.tax)


        print(_earned)

        if today:

            # update today's total sales amount and revenue
            for object in today:
                sales       = object.sales
                revenue     = object.revenue
                
                # get product price 
                sold        = int(sales) + int(instance.total)
                earned      = int(revenue) + int(_earned)
                today.update(
                    sales   = sold,
                    revenue = earned,
                )

        else:
            # get product price 
            Sales.objects.create(
                sales   = instance.total,
                revenue = _earned,
                business   = instance.saler
            )

post_save.connect(Sold, sender=Invoice)