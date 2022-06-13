from django.conf import settings
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    re_path(r'autocomplete/(?P<keyword>[\w-]+)', views.autocomplete, name='autocomplete'),
    re_path(r'collect/', views.collectData, name='collectData'),
    re_path(r'history/', views.history, name='history'),
    re_path(r'search/(?P<keyword>[\w-]+)', views.search, name='search'),
]

app_name = 'search'