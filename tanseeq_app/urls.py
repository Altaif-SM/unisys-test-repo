from django.contrib.auth.decorators import login_required
from django.urls import path
from tanseeq_app.views import *


app_name = 'tanseeq_app'

urlpatterns = [
    path('admin/', login_required(TanseeqAdminHome.as_view()), name='tanseeq_admin'),

    path('tanseeq_period/', login_required(TanseeqPeriodListView.as_view()), name='list_tanseeq_period'),
    path('tanseeq_period/add', TanseeqPeriodView.as_view(), name='add_tanseeq_period'),
    path('tanseeq_period/<int:pk>', TanseeqPeriodView.as_view(), name='tanseeq_period'),

    path('university_guide/', login_required(UniversityGuideList.as_view()), name='list_university_guide'),
    path('update_university_guide/', login_required(UniversityGuideUpdateView.as_view()), name='update_university_guide'),
    path(
        'delete_university_guide/<int:pk>',
        login_required(UniversityGuideDeleteView.as_view()),
        name='delete_university_guide'
    ),
]
