from django.views.generic import View, ListView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from tanseeq_app.models import (
    AppliedPrograms,
    ApplicationDetails,
    SecondaryCertificateInfo,
    ApplicantAttachment,
)
from tanseeq_app.forms.student_forms import(
    ApplicationInfoForm,
    SecondaryCertificationForm,
)
from tanseeq_app.forms.reviewer_forms import ReviewerForm


class ListReviewApplications(ListView):
    model = AppliedPrograms
    template_name = "tanseeq_reviewer/list_review_applications.html"

    def get_queryset(self):
        university = self.request.GET.get("university")
        filter_by_status = self.request.GET.get("filter_by_status")
        filters = {}
        if university:
            filters["program_details__university_id"] = university
        if filter_by_status:
            filters["review_status"] = filter_by_status if filter_by_status in ["0", "1"] else None

        query_set = self.model.objects.filter(bond_no__isnull=False, is_denied=False, **filters)
        return query_set


class ReviewApplication(View):
    model = AppliedPrograms
    template_name = "tanseeq_reviewer/review_application.html"
    form_class = ReviewerForm

    def get_context_data(self, pk):
        applied_program = get_object_or_404(self.model, pk=pk)
        app_details_obj = get_object_or_404(ApplicationDetails, user_id=applied_program.user_id)
        secondary_cert_obj = get_object_or_404(SecondaryCertificateInfo, created_by_id=applied_program.user_id)

        context = {
            "attachments": get_object_or_404(ApplicantAttachment, created_by_id=applied_program.user_id),
            "app_details_obj": app_details_obj,
            "app_details_form": ApplicationInfoForm(instance=app_details_obj),
            "secondary_cert_obj": secondary_cert_obj,
            "secondary_cert_form": SecondaryCertificationForm(instance=secondary_cert_obj),
            "applied_program": applied_program,
            "form": self.form_class(instance=applied_program)
        }

        return context

    def get(self, request, pk):
        context = self.get_context_data(pk)
        return render(request, self.template_name, context)
    
    def update_details(self, form):
        data = self.request.POST
        if form.is_valid():
            form.save()
        else:
            data = {"msg": "error", "form_errors": form.errors}
            return JsonResponse(data, status=400)
        return JsonResponse({"msg": "updated."}, status=200)

    def post(self, request, pk):
        form_of = request.POST.get("form")
        applied_program = get_object_or_404(self.model, pk=pk)
        data = self.request.POST

        if form_of and form_of == "application_details":
            instance = get_object_or_404(ApplicationDetails, user_id=applied_program.user_id)
            form = ApplicationInfoForm(data, instance=instance)
            return self.update_details(applied_program, form)

        elif form_of and form_of == "secondary_cert":
            instance = get_object_or_404(SecondaryCertificateInfo, created_by_id=applied_program.user_id)
            form = SecondaryCertificationForm(data, instance=instance)
            return self.update_details(applied_program, form)

        instance = get_object_or_404(self.model, pk=pk)
        form = self.form_class(data, instance=instance)
        if form.is_valid():
            form.save()
        else:
            context = self.get_context_data(pk)
            context["form"] = form
            return render(request, self.template_name, context)
        
        return redirect("tanseeq_app:reviewer_review_application", pk=pk)
