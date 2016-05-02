from polls.views import PlaylistViewSet, TrackViewSet
from rest_framework import renderers
from django.conf.urls import url
from . import views

playlist_list = PlaylistViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

playlist_detail = PlaylistViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

track_list = TrackViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

track_detail = TrackViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    url(r'^$', views.spotify_test),
    url(r'^account-access/$', views.get_account_access),
    url(r'^spotify-playlists/$', views.get_spotify_playlists),
]
