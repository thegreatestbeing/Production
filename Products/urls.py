from django.conf import settings
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views

from Products.views import create, delete, update, products

urlpatterns = [
    re_path(r'^product/create/$', create, name='create'),
    re_path(r'^product/delete/$', delete, name='delete'),
    re_path(r'^product/update/$', update, name='update'),
    re_path(r'^products/$', products, name='products'),
    # re_path(r'^$', views.product, name='home'),
]

app_name = 'products'