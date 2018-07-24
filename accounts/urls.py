from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('home/', views.home, name='home'),
    # path('signin/', views.template_signin, name='signin'),
    path('signup/', views.template_signup, name='signup'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('user_signin/', views.user_signin, name='user_signin'),
    path('user_signout/', views.user_signout, name='user_signout'),
    # path('forget_password/', views.forget_password, name='forget_password'),
]