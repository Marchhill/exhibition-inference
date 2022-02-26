from django.contrib import admin

from .models import Session, Reading

admin.site.site_header = "Exhibition Inference Database Admin"

# Register your models here.
admin.site.register(Session)
admin.site.register(Reading)
