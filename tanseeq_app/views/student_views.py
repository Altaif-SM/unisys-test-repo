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
)
from tanseeq_app.forms.student_forms import (
    ApplicationInfoForm,
    SecondaryCertificationForm,
    StudentStudyModeForm
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
            instance = get_object_or_404(self.model, created_by = request.user)
            context["instance"] = instance
            context["form"] = self.form_class(instance=get_object_or_404(self.model, created_by = request.user))
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
                obj.tanseeq_id = random.SystemRandom().randint(100000,999999)
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
    redirect_url = 'tanseeq_app:student_study_mode'

    def get(self, request, pk=None):
        context = {
            "form": self.form_class(),
        }
        if SecondaryCertificateInfo.objects.filter(created_by=request.user).exists():
            instance = get_object_or_404(self.model, created_by = request.user)
            context["instance"] = instance
            context["form"] = self.form_class(instance=get_object_or_404(self.model, created_by = request.user))
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
            if not SecondaryCertificateInfo.objects.filter(created_by=request.user).exists():
                obj.created_by = request.user
            obj.save()
            messages.success(request, "Record saved.")
        else:
            context = {
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect(self.redirect_url)


class StudentStudyModeView(View):
    model = SecondaryCertificateInfo
    template_name = "tanseeq_student/study_mode.html"
    form_class = StudentStudyModeForm
    redirect_url = "tanseeq_app:list_student_programs"

    def get_context_data(self, **kwargs):
        user = self.request.user
        instance = self.model.objects.filter(created_by=user).first()
        context = {
            "form" : self.form_class(instance=instance) if instance else self.form_class()
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
            messages.error(request, "Please add the Secondary certificate first.")
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
        extra_filters = {}
        if faculty_id:
            extra_filters["faculty_id"] = faculty_id
        cert_obj = SecondaryCertificateInfo.objects.filter(created_by=user).first()
        queryset = ConditionFilters.objects.filter(
            type_of_secondary = cert_obj.secondary_certificate,
            study_mode = cert_obj.study_mode,
            average__lte = cert_obj.average,
            year = cert_obj.year,
            **extra_filters
        ).select_related("program")
        return queryset

    def get(self, request, *args, **kwargs):
        cert_obj = SecondaryCertificateInfo.objects.filter(created_by=request.user).exists()
        if not cert_obj:
            messages.info(self.request, "Please add secondary certificate first.")
            return redirect("tanseeq_app:add_secondary_certificate_info")
        return super().get(args, kwargs)