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
from django.contrib import admin
from django.conf.urls import url, include
import users.views, establishments.views, polls.views
import polls.urls
import users.urls
import establishments.urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from joogpoint import settings

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'establishments', establishments.views.EstablishmentViewSet)
router.register(r'users', users.views.UserViewSet)
router.register(r'profiles', users.views.ProfileViewSet)
router.register(r'playlists', polls.views.PlaylistViewSet)
router.register(r'tracks', polls.views.TrackViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^spotify/', include(polls.urls)),
    url(r'^accounts/', include(users.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})
]
