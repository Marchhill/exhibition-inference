from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submitReading, name='submit'),
    path('device/', views.manageDevice, name='device'),
    path('metadata/', views.metadata, name='metadata')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
