from django.urls import path

from . import views


app_name = 'agents'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('personal_info/', views.personal_info, name='personal_info'),
    path('corporate_info/', views.corporate_info, name='corporate_info'),
    path('attachment/', views.attachment, name='attachment'),
]
