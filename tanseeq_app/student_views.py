from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from tanseeq_app.models import (
    PersonalDetails,
)
from tanseeq_app.forms import (
    PersonalInfoForm,
)
# Create your views here.


class TanseeqStudentHome(TemplateView):
    template_name = 'tanseeq_student/student_home.html'


class PersonalInfoView(View):
    model = PersonalDetails
    form_class = PersonalInfoForm
    template_name = "tanseeq_student/personal_info.html"
    redirect_url = 'tanseeq_app:add_personal_info'

    def get(self, request, pk=None):
        context = {
            "form": self.form_class(),
        }
        if PersonalDetails.objects.filter(created_by=request.user).exists():
            instance = get_object_or_404(self.model, created_by=request.user)
            context["instance"] = instance
            context["form"] = self.form_class(instance=get_object_or_404(self.model, created_by=request.user))
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, pk=None):
        if PersonalDetails.objects.filter(created_by=request.user).exists():
            instance = get_object_or_404(self.model, created_by=request.user)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not PersonalDetails.objects.filter(created_by=request.user):
                obj.created_by = request.user
                obj.user = request.user
            obj.save()
            obj.user.first_name = form.data['first_name']
            obj.user.last_name = form.data['last_name']
            obj.user.save()

            if pk:
                messages.success(request, "Record Updated.")
            else:
                messages.success(request, "Record saved.")
        else:
            context = {
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect(self.redirect_url)
