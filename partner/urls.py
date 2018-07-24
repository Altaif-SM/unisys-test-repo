from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'partner'

urlpatterns = [
                  path('template_registered_application/', views.template_registered_application,
                       name='template_registered_application'),
                  path('filter_registered_application/', views.filter_registered_application,name='filter_registered_application'),
                  path('export_registered_application/', views.export_registered_application,name='export_registered_application'),
                  path('template_applicant_all_details/<int:app_id>/', views.template_applicant_all_details,
                       name='template_applicant_all_details'),

                  path('template_approving_application/', views.template_approving_application,
                       name='template_approving_application'),
                  path('filter_application_status/', views.filter_application_status, name='filter_application_status'),
                  path('change_application_status/', views.change_application_status, name='change_application_status'),

                  path('template_application_approval_details/<int:app_id>/',
                       views.template_application_approval_details, name='template_application_approval_details'),

                  path('template_student_progress_history/', views.template_student_progress_history,
                       name='template_student_progress_history'),
                  path('filter_application_history/', views.filter_application_history,
                       name='filter_application_history'),

                  path('template_psychometric_test_report/', views.template_psychometric_test_report,
                       name='template_psychometric_test_report'),
                  path('filter_psychometric_test_report/', views.filter_psychometric_test_report,
                       name='filter_psychometric_test_report'),

                  path('template_link_student_program/', views.template_link_student_program,
                       name='template_link_student_program'),

                  path('get_semester_modules/', views.get_semester_modules, name='get_semester_modules'),
                  path('save_student_program/', views.save_student_program, name='save_student_program'),

                  path('template_academic_progress/', views.template_academic_progress,
                       name='template_academic_progress'),
                  path('filter_academic_progress/', views.filter_academic_progress, name='filter_academic_progress'),

                  path('template_academic_progress_details/<int:app_id>/', views.template_academic_progress_details,
                       name='template_academic_progress_details'),
                  path('export_academic_progress_details/', views.export_academic_progress_details,
                       name='export_academic_progress_details'),
                  path('template_attendance_report/', views.template_attendance_report,
                       name='template_attendance_report'),
                  path('filter_attendance_report/', views.filter_attendance_report, name='filter_attendance_report'),

                  path('template_accepted_students/', views.template_accepted_students, name='template_accepted_students'),

                  path('template_link_students_donor/', views.template_link_students_donor, name='template_link_students_donor'),
                  path('save_students_donor_linking/', views.save_students_donor_linking, name='save_students_donor_linking'),
                  path('template_donor_students_linking/', views.template_donor_students_linking, name='template_donor_students_linking'),
                  path('filter_donor_student_linking/', views.filter_donor_student_linking, name='filter_donor_student_linking'),

                  path('template_student_agreement/', views.template_student_agreement, name='template_student_agreement'),
                  path('template_semester_result/', views.template_semester_result, name='template_semester_result'),

                  # path('generate_student_details_pdf/<int:app_id>/', views.generate_student_details_pdf,name='generate_student_details_pdf'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
