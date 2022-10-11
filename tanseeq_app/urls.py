from django.contrib.auth.decorators import login_required
from django.urls import path
from tanseeq_app.views import *


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
]
