from django.contrib.auth.decorators import login_required
from django.urls import path
from tanseeq_app.views import *
from tanseeq_app.student_views import *

app_name = 'tanseeq_app'

urlpatterns = [
    path('admin/', login_required(TanseeqAdminHome.as_view()), name='tanseeq_admin'),
    path('tanseeq_period/', login_required(TanseeqPeriodListView.as_view()), name='list_tanseeq_period'),
    path('add/tanseeq_period', TanseeqPeriodView.as_view(), name='add_tanseeq_period'),
    path('tanseeq_period/<int:pk>', TanseeqPeriodView.as_view(), name='tanseeq_period'),

    path('university_guide/', login_required(UniversityGuideList.as_view()), name='list_university_guide'),
    path(
    'update_university_guide/', login_required(UniversityGuideUpdateView.as_view()), name='update_university_guide'
    ),
    path(
        'delete_university_guide/<int:pk>',
        login_required(UniversityGuideDeleteView.as_view()),
        name='delete_university_guide'
    ),
    path(
        'secondary_certificate/',
        login_required(SecondarySchoolCertificateListView.as_view()),
        name='list_secondary_certificate'
    ),
    path(
        'secondary_certificate/<int:pk>',
        login_required(SecondarySchoolCertificateListView.as_view()),
        name='secondary_certificate'
    ),
    path(
        'update_secondary_certificate/',
        login_required(SecondarySchoolCertificateUpdateView.as_view()),
        name='update_secondary_certificate'
    ),

    path(
        'university_attachment/', login_required(UniversityAttachmentList.as_view()), name='list_university_attachment'
    ),
    path(
        'add/university_attachment/',
        login_required(UniversityAttachmentView.as_view()),
        name='add_university_attachment'
    ),
    path(
        'update/<int:pk>/university_attachment/',
        login_required(UniversityAttachmentView.as_view()),
        name='update_university_attachment'
    ),
    path(
        'delete/<int:pk>/university_attachment/',
        login_required(UniversityAttachmentView.as_view()),
        name='delete_university_attachment'
    ),
    path(
        'study_mode/', login_required(StudyModeList.as_view()), name='list_study_mode'
    ),
    path(
        'add/study_mode/',
        login_required(StudyModeView.as_view()),
        name='add_study_mode'
    ),
    path(
        'update/<int:pk>/study_mode/',
        login_required(StudyModeView.as_view()),
        name='update_study_mode'
    ),
    path(
        'delete/<int:pk>/study_mode/',
        login_required(StudyModeView.as_view()),
        name='delete_study_mode'
    ),

        path(
        'tanseeq_faculty/',
        login_required(TanseeqFacultyList.as_view()),
        name='list_tanseeq_faculty'
    ),
    path(
        'add/tanseeq_faculty/',
        login_required(TanseeqFacultyView.as_view()),
        name='add_tanseeq_faculty'
    ),
    path(
        'edit/<int:pk>/tanseeq_faculty/',
        login_required(TanseeqFacultyView.as_view()),
        name='edit_tanseeq_faculty'
    ),
    path(
        'delete/<int:pk>/tanseeq_faculty/',
        login_required(TanseeqFacultyView.as_view()),
        name='delete_tanseeq_faculty'
    ),

    path(
        'tanseeq_program/',
        login_required(TanseeqProgramList.as_view()),
        name='list_tanseeq_program'
    ),
    path(
        'add/tanseeq_program/',
        login_required(TanseeqProgramView.as_view()),
        name='add_tanseeq_program'
    ),
    path(
        'edit/<int:pk>/tanseeq_program/',
        login_required(TanseeqProgramView.as_view()),
        name='edit_tanseeq_program'
    ),
    path(
        'delete/<int:pk>/tanseeq_program/',
        login_required(TanseeqProgramView.as_view()),
        name='delete_tanseeq_program'
    ),
    
    path(
        'tanseeq_filters/',
        login_required(ConditionFiltersList.as_view()),
        name='list_tanseeq_filters'
    ),
    path(
        'add/tanseeq_filter/',
        login_required(ConditionsView.as_view()),
        name='add_tanseeq_filter'
    ),
    path(
        'edit/<int:pk>/tanseeq_filter/',
        login_required(ConditionsView.as_view()),
        name='edit_tanseeq_filter'
    ),
    path(
        'delete/<int:pk>/tanseeq_filter/',
        login_required(ConditionsView.as_view()),
        name='delete_tanseeq_filter'
    ),
    path(
        'get_universities/',
        login_required(get_universities),
        name='get_universities'
    ),
    path(
        'tanseeq_fees/', login_required(TanseeqFeeList.as_view()), name='list_tanseeq_fees'
    ),
    path(
        'add/tanseeq_fees/',
        login_required(TansseqFeeView.as_view()),
        name='add_tanseeq_fees'
    ),
    path(
        'update/<int:pk>/tanseeq_fee/',
        login_required(TansseqFeeView.as_view()),
        name='update_tanseeq_fee'
    ),
    path(
        'delete/<int:pk>/tanseeq_fee/',
        login_required(TansseqFeeView.as_view()),
        name='delete_tanseeq_fees'
    ),
    path(
        'tanseeq_courses/', login_required(TanseeqCourseListView.as_view()), name='list_tanseeq_courses'
    ),
    path(
        'update_tanseeq_course/',
        login_required(TanseeqCourseUpdateView.as_view()),
        name='update_tanseeq_course'
    ),
    path(
        'course/<int:pk>',
        login_required(CourseListView.as_view()),
        name='list_course'
    ),
    path(
        'tanseeq_courses/<int:pk>',
        login_required(TanseeqCourseListView.as_view()),
        name='tanseeq_courses'
    ),
    path(
        'update_course/',
        login_required(CourseUpdateView.as_view()),
        name='update_course'
    ),
    path('student/', login_required(TanseeqStudentHome.as_view()), name='tanseeq_student'),
    path(
        'personal_info/',
        login_required(PersonalInfoView.as_view()),
        name='personal_info'
    ),
    path(
        'secondary_certificate/',
        login_required(SecondaryCertificateView.as_view()),
        name='secondary_certificate'
    ),

]
TanseeqProgramList