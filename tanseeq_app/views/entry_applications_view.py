from django.views.generic import TemplateView, View, ListView
from accounts.models import User
from tanseeq_app.models import (
    ApplicationDetails,
)
from django.utils.decorators import method_decorator
from common.decorators import check_permissions


# Create your views here.
@method_decorator(check_permissions(User.TANSEEQ_APPLICATION_ENTRY), name='dispatch')
class ListAppliedApplicantsEntry(ListView):
    model = ApplicationDetails
    template_name = "tanseeq_application_entry/list_applied_applicants_entry.html"

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)

