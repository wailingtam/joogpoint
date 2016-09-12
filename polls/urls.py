from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^account-access/$', views.get_account_access),
    # url(r'^spotify-playlists/$', views.get_spotify_playlists),
    # url(r'^playlist-tracks/$', views.get_spotify_playlist_tracks),
    url(r'^search/$', views.song_search),
    url(r'^callback/$', views.callback)
]
