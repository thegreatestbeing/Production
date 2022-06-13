from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save, pre_save

from Inventory.models import Business, Relation



def post_create_owner(sender, instance, created, *args, **kwargs):
    if created:
        # get the user that user is requesting 
        Relation.objects.create(business=instance, user=instance.user, role='O')

        # print('user :', instance.user)
post_save.connect(post_create_owner, sender=Business)