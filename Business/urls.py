"""Business URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
	# include re_path of all applications in that page!
    re_path(r'^admin/', admin.site.urls),

    re_path(r"^", include("Account.urls", namespace='account')),
    # re_path(r"^", include("Analytics.urls", namespace='analytics')),
    # re_path(r"^", include("Cart.urls", namespace='cart')),
    re_path(r"^", include("Inventory.urls", namespace="inventory")),
    # re_path(r"^", include("Notifications.urls", namespace="notifications")),
    re_path(r"^", include("Products.urls", namespace="products")),
    # re_path(r"^", include("Revenue.urls", namespace="revenue")),
    # re_path(r"^", include("Reviews.urls", namespace="reviews")),
    re_path(r"^", include("Search.urls", namespace="search")),
    # re_path(r"^", include("settings.urls", namespace="settings")),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

