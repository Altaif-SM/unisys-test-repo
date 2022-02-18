from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

app_name = 'student'

urlpatterns = [
                  path('student_home/', views.student_home, name='student_home'),
                  path('delete_application/<int:app_id>/', views.delete_application,
                       name='delete_application'),

                  path('applicant_personal_info/', views.applicant_personal_info, name='applicant_personal_info'),
                  path('save_update_applicant_personal_info/', views.save_update_applicant_personal_info,
                       name='save_update_applicant_personal_info'),

                  path('applicant_family_info/', views.applicant_family_info, name='applicant_family_info'),
                  path('save_update_applicant_family_info/', views.save_update_applicant_family_info,
                       name='save_update_applicant_family_info'),

                  path('applicant_family_mother_sibling_info/', views.applicant_family_mother_sibling_info,
                       name='applicant_family_mother_sibling_info'),
                  path('save_update_applicant_family_mother_sibling_info/',
                       views.save_update_applicant_family_mother_sibling_info,
                       name='save_update_applicant_family_mother_sibling_info'),

                  path('applicant_academic_english_qualification/', views.applicant_academic_english_qualification,
                       name='applicant_academic_english_qualification'),
                  path('save_update_applicant_academic_english_qualification/',
                       views.save_update_applicant_academic_english_qualification,
                       name='save_update_applicant_academic_english_qualification'),

                  path('applicant_curriculum_experience_info/', views.applicant_curriculum_experience_info,
                       name='applicant_curriculum_experience_info'),
                  path('save_update_applicant_curriculum_experience_info/',
                       views.save_update_applicant_curriculum_experience_info,
                       name='save_update_applicant_curriculum_experience_info'),

                  path('applicant_credit_transfer/', views.applicant_credit_transfer,
                       name='applicant_credit_transfer'),
                  path('save_credit_transfer/',
                       views.save_credit_transfer,
                       name='save_credit_transfer'),

                  path('applicant_employement_history_info/', views.applicant_employement_history_info,
                       name='applicant_employement_history_info'),
                  path('save_update_applicant_employement_history_info/',
                       views.save_update_applicant_employement_history_info,
                       name='save_update_applicant_employement_history_info'),

                  path('applicant_scholarship_about_yourself_info/', views.applicant_scholarship_about_yourself_info,
                       name='applicant_scholarship_about_yourself_info'),
                  path('get_degrees/', views.get_degrees, name='get_degrees'),
                  path('save_update_applicant_scholarship_about_yourself_info/',
                       views.save_update_applicant_scholarship_about_yourself_info,
                       name='save_update_applicant_scholarship_about_yourself_info'),

                  path('my_application/', views.my_application, name='my_application'),
                  path('submit_application/', views.submit_application, name='submit_application'),

                  path('applicant_psychometric_test/', views.applicant_psychometric_test,
                       name='applicant_psychometric_test'),
                  path('save_psychometric_test/', views.save_psychometric_test, name='save_psychometric_test'),
                  path('applicant_agreement_submission/', views.applicant_agreement_submission,
                       name='applicant_agreement_submission'),
                  path('save_agreement_submission/', views.save_agreement_submission, name='save_agreement_submission'),

                  path('applicant_program_certificate_submission/', views.applicant_program_certificate_submission,
                       name='applicant_program_certificate_submission'),

                  path('save_applicant_program_certificate_submission/',
                       views.save_applicant_program_certificate_submission,
                       name='save_applicant_program_certificate_submission'),

                  path('delete_applicant_program_certificate_submission/',
                       views.delete_applicant_program_certificate_submission,
                       name='delete_applicant_program_certificate_submission'),

                  path('applicant_academic_progress/', views.applicant_academic_progress,
                       name='applicant_academic_progress'),

                  path('save_applicant_academic_progress/', views.save_applicant_academic_progress,
                       name='save_applicant_academic_progress'),

                  path('applicant_progress_history/', views.applicant_progress_history,name='applicant_progress_history'),
                  path('save_other_university/', views.save_other_university,name='save_other_university'),

                #========import_student_application======================

                  path('import_student_application/', views.import_student_application,name='import_student_application'),
                  path('import_applicant_qualification_info/', views.import_applicant_qualification_info,name='import_applicant_qualification_info'),
                  path('import_applicant_donor_mapping/', views.import_applicant_donor_mapping,name='import_applicant_donor_mapping'),
                  path('import_applicant_records_tile/', views.import_applicant_records_tile,name='import_applicant_records_tile'),
                  path('export_templates/', views.export_templates,name='export_templates'),
                  path('export_applicant_info_template/', views.export_applicant_info_template,name='export_applicant_info_template'),
                  path('export_applicant_qualification_template/', views.export_applicant_qualification_template,name='export_applicant_qualification_template'),
                  path('export_applicant_donor_mapping/', views.export_applicant_donor_mapping,name='export_applicant_donor_mapping'),



                  path('get_degrees_from_universities/', views.get_degrees_from_universities,name='get_degrees_from_universities'),
                  path('get_courses_from_degrees/', views.get_courses_from_degrees,name='get_courses_from_degrees'),


                  path('applicant_additional_information/', views.applicant_additional_information, name='applicant_additional_information'),
                  path('save_update_applicant_additional_info/', views.save_update_applicant_additional_info,
                       name='save_update_applicant_additional_info'),

                  path('applicant_attachment_submission/', views.applicant_attachment_submission,
                       name='applicant_attachment_submission'),
                  path('save_attachement_submission/', views.save_attachement_submission, name='save_attachement_submission'),

                  path('applicant_declaration/', views.applicant_declaration, name='applicant_declaration'),
                  path('application_offer_letter/', views.application_offer_letter, name='application_offer_letter'),


                  path('application_offer_letter_pdf/<int:app_id>/', views.application_offer_letter_pdf,
                       name='application_offer_letter_pdf'),

                  path('applicant_intake_info/', views.applicant_intake_info, name='applicant_intake_info'),
                  path('get_learning_centre_from_country/', views.get_learning_centre_from_country, name='get_learning_centre_from_country'),
                  path('get_university_from_type/', views.get_university_from_type, name='get_university_from_type'),
                  path('save_update_applicant_intake_info/', views.save_update_applicant_intake_info, name='save_update_applicant_intake_info'),
                  path('get_branch_campus_from_program/', views.get_branch_campus_from_program, name='get_branch_campus_from_program'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
