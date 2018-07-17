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
                  path('filter_student_selection/', views.filter_student_selection,
                       name='filter_student_selection'),
                  path('template_student_details/<int:app_id>/', views.template_student_details,
                       name='template_student_details'),
                  path('template_student_reports/', views.template_student_reports,
                       name='template_student_reports'),
                  path('template_application_progress_history/', views.template_application_progress_history,
                       name='template_application_progress_history'),
                  path('template_my_payments/', views.template_my_payments,
                       name='template_my_payments'),
                  path('template_students_receipts/', views.template_students_receipts,
                       name='template_students_receipts'),
                  path('approve_sponsorship/', views.approve_sponsorship,
                       name='approve_sponsorship'),
                  path('filter_student_report/', views.filter_student_report,
                       name='filter_student_report'),
                  path('filter_application_history/', views.filter_application_history,
                       name='filter_application_history'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
