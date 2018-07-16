from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'donor'

urlpatterns = [
                  path('template_donor_dashboard/', views.template_donor_dashboard,
                       name='template_donor_dashboard'),
                  path('template_student_selection/', views.template_student_selection,
                       name='template_student_selection'),
                  path('template_student_reports/', views.template_student_reports,
                       name='template_student_reports'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
