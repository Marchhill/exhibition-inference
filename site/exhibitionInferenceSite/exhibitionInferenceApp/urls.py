from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "exhibitionInferenceApp_ns"
urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submitReading, name='submit'),
    path('frontdesk/devices/', views.frontdeskDeviceSelect,
         name='frontdesk-device-select'),
    path('frontdesk/devices/<str:hardwareId>/',
         views.frontdeskDevice, name='frontdesk-device'),
    path('metadata/', views.metadata, name='metadata')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
