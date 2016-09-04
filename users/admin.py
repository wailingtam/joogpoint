from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "spotify_username", "facebook_username",
                    "twitter_username")
    search_fields = ['user__username']

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
