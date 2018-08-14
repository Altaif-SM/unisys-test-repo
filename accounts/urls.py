from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('home/', views.home, name='home'),
    # path('signin/', views.template_signin, name='signin'),
    # path('signup/', views.template_signup, name='signup'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('user_signin/', views.user_signin, name='user_signin'),
    path('user_signout/', views.user_signout, name='user_signout'),
    # path('forget_password/', views.forget_password, name='forget_password'),
    path('template_manage_user/', views.template_manage_user,name='template_manage_user'),
    path('account_activate/<int:user_id>/', views.account_activate,name='account_activate'),

    path('update_switch/', views.update_switch,name='update_switch'),
]