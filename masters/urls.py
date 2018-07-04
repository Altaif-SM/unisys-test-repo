from django.urls import path

from . import views

app_name = 'masters'

urlpatterns = [

    # *******------------- Year Master ---------------************
    path('template_year_master/', views.template_year_master, name='template_year_master'),
    path('save_year/', views.save_year, name='save_year'),
    path('update_year/', views.update_year, name='update_year'),
    path('delete_year/', views.delete_year, name='delete_year'),

    # ********------ Scholarship Master --------****************************
    path('template_scholarship_master/', views.template_scholarship_master, name='template_scholarship_master'),
    path('save_scholarship/', views.save_scholarship, name='save_scholarship'),
    path('update_scholarship/', views.update_scholarship, name='update_scholarship'),
    path('delete_scholarship/', views.delete_scholarship, name='delete_scholarship'),

    # ********------ Country Master --------****************************
    path('template_country_master/', views.template_country_master, name='template_country_master'),
    path('save_country/', views.save_country, name='save_country'),
    path('update_country/', views.update_country, name='update_country'),
    path('delete_country/', views.delete_country, name='delete_country'),


    # ********------ university Master --------****************************
    path('template_university_master/', views.template_university_master, name='template_university_master'),
    path('save_university/', views.save_university, name='save_university'),
    path('update_university/', views.update_university, name='update_university'),
    path('delete_university/', views.delete_university, name='delete_university'),

    path('template_degree_formula_master/', views.template_degree_formula_master,
         name='template_degree_formula_master'),

    path('get_table_data/', views.get_table_data, name='get_table_data'),

]
