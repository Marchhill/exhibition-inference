from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "exhibitionInferenceApp_ns"
urlpatterns = [
    path("", views.index, name="index"),
    path("visualisation/", views.visualisationDefault,
         name="visualisation-default"),
    path("visualisation/all/", views.visualisationAll, name="visualisation-all"),
    path("visualisation/startEndQuery/",
         views.visualisationStartEndQuery, name="visualisation-start-end-query"),
    path("visualisation/start/<str:startTime>/end/<str:endTime>/",
         views.visualisationStartEnd, name="visualisation-start-end"),
    path("visualisation/session/<int:sessionId>/",
         views.visualisationSession, name="visualisation-session"),
    path("data", views.dataDefault, name="data-default"),
    path("submit/", views.submitReading, name="submit"),
    path(
        "frontdesk/devices/",
        views.frontdeskDeviceSelect,
        name="frontdesk-device-select"
    ),
    path(
        "frontdesk/devices/<str:hardwareId>",
        views.frontdeskDeviceManage,
        name="frontdesk-device-manage"
    ),
    path(
        "frontdesk/devices/<str:hardwareId>/submit",
        views.frontdeskDeviceManageSubmit,
        name="frontdesk-device-manage-submit"
    ),
    path(
        "frontdesk/sessions/",
        views.frontdeskSessionSelect,
        name="frontdesk-session-select"
    ),
    path(
        "frontdesk/sessions/<int:sessionId>",
        views.frontdeskSessionManage,
        name="frontdesk-session-manage"
    ),
    path(
        "frontdesk/sessions/<int:sessionId>/submit",
        views.frontdeskSessionManageSubmit,
        name="frontdesk-session-manage-submit"
    ),
    path("login/", views.login, name="login"),
    path("login/submit/", views.loginPost, name="login-submit"),
    path("logout/", views.logout, name="logout"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
