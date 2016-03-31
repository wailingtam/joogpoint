"""joogpoint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import include, url
from django.contrib import admin
# from rest_framework import routers
# from users import views
#
# router = routers.DefaultRouter()
# # router.register(r'users', views.UserViewSet)
#
# urlpatterns = [
#     url(r'^', include('establishments.urls')),
#     url(r'^admin/', admin.site.urls),
#     url(r'^users/', include('users.urls')),
#     # url(r'^', include(router.urls)), uncomment later
#     url(r'^api-auth/', include('rest_framework.urls')),
#
# ]

from django.conf.urls import url, include
import establishments.views
import users.views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'establishments', establishments.views.EstablishmentViewSet)
router.register(r'users', users.views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]