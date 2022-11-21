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
    path('applicant_personal_info/<int:user_id>', views.applicant_personal_info, name='applicant_personal_info'),
    path('save_update_applicant_personal_info/', views.save_update_applicant_personal_info, name='save_update_applicant_personal_info'),
    path('applicant_intake_info/', views.applicant_intake_info, name='applicant_intake_info'),
    path('save_update_applicant_intake_info/', views.save_update_applicant_intake_info, name='save_update_applicant_intake_info'),
    path('applicant_academic_english_qualification/', views.applicant_academic_english_qualification, name='applicant_academic_english_qualification'),
    path('save_update_applicant_academic_english_qualification/', views.save_update_applicant_academic_english_qualification, name='save_update_applicant_academic_english_qualification'),
    path('applicant_credit_transfer/', views.applicant_credit_transfer, name='applicant_credit_transfer'),
    path('save_credit_transfer/', views.save_credit_transfer, name='save_credit_transfer'),
    path('applicant_credit_transfer_attachement/', views.applicant_credit_transfer_attachement, name='applicant_credit_transfer_attachement'),
    path('save_credit_transfer_attachement/', views.save_credit_transfer_attachement, name='save_credit_transfer_attachement'),
    path('applicant_employement_history_info/', views.applicant_employement_history_info, name='applicant_employement_history_info'),
    path('save_update_applicant_employement_history_info/', views.save_update_applicant_employement_history_info, name='save_update_applicant_employement_history_info'),
    path('applicant_additional_information/', views.applicant_additional_information, name='applicant_additional_information'),
    path('save_update_applicant_additional_info/', views.save_update_applicant_additional_info, name='save_update_applicant_additional_info'),

    path('checkout/', views.checkout, name='checkout'),
    path('create_checkout_session/', views.CreateCheckoutSessionView.as_view(),name='create_checkout_session'),
    path('stripe_checkout_success/<str:session_id>/', views.stripe_checkout_success, name='stripe_checkout_success'),

    path('applicant_attachment_submission/', views.applicant_attachment_submission,
                       name='applicant_attachment_submission'),
    path('save_attachement_submission/', views.save_attachement_submission, name='save_attachement_submission'),
    path('applicant_declaration/', views.applicant_declaration, name='applicant_declaration'),
    path('submit_application/', views.submit_application, name='submit_application'),

]
