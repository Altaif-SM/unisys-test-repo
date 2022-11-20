from django.http.request import QueryDict
from django.views.generic import View, ListView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from tanseeq_app.models import AppliedPrograms
from common.decorators import check_permissions
from tanseeq_app.forms.faculty_forms import FacultyReviewForm
from django.shortcuts import get_object_or_404
from accounts.models import User


@method_decorator(check_permissions(User.TANSEEQ_FACULTY), name='dispatch')
class ListFacultyStudents(ListView):
    model = AppliedPrograms
    template_name = "tanseeq_faculty/list_students.html"

    def get_queryset(self):
        user = self.request.user
        filter_by_fee = self.request.GET.get("filter_by_status")
        filters={}
        if filter_by_fee == "paid":
            filters["bond_no__isnull"] = False
        elif filter_by_fee == "un paid":
            filters["bond_no__isnull"] = True
        queryset = self.model.objects.filter(
            program_details__university=user.university,
            program_details__faculty__in=user.tanseeq_faculty.all(),
            program_details__program__in=user.tanseeq_program.all(),
            is_denied=False,
            review_status__in=[
                AppliedPrograms.ACCEPTED_BY_FACULTY, AppliedPrograms.REJECTED_BY_FACULTY, AppliedPrograms.ACCEPTED_BY_EXAMINER
            ],
            **filters
        ).select_related("program_details")
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FacultyReviewForm()
        return context


@method_decorator(check_permissions(User.TANSEEQ_FACULTY), name='dispatch')
class ManageFacultyStudentApplication(View):
    model = AppliedPrograms

    def patch(self, request, pk):
        user = self.request.user
        data = QueryDict(request.body)
        instance = get_object_or_404(
            AppliedPrograms,
            pk=pk,
            program_details__university=user.university,
            program_details__faculty__in=user.tanseeq_faculty.all(),
            program_details__program__in=user.tanseeq_program.all(),
            review_status__in=[
                AppliedPrograms.ACCEPTED_BY_FACULTY, AppliedPrograms.REJECTED_BY_FACULTY, AppliedPrograms.ACCEPTED_BY_EXAMINER
            ]
        )
        form = FacultyReviewForm(data, instance=instance)
        if form.is_valid():
            form.save()
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    