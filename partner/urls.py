from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'partner'

urlpatterns = [path('template_registered_application/', views.template_registered_application,
                    name='template_registered_application'),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
