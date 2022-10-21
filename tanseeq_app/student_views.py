from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from tanseeq_app.models import (
    ApplicationDetails,
    SecondaryCertificateInfo,
)
from tanseeq_app.forms import (
    ApplicationInfoForm,
    SecondaryCertificationForm,
)
import random

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
    redirect_url = 'tanseeq_app:add_secondary_certificate_info'

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
