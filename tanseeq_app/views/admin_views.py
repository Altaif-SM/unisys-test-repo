from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, ListView, UpdateView, DeleteView
from accounts.models import User, UserRole
from tanseeq_app.models import (
    TanseeqPeriod,
    SecondarySchoolCetificate,
    UniversityAttachment,
    TanseeqFaculty,
    TanseeqProgram,
    ConditionFilters,
    TanseeqFee,
    TanseeqCourses,
    Course,
    ApplicationDetails,
    AppliedPrograms,
)
from masters.models import UniversityDetails, YearDetails, StudyModeDetails
from tanseeq_app.forms.admin_forms import (
    TanseeqPeriodForm,
    UniversityDetailsForm,
    SecondarySchoolCertificateForm,
    UniversityAttachmentForm,
    StudyModeForm,
    TanseeqFacultyForm,
    TanseeqProgramForm,
    ConditionFiltersForm,
    TanseeqFeeForm,
    TanseeqCourseForm,
    CourseForm,
    TanseeqUserForm,
)
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http.request import QueryDict
from django.utils.decorators import method_decorator
from common.decorators import check_permissions
# Create your views here.


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class TanseeqAdminHome(TemplateView):
    template_name = 'tanseeq_admin/admin_home.html'


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class TanseeqPeriodListView(ListView):
    model = TanseeqPeriod
    template_name = 'tanseeq_admin/tanseeq_period_view.html'

    def get_queryset(self):
        if self.request.user.is_tanseeq_university_admin():
            return self.model.objects.filter(created_by=self.request.user)
        else:
            return self.model.objects.all()

@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class TanseeqPeriodView(View):
    model = TanseeqPeriod

    def get(self, request, pk=None):
        context = self.get_context()
        if request.user.is_tanseeq_university_admin():
            university_objs = UniversityDetails.objects.filter(id = request.user.university.id)
        else:
            university_objs = UniversityDetails.active_records()
        context["university_objs"] = university_objs
        context["is_edit"] = pk
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            context["instance"] = instance
            context["selected_universities"] = list(instance.universities.values_list('id',flat=True))
        return render(request, 'tanseeq_admin/add_tanseeq_period.html', context)

    @staticmethod
    def get_context():
        academic_year_objs = YearDetails.active_records()
        return {
            "academic_year_objs": academic_year_objs,
        }

    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk, created_by=request.user)
            form = TanseeqPeriodForm(request.POST, instance=instance)
        else:
            form = TanseeqPeriodForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not pk:
                obj.created_by = request.user
                messages.success(request, "Record saved.")
            else:
                messages.success(request, "Record Updated.")
            obj.save()
            form.save_m2m()
        else:
            context = self.get_context()
            if request.user.is_tanseeq_university_admin():
                university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
            else:
                university_objs = UniversityDetails.active_records()
            context["university_objs"] = university_objs
            context['form'] = form
            return render(request, 'tanseeq_admin/add_tanseeq_period.html', context)
        return redirect('tanseeq_app:list_tanseeq_period')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk, created_by=request.user)
        instance.delete()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class UniversityGuideList(ListView):
    model = UniversityDetails
    template_name = "tanseeq_admin/list_university_guide.html"
    fields = ["university_name", "file"]


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class UniversityGuideUpdateView(UpdateView):
    model = UniversityDetails
    template_name = "tanseeq_admin/add_university_guide.html"
    form_class = UniversityDetailsForm

    def post(self, request, *args, **kwargs):
        university_id = request.POST.get("university_id")
        instance = get_object_or_404(self.model, pk=university_id)
        form = self.form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class UniversityGuideDeleteView(DeleteView):
    model = UniversityDetails

    def post(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.file.delete()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class SecondarySchoolCertificateListView(ListView):
    model = SecondarySchoolCetificate
    template_name = 'tanseeq_admin/secondary_certificate_view.html'

    def get_queryset(self):
        if self.request.user.is_tanseeq_university_admin():
            return self.model.objects.filter(created_by=self.request.user)
        else:
            return self.model.objects.all()

    def post(self, request, pk=None):
        form = SecondarySchoolCertificateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            messages.success(request, "Record saved.")
            return redirect('tanseeq_app:list_secondary_certificate')
        else:
            messages.warning(request, "Record not saved.")
            return redirect('tanseeq_app:list_secondary_certificate')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk, created_by=request.user)
        instance.delete()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class SecondarySchoolCertificateUpdateView(UpdateView):
    model = SecondarySchoolCetificate
    template_name = "tanseeq_admin/secondary_certificate_view.html"
    form_class = SecondarySchoolCertificateForm

    def post(self, request, *args, **kwargs):
        school_certificate_id = request.POST.get("school_certificate_id")
        instance = get_object_or_404(self.model, pk=school_certificate_id)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class UniversityAttachmentList(ListView):
    model = UniversityAttachment
    template_name = "tanseeq_admin/list_university_attachment.html"

    def get_queryset(self):
        if self.request.user.is_tanseeq_university_admin():
            return self.model.objects.filter(created_by=self.request.user)
        else:
            return self.model.objects.all()

@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class UniversityAttachmentView(View):
    model = UniversityAttachment
    form_class = UniversityAttachmentForm
    template_name = "tanseeq_admin/add_university_attachment.html"
    def get(self, request, pk=None):
        if request.user.is_tanseeq_university_admin():
            university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
        else:
            university_objs = UniversityDetails.active_records()
        context = {
            "university_objs": university_objs,
            "form": self.form_class(),
        }
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            context["instance"] = instance
            context["selected_universities"] = list(instance.universities.values_list('id', flat=True))
            context["form"] = self.form_class(instance=get_object_or_404(self.model, pk=pk))

        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.created_by:
                obj.created_by = request.user
            obj.save()
            form.save_m2m()
            if pk:
                messages.success(request, "Record Updated.")
            else:
                messages.success(request, "Record saved.")
        else:
            if request.user.is_tanseeq_university_admin():
                university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
            else:
                university_objs = UniversityDetails.active_records()
            context = {
                "university_objs": university_objs,
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect('tanseeq_app:list_university_attachment')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return JsonResponse({"status": 200})


class StudyModeList(ListView):
    model = StudyModeDetails
    template_name = "tanseeq_admin/list_study_mode.html"

    def get(self, request, *args, **kwargs):
        if request.GET.get("type") == "JSON":
            queryset = self.get_queryset()
            data = serializers.serialize("json", queryset)
            return JsonResponse(data, status=200, safe=False)
        return super().get(args, kwargs)

    def get_queryset(self):
        university_id = self.request.GET.get("university")
        if university_id:
            return self.model.objects.filter(universities=university_id)
            return super().get_queryset()
        else:
            if self.request.user.is_tanseeq_university_admin():
                return self.model.objects.filter(created_by=self.request.user)
            else:
                return self.model.objects.all()

@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class StudyModeView(View):
    model = StudyModeDetails
    form_class = StudyModeForm

    def get(self, request, pk=None):
        if request.user.is_tanseeq_university_admin():
            university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
        else:
            university_objs = UniversityDetails.active_records()
        context = {
            "university_objs": university_objs,
            "form": self.form_class(),
        }
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            context["instance"] = instance
            context["form"] = self.form_class(instance=get_object_or_404(self.model, pk=pk))

        return render(request, "tanseeq_admin/add_study_mode.html", context)

    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()
            if pk:
                messages.success(request, "Record Updated.")
            else:
                messages.success(request, "Record saved.")
        else:
            if request.user.is_tanseeq_university_admin():
                university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
            else:
                university_objs = UniversityDetails.active_records()
            context = {
                "university_objs": university_objs,
                "form": form,
            }
            return render(request, 'tanseeq_admin/add_study_mode.html', context)
        return redirect('tanseeq_app:list_study_mode')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        messages.success(request, "Record removed.")
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class StudyModeView(View):
    model = StudyModeDetails
    form_class = StudyModeForm

    def get(self, request, pk=None):
        if request.user.is_tanseeq_university_admin():
            university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
        else:
            university_objs = UniversityDetails.active_records()
        context = {
            "university_objs": university_objs,
            "form": self.form_class(),
        }
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            context["instance"] = instance
            context["selected_universities"] = list(instance.universities.values_list('id', flat=True))
            context["form"] = self.form_class(instance=get_object_or_404(self.model, pk=pk))

        return render(request, "tanseeq_admin/add_study_mode.html", context)

    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.created_by:
                obj.created_by = request.user
            obj.save()
            form.save_m2m()
            if pk:
                messages.success(request, "Record Updated.")
            else:
                messages.success(request, "Record saved.")
        else:
            if request.user.is_tanseeq_university_admin():
                university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
            else:
                university_objs = UniversityDetails.active_records()
            context = {
                "university_objs": university_objs,
                "form": form,
            }
            return render(request, 'tanseeq_admin/add_study_mode.html', context)
        return redirect('tanseeq_app:list_study_mode')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return JsonResponse({"status": 200})


class TanseeqFacultyList(ListView):
    model = TanseeqFaculty
    template_name = "tanseeq_admin/list_tanseeq_faculty.html"

    def get(self, request, *args, **kwargs):
        if request.GET.get("type") == "JSON":
            queryset = self.get_queryset()
            data = serializers.serialize("json", queryset)
            return JsonResponse(data, status=200, safe=False)
        return super().get(args, kwargs)

    def get_queryset(self):
        university_id = self.request.GET.get("university")
        if university_id:
            return self.model.objects.filter(universities__id=university_id)
        else:
            if self.request.user.is_tanseeq_university_admin():
                return self.model.objects.filter(created_by=self.request.user)
            else:
                return self.model.objects.all()



@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class TanseeqFacultyView(View):
    model = TanseeqFaculty
    form_class = TanseeqFacultyForm
    template_name = "tanseeq_admin/add_tanseeq_faculty.html"

    def get(self, request, pk=None):
        if request.user.is_tanseeq_university_admin():
            university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
        else:
            university_objs = UniversityDetails.active_records()
        context = {
            "university_objs": university_objs,
            "form": self.form_class(),
        }
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            context["instance"] = instance
            context["selected_universities"] = list(instance.universities.values_list('id', flat=True))
            context["form"] = self.form_class(instance=get_object_or_404(self.model, pk=pk))
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.created_by:
                obj.created_by = request.user
            obj.save()
            form.save_m2m()
            if pk:
                messages.success(request, "Record Updated.")
            else:
                messages.success(request, "Record saved.")
        else:
            if request.user.is_tanseeq_university_admin():
                university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
            else:
                university_objs = UniversityDetails.active_records()
            context = {
                "university_objs": university_objs,
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect('tanseeq_app:list_tanseeq_faculty')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class TanseeqProgramList(ListView):
    model = TanseeqProgram
    template_name = "tanseeq_admin/list_tanseeq_program.html"

    def get(self, request, *args, **kwargs):
        if request.GET.get("type") == "JSON":
            queryset = self.get_queryset()
            data = serializers.serialize("json", queryset)
            return JsonResponse(data, status=200, safe=False)
        return super().get(args, kwargs)

    def get_queryset(self):
        faculty_id = self.request.GET.get("faculty")
        university_id =  self.request.GET.get("university")
        filters = {}
        if university_id:
            if university_id:
                filters["university_id"] = university_id
            if faculty_id:
                filters["faculty_id"] = faculty_id
            if self.request.GET.get("faculty[]"):
                filters["faculty_id__in"] = self.request.GET.getlist("faculty[]")
            return self.model.objects.filter(**filters)
        if self.request.user.is_tanseeq_university_admin():
            return self.model.objects.filter(created_by=self.request.user)
        else:
            return self.model.objects.all()



@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class TanseeqProgramView(View):
    model = TanseeqProgram
    form_class = TanseeqProgramForm
    template_name = "tanseeq_admin/add_tanseeq_program.html"

    def get(self, request, pk=None):
        faculties = []
        if request.user.is_tanseeq_university_admin():
            university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
        else:
            university_objs = UniversityDetails.active_records()
        context = {
            "university_objs": university_objs,
            "form": self.form_class(),
        }
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            if instance.university:
                faculties = TanseeqFaculty.objects.filter(universities__id=instance.university.id)
            context["faculties"] = faculties
            context["instance"] = instance
            context["form"] = self.form_class(instance=get_object_or_404(self.model, pk=pk))
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            # obj.faculty_id = form.data['faculty']
            if not obj.created_by:
                obj.created_by = request.user
            obj.save()
            form.save_m2m()
            if pk:
                messages.success(request, "Record Updated.")
            else:
                messages.success(request, "Record saved.")
        else:
            if request.user.is_tanseeq_university_admin():
                university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
            else:
                university_objs = UniversityDetails.active_records()
            context = {
                "university_objs": university_objs,
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect('tanseeq_app:list_tanseeq_program')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class ConditionFiltersList(ListView):
    model = ConditionFilters
    template_name = "tanseeq_admin/list_condition_filters.html"
    
    def get_queryset(self):
        filters = {
            "university_id": self.request.GET.get("university"),
            "faculty_id": self.request.GET.get("faculty"),
            "study_mode_id": self.request.GET.get("study_mode")
        }
        if (self.request.GET.get("university") is not None) or (self.request.GET.get("faculty") is not None) or (self.request.GET.get("study_mode") is not None):
            query_set = self.model.objects.filter(**{k: v for k, v in filters.items() if v })
            return query_set
        else:
            if self.request.user.is_tanseeq_university_admin():
                return self.model.objects.filter(created_by=self.request.user)
            else:
                return self.model.objects.all()

@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class ConditionsView(View):
    model = ConditionFilters
    form_class = ConditionFiltersForm
    template_name = "tanseeq_admin/add_condition_filters.html"
    redirect_url = 'tanseeq_app:list_tanseeq_filters'

    def get(self, request, pk=None):
        if request.user.is_tanseeq_university_admin():
            university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
        else:
            university_objs = UniversityDetails.active_records()
        context = {
            "university_objs": university_objs,
            "form": self.form_class(),
        }
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            context["instance"] = instance
            context["form"] = self.form_class(instance=get_object_or_404(self.model, pk=pk))
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        print("running context")
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.created_by:
                obj.created_by = request.user
            obj.save()
            form.save_m2m()
            if pk:
                messages.success(request, "Record Updated.")
            else:
                messages.success(request, "Record saved.")
        else:
            if request.user.is_tanseeq_university_admin():
                university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
            else:
                university_objs = UniversityDetails.active_records()
            context = {
                "university_objs": university_objs,
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect(self.redirect_url)

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return JsonResponse({"status": 200})


def get_universities(request):
    if request.user.is_tanseeq_university_admin():
        university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
    else:
        university_objs = UniversityDetails.active_records()
    data = serializers.serialize("json", university_objs)
    return JsonResponse(data,status=200, safe=False)


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class TanseeqFeeList(ListView):
    model = TanseeqFee
    template_name = "tanseeq_admin/list_tansseq_fees.html"

    def get_queryset(self):
        if self.request.user.is_tanseeq_university_admin():
            return self.model.objects.filter(created_by=self.request.user)
        else:
            return self.model.objects.all()

@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class TansseqFeeView(View):
    model = TanseeqFee
    form_class = TanseeqFeeForm
    template_name = "tanseeq_admin/add_tanseeq_fee.html"
    def get(self, request, pk=None):
        if request.user.is_tanseeq_university_admin():
            university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
        else:
            university_objs = UniversityDetails.active_records()
        context = {
            "university_objs": university_objs,
            "form": self.form_class(),
        }
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            context["instance"] = instance
            context["selected_universities"] = list(instance.universities.values_list('id', flat=True))
            context["form"] = self.form_class(instance=get_object_or_404(self.model, pk=pk))

        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.created_by:
                obj.created_by = request.user
            obj.save()
            form.save_m2m()
            if pk:
                messages.success(request, "Record Updated.")
            else:
                messages.success(request, "Record saved.")
        else:
            if request.user.is_tanseeq_university_admin():
                university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
            else:
                university_objs = UniversityDetails.active_records()
            context = {
                "university_objs": university_objs,
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect('tanseeq_app:list_tanseeq_fees')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class TanseeqCourseListView(ListView):
    model = TanseeqCourses
    template_name = 'tanseeq_admin/list_tanseeq_courses.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(created_by=self.request.user)
        return queryset

    def post(self, request, pk=None):
        form = TanseeqCourseForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            messages.success(request, "Record saved.")
            return redirect('tanseeq_app:list_tanseeq_courses')
        else:
            context = {
                "form": form,
            }
            return render(request, 'tanseeq_admin/list_tanseeq_courses.html', context)

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk, created_by=request.user)
        instance.delete()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class TanseeqCourseUpdateView(UpdateView):
    model = TanseeqCourses
    template_name = "tanseeq_admin/list_tanseeq_courses.html"
    form_class = TanseeqCourseForm

    def post(self, request, *args, **kwargs):
        tanseeq_course_id = request.POST.get("tanseeq_course_id")
        instance = get_object_or_404(self.model, pk=tanseeq_course_id)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class CourseListView(View):
    model = Course
    form_class = CourseForm
    def get(self, request, pk=None):
        courses_obj = TanseeqCourses.objects.get(id = pk).courses.all()
        context = {
            "courses_obj": courses_obj,
            "form": self.form_class(),
            "tanseeq_course_id": pk,
        }
        return render(request, "tanseeq_admin/list_courses.html", context)

    def post(self, request, pk=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            tanseeq_course_obj = TanseeqCourses.objects.get(id=pk)
            course_obj = Course.objects.create(course=form.data['course'], mark=form.data['mark'])
            tanseeq_course_obj.courses.add(course_obj)
            messages.success(request, "Record saved.")
            return redirect('/tanseeq/course/' + str(pk))
        else:
            courses_obj = TanseeqCourses.objects.get(id=pk).courses.all()
            context = {
                "courses_obj": courses_obj,
                "form": form,
            }
            return render(request, 'tanseeq_admin/list_courses.html', context)

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    template_name = "tanseeq_admin/list_courses.html"
    form_class = CourseForm

    def post(self, request, *args, **kwargs):
        course_id = request.POST.get("course_id")
        instance = get_object_or_404(self.model, pk=course_id)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class ListAppliedApplicants(ListView):
    model = ApplicationDetails
    template_name = "tanseeq_admin/list_applied_applicants.html"

    def get_queryset(self):
        if self.request.user.is_tanseeq_university_admin():
            return self.model.objects.filter(created_by=self.request.user)
        else:
            return self.model.objects.all()

@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class ListUsers(ListView):
    model = User
    template_name = "tanseeq_admin/list_users.html"
    context_object_name = "user_recs"
    crumbs = [
        {"title": "Home", "url": "/"},
        {"title": "Users", "url": "tanseeq_app:list_tanseeq_users"},
    ]

    def get_queryset(self):
        if self.request.user.is_tanseeq_university_admin():
            return User.objects.filter(created_by=self.request.user)
        else:
            return User.objects.filter(tanseeq_role__name__in = [
                User.TANSEEQ_FINANCE, User.TANSEEQ_REVIEWER,
                User.TANSEEQ_EXAMINER, User.TANSEEQ_FACULTY,User.TANSEEQ_UNIVERSITY_ADMIN,User.TANSEEQ_APPLICATION_ENTRY
        ])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["crumbs"] = self.crumbs
        return context


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class ManageUsers(View):
    model = User
    template_name = "tanseeq_admin/add_user.html"
    form_class = TanseeqUserForm
    redirect_url = "tanseeq_app:list_tanseeq_users"
    crumbs = [
        {"title": "Home", "url": "/"},
        {"title": "Users", "url": redirect_url},
        {"title": "Manage User"},
    ]
    def get_context_data(self, pk):
        if pk:
            user = self.model.objects.filter(id=pk, created_by=self.request.user).first()
            form = self.form_class(instance=user)
        else:
            form = self.form_class()
        return {"form": form, "crumbs": self.crumbs}

    def get(self, request, pk=None):
        context = self.get_context_data(pk)
        return render(request, self.template_name, context)
    
    def post(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.model, pk=pk, created_by=request.user)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            if form.cleaned_data["password1"]:
                obj.set_password(form.cleaned_data["password1"])


            if pk:
                messages.success(request, "Record Updated.")
            else:
                obj.created_by = request.user
                obj.username = obj.email
                messages.success(request, "Record saved.")
            # obj.role.add(UserRole.objects.get(id=form.data['tanseeq_role']))
            obj.save()
            obj.role.add(UserRole.objects.get(id=form.data['tanseeq_role']))
            form.save_m2m()
        else:
            context = {
                "form": form,
                "crumbs": self.crumbs,
            }
            return render(request, self.template_name, context)
        return redirect(self.redirect_url)


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class ManageApplicationStatus(View):
    model = ApplicationDetails

    def patch(self, request, pk):
        data = QueryDict(request.body)
        status = data.get("status")
        if not status:
            return JsonResponse({"msg": "Application status is required."}, status=304)
        obj = self.model.objects.filter(pk=pk)
        if not obj:
            return JsonResponse({}, status=404)
        obj.update(application_status=status)
        return JsonResponse({}, status=200)

@method_decorator(check_permissions(User.TANSEEQ_UNIVERSITY_ADMIN), name='dispatch')
class TanseeqUniversityAdminHome(TemplateView):
    template_name = 'tanseeq_university_admin/university_admin_home.html'


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class ListFinanceApplications(ListView):
    model = AppliedPrograms
    template_name = "tanseeq_admin/list_finance_applications.html"
    finance_users = User.objects.filter(tanseeq_role__name__in=[User.TANSEEQ_FINANCE])
    def get_queryset(self):
        accountant = self.request.GET.get("accountant")
        filters = {}
        if accountant:
            filters["created_by_id"] = accountant
        query_set = self.model.objects.filter(bond_no__isnull=False, is_denied=False, **filters)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["finance_user_list"] = self.finance_users
        return context

@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class ListApplicantsReports(ListView):
    model = AppliedPrograms
    template_name = "tanseeq_admin/list_applicants_reporst.html"

    def get_queryset(self):
        university = self.request.GET.get("university")
        faculty = self.request.GET.get("faculty")
        study_mode = self.request.GET.get("study_mode")
        program = self.request.GET.get("program")
        from_date = self.request.GET.get("from_date")
        to_date = self.request.GET.get("to_date")
        filters = {}
        if university:
            filters["program_details__university_id"] = university
        if faculty:
            filters["program_details__faculty_id"] = faculty
        if study_mode:
            filters["program_details__study_mode_id"] = study_mode
        if program:
            filters["program_details__program_id"] = program
        if from_date and to_date:
            filters["created_on__range"] = [from_date, to_date]
        query_set = self.model.objects.filter(bond_no__isnull=False, is_denied=False, **filters)
        return query_set



def upload_excel(request):
    if request.method == 'POST':
        try:
            # 1st script
            # file_recs = request.FILES['excel'].get_records()
            # for file_rec in file_recs:
            #     if not UniversityDetails.objects.filter(university_code=file_rec['University Code']):
            #         UniversityDetails.objects.create(university_code=file_rec['University Code'],
            #                                          university_name=file_rec['University Name'],
            #                                          university_type_id=1,
            #                                          type_id=1,
            #                                          is_tanseeq_university=True)
            # 2nd Script
            # file_recs = request.FILES['excel'].get_records()
            # for file_rec in file_recs:
            #     if file_rec['University Code'] == 1:
            #         if not TanseeqFaculty.objects.filter(code=file_rec['Facult Code'], name = file_rec['Faculty Name']):
            #             university_obj = UniversityDetails.objects.get(university_code=file_rec['University Code'])
            #             faculty_obj = TanseeqFaculty.objects.create(
            #                 name=file_rec['Faculty Name'],code = file_rec['Facult Code']
            #
            #                 )
            #             faculty_obj.universities.add(university_obj)
            #
            #     elif file_rec['University Code'] == 2:
            #         if not TanseeqFaculty.objects.filter(code=file_rec['Facult Code'], name = file_rec['Faculty Name']):
            #             university_obj = UniversityDetails.objects.get(university_code=file_rec['University Code'])
            #             faculty_obj = TanseeqFaculty.objects.create(
            #                 name=file_rec['Faculty Name'], code=file_rec['Facult Code']
            #
            #             )
            #             faculty_obj.universities.add(university_obj)
            #     elif file_rec['University Code'] == 3:
            #         if not TanseeqFaculty.objects.filter(code=file_rec['Facult Code'], name = file_rec['Faculty Name']):
            #             university_obj = UniversityDetails.objects.get(university_code=file_rec['University Code'])
            #             faculty_obj = TanseeqFaculty.objects.create(
            #                 name=file_rec['Faculty Name'], code=file_rec['Facult Code']
            #
            #             )
            #             faculty_obj.universities.add(university_obj)
            #     elif file_rec['University Code'] == 4:
            #         if not TanseeqFaculty.objects.filter(code=file_rec['Facult Code'], name=file_rec['Faculty Name']):
            #             university_obj = UniversityDetails.objects.get(university_code=file_rec['University Code'])
            #             faculty_obj = TanseeqFaculty.objects.create(
            #                 name=file_rec['Faculty Name'], code=file_rec['Facult Code']
            #
            #             )
            #             faculty_obj.universities.add(university_obj)
            #     elif file_rec['University Code'] == 5:
            #         if not TanseeqFaculty.objects.filter(code=file_rec['Facult Code'], name = file_rec['Faculty Name']):
            #             university_obj = UniversityDetails.objects.get(university_code=file_rec['University Code'])
            #             faculty_obj = TanseeqFaculty.objects.create(
            #                 name=file_rec['Faculty Name'], code=file_rec['Facult Code']
            #
            #             )
            #             faculty_obj.universities.add(university_obj)
            #     elif file_rec['University Code'] == 6:
            #         if not TanseeqFaculty.objects.filter(code=file_rec['Facult Code'], name = file_rec['Faculty Name']):
            #             university_obj = UniversityDetails.objects.get(university_code=file_rec['University Code'])
            #             faculty_obj = TanseeqFaculty.objects.create(
            #                 name=file_rec['Faculty Name'], code=file_rec['Facult Code']
            #
            #             )
            #             faculty_obj.universities.add(university_obj)
            # 3rdt script
            # file_recs = request.FILES['excel'].get_records()
            # for file_rec in file_recs:
            #     university_obj = UniversityDetails.objects.get(university_code=file_rec['University Code'])
            #     faculty_obj = TanseeqFaculty.objects.filter(name=file_rec['Faculty Name']).first()
            #     TanseeqProgram.objects.create(university_id=university_obj.id,
            #                                      faculty_id=faculty_obj.id,
            #                                      name=file_rec['Program Name'],
            #                                      code=file_rec['Program Code'],
            #                                   )
            messages.success(request, "Record saved")
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))
        return redirect('/tanseeq/upload_excel/')
    else:
        return render(request, 'tanseeq_admin/upload_university_template.html')