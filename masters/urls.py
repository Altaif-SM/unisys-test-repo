from django.urls import path

from . import views

app_name = 'masters'

urlpatterns = [
    path('template_year_master/', views.template_year_master, name='template_year_master'),

    path('get_table_data/', views.get_table_data, name='get_table_data'),
    path('save_year/', views.save_year, name='save_year'),
]