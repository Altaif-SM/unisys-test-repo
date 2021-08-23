from django.urls import path

from . import views
from accounts import views as account_view
app_name = 'masters'




urlpatterns = [

    # *******------------- Year Master ---------------************
    path('template_year_master/', views.template_year_master, name='template_year_master'),
    path('save_year/', views.save_year, name='save_year'),
    path('update_year/', views.update_year, name='update_year'),
    path('delete_year/', views.delete_year, name='delete_year'),

    path('change_session_year/', views.change_session_year, name='change_session_year'),

    # ********------ Scholarship Master --------****************************
    path('template_scholarship_master/', views.template_scholarship_master, name='template_scholarship_master'),
    path('save_scholarship/', views.save_scholarship, name='save_scholarship'),
    path('update_scholarship/', views.update_scholarship, name='update_scholarship'),
    path('delete_scholarship/', views.delete_scholarship, name='delete_scholarship'),

    # ********------ Terms and Condition Master --------****************************
    path('terms_condition_master/', views.terms_condition_master, name='terms_condition_master'),
    path('save_terms_condition/', views.save_terms_condition, name='save_terms_condition'),

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
    path('formula_type_master/', views.formula_type_master, name='formula_type_master'),

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


    # ********------ development program master Master --------****************************
    path('template_development_program_master/', views.template_development_program_master,
         name='template_development_program_master'),
    path('save_development_program_master/', views.save_development_program_master, name='save_development_program_master'),
    path('update_development_program_master/', views.update_development_program_master, name='update_development_program_master'),
    path('delete_development_program_master/', views.delete_development_program_master, name='delete_development_program_master'),

    # ********------ manage partner Master --------****************************
    path('template_manage_partner_master/', views.template_manage_partner_master,
         name='template_manage_partner_master'),
    path('save_manage_partner_master/', views.save_manage_partner_master, name='save_manage_partner_master'),
    path('update_manage_partner_master/', views.update_manage_partner_master, name='update_manage_partner_master'),
    path('delete_manage_partner_master/', views.delete_manage_partner_master, name='delete_manage_partner_master'),
    path('export_partner_list/', views.export_partner_list, name='export_partner_list'),

    # ********------ manage donor Master --------****************************
    path('template_manage_donor_master/', views.template_manage_donor_master,
         name='template_manage_donor_master'),
    path('save_manage_donor_master/', views.save_manage_donor_master, name='save_manage_donor_master'),
    path('update_manage_donor_master/', views.update_manage_donor_master, name='update_manage_donor_master'),
    path('delete_manage_donor_master/', views.delete_manage_donor_master, name='delete_manage_donor_master'),

    path('email_templates_list/', views.email_templates_list, name='email_templates_list'),
    path('create_email_template/', views.create_email_template, name='create_email_template'),
    path('email_templates_view/<int:rec_id>/',views.email_templates_view, name='email_templates_view'),
    path('save_email_template/', views.save_email_template, name='save_email_template'),


    path('development_program_pdf/', views.development_program_pdf, name='development_program_pdf'),
    path('generate_PDF/', views.generate_PDF, name='generate_PDF'),

    path('get_table_data/', views.get_table_data, name='get_table_data'),

    path('template_partner_details/<int:partner_id>/', views.template_partner_details, name='template_partner_details'),
    path('partner_all_details_pdf/<int:partner_id>/', views.partner_all_details_pdf, name='partner_all_details_pdf'),
    path('template_donar_details/<int:donor_id>/', views.template_donar_details, name='template_donar_details'),
    path('donar_all_details_pdf/<int:donor_id>/', views.donar_all_details_pdf, name='donar_all_details_pdf'),

    path('university_details/', views.university_details, name='university_details'),
    path('save_university_details/', views.save_university_details, name='save_university_details'),

    path('language_settings/', views.language_settings, name='language_settings'),
    path('add_language/', views.add_language, name='add_language'),
    path('edit_language/<int:language_id>/', views.edit_language, name='edit_language'),
    path('delete_language/', views.delete_language, name='delete_language'),

    path('currency_settings/', views.currency_settings, name='currency_settings'),
    path('add_currency/', views.add_currency, name='add_currency'),
    path('edit_currency/<int:currency_id>/', views.edit_currency, name='edit_currency'),
    path('delete_currency/', views.delete_currency, name='delete_currency'),

    path('university_settings/', views.university_settings, name='university_settings'),
    path('add_university/', views.add_university, name='add_university'),
    path('edit_university/<int:university_id>/', views.edit_university, name='edit_university'),
    path('delete_university/', views.delete_university, name='delete_university'),

    path('faculty_settings/', views.faculty_settings, name='faculty_settings'),
    path('add_faculty/', views.add_faculty, name='add_faculty'),
    path('edit_faculty/<int:faculty_id>/', views.edit_faculty, name='edit_faculty'),
    path('delete_faculty/', views.delete_faculty, name='delete_faculty'),

    path('program_settings/', views.program_settings, name='program_settings'),

    path('study_mode_settings/', views.study_mode_settings, name='study_mode_settings'),
    path('add_program/', views.add_program, name='add_program'),
    path('edit_study_mode/', views.edit_study_mode, name='edit_study_mode'),
    path('delete_study_mode/', views.delete_study_mode, name='delete_study_mode'),

]
