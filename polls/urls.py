from polls.views import PlaylistViewSet, TrackViewSet
from rest_framework import renderers
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.spotify_test),
]

playlist_list = PlaylistViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

track_list = TrackViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# playlist_set_playlist = PlaylistViewSet.as_view({
#     'put': 'change-playlist'
# })