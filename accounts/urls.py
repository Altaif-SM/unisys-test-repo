from django.urls import path
from accounts.decoratars import user_login_required
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
    path('staff_settings/', user_login_required(views.staff_settings),name='staff_settings'),
    path('agent_settings/', user_login_required(views.agent_settings), name='agent_settings'),
    path('add_agent/', user_login_required(views.add_agent), name='add_agent'),
    path('update_agent/<int:agent_id>/', user_login_required(views.update_agent), name='update_agent'),
    path('agent_recruiter_settings/', user_login_required(views.agent_recruiter_settings), name='agent_recruiter_settings'),
    path('add_agent_recruiter/', user_login_required(views.add_agent_recruiter),name='add_agent_recruiter'),
    path('add_staff/', user_login_required(views.add_staff), name='add_staff'),
    path('delete_staff/', user_login_required(views.delete_staff), name='delete_staff'),
    path('edit_agent_recruiter/<int:recruiter_id>/', user_login_required(views.edit_agent_recruiter), name='edit_agent_recruiter'),
    path('edit_staff/<int:staff_id>/', user_login_required(views.edit_staff), name='edit_staff'),
    path('edit_agent/<int:agent_id>/', user_login_required(views.edit_agent), name='edit_agent'),
    path('get_email_exists/', views.get_email_exists, name='get_email_exists'),
    path('get_university_exists/', views.get_university_exists, name='get_university_exists'),
    path('get_faculty_from_account_type/', views.get_faculty_from_account_type, name='get_faculty_from_account_type'),
    path('get_program_from_account_type/', views.get_program_from_account_type, name='get_program_from_account_type'),
    path('get_program_from_faculty/', views.get_program_from_faculty, name='get_program_from_faculty'),
    path('list_supervisor_progress_meetings/', views.SupervisorProgressMeetingsList.as_view(), name='list_supervisor_progress_meetings'),
    path('update_progress_meetings/<int:progress_id>/', user_login_required(views.update_progress_meetings), name='update_progress_meetings'),
    path('list_qualifying_test/', views.QualifyingTestList.as_view(), name='list_qualifying_test'),
    path('update/qualifyingteststatus/<int:pk>', views.UpdateQualifyingTestStatus.as_view(), name='update_qualifying_test_status'),
]