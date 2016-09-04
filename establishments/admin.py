from django.contrib import admin
from .models import Establishment


class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "address", "city")
    search_fields = ["name", "owner__username"]
    ordering = ("name", "country", "city")


admin.site.register(Establishment, EstablishmentAdmin)
