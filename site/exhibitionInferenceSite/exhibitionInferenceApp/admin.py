from django.contrib import admin

from .models import Metadata, Session, Reading, Device

admin.site.site_header = "Exhibition Inference Database Admin"


class MetadataAdmin(admin.ModelAdmin):
    list_display = ("key", "value")


class SessionAdmin(admin.ModelAdmin):
    list_display = ("admin_session_id", "device_id",
                    "startTime", "endTime", "metadata")
    # admin_session_id refers to the method models.Session.admin_session_id
    # (used for the naming: for readability in admin portal)


class ReadingAdmin(admin.ModelAdmin):
    list_display = ("id", "x", "y", "z", "t", "session_id", "quality")


class DeviceAdmin(admin.ModelAdmin):
    list_display = ("hardwareId", "metadata")


# Register your models here.
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(Device, DeviceAdmin)
