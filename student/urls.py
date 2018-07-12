from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

app_name = 'student'

urlpatterns = [
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

                  path('applicant_scholarship_about_yourself_info/', views.applicant_scholarship_about_yourself_info,
                       name='applicant_scholarship_about_yourself_info'),
                  path('save_update_applicant_scholarship_about_yourself_info/',
                       views.save_update_applicant_scholarship_about_yourself_info,
                       name='save_update_applicant_scholarship_about_yourself_info'),

                  path('my_application/', views.my_application, name='my_application'),
                  path('submit_application/', views.submit_application, name='submit_application'),
                  # path('generate_PDF/', views.generate_PDF, name='generate_PDF'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
