from django.conf import settings
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    re_path(r'^$', views.inventory, name='home'),
    # re_path(r'^$', views.product, name='home'),
]

app_name = 'inventory'