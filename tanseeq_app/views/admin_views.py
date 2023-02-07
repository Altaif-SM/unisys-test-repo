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
    ExamDetails,
    TanseeqFee,
    TanseeqCourses,
    ApplicationDetails,
    AppliedPrograms,
    TanseeqStudyMode,
    SecondaryCertificateInfo,
)
from masters.models import UniversityDetails, YearDetails, StudyModeDetails, CountryDetails, CitiDetails
from tanseeq_app.forms.admin_forms import (
    TanseeqPeriodForm,
    UniversityDetailsForm,
    SecondarySchoolCertificateForm,
    UniversityAttachmentForm,
    StudyModeForm,
    TanseeqFacultyForm,
    TanseeqProgramForm,
    ConditionFiltersForm,
    ComparisonExamForm,
    TanseeqFeeForm,
    TanseeqCourseForm,
    TanseeqUserForm,
    TanseeqStudyModeForm,
)
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http.request import QueryDict
from django.utils.decorators import method_decorator
from common.decorators import check_permissions
import json
from django.contrib.auth.hashers import make_password
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Value as V, Q
from django.core.paginator import Paginator
from django.utils.html import escape
from datetime import datetime
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
class TanseeqStudyModeListView(ListView):
    model = TanseeqStudyMode
    template_name = 'tanseeq_admin/list_tanseeq_study_mode.html'

    def get_queryset(self):
        if self.request.user.is_tanseeq_university_admin():
            return self.model.objects.filter(created_by=self.request.user)
        else:
            return self.model.objects.all()

    def post(self, request, pk=None):
        form = TanseeqStudyModeForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            messages.success(request, "Record saved.")
            return redirect('tanseeq_app:list_tanseeq_study_mode')
        else:
            messages.warning(request, "Record not saved.")
            return redirect('tanseeq_app:list_tanseeq_study_mode')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk, created_by=request.user)
        instance.delete()
        return JsonResponse({"status": 200})


@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class TanseeqStudyModeUpdateView(UpdateView):
    model = TanseeqStudyMode
    template_name = "tanseeq_admin/secondary_certificate_view.html"
    form_class = TanseeqStudyModeForm

    def post(self, request, *args, **kwargs):
        study_mode_id = request.POST.get("study_mode_id")
        instance = get_object_or_404(self.model, pk=study_mode_id)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
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
            finalDict = []
            queryset = self.get_queryset()
            data = serializers.serialize("json", queryset)
            # return JsonResponse(data, status=200, safe=False)
            for rec in queryset:
                raw_dict = {}
                if rec.study_mode:
                    raw_dict['study_mode'] = rec.study_mode.study_mode
                    raw_dict['id'] = rec.id
                    finalDict.append(raw_dict)
            return JsonResponse(finalDict, status=200, safe=False)

        return super().get(args, kwargs)

    def get_queryset(self):
        university_id = self.request.GET.get("university")
        if university_id:
            return self.model.objects.filter(universities=university_id)
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
        tanseeq_study_modes = TanseeqStudyMode.objects.all()
        if request.user.is_tanseeq_university_admin():
            university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
        else:
            university_objs = UniversityDetails.active_records()
        context = {
            "university_objs": university_objs,
            "tanseeq_study_modes": tanseeq_study_modes,
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
            tanseeq_study_modes = TanseeqStudyMode.objects.all()
            if request.user.is_tanseeq_university_admin():
                university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
            else:
                university_objs = UniversityDetails.active_records()
            context = {
                "university_objs": university_objs,
                "tanseeq_study_modes": tanseeq_study_modes,
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
        tanseeq_study_modes = TanseeqStudyMode.objects.all()
        if request.user.is_tanseeq_university_admin():
            university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
        else:
            university_objs = UniversityDetails.active_records()
        context = {
            "university_objs": university_objs,
            "tanseeq_study_modes": tanseeq_study_modes,
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
            tanseeq_study_modes = TanseeqStudyMode.objects.all()
            if request.user.is_tanseeq_university_admin():
                university_objs = UniversityDetails.objects.filter(id=request.user.university.id)
            else:
                university_objs = UniversityDetails.active_records()
            context = {
                "university_objs": university_objs,
                "tanseeq_study_modes": tanseeq_study_modes,
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
        filters = {}
        if university_id:
            filters["universities__id"] = university_id
        if self.request.GET.get("university[]"):
            filters["universities__id__in"] = self.request.GET.getlist("university[]")
        return self.model.objects.filter(**filters)



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
class ExamResultList(ListView):
    model = AppliedPrograms
    template_name = "tanseeq_admin/list_exam_result.html"

    def get_queryset(self):
        university = self.request.GET.get("university")
        filter_by_status = self.request.GET.get("filter_by_status")
        filters = {}
        if university:
            filters["program_details__university_id"] = university
        if filter_by_status:
            filters["review_status"] = filter_by_status if filter_by_status in ["0", "1"] else None

        query_set = self.model.objects.filter(review_status = 1, **filters)
        return query_set

@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class ComparisonExamList(ListView):
    model = ExamDetails
    template_name = "tanseeq_admin/list_comparsion_exam.html"

    def get_queryset(self):
        filters = {
            "university_id": self.request.GET.get("university"),
            "faculty_id": self.request.GET.get("faculty"),
            "study_mode_id": self.request.GET.get("study_mode"),
            "subject_id": self.request.GET.get("subject")
        }
        if (self.request.GET.get("university") is not None) or (self.request.GET.get("faculty") is not None) or (
                self.request.GET.get("study_mode") is not None) or (
                self.request.GET.get("subject") is not None):
            query_set = self.model.objects.filter(**{k: v for k, v in filters.items() if v})
            return query_set
        else:
            if self.request.user.is_tanseeq_university_admin():
                return self.model.objects.filter(created_by=self.request.user)
            else:
                return self.model.objects.all()

def add_exam_marks(request):
    try:
        exam_data = json.loads(request.POST.get('exam_data'))
        action_type = request.POST.get('action_type')
        for rec in exam_data:
            exam_obj = AppliedPrograms.objects.get(id=rec['exam_id'])
            if action_type == 'Submitted':
                exam_obj.mark = rec['exam_mark'] if rec['exam_mark'] else None
                exam_obj.save()
        messages.success(request, "Record Updated.")
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('tanseeq_app:list_exam_result')

@method_decorator(check_permissions(User.TANSEEQ_ADMIN), name='dispatch')
class ComparisonExamView(View):
    model = ExamDetails
    form_class = ComparisonExamForm
    template_name = "tanseeq_admin/add_comparison_exam.html"
    redirect_url = 'tanseeq_app:list_comparison_exam'

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

def get_subjects(request):
    subject_objs = TanseeqCourses.objects.all()
    data = serializers.serialize("json", subject_objs)
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
            context["selected_faculties"] = TanseeqFaculty.objects.filter(universities__id__in = context["selected_universities"])
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
class ListAppliedApplicants(ListView):
    model = ApplicationDetails
    template_name = "tanseeq_admin/list_applied_applicants.html"

    def get_queryset(self):
        if self.request.user.is_tanseeq_university_admin():
            return self.model.objects.filter(created_by=self.request.user)
        else:
            applicant_recs = self.model.objects.all()
            paginator = Paginator(applicant_recs, 10)
            page = self.request.GET.get('page')
            return paginator.get_page(page)
            # return self.model.objects.all()[:10]

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
class ManagePasswordReset(View):
    model = User

    def patch(self, request, pk):
        obj = self.model.objects.get(id = pk)
        obj.set_password('000000')
        obj.save()
        return JsonResponse({}, status=200)

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
        if self.request.user.is_tanseeq_university_admin():
            filters["program_details__university_id"] = self.request.user.university.id
        else:
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

def reviewer_reports_view(request):
    try:
        university = request.GET.get("university")
        study_mode = request.GET.get("study_mode")
        filters = {}
        if request.user.is_tanseeq_university_admin():
            filters["program_details__university_id"] = request.user.university.id
        else:
            if university:
                filters["program_details__university_id"] = university
        if study_mode:
            filters["program_details__study_mode_id"] = study_mode
        query_set = AppliedPrograms.objects.filter(bond_no__isnull=False, is_denied=False, **filters)
        reviewer_list = []
        reviewer_users =  User.objects.filter(tanseeq_role__name__in=[User.TANSEEQ_REVIEWER])
        for reviewer_obj in reviewer_users:
            reviewer_dict = {}
            reviewer_dict['reviewer'] = reviewer_obj
            reviewer_dict['reviewed_applications'] = query_set.filter(created_by = reviewer_obj).count()
            reviewer_dict['approved_applications'] = query_set.filter(created_by = reviewer_obj,review_status = 1).count()
            reviewer_dict['rejected_applications'] = query_set.filter(created_by = reviewer_obj,review_status = 0).count()
            reviewer_list.append(reviewer_dict)
        context = {
            'reviewer_list':reviewer_list,
        }
        return render(request, 'tanseeq_admin/list_reviewer_reports.html',context)
    except Exception as e:
        return redirect('/tanseeq_app/reviewer_reports/')


def upload_excel(request):
    if request.method == 'POST':
        try:
            #1st script
            # file_recs = request.FILES['excel'].get_records()
            # uni_count = 0
            # for file_rec in file_recs:
            #     if not UniversityDetails.objects.filter(university_code=file_rec['University Code']):
            #         UniversityDetails.objects.create(university_code=file_rec['University Code'],
            #                                          university_name=file_rec['University Name'],
            #                                          is_tanseeq_university=True)
            #         uni_count = uni_count + 1
            #
            # print("uni_count>>>>>>>>"+str(uni_count))

            # 4th script country
            # file_recs = request.FILES['excel'].get_records()
            # uni_count = 0
            # for file_rec in file_recs:
            #     CountryDetails.objects.create(
            #                                   country_name=file_rec['country'],
            #                                   country_code=file_rec['id'],
            #                                     is_tanseeq_country = True
            #                                   )
            #     uni_count = uni_count + 1
            # print("uni_count>>>>>>>>" + str(uni_count))
            # messages.success(request, "Record saved")

            # 5th script city
            # file_recs = request.FILES['excel'].get_records()
            # uni_count = 0
            # for file_rec in file_recs:
            #     country_obj = CountryDetails.objects.get(country_code=file_rec['country'])
            #     city_obj = CitiDetails.objects.create(city=file_rec['name'])
            #     country_obj.city.add(city_obj)
            #     uni_count = uni_count + 1
            # print("uni_count>>>>>>>>" + str(uni_count))

            # 6th Secondary Certificate script
            # file_recs = request.FILES['excel'].get_records()
            # certificate_count = 0
            # for file_rec in file_recs:
            #     if not SecondarySchoolCetificate.objects.filter(school_certificate=file_rec['secondary certificate']):
            #         SecondarySchoolCetificate.objects.create(school_certificate=file_rec['secondary certificate'],created_by=request.user)
            #         certificate_count = certificate_count + 1
            # print("certificate_count>>>>>>>>" + str(certificate_count))

            # # 5th Study mode script
            # file_recs = request.FILES['excel'].get_records()
            # uni_count = 0
            # for file_rec in file_recs:
            #     if not TanseeqStudyMode.objects.filter(study_mode=file_rec['study mode']):
            #         tanseeq_study_mode_obj = TanseeqStudyMode.objects.create(study_mode=file_rec['study mode'], created_by=request.user)
            #         study_mode_obj = StudyModeDetails.objects.create(study_mode_id=tanseeq_study_mode_obj.id,)
            #         university_obj = UniversityDetails.objects.get(university_name= 'جامعة تعز')
            #         study_mode_obj.universities.add(university_obj)
            #         uni_count = uni_count + 1
            # print("study_mode_count>>>>>>>>" + str(uni_count))


            #2nd Script
            # file_recs = request.FILES['excel'].get_records()
            # uni_count = 0
            # for file_rec in file_recs:
            #     university_obj = UniversityDetails.objects.get(university_name='جامعة تعز')
            #     if not TanseeqFaculty.objects.filter(name = file_rec['faculty name'],universities__id = university_obj.id):
            #         faculty_obj = TanseeqFaculty.objects.create(
            #             name=file_rec['faculty name']
            #
            #             )
            #         faculty_obj.universities.add(university_obj)
            #         uni_count = uni_count + 1
            # print("uni_count>>>>>>>>" + str(uni_count))

            # #3rdt script
            # file_recs = request.FILES['excel'].get_records()
            # uni_count = 0
            # program_list = []
            # for file_rec in file_recs:
            #     university_obj = UniversityDetails.objects.get(university_name='جامعة تعز')
            #     faculty_obj = TanseeqFaculty.objects.filter(name=file_rec['faculty name']).first()
            #     if not TanseeqProgram.objects.filter(university_id=university_obj.id, faculty_id=faculty_obj.id,name=file_rec['name']):
            #         TanseeqProgram.objects.create(university_id=university_obj.id,
            #                                          faculty_id=faculty_obj.id,
            #                                          name=file_rec['name'],
            #                                       )
            #         uni_count = uni_count + 1
            #     else:
            #         program_list.append(file_rec['name'])
            # print("uni_count>>>>>>>>" + str(uni_count))
            # print("program_list>>>>>>>>" + str(program_list))





            # 7th Condition Script
            # file_recs = request.FILES['excel'].get_records()
            # faculty_name_list = []
            # certificate_count = 0
            # for file_rec in file_recs:
            #     university_obj = UniversityDetails.objects.get(university_name='جامعة تعز')
            #     # if TanseeqFaculty.objects.filter(name = file_rec['faculty name'],universities__id = university_obj.id).exists():
            #     #     pass
            #     # else:
            #     #     faculty_name_list.append(file_rec['faculty name'])
            #     # certificate_count = certificate_count + 1
            #     faculty_obj = TanseeqFaculty.objects.get(name = file_rec['faculty name'],universities__id = university_obj.id)
            #     if TanseeqProgram.objects.filter(university_id = university_obj.id,faculty_id = faculty_obj.id, name = file_rec['name']).exists():
            #         certificate_count = certificate_count + 1
            #     else:
            #         faculty_name_list.append(file_rec['name'])
            # print("faculty name>>>>>>>>" + str(certificate_count))
            # print("faculty_name_list>>>>>>>>" + str(faculty_name_list))

            # #7th Condition Script
            # certificate_count = 0
            # start_year = 1984
            # for rec in range(1, 41):
            #     start_date = str(start_year) + '-' + '01' '-' + '01'
            #     end_date = str(start_year) + '-' + '12' '-' + '31'
            #     year_obj = YearDetails.objects.create(year_name=str(start_year), start_date=start_date, end_date=end_date,
            #                                           is_tanseeq_year=True)
            #     start_year = int(start_year) + 1
            #     year_obj.created_by = request.user
            #     year_obj.save()
            # print("Success")

            # 7th Condition Script
            # file_recs = request.FILES['excel'].get_records()
            # certificate_count = 0
            # university_obj = UniversityDetails.objects.get(university_name='جامعة تعز')
            # for file_rec in file_recs:
            #     is_exam = False
            #     isAdmissionExam = int(file_rec['isAdmissionExam'])
            #     if isAdmissionExam == 1:
            #         is_exam = True
            #     academic_year = YearDetails.objects.get(year_name=file_rec['lastSecondaryYear'])
            #     school_certificate_obj = SecondarySchoolCetificate.objects.filter(school_certificate = file_rec['secondary certificate']).first()
            #     mode_obj = TanseeqStudyMode.objects.filter(study_mode = file_rec['study mode']).first()
            #     study_mode_obj = StudyModeDetails.objects.filter(study_mode_id = mode_obj.id, universities__id = university_obj.id).first()
            #     faculty_obj = TanseeqFaculty.objects.filter(name = file_rec['faculty name'], universities__id = university_obj.id).first()
            #     program_obj = TanseeqProgram.objects.filter(faculty_id = faculty_obj.id, university_id = university_obj.id, name = file_rec['name']).first()
            #     condition_obj = ConditionFilters.objects.create(university_id = university_obj.id, study_mode_id = study_mode_obj.id,faculty_id = faculty_obj.id,program_id = program_obj.id,type_of_secondary_id = school_certificate_obj.id,average = float(file_rec['precentage']),capacity = int(file_rec['capacity']),is_exam = is_exam,academic_year = academic_year,start_date = str(file_rec['openDate']), end_date = str(file_rec['closeDate']),fee = float(0))
            #     condition_obj.created_by = request.user
            #     condition_obj.save()
            #     certificate_count = certificate_count + 1
            # print("Success>>>>>>>>")

            # Applicant details Script
            # redirect_flag = False
            # try:
            #     applicant_count = 0
            #     seat_no_count = 0
            #     seat_no_exist_list = []
            #     file_recs = request.FILES['excel'].get_records()
            #     for file_rec in file_recs:
            #         if not User.objects.filter(username__iexact=file_rec['Seat No']).exists():
            #             try:
            #                 nationality_obj = CountryDetails.objects.get(id=file_rec['Nationality'])
            #             except Exception as e:
            #                 messages.warning(request,"Nationality Not Found" + "for applicant" + str(file_rec['Seat No']))
            #                 continue
            #             try:
            #                 country_obj = CountryDetails.objects.get(id=file_rec['Country'])
            #             except Exception as e:
            #                 messages.warning(request, "Country Not Found" + "for applicant" + str(file_rec['Seat No']))
            #                 continue
            #             try:
            #                 city_obj = CitiDetails.objects.get(id=file_rec['City'])
            #             except Exception as e:
            #                 messages.warning(request, "City Not Found" + "for applicant" + str(file_rec['Seat No']))
            #                 continue
            #             try:
            #                 certificate_obj = SecondarySchoolCetificate.objects.get(school_certificate=file_rec['Secondary Certificate'])
            #             except Exception as e:
            #                 messages.warning(request, "City Not Found" + "for applicant" + str(file_rec['Seat No']))
            #                 continue
            #             try:
            #                 academicyear_obj = YearDetails.objects.get(year_name=file_rec['Graduatation Year'])
            #             except Exception as e:
            #                 messages.warning(request,"Year Details Not Found" + "for applicant" + str(file_rec['Seat No']))
            #                 continue
            #             try:
            #                 school_country_obj = CountryDetails.objects.get(id=file_rec['School country'])
            #             except Exception as e:
            #                 messages.warning(request, "School Country Not Found" + "for applicant" + str(file_rec['Seat No']))
            #                 continue
            #             try:
            #                 school_city_obj = CitiDetails.objects.get(id=file_rec['School City'])
            #             except Exception as e:
            #                 messages.warning(request, "School City Not Found" + "for applicant" + str(file_rec['Seat No']))
            #                 continue
            #             try:
            #                 university_obj = UniversityDetails.objects.get(university_name='جامعة تعز')
            #                 mode_obj = TanseeqStudyMode.objects.filter(study_mode=file_rec['Study mode']).first()
            #                 study_mode_obj = StudyModeDetails.objects.filter(study_mode_id = mode_obj.id, universities__id = university_obj.id).first()
            #             except Exception as e:
            #                 messages.warning(request, "Study mode Not Found" + "for applicant" + str(file_rec['Seat No']))
            #                 continue
            #
            #             user = User.objects.create(first_name=file_rec['First Name'],
            #                                        username=file_rec['Seat No'], email=file_rec['Email'],
            #                                        password=make_password(file_rec['Seat No']), is_active=True,
            #                                        )
            #             user.role.add(UserRole.objects.get(name='Tanseeq Student'))
            #             role_obj = UserRole.objects.get(name= 'Tanseeq Student')
            #             user.tanseeq_role_id = role_obj.id
            #             user.save()
            #             application_obj = ApplicationDetails.objects.create(first_name=file_rec['First Name'],
            #                                                                 tanseeq_id = file_rec['regNo'],
            #                                                                 applicant_id = str(file_rec['applicantId']),
            #                                                                 gender_type = file_rec['Gender Type'],
            #                                                                 nationality_id = nationality_obj.id,
            #                                                                 birth_date = str(file_rec['Birth Date']),
            #                                                                 country_id = country_obj.id,
            #                                                                 city_id = city_obj.id,
            #                                                                 district = file_rec['District'],
            #                                                                 address = file_rec['Address'],
            #                                                                 user = user,
            #                                                                 created_by = user,
            #                                                                 contact_number = str(file_rec['Contact Number']),
            #                                                                 )
            #             SecondaryCertificateInfo.objects.create(secondary_certificate_id=certificate_obj.id,
            #                                                     school_name = file_rec['School Name'],
            #                                                     academic_year_id = academicyear_obj.id,
            #                                                     seat_number = str(file_rec['Seat No']),
            #                                                     average = float(file_rec['Average']),
            #                                                     country_id = school_country_obj.id,
            #                                                     city_id = school_city_obj.id,
            #                                                     application = application_obj,
            #                                                     created_by = user,
            #                                                     district = str(file_rec['School District']) if str(file_rec['School District']) else ''
            #                                                     )
            #             application_obj.application_status = 'Submitted'
            #             application_obj.save()
            #             applicant_count = applicant_count + 1
            #             print("applicant_count>>>>>>>"+str(applicant_count))
            #             redirect_flag = True
            #         else:
            #             seat_no_count = seat_no_count + 1
            #             seat_no_exist_list.append(str(file_rec['Seat No']))
            #             messages.warning(request, "Seat No already exists" + str(file_rec['Seat No']))
            #             continue
            #     print("seat_no_count>>>>>>>"+str(seat_no_count))
            #     print("seat_no_exist_list>>>>>>>"+str(seat_no_exist_list))
            #     if redirect_flag:
            #         messages.success(request, "Record saved>>>>>>>>")
            #         return redirect('tanseeq_app:list_tanseeq_study_mode')
            # except Exception as e:
            #     messages.warning(request, "Form have some error" + str(e))
            # return redirect('/tanseeq/upload_excel/')
            pass
        except Exception as e:
            print("Error>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            messages.warning(request, "Form have some error" + str(e))
        return redirect('/tanseeq/upload_excel/')
    else:
        return render(request, 'tanseeq_admin/upload_university_template.html')

class ApplicantFilterList(BaseDatatableView):
    model = ApplicationDetails
    columns = ['id','created_on','tanseeq_id', 'first_name','created_by','application_status','is_active']
    order_columns = []
    max_display_length = 100

    def get_initial_queryset(self):
        if self.request.user.is_tanseeq_university_admin():
            return self.model.objects.filter(created_by=self.request.user)
        else:
            return ApplicationDetails.objects.all()

    def render_column(self, row, column):
        return super(ApplicantFilterList, self).render_column(row, column)

    def render_column(self, row, column):
        if column == 'first_name':
            first_name = row.first_name if row.first_name else ""
            last_name = row.last_name if row.last_name else ""
            return escape('{0} {1}'.format(first_name, last_name))
        elif column == 'created_on':
            try:
                return escape('{0}'.format(str(row.created_on.date())))
            except:
                return ""
        elif column == 'created_by':
            try:
                if row.created_by.tanseeq_role.name == 'Tanseeq Admin':
                    return escape('{0}'.format(str('Tanseeq Admin')))
                else:
                    first_name = row.created_by.first_name if row.created_by else ""
                    last_name = row.created_by.last_name if row.created_by.last_name else ""
                    return escape('{0} {1}'.format(first_name, last_name))
            except:
                return ""
        else:
            return super(ApplicantFilterList, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            q = Q(tanseeq_id__istartswith=search)
            qs = qs.filter(q)
        return qs