from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password", "name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


class TerrainAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["name"]
    search_fields = ["name"]


class ClimateAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["name"]
    search_fields = ["name"]


class PlanetAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["name", "population"]
    search_fields = ["name", "population"]
    fieldsets = [
        (None, {
            'fields': [
                'name',
                "population",
                "terrains",
                "climates"
            ],
        }),
    ]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Climate, ClimateAdmin)
admin.site.register(models.Terrain, TerrainAdmin)
admin.site.register(models.Planet, PlanetAdmin)
