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

    # ********------ semester Master --------****************************
    path('template_semester_master/', views.template_semester_master, name='template_semester_master'),
    path('save_semester/', views.save_semester, name='save_semester'),
    path('update_semester/', views.update_semester, name='update_semester'),
    path('delete_semester/', views.delete_semester, name='delete_semester'),

    # ********------ degree Master --------****************************
    path('template_degree_master/', views.template_degree_master, name='template_degree_master'),
    path('save_degree/', views.save_degree, name='save_degree'),
    path('update_degree/', views.update_degree, name='update_degree'),
    path('delete_degree/', views.delete_degree, name='delete_degree'),

    # ********------ program Master --------****************************
    path('template_program_master/', views.template_program_master, name='template_program_master'),
    path('save_program/', views.save_program, name='save_program'),
    path('update_program/', views.update_program, name='update_program'),
    path('delete_program/', views.delete_program, name='delete_program'),

    # ********------ module Master --------****************************
    path('template_module_master/', views.template_module_master, name='template_module_master'),
    path('save_module/', views.save_module, name='save_module'),
    path('update_module/', views.update_module, name='update_module'),
    path('delete_module/', views.delete_module, name='delete_module'),

    # ********------ master and phd Master --------****************************
    path('template_master_and_phd_master/', views.template_master_and_phd_master,
         name='template_master_and_phd_master'),
    path('save_master_and_phd/', views.save_master_and_phd, name='save_master_and_phd'),
    path('update_master_and_phd/', views.update_master_and_phd, name='update_master_and_phd'),
    path('delete_master_and_phd/', views.delete_master_and_phd, name='delete_master_and_phd'),

    # ********------ master and course work Master --------****************************
    path('template_master_course_work_master/', views.template_master_course_work_master,
         name='template_master_course_work_master'),
    path('save_master_course_work/', views.save_master_course_work, name='save_master_course_work'),
    path('update_master_course_work/', views.update_master_course_work, name='update_master_course_work'),
    path('delete_master_course_work/', views.delete_master_course_work, name='delete_master_course_work'),

    # ********------ master and course work Master --------****************************
    path('template_degree_formula_master/', views.template_degree_formula_master,
         name='template_degree_formula_master'),
    path('save_degree_formula_master/', views.save_degree_formula_master, name='save_degree_formula_master'),
    path('update_degree_formula_master/', views.update_degree_formula_master, name='update_degree_formula_master'),
    path('delete_degree_formula_master/', views.delete_degree_formula_master, name='delete_degree_formula_master'),

    path('get_table_data/', views.get_table_data, name='get_table_data'),

]
