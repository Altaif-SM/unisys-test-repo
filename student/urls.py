from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('applicant_personal_info/', views.applicant_personal_info, name='applicant_personal_info'),
    path('applicant_family_info/', views.applicant_family_info, name='applicant_family_info'),
    path('applicant_family_mother_sibling_info/', views.applicant_family_mother_sibling_info,
         name='applicant_family_mother_sibling_info'),
    path('applicant_academic_english_qualification/', views.applicant_academic_english_qualification,
         name='applicant_academic_english_qualification'),
    path('applicant_curriculum_experience_info/', views.applicant_curriculum_experience_info,
         name='applicant_curriculum_experience_info'),
    path('applicant_scholarship_about_yourself_info/', views.applicant_scholarship_about_yourself_info,
         name='applicant_scholarship_about_yourself_info'),
]
