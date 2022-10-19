from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, ListView, UpdateView, DeleteView
from tanseeq_app.models import (
    TanseeqPeriod,
    SecondarySchoolCetificate,
    UniversityAttachment,
    TanseeqFaculty,
    TanseeqProgram,
    TanseeqFee,
    TanseeqCourses,
    Course,
)
from masters.models import UniversityDetails, YearDetails, StudyModeDetails
from tanseeq_app.forms import (
    TanseeqPeriodForm,
    UniversityDetailsForm,
    SecondarySchoolCertificateForm,
    UniversityAttachmentForm,
    StudyModeForm,
    TanseeqFacultyForm,
    TanseeqProgramForm,
    TanseeqFeeForm,
    TanseeqCourseForm,
    CourseForm,
)
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.


class TanseeqAdminHome(TemplateView):
    template_name = 'tanseeq_admin/admin_home.html'

class TanseeqPeriodListView(ListView):
    model = TanseeqPeriod
    template_name = 'tanseeq_admin/tanseeq_period_view.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(created_by=self.request.user)
        return queryset


class TanseeqPeriodView(View):
    model = TanseeqPeriod

    def get(self, request, pk=None):
        context = self.get_context()
        context["is_edit"] = pk
        if pk:
            instance = get_object_or_404(self.model, pk=pk)
            context["instance"] = instance
            context["selected_universities"] = list(instance.universities.values_list('id',flat=True))
        return render(request, 'tanseeq_admin/add_tanseeq_period.html', context)

    @staticmethod
    def get_context():
        university_objs = UniversityDetails.active_records()
        academic_year_objs = YearDetails.active_records()
        return {
            "university_objs": university_objs,
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
            context['form'] = form
            return render(request, 'tanseeq_admin/add_tanseeq_period.html', context)
        return redirect('tanseeq_app:list_tanseeq_period')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk, created_by=request.user)
        instance.delete()
        return JsonResponse({"status": 200})


class UniversityGuideList(ListView):
    model = UniversityDetails
    template_name = "tanseeq_admin/list_university_guide.html"
    fields = ["university_name", "file"]


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


class UniversityGuideDeleteView(DeleteView):
    model = UniversityDetails

    def post(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.file.delete()
        return JsonResponse({"status": 200})


class SecondarySchoolCertificateListView(ListView):
    model = SecondarySchoolCetificate
    template_name = 'tanseeq_admin/secondary_certificate_view.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(created_by=self.request.user)
        return queryset

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


class UniversityAttachmentList(ListView):
    model = UniversityAttachment
    template_name = "tanseeq_admin/list_university_attachment.html"


class UniversityAttachmentView(View):
    model = UniversityAttachment
    form_class = UniversityAttachmentForm
    template_name = "tanseeq_admin/add_university_attachment.html"
    def get(self, request, pk=None):
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
            context = {
                "university_objs": UniversityDetails.active_records(),
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


class StudyModeView(View):
    model = StudyModeDetails
    form_class = StudyModeForm

    def get(self, request, pk=None):
        context = {
            "university_objs": UniversityDetails.active_records(),
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
            context = {
                "university_objs": UniversityDetails.active_records(),
                "form": form,
            }
            return render(request, 'tanseeq_admin/add_study_mode.html', context)
        return redirect('tanseeq_app:list_study_mode')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        messages.success(request, "Record removed.")
        return JsonResponse({"status": 200})

class StudyModeView(View):
    model = StudyModeDetails
    form_class = StudyModeForm

    def get(self, request, pk=None):
        context = {
            "university_objs": UniversityDetails.active_records(),
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
            context = {
                "university_objs": UniversityDetails.active_records(),
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


class TanseeqFacultyView(View):
    model = TanseeqFaculty
    form_class = TanseeqFacultyForm
    template_name = "tanseeq_admin/add_tanseeq_faculty.html"

    def get(self, request, pk=None):
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
            context = {
                "university_objs": UniversityDetails.active_records(),
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect('tanseeq_app:list_tanseeq_faculty')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return JsonResponse({"status": 200})


class TanseeqProgramList(ListView):
    model = TanseeqProgram
    template_name = "tanseeq_admin/list_tanseeq_program.html"


class TanseeqProgramView(View):
    model = TanseeqProgram
    form_class = TanseeqProgramForm
    template_name = "tanseeq_admin/add_tanseeq_program.html"

    def get(self, request, pk=None):
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
            context = {
                "university_objs": UniversityDetails.active_records(),
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect('tanseeq_app:list_tanseeq_program')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return JsonResponse({"status": 200})

class TanseeqFeeList(ListView):
    model = TanseeqFee
    template_name = "tanseeq_admin/list_tansseq_fees.html"


class TansseqFeeView(View):
    model = TanseeqFee
    form_class = TanseeqFeeForm
    template_name = "tanseeq_admin/add_tanseeq_fee.html"
    def get(self, request, pk=None):
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
            context = {
                "university_objs": UniversityDetails.active_records(),
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect('tanseeq_app:list_tanseeq_fees')

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return JsonResponse({"status": 200})


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