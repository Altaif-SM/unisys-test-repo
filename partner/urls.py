from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from . import filters

app_name = 'partner'


urlpatterns = [
                  path('partner_home/', views.partner_home, name='partner_home'),

                  path('template_registered_application/', views.template_registered_application,
                       name='template_registered_application'),
                  path('template_applicant_scholarship/', views.template_applicant_scholarship,
                       name='template_applicant_scholarship'),

                  path('filter_registered_application/', views.filter_registered_application,
                       name='filter_registered_application'),
                  path('export_registered_application/', views.export_registered_application,
                       name='export_registered_application'),
                  path('template_applicant_all_details/<int:app_id>/', views.template_applicant_all_details,
                       name='template_applicant_all_details'),

                  path('template_approving_application/', views.template_approving_application,
                       name='template_approving_application'),
                  path('filter_application_status/', views.filter_application_status, name='filter_application_status'),
                  path('change_application_status/', views.change_application_status, name='change_application_status'),
                  path('change_final_application_status/', views.change_final_application_status,
                       name='change_final_application_status'),

                  path('template_application_approval_details/<int:app_id>/',
                       views.template_application_approval_details, name='template_application_approval_details'),

                  path('template_student_progress_history/', views.template_student_progress_history,
                       name='template_student_progress_history'),
                  path('get_country_applications/', views.get_country_applications, name='get_country_applications'),
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
                  path('approve_applicant_semester_result/<int:app_id>/', views.approve_applicant_semester_result,
                       name='approve_applicant_semester_result'),
                  path('export_academic_progress_details/', views.export_academic_progress_details,
                       name='export_academic_progress_details'),
                  path('template_attendance_report/', views.template_attendance_report,
                       name='template_attendance_report'),
                  path('filter_attendance_report/', views.filter_attendance_report, name='filter_attendance_report'),

                  path('template_accepted_students/', views.template_accepted_students,
                       name='template_accepted_students'),

                  path('template_link_students_donor/', views.template_link_students_donor,
                       name='template_link_students_donor'),
                  path('save_students_donor_linking/', views.save_students_donor_linking,
                       name='save_students_donor_linking'),
                  path('template_donor_students_linking/', views.template_donor_students_linking,
                       name='template_donor_students_linking'),
                  path('filter_donor_student_linking/', views.filter_donor_student_linking,
                       name='filter_donor_student_linking'),

                  path('template_student_agreement/', views.template_student_agreement,
                       name='template_student_agreement'),

                  path('filter_student_agreement/', views.filter_student_agreement, name='filter_student_agreement'),
                  path('template_semester_result/', views.template_semester_result, name='template_semester_result'),
                  path('donar_student_linking_export/', views.donar_student_linking_export,
                       name='donar_student_linking_export'),

                  path('template_link_students_parent/', views.template_link_students_parent,
                       name='template_link_students_parent'),
                  path('save_students_parent_linking/', views.save_students_parent_linking,
                       name='save_students_parent_linking'),

                  path('application_all_details_pdf/<int:app_id>/', views.application_all_details_pdf,
                       name='application_all_details_pdf'),
                  # path('generate_student_details_pdf/<int:app_id>/', views.generate_student_details_pdf,name='generate_student_details_pdf'),


                  path('update_semister_module_link_student/', views.update_semister_module_link_student, name='update_semister_module_link_student'),
                  path('companies_datatable/', filters.FilterCompaniesList.as_view(), name='companies_datatable'),
                  path('assign_supervisior/<int:application_id>/', views.assign_supervisior, name='assign_supervisior'),
                  path('approved_application/', views.approved_application, name='approved_application'),
                  path('accepted_application/', views.accepted_application, name='accepted_application'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
