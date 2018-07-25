from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'parent'

urlpatterns = [
                  path('template_parent_dashboard/', views.template_parent_dashboard,
                       name='template_parent_dashboard'),

                  path('template_student_application_progress_history/', views.template_student_application_progress_history,
                       name='template_student_application_progress_history'),

                  path('filter_application_history/', views.filter_application_history,
                       name='filter_application_history'),

                  path('template_student_academic_report/', views.template_student_academic_report,
                       name='template_student_academic_report'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
