from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "exhibitionInferenceApp_ns"
urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submitReading, name='submit'),
    path(
        'frontdesk/devices/',
        views.frontdeskDeviceSelect,
        name='frontdesk-device-select'
    ),
    path(
        'frontdesk/devices/<str:hardwareId>/',
        views.frontdeskDeviceManage,
        name='frontdesk-device-manage'
    ),
    path(
        'frontdesk/devices/<str:hardwareId>/submit/',
        views.frontdeskDeviceManageSubmit,
        name='frontdesk-device-manage-submit'
    ),
    path('login/', views.login, name='login'),
    path('login/submit/', views.loginPost, name='login-submit'),
    path('logout/', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
