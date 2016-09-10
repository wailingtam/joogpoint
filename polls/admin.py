from django.contrib import admin
from .models import Playlist, Track


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("establishment", "spotify_url", "explicit_lyrics")
    search_fields = ['establishment__name']


class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "votes", "order", "request_user", "get_establishment",
                    "get_establishment_address", "in_playlist")
    search_fields = ['playlist__establishment__name', 'title', 'artist']

    def get_establishment(self, obj):
        return obj.playlist.establishment

    get_establishment.short_description = "Establishment"

    def get_establishment_address(self, obj):
        return obj.playlist.establishment.address

    get_establishment_address.short_description = "Address"


admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Track, TrackAdmin)
