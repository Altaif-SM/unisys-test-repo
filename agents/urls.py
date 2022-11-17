from django.urls import path

from . import views


app_name = 'agents'



urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('personal_info/', views.personal_info, name='personal_info'),
    path('corporate_info/', views.corporate_info, name='corporate_info'),
    path('attachment/', views.attachment, name='attachment'),
    path('declaration/', views.declaration, name='declaration'),
    path('recruiter_dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter_approved_application/', views.recruiter_approved_application, name='recruiter_approved_application'),
    path('referral_fee_topup/', views.referral_fee_topup, name='referral_fee_topup'),
    path('agent_application_details/<int:agent_id>/', views.agent_application_details,name='agent_application_details'),
    path('applicant_personal_info/', views.applicant_personal_info, name='applicant_personal_info'),
]
