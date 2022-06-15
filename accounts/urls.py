from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('signin/', views.template_signin, name='signin'),
    # path('signup/', views.template_signup, name='signup'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('user_signin/', views.user_signin, name='user_signin'),
    path('user_signout/', views.user_signout, name='user_signout'),
    path('change_password/', views.change_password, name='change_password'),
    # path('forget_password/', views.forget_password, name='forget_password'),
    path('template_manage_user/', views.template_manage_user,name='template_manage_user'),
    path('account_activate/<int:user_id>/', views.account_activate,name='account_activate'),

    path('update_switch/', views.update_switch,name='update_switch'),
    path('delete_user/<int:user_id>/', views.delete_user,name='delete_user'),
    path('check_active_year/', views.CheckActiveYear, name='check_active_year'),
    path('staff_settings/', views.staff_settings,name='staff_settings'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('delete_staff/', views.delete_staff, name='delete_staff'),
    path('edit_staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('get_email_exists/', views.get_email_exists, name='get_email_exists'),
    path('get_university_exists/', views.get_university_exists, name='get_university_exists'),
    path('get_faculty_from_account_type/', views.get_faculty_from_account_type, name='get_faculty_from_account_type'),
    path('get_program_from_account_type/', views.get_program_from_account_type, name='get_program_from_account_type'),
    path('get_program_from_faculty/', views.get_program_from_faculty, name='get_program_from_faculty'),
    path('agent_dashboard/', views.agent_dashboard, name='agent_dashboard'),
]