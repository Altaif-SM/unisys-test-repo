import random
from django.views.generic import TemplateView, View, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
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
from masters.models import CountryDetails, YearDetails
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from django.core import serializers
from django.utils.decorators import method_decorator
from accounts.models import User,UserRole
from common.decorators import check_permissions
from tanseeq_app.helpers import get_tanseeq_application, get_tanseeq_application_by_email
from django.contrib.auth.hashers import make_password

# Create your views here.


class PersonalInfoDetailsView(View):
    model = ApplicationDetails
    form_class = ApplicationInfoForm
    template_name = "tanseeq_admin_applications/personal_info.html"
    redirect_url = 'tanseeq_app:secondary_certificate_info_details'

    def get(self, request, pk=None):
        if pk:
            application_email = ApplicationDetails.objects.get(id = pk).user.username
            request.session['form_data'] = {'email': application_email}
        else:
            application_email = None
            if request.session.get('form_data'):
                form_data = request.session.get('form_data')
                application_email = form_data.get('email')
        tanseeq_application = None
        if application_email:
            tanseeq_application = get_tanseeq_application_by_email(application_email)
        context = {
            "form": self.form_class(),
            "tanseeq_application":tanseeq_application,
        }
        if ApplicationDetails.objects.filter(user__username = application_email).exists():
            instance = get_object_or_404(self.model, user__username = application_email)
            context["instance"] = instance
            context["cities"] = CountryDetails.objects.get(id = instance.country.id).city.all()
            context["form"] = self.form_class(
                instance=get_object_or_404(self.model, user__username = application_email))
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, pk=None):
        application_email = None
        if request.session.get('form_data'):
            form_data = request.session.get('form_data')
            application_email = form_data.get('email')
        if ApplicationDetails.objects.filter(user__username = application_email).exists():
            instance = get_object_or_404(self.model, user__username = application_email)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            if User.objects.filter(email=application_email).exists():
                user = User.objects.get(email=application_email)
            else:
                user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                                           username=request.POST['email'], email=request.POST['email'],
                                           password=make_password('123456'))
                user.role.add(UserRole.objects.get(name='Tanseeq Student'))
                if request.user.is_tanseeq_university_admin():
                    role_id = UserRole.objects.get(name='Tanseeq University Admin').id
                elif request.user.is_tanseeq_application_entry():
                    role_id = UserRole.objects.get(name='Tanseeq Application Entry').id
                else:
                    role_id = UserRole.objects.get(name='Tanseeq Admin').id
                user.tanseeq_role_id = role_id
                user.save()
            obj = form.save(commit=False)
            if not ApplicationDetails.objects.filter(user = user):
                obj.created_by = request.user
                obj.user = user
                obj.tanseeq_id = random.SystemRandom().randint(100000, 999999)
            obj.save()
            request.session['form_data'] = request.POST
            messages.success(request, "Record saved.")
        else:
            context = {
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect(self.redirect_url)


class SecondaryCertificateInfoDetailsView(View):
    model = SecondaryCertificateInfo
    form_class = SecondaryCertificationForm
    template_name = "tanseeq_admin_applications/secondary_certificate_info.html"
    redirect_url = 'tanseeq_app:attachment_details'

    def get(self, request, pk=None):
        application_email = None
        if request.session.get('form_data'):
            form_data = request.session.get('form_data')
            application_email = form_data.get('email')
        tanseeq_application = None
        if application_email:
            tanseeq_application = get_tanseeq_application_by_email(application_email)

        cert_obj = ApplicationDetails.objects.filter(user__username = application_email).exists()
        if not cert_obj:
            messages.info(
                self.request, "Please add personal info first.")
            return redirect("tanseeq_app:personal_info_details")
        academic_year_objs = YearDetails.active_records()
        context = {
            "form": self.form_class(),
            "tanseeq_application": tanseeq_application,
            "academic_year_objs": academic_year_objs,
        }
        if SecondaryCertificateInfo.objects.filter(application__user__username = application_email).exists():
            instance = get_object_or_404(self.model, application__user__username = application_email)
            context["instance"] = instance
            context["cities"] = CountryDetails.objects.get(id=instance.country.id).city.all()
            context["form"] = self.form_class(
                instance=get_object_or_404(self.model, application__user__username = application_email))
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, pk=None):
        application_email = None
        if request.session.get('form_data'):
            form_data = request.session.get('form_data')
            application_email = form_data.get('email')

        if SecondaryCertificateInfo.objects.filter(application__user__username = application_email).exists():
            instance = get_object_or_404(self.model, application__user__username = application_email)
            form = self.form_class(request.POST, instance=instance)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            application_obj = ApplicationDetails.objects.filter(user__username = application_email).first()
            if not SecondaryCertificateInfo.objects.filter(application__user__username = application_email).exists():
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


class StudentStudyModeDetailsView(View):
    """
    Not using it at the moment
    """
    model = SecondaryCertificateInfo
    template_name = "tanseeq_admin_applications/study_mode.html"
    form_class = StudentStudyModeForm
    redirect_url = "tanseeq_app:student_programs_details"

    def get_context_data(self, **kwargs):
        application_email = None
        if self.request.session.get('form_data'):
            form_data = self.request.session.get('form_data')
            application_email = form_data.get('email')
        tanseeq_application = None
        if application_email:
            tanseeq_application = get_tanseeq_application_by_email(application_email)

        instance = self.model.objects.filter(application__user__username = application_email).first()
        context = {
            "form": self.form_class(instance=instance) if instance else self.form_class(),
            "tanseeq_application": tanseeq_application
        }
        return context

    def get(self, request):
        application_email = None
        if self.request.session.get('form_data'):
            form_data = self.request.session.get('form_data')
            application_email = form_data.get('email')
        cert_obj = ApplicationDetails.objects.filter(user__username=application_email).exists()
        if not cert_obj:
            messages.info(self.request, "Please add personal info first.")
            return redirect("tanseeq_app:personal_info_details")
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request):
        application_email = None
        if request.session.get('form_data'):
            form_data = request.session.get('form_data')
            application_email = form_data.get('email')
        instance = self.model.objects.filter(application__user__username = application_email).first()
        if instance:
            form = self.form_class(request.POST, instance=instance)
        else:
            messages.error(
                request, "Please add the Secondary certificate first.")
            return redirect("tanseeq_app:secondary_certificate_info_details")
        if form.is_valid():
            form.save()
        else:
            context = {
                "form": form,
            }
            return render(request, self.template_name, context)
        return redirect(self.redirect_url)

class ApplicantAttachmentsDetailsView(View):
    model = ApplicantAttachment
    form_class = ApplicantAttachementsForm
    template_name = "tanseeq_admin_applications/applicant_attachment_view.html"
    redirect_url = 'tanseeq_app:student_programs_details'

    def get(self, request, pk=None):
        application_email = None
        if request.session.get('form_data'):
            form_data = request.session.get('form_data')
            application_email = form_data.get('email')
        tanseeq_application = None
        if application_email:
            tanseeq_application = get_tanseeq_application_by_email(application_email)

        cert_obj = ApplicationDetails.objects.filter(user__username=application_email).exists()
        if not cert_obj:
            messages.info(
                self.request, "Please add personal info first.")
            return redirect("tanseeq_app:personal_info_details")

        context = {
            "tanseeq_application":tanseeq_application,
        }
        if ApplicantAttachment.objects.filter(application__user__username = application_email).exists():
            instance = get_object_or_404(self.model, application__user__username = application_email)
            context["instance"] = instance
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, pk=None):
        application_email = None
        if request.session.get('form_data'):
            form_data = request.session.get('form_data')
            application_email = form_data.get('email')

        application_obj = ApplicationDetails.objects.filter(user__username=application_email).first()
        instance, created = ApplicantAttachment.objects.get_or_create(application__user__username = application_email, application = application_obj)
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

class ListStudentProgramsDetails(ListView):
    model = ConditionFilters
    template_name = "tanseeq_admin_applications/list_student_programs.html"

    def get_queryset(self):

        faculty_id = self.request.GET.get("faculty")
        university_id = self.request.GET.get("university")
        study_mode_id = self.request.GET.get("study_mode")

        application_email = None
        if self.request.session.get('form_data'):
            form_data = self.request.session.get('form_data')
            application_email = form_data.get('email')

        user = User.objects.get(username = application_email)

        cert_obj = SecondaryCertificateInfo.objects.filter(application__user__username = application_email).first()
        extra_filters = {}
        if faculty_id:
            extra_filters["faculty_id"] = faculty_id
        if university_id:
            extra_filters["university_id"] = university_id

        if study_mode_id:
            extra_filters["study_mode_id"] = study_mode_id
        else:
            if cert_obj.study_mode:
                extra_filters["study_mode_id"] = cert_obj.study_mode.id


        if ConditionFilters.objects.filter(academic_year__end_date = cert_obj.academic_year.end_date).exists():
            queryset = ConditionFilters.objects.filter(
                type_of_secondary_id=cert_obj.secondary_certificate.id,
                average__lte=cert_obj.average,
                academic_year__end_date__gte=cert_obj.academic_year.end_date,
                **extra_filters
            ).select_related("university", "faculty", "program").extra(
                select={
                    'is_applied': 'SELECT 1 FROM tanseeq_app_appliedprograms WHERE ' +
                    'program_details_id=tanseeq_app_conditionfilters.id AND user_id = %s'
                }, select_params=(user.id,)
            )
            return queryset
        else:
            return ConditionFilters.objects.none()

    def get(self, request, *args, **kwargs):
        application_email = None
        if self.request.session.get('form_data'):
            form_data = self.request.session.get('form_data')
            application_email = form_data.get('email')
        cert_obj = ApplicationDetails.objects.filter(user__username = application_email).exists()
        if not cert_obj:
            messages.info(
                self.request, "Please add personal info first.")
            return redirect("tanseeq_app:personal_info_details")

        cert_obj = SecondaryCertificateInfo.objects.filter(application__user__username = application_email).exists()
        if not cert_obj:
            messages.info(
                self.request, "Please add secondary certificate first.")
            return redirect("tanseeq_app:secondary_certificate_info_details")
        return super().get(args, kwargs)


class ListAppliedProgramsDetails(ListView):
    model = AppliedPrograms
    template_name = "tanseeq_admin_applications/list_applied_programs.html"

    def get_queryset(self):
        # user = self.request.user
        application_email = None
        if self.request.session.get('form_data'):
            form_data = self.request.session.get('form_data')
            application_email = form_data.get('email')
        return self.model.objects.filter(user__username=application_email).select_related("program_details")


class ApplyProgramDetailsView(View):
    model = AppliedPrograms
    form_class = ApplyProgramForm

    def is_eligible(self, condition_filter_id, get_obj=False):
        # user = self.request.user
        application_email = None
        if self.request.session.get('form_data'):
            form_data = self.request.session.get('form_data')
            application_email = form_data.get('email')
        cert_obj = SecondaryCertificateInfo.objects.filter(
            application__user__username = application_email).first()
        is_conditions_pass = ConditionFilters.objects.filter(
            id=condition_filter_id,
            type_of_secondary=cert_obj.secondary_certificate,
            average__lte=cert_obj.average,
            academic_year__end_date__gte=cert_obj.academic_year.end_date,
            # academic_year__end_date__lte=cert_obj.academic_year.end_date,
        )
        if get_obj:
            return is_conditions_pass.first()
        return is_conditions_pass.exists()

    def check_applied(self, condition_filter_id):
        # user = self.request.user
        application_email = None
        if self.request.session.get('form_data'):
            form_data = self.request.session.get('form_data')
            application_email = form_data.get('email')
        is_obj = self.model.objects.filter(
            user__username=application_email, program_details_id=condition_filter_id).exists()
        return is_obj

    def post(self, request):
        # user = self.request.user
        application_email = None
        if self.request.session.get('form_data'):
            form_data = self.request.session.get('form_data')
            application_email = form_data.get('email')

        condition_filter_id = request.POST.get("condition_filter_id")
        is_applied = self.check_applied(condition_filter_id)

        if is_applied:
            return JsonResponse({"msg": "Already Applied"}, status=200, safe=False)

        is_eligible = self.is_eligible(condition_filter_id)
        if not is_eligible:
            return JsonResponse({"msg": "Not Eligible"}, status=200, safe=False)

        request_copy = request.POST.copy()
        request_copy["user"] = User.objects.get(email = application_email).id
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
        application_email = None
        if self.request.session.get('form_data'):
            form_data = self.request.session.get('form_data')
            application_email = form_data.get('email')
        obj = get_object_or_404(self.model, pk=pk, user__username = application_email)
        data = {"msg": "Program Removed"}
        is_eligible = self.is_eligible(obj.program_details.id)
        if is_eligible:
            obj.delete()
            return JsonResponse(data, status=202, safe=False)
        else:
            data["msg"] = "No Such Program Found"
            return JsonResponse(data, status=404, safe=False)

class DeclarationSubmissionDetailsView(View):
    model = ApplicationDetails
    template_name = "tanseeq_admin_applications/applicant_declaration.html"
    form_class = ApplicationInfoForm
    redirect_url = "tanseeq_app:list_applicants"

    def get_context_data(self, **kwargs):
        # user = self.request.user
        application_email = None
        if self.request.session.get('form_data'):
            form_data = self.request.session.get('form_data')
            application_email = form_data.get('email')
        instance = self.model.objects.filter(user__username = application_email).first()
        context = {
            "instance":instance,
        }
        return context

    def get(self, request):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request):
        # user = request.user
        application_email = None
        if self.request.session.get('form_data'):
            form_data = self.request.session.get('form_data')
            application_email = form_data.get('email')
        obj = self.model.objects.filter(user__username = application_email).first()
        obj.application_status = 'Submitted'
        obj.save()
        data = {"msg": "Application Submitted"}
        return JsonResponse(data, status=202, safe=False)



def print_voucher_details(request, pk):
    try:
        application_email = None
        if request.session.get('form_data'):
            form_data = request.session.get('form_data')
            application_email = form_data.get('email')

        redirect_url = "tanseeq_app:applied_programs_details"
        template = get_template("tanseeq_student/print_voucher.html")
        applied_program_obj = get_object_or_404(AppliedPrograms, pk=pk)
        attachments = get_object_or_404(ApplicantAttachment, application__user__username = application_email,),
        secondary_cert_obj = get_object_or_404(SecondaryCertificateInfo, application__user__username = application_email)
        photo = attachments[0].photo.path
        context = {
            "applied_program_obj": applied_program_obj,
            "secondary_cert_obj": secondary_cert_obj,
            "photo": photo,
            "ttcc_logo": settings.MEDIA_ROOT + 'Voucher/ttcc_logo.png',
            "bar_code": settings.MEDIA_ROOT + 'Voucher/bar_code.png',
        }
        context = (context)
        html = template.render(context)
        """Local Path"""
        # file = open('test.pdf', "w+b")
        """Production Path"""
        file = open('/var/www/university_system_project/university_system/test.pdf', "w+b")
        pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
        file.seek(0)
        pdf = file.read()
        file.close()
        return HttpResponse(pdf, 'application/pdf')
    except Exception as e:
        messages.warning(request, "An error occurred " + str(e))
        return redirect(redirect_url)


class TanseeqCityList(ListView):
    model = CountryDetails

    def get(self, request, *args, **kwargs):
        if request.GET.get("type") == "JSON":
            queryset = self.get_queryset()
            data = serializers.serialize("json", queryset)
            return JsonResponse(data, status=200, safe=False)
        return super().get(args, kwargs)

    def get_queryset(self):
        country_id = self.request.GET.get("country")
        if country_id:
            return self.model.objects.get(id=country_id).city.all()
        return super().get_queryset()


