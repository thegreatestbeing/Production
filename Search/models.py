# =================================================================
# 
#                        Search History Model       
#                               
#   Implimentation Required :~
# 
# 
# 
#   Implimented :~
#
# 
#  
# =================================================================



# =================================================================
# 
#                              Imports
# 
# =================================================================


import os 
from datetime import date, datetime
from django.conf import settings as appsettings
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.utils.translation import ugettext_lazy as _

User    = get_user_model()

# models imports
from Products.models import *

# =================================================================
# 
#                              Models
# 
# =================================================================

class Search(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    history     = models.CharField(max_length=512, blank=False, null=False)
    timestamp   = models.DateTimeField(auto_now_add=True)

# Add keyword automatically 
class Keywords(models.Model):
    keyword     = models.CharField(max_length=256, unique=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = _('Keyword')
        verbose_name_plural = _('keywords')

# Signals 
def addKeyword(sender, instance, created, *args, **kwargs):
    if created:
        pass
post_save.connect(addKeyword, sender=Category)
           

