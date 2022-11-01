import random
from django.views.generic import TemplateView, View, ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from tanseeq_app.models import (
    ApplicationDetails,
    SecondaryCertificateInfo,
    ConditionFilters,
    AppliedPrograms,
    ApplicantAttachment,
)
from tanseeq_app.forms.student_forms import (
    ApplicationInfoForm,
    SecondaryCertificationForm,
    StudentStudyModeForm,
    ApplyProgramForm,
    ApplicantAttachementsForm,
)


# Create your views here.
class TanseeqStudentHome(TemplateView):
    template_name = 'tanseeq_student/student_home.html'


class PersonalInfoView(View):
    model = ApplicationDetails
    form_class = ApplicationInfoForm
    template_name = "tanseeq_student/personal_info.html"
    redirect_url = 'tanseeq_app:add_secondary_certificate_info'

    def get(self, request, pk=None):
        context = {
            "form": self.form_class(),
        }
        if ApplicationDetails.objects.filter(created_by=request.user).exists():
            instance = get_object_or_404(self.model, created_by=request.user)
            context["instance"] = instance
            context["form"] = self.form_class(
                instance=get_object_or_404(self.model, created_by=request.user))
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, pk=None):
        if ApplicationDetails.objects.filter(created_by=request.user).exists():
            instance = get_object_or_404(self.model, created_by=request.user)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not ApplicationDetails.objects.filter(created_by=request.user).exists():
                obj.created_by = request.user
                obj.user = request.user
                obj.tanseeq_id = random.SystemRandom().randint(100000, 999999)
            obj.save()
            messages.success(request, "Record saved.")
        else:
            context = {
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect(self.redirect_url)


class SecondaryCertificateInfoView(View):
    model = SecondaryCertificateInfo
    form_class = SecondaryCertificationForm
    template_name = "tanseeq_student/secondary_certificate_info.html"
    redirect_url = 'tanseeq_app:applicant_attachments'

    def get(self, request, pk=None):

        cert_obj = ApplicationDetails.objects.filter(
            created_by=request.user).exists()
        if not cert_obj:
            messages.info(
                self.request, "Please add personal info first.")
            return redirect("tanseeq_app:add_personal_info")

        context = {
            "form": self.form_class(),
        }
        if SecondaryCertificateInfo.objects.filter(created_by=request.user).exists():
            instance = get_object_or_404(self.model, created_by=request.user)
            context["instance"] = instance
            context["form"] = self.form_class(
                instance=get_object_or_404(self.model, created_by=request.user))
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, pk=None):
        if SecondaryCertificateInfo.objects.filter(created_by=request.user).exists():
            instance = get_object_or_404(self.model, created_by=request.user)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            application_obj = ApplicationDetails.objects.filter(created_by=request.user).first()
            if not SecondaryCertificateInfo.objects.filter(created_by=request.user).exists():
                obj.created_by = request.user
                obj.application = application_obj
            obj.save()
            messages.success(request, "Record saved.")
        else:
            context = {
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect(self.redirect_url)


class StudentStudyModeView(View):
    """
    Not using it at the moment
    """
    model = SecondaryCertificateInfo
    template_name = "tanseeq_student/study_mode.html"
    form_class = StudentStudyModeForm
    redirect_url = "tanseeq_app:list_student_programs"

    def get_context_data(self, **kwargs):
        user = self.request.user
        instance = self.model.objects.filter(created_by=user).first()
        context = {
            "form": self.form_class(instance=instance) if instance else self.form_class()
        }
        return context

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request):
        user = request.user
        instance = self.model.objects.filter(created_by=user).first()
        if instance:
            form = self.form_class(request.POST, instance=instance)
        else:
            messages.error(
                request, "Please add the Secondary certificate first.")
            return redirect("tanseeq_app:add_personal_info")
        if form.is_valid():
            form.save()
        else:
            context = {
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect(self.redirect_url)


class ListStudentPrograms(ListView):
    model = ConditionFilters
    template_name = "tanseeq_student/list_student_programs.html"

    def get_queryset(self):
        user = self.request.user
        faculty_id = self.request.GET.get("faculty")
        university_id = self.request.GET.get("university")
        study_mode_id = self.request.GET.get("study_mode")

        if (faculty_id is None) or (university_id is None) or (study_mode_id is None):
            return SecondaryCertificateInfo.objects.none()

        extra_filters = {}
        if faculty_id:
            extra_filters["faculty_id"] = faculty_id
        if university_id:
            extra_filters["university_id"] = university_id
        if study_mode_id:
            extra_filters["study_mode_id"] = study_mode_id

        cert_obj = SecondaryCertificateInfo.objects.filter(
            created_by=user).first()
        queryset = ConditionFilters.objects.filter(
            type_of_secondary=cert_obj.secondary_certificate,
            average__lte=cert_obj.average,
            year__gte=cert_obj.year,
            **extra_filters
        ).select_related("university", "faculty", "program").extra(
            select={
                'is_applied': 'SELECT 1 FROM tanseeq_app_appliedprograms WHERE ' +
                'program_details_id=tanseeq_app_conditionfilters.id AND user_id = %s'
            }, select_params=(self.request.user.id,)
        )
        return queryset

    def get(self, request, *args, **kwargs):
        cert_obj = ApplicationDetails.objects.filter(
            created_by=request.user).exists()
        if not cert_obj:
            messages.info(
                self.request, "Please add personal info first.")
            return redirect("tanseeq_app:add_personal_info")

        cert_obj = SecondaryCertificateInfo.objects.filter(
            created_by=request.user).exists()
        if not cert_obj:
            messages.info(
                self.request, "Please add secondary certificate first.")
            return redirect("tanseeq_app:add_secondary_certificate_info")
        return super().get(args, kwargs)


class ListAppliedPrograms(ListView):
    model = AppliedPrograms
    template_name = "tanseeq_student/list_applied_programs.html"

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(user=user).select_related("program_details")


class ApplyProgramView(View):
    model = AppliedPrograms
    form_class = ApplyProgramForm

    def is_eligible(self, condition_filter_id, get_obj=False):
        user = self.request.user
        cert_obj = SecondaryCertificateInfo.objects.filter(
            created_by=user).first()
        is_conditions_pass = ConditionFilters.objects.filter(
            id=condition_filter_id,
            type_of_secondary=cert_obj.secondary_certificate,
            average__lte=cert_obj.average,
            year__gte=cert_obj.year,
        ).exists()
        if get_obj:
            return ConditionFilters.objects.filter(
                id=condition_filter_id,
                type_of_secondary=cert_obj.secondary_certificate,
                average__lte=cert_obj.average,
                year__gte=cert_obj.year,
            ).first()
        return is_conditions_pass

    def check_applied(self, condition_filter_id):
        user = self.request.user
        is_obj = self.model.objects.filter(
            user=user, program_details_id=condition_filter_id).exists()
        return is_obj

    def post(self, request):
        user = self.request.user
        condition_filter_id = request.POST.get("condition_filter_id")
        is_applied = self.check_applied(condition_filter_id)

        if is_applied:
            return JsonResponse({"msg": "Already Applied"}, status=200, safe=False)

        is_eligible = self.is_eligible(condition_filter_id)
        if not is_eligible:
            return JsonResponse({"msg": "Not Eligible"}, status=200, safe=False)

        request_copy = request.POST.copy()
        request_copy["user"] = user.id
        request_copy["program_details"] = condition_filter_id
        form = self.form_class(request_copy)
        if form.is_valid():
            form.save()
        else:
            data = {"msg": "error", "form_errors": form.errors}
            return JsonResponse(data, status=200, safe=False)
        data = {"msg": "Applied"}
        return JsonResponse(data, status=200, safe=False)

    def delete(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk, user=request.user)
        data = {"msg": "Program Removed"}
        is_eligible = self.is_eligible(obj.program_details.id)
        if is_eligible:
            obj.delete()
            return JsonResponse(data, status=202, safe=False)
        else:
            data["msg"] = "No Such Program Found"
            return JsonResponse(data, status=404, safe=False)


class ApplicantAttachmentsView(View):
    model = ApplicantAttachment
    form_class = ApplicantAttachementsForm
    template_name = "tanseeq_student/applicant_attachment_view.html"
    redirect_url = 'tanseeq_app:list_student_programs'

    def get(self, request, pk=None):

        cert_obj = ApplicationDetails.objects.filter(
            created_by=request.user).exists()
        if not cert_obj:
            messages.info(
                self.request, "Please add personal info first.")
            return redirect("tanseeq_app:add_personal_info")

        context = {}
        if ApplicantAttachment.objects.filter(created_by=request.user).exists():
            instance = get_object_or_404(self.model, created_by=request.user)
            context["instance"] = instance
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, pk=None):
        application_obj = ApplicationDetails.objects.filter(created_by=request.user).first()
        instance, created = ApplicantAttachment.objects.get_or_create(created_by=request.user, application = application_obj)
        form = self.form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Record saved.")
            return redirect(self.redirect_url)
        else:
            context = {
                "form": form,
            }
            return render(request, self.template_name, context)
