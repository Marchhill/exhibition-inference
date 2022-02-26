from django.contrib import admin

from .models import Metadata, Session, Reading

admin.site.site_header = "Exhibition Inference Database Admin"


class MetadataAdmin(admin.ModelAdmin):
    list_display = ("key", "value")


# Register your models here.
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(Session)
admin.site.register(Reading)
