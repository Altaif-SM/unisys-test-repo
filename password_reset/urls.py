
from django.urls import path, re_path

from . import views
from django.conf.urls.static import static, serve
from django.conf import settings

app_name = 'password_reset'
urlpatterns = [
    re_path('media/(?P<path>.*)', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path('static/(?P<path>.*)', serve,{'document_root': settings.STATIC_ROOT}),

    re_path('recover/(?P<signature>.+)/', views.recover_done,
        name='password_reset_sent'),
    path('recover/', views.recover, name='password_reset_recover'),
    path('reset/done/', views.reset_done, name='password_reset_done'),
    re_path('reset/(?P<token>[\w:-]+)/', views.reset,
        name='password_reset_reset'),
    #url(r'^password_change/(?P<user_id>[0-9]+)', views.password_change, name='password_change'),

]