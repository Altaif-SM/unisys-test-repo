from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'partner'

urlpatterns = [
                  path('template_registered_application/', views.template_registered_application,
                       name='template_registered_application'),
                  path('filter_registered_application/', views.filter_registered_application,
                       name='filter_registered_application'),

                  path('template_approving_application/', views.template_approving_application,
                       name='template_approving_application'),
                  path('filter_application_status/', views.filter_application_status, name='filter_application_status'),
                  path('change_application_status/', views.change_application_status, name='change_application_status'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
