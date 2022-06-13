from django.contrib import admin
from Account.models import User, EmailActivation
# Register your models here.

admin.site.register(EmailActivation)
admin.site.register(User)