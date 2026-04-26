from django.contrib import admin

from .models import OsServerReport, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)
    search_fields = ("user__username",)


@admin.register(OsServerReport)
class OsServerReportAdmin(admin.ModelAdmin):
    list_display = (
        "fqdn",
        "ip_address",
        "os_version",
        "segment",
        "criticality",
        "owner",
        "updated_at",
    )
    search_fields = ("fqdn", "ip_address", "info_system_code", "owner__username")
    list_filter = ("criticality", "internet_access", "siem_connection_possible")
