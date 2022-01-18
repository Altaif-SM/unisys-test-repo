from django.urls import path

from . import views
from accounts import views as account_view
app_name = 'masters'






urlpatterns = [

    # *******------------- Year Master ---------------************
    path('template_year_master/', views.template_year_master, name='template_year_master'),
    path('save_year/', views.save_year, name='save_year'),
    path('update_year/', views.update_year, name='update_year'),
    path('delete_years/', views.delete_years, name='delete_years'),

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
    path('country_settings/', views.country_settings, name='country_settings'),
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
    path('delete_semesters/', views.delete_semesters, name='delete_semesters'),

    # ********------ degree Master --------****************************
    path('template_degree_master/', views.template_degree_master, name='template_degree_master'),
    path('save_degree/', views.save_degree, name='save_degree'),
    path('update_degree/', views.update_degree, name='update_degree'),
    path('delete_degree/', views.delete_degree, name='delete_degree'),

    # ********------ program Master --------****************************
    path('template_program_master/', views.template_program_master, name='template_program_master'),
    path('save_program/', views.save_program, name='save_program'),
    path('update_program/', views.update_program, name='update_program'),
    path('delete_programs/', views.delete_programs, name='delete_programs'),

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

    path('study_mode_settings/', views.study_mode_settings, name='study_mode_settings'),
    path('add_study_mode/', views.add_study_mode, name='add_study_mode'),
    path('edit_study_mode/', views.edit_study_mode, name='edit_study_mode'),
    path('delete_study_mode/', views.delete_study_mode, name='delete_study_mode'),

    path('study_level_settings/', views.study_level_settings, name='study_level_settings'),
    path('add_study_level/', views.add_study_level, name='add_study_level'),
    path('edit_study_level/', views.edit_study_level, name='edit_study_level'),
    path('delete_study_level/', views.delete_study_level, name='delete_study_level'),

    path('study_type_settings/', views.study_type_settings, name='study_type_settings'),
    path('add_study_type/', views.add_study_type, name='add_study_type'),
    path('edit_study_type/', views.edit_study_type, name='edit_study_type'),
    path('delete_study_type/', views.delete_study_type, name='delete_study_type'),

    path('program_fee_settings/', views.program_fee_settings, name='program_fee_settings'),
    path('add_program_fee/', views.add_program_fee, name='add_program_fee'),
    path('edit_program_fee/<int:program_id>/', views.edit_program_fee, name='edit_program_fee'),

    path('program_settings/', views.program_settings, name='program_settings'),
    path('add_program/', views.add_program, name='add_program'),
    path('edit_program/<int:program_id>/', views.edit_program, name='edit_program'),
    path('delete_program/', views.delete_program, name='delete_program'),

    path('year_settings/', views.year_settings, name='year_settings'),
    path('add_year/', views.add_year, name='add_year'),
    path('delete_year/', views.delete_year, name='delete_year'),

    path('semester_settings/', views.semester_settings, name='semester_settings'),
    path('add_semester/', views.add_semester, name='add_semester'),
    path('delete_semester/', views.delete_semester, name='delete_semester'),
    path('edit_semester/<int:semester_id>/', views.edit_semester, name='edit_semester'),

    path('activity_settings/', views.activity_settings, name='activity_settings'),
    path('add_activity/', views.add_activity, name='add_activity'),
    path('update_activity/', views.update_activity, name='update_activity'),
    path('delete_activity/', views.delete_activity, name='delete_activity'),

    path('student_mode_settings/', views.student_mode_settings, name='student_mode_settings'),
    path('add_student_mode/', views.add_student_mode, name='add_student_mode'),
    path('update_student_mode/', views.update_student_mode, name='update_student_mode'),
    path('delete_student_mode/', views.delete_student_mode, name='delete_student_mode'),

    path('learning_centers_settings/', views.learning_centers_settings, name='learning_centers_settings'),
    path('add_learning_centers/', views.add_learning_centers, name='add_learning_centers'),
    path('edit_learning_centers/<int:learning_center_id>/', views.edit_learning_centers, name='edit_learning_centers'),
    path('delete_learning_centers/', views.delete_learning_centers, name='delete_learning_centers'),

    path('university_partner_settings/', views.university_partner_settings, name='university_partner_settings'),
    path('add_university_partner/', views.add_university_partner, name='add_university_partner'),
    path('edit_university_partner/<int:university_id>/', views.edit_university_partner, name='edit_university_partner'),
    path('delete_university_partner/', views.delete_university_partner, name='delete_university_partner'),

    path('campus_settings/', views.campus_settings, name='campus_settings'),
    path('add_campus/', views.add_campus, name='add_campus'),
    path('edit_campus/<int:campus_id>/', views.edit_campus, name='edit_campus'),
    path('delete_campus/', views.delete_campus, name='delete_campus'),

    path('calendar_settings/', views.calendar_settings, name='calendar_settings'),
    path('add_calendar/', views.add_calendar, name='add_calendar'),
    path('edit_calender/<int:calender_id>/', views.edit_calender, name='edit_calender'),
    path('delete_calender/', views.delete_calender, name='delete_calender'),

    path('department_settings/', views.department_settings, name='department_settings'),
    path('add_department/', views.add_department, name='add_department'),
    path('edit_department/<int:department_id>/', views.edit_department, name='edit_department'),
    path('delete_department/', views.delete_department, name='delete_department'),
    path('link_department_staff/', views.link_department_staff, name='link_department_staff'),
    path('delete_department_staff/', views.delete_department_staff, name='delete_department_staff'),

    path('document_settings/', views.document_settings, name='document_settings'),
    path('edit_document/<int:doc_id>/', views.edit_document, name='edit_document'),
    path('update_documet/', views.update_documet, name='update_documet'),
    path('delete_document/', views.delete_document, name='delete_document'),

    path('link_campus_staff/', views.link_campus_staff, name='link_campus_staff'),
    path('delete_campus_staff/', views.delete_campus_staff, name='delete_campus_staff'),

    path('link_faculty_staff/', views.link_faculty_staff, name='link_faculty_staff'),
    path('delete_faculty_user/', views.delete_faculty_user, name='delete_faculty_user'),

    path('link_university_staff/', views.link_university_staff, name='link_university_staff'),
    path('delete_university_user/', views.delete_university_user, name='delete_university_user'),

    path('group_settings/', views.group_settings, name='group_settings'),
    path('add_group/', views.add_group, name='add_group'),
    path('update_group/', views.update_group, name='update_group'),
    path('delete_group/', views.delete_group, name='delete_group'),

    path('payment_settings/', views.payment_settings, name='payment_settings'),
    path('api_test/', views.api_test, name='api_test'),
    path('get_departments_from_faculty/', views.get_departments_from_faculty, name='get_departments_from_faculty'),
    path('get_programs_from_filter/', views.get_programs_from_filter, name='get_programs_from_filter'),

    path('arabic_lang_proficiency_settings/', views.arabic_lang_proficiency_settings, name='arabic_lang_proficiency_settings'),
    path('add_arabic_lang_proficiency/', views.add_arabic_lang_proficiency, name='add_arabic_lang_proficiency'),
    path('edit_arabic_lang_proficiency/', views.edit_arabic_lang_proficiency, name='edit_arabic_lang_proficiency'),
    path('delete_arabic_lang_proficiency/', views.delete_arabic_lang_proficiency, name='delete_arabic_lang_proficiency'),

    path('english_lang_proficiency_settings/', views.english_lang_proficiency_settings, name='english_lang_proficiency_settings'),
    path('add_english_lang_proficiency/', views.add_english_lang_proficiency, name='add_english_lang_proficiency'),
    path('edit_english_lang_proficiency/', views.edit_english_lang_proficiency, name='edit_english_lang_proficiency'),
    path('delete_english_lang_proficiency/', views.delete_english_lang_proficiency, name='delete_english_lang_proficiency'),
    path('get_year_from_university/', views.get_year_from_university, name='get_year_from_university'),
    path('get_intake_semester_from_year/', views.get_intake_semester_from_year, name='get_intake_semester_from_year'),
    path('get_semester_already_exists/', views.get_semester_already_exists, name='get_semester_already_exists'),


]
