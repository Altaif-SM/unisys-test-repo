from django.urls import path

from . import views

app_name = 'masters'

urlpatterns = [

    # ******* Year Master ************
    path('template_year_master/', views.template_year_master, name='template_year_master'),
    path('save_year/', views.save_year, name='save_year'),
    path('update_year/', views.update_year, name='update_year'),
    path('delete_year/', views.delete_year, name='delete_year'),

    path('template_scholarship_master/', views.template_scholarship_master, name='template_scholarship_master'),
    path('template_degree_formula_master/', views.template_degree_formula_master,
         name='template_degree_formula_master'),

    path('get_table_data/', views.get_table_data, name='get_table_data'),

]
