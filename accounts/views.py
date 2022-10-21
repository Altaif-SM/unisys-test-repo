from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from accounts.decoratars import user_login_required, registration_required
from accounts.forms import loginForm, signUpForm, ChangePasswordForm
from accounts.service import *
from accounts.models import UserRole
from student.models import StudentDetails, ApplicationDetails, ScholarshipSelectionDetails
from masters.models import AddressDetails, CountryDetails, ScholarshipDetails, GuardianDetails, EmailTemplates, \
    YearDetails,FacultyDetails,ProgramDetails,UniversityTypeDetails,AgentIDDetails
from agents.models import *
from partner.models import PartnerDetails
from donor.models import DonorDetails
import json
from common.utils import *
from django.template.context_processors import csrf
from accounts.service import UserService
from datetime import date
from masters.models import UniversityDetails
from django.http import JsonResponse
# Create your views here.

def index(request):
    return render(request, "index.html")


@user_login_required
def home(request):
    if request.user.is_authenticated:
        user = request.user

        raw_list = []

        if request.user.is_super_admin():

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,first_interview=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,first_interview_attend=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,incomplete=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,
                                                              admin_approval=True, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,application_rejection=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_online_admission=True).count())

            scholarship_list = []
            country_list = []

            for scholarship in ScholarshipDetails.objects.all():
                raw_dict = {}
                raw_dict['scholarship_name'] = scholarship.scholarship_name
                raw_dict['scholarship_count'] = ApplicationDetails.objects.filter(
                    applicant_scholarship_rel__scholarship=scholarship).count()

                scholarship_list.append(raw_dict)

            for country in CountryDetails.objects.all():
                raw_dict = {}
                raw_dict['country_name'] = country.country_name.capitalize()
                raw_dict['country_count'] = ApplicationDetails.objects.filter(address__country=country,is_online_admission=True).count()

                country_list.append(raw_dict)

        elif request.user.is_partner():
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True,

                                                              admin_approval=False, is_sponsored=False,
                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                              year=get_current_year(request)).count())

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True,

                                                              admin_approval=False, is_sponsored=False,
                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                              year=get_current_year(request)).count())

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True,

                                                              admin_approval=False, is_sponsored=False,
                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                              year=get_current_year(request)).count())

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True,

                                                              admin_approval=False, is_sponsored=False,
                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                              year=get_current_year(request)).count())

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True,

                                                              admin_approval=True, is_sponsored=False,
                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                              year=get_current_year(request)).count())

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True,

                                                              admin_approval=True, is_sponsored=True,
                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                              year=get_current_year(request)).count())

            raw_list.append(
                ApplicationDetails.objects.filter(nationality=request.user.partner_user_rel.get().address.country,
                                                  year=get_current_year(request)).count())

            scholarship_list = []
            country_list = []

            for scholarship in ScholarshipDetails.objects.all():
                raw_dict = {}
                raw_dict['scholarship_name'] = scholarship.scholarship_name
                raw_dict['scholarship_count'] = ApplicationDetails.objects.filter(
                    applicant_scholarship_rel__scholarship=scholarship,
                    nationality=request.user.partner_user_rel.get().address.country,
                    year=get_current_year(request)).count()

                scholarship_list.append(raw_dict)

            for country in CountryDetails.objects.all():
                raw_dict = {}
                raw_dict['country_name'] = country.country_name
                raw_dict['country_count'] = ApplicationDetails.objects.filter(address__country=country,
                                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                                              year=get_current_year(request)).count()

                country_list.append(raw_dict)

        else:
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,
                                                              first_interview=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,
                                                              first_interview_attend=True).count())
            raw_list.append(
                ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True, incomplete=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,


                                                              admin_approval=True, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,
                                                              application_rejection=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_online_admission=True).count())

            scholarship_list = []
            country_list = []

            for scholarship in ScholarshipDetails.objects.all():
                raw_dict = {}
                raw_dict['scholarship_name'] = scholarship.scholarship_name
                raw_dict['scholarship_count'] = ApplicationDetails.objects.filter(
                    applicant_scholarship_rel__scholarship=scholarship).count()

                scholarship_list.append(raw_dict)

            for country in CountryDetails.objects.all():
                raw_dict = {}
                raw_dict['country_name'] = country.country_name.capitalize()
                raw_dict['country_count'] = ApplicationDetails.objects.filter(address__country=country,is_online_admission=True).count()

                country_list.append(raw_dict)

        # if user.is_superuser:
        # try:
        #     current_acd_year = YearDetails.objects.get(active_year=True)
        #     end_date = current_acd_year.end_date
        #     todayDate = date.today()
        #     active_year = False
        #     if end_date <= todayDate:
        #         active_year = True
        #         User.objects.filter().update(registration_switch=False)
        #         User.objects.filter().update(submission_switch=False)
        # except:
        #     active_year = False
        #     User.objects.filter().update(registration_switch=False)
        #     User.objects.filter().update(submission_switch=False)
        # return render(request, "template_admin_dashboard.html",
        #               {'user': user, 'raw_list': raw_list, 'scholarship_list': json.dumps(scholarship_list),'active_year':active_year,
        #                'country_list': json.dumps(country_list)})
        if User.objects.all():
            registration_flag = User.objects.filter()[0].registration_switch
            submission_switch = User.objects.filter()[0].submission_switch
        else:
            registration_flag = False
            submission_switch = False

        return render(request, "template_admin_dashboard.html",
                      {'user': user, 'raw_list': raw_list, 'scholarship_list': json.dumps(scholarship_list),
                       'country_list': json.dumps(country_list),'registration_flag':registration_flag,'submission_switch':submission_switch})

@user_login_required
def dashboard(request):
    if request.user.is_authenticated:
        user = request.user

        raw_list = []

        if request.user.is_super_admin():

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,university=request.user.university).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,first_interview=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,first_interview_attend=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,incomplete=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,

                                                              admin_approval=True, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,application_rejection=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_online_admission=True).count())

            scholarship_list = []
            country_list = []

            for scholarship in ScholarshipDetails.objects.all():
                raw_dict = {}
                raw_dict['scholarship_name'] = scholarship.scholarship_name
                raw_dict['scholarship_count'] = ApplicationDetails.objects.filter(
                    applicant_scholarship_rel__scholarship=scholarship).count()

                scholarship_list.append(raw_dict)

            for country in CountryDetails.objects.all():
                raw_dict = {}
                raw_dict['country_name'] = country.country_name.capitalize()
                raw_dict['country_count'] = ApplicationDetails.objects.filter(address__country=country,is_online_admission=True).count()

                country_list.append(raw_dict)

        elif request.user.is_administrator():
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,university=request.user.university).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,university=request.user.university,
                                                              first_interview=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,university=request.user.university,
                                                              first_interview_attend=True).count())
            raw_list.append(
                ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True, incomplete=True,university=request.user.university).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,


                                                              admin_approval=True, is_sponsored=False,university=request.user.university).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,
                                                              application_rejection=True,university=request.user.university).count())
            raw_list.append(ApplicationDetails.objects.filter(is_online_admission=True,university=request.user.university).count())

            scholarship_list = []
            country_list = []

            for scholarship in ScholarshipDetails.objects.all():
                raw_dict = {}
                raw_dict['scholarship_name'] = scholarship.scholarship_name
                raw_dict['scholarship_count'] = ApplicationDetails.objects.filter(
                    applicant_scholarship_rel__scholarship=scholarship).count()

                scholarship_list.append(raw_dict)

            for country in CountryDetails.objects.all():
                raw_dict = {}
                raw_dict['country_name'] = country.country_name.capitalize()
                raw_dict['country_count'] = ApplicationDetails.objects.filter(address__country=country,
                                                                              is_online_admission=True).count()

                country_list.append(raw_dict)

        elif request.user.is_faculty():
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,faculty=request.user.faculty).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,faculty=request.user.faculty,
                                                              first_interview=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,faculty=request.user.faculty,
                                                              first_interview_attend=True).count())
            raw_list.append(
                ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True, incomplete=True,faculty=request.user.faculty).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,

                                                              admin_approval=True, is_sponsored=False,faculty=request.user.faculty).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,
                                                              application_rejection=True,faculty=request.user.faculty).count())
            raw_list.append(ApplicationDetails.objects.filter(is_online_admission=True,faculty=request.user.faculty).count())

            scholarship_list = []
            country_list = []

            for scholarship in ScholarshipDetails.objects.all():
                raw_dict = {}
                raw_dict['scholarship_name'] = scholarship.scholarship_name
                raw_dict['scholarship_count'] = ApplicationDetails.objects.filter(
                    applicant_scholarship_rel__scholarship=scholarship).count()

                scholarship_list.append(raw_dict)

            for country in CountryDetails.objects.all():
                raw_dict = {}
                raw_dict['country_name'] = country.country_name.capitalize()
                raw_dict['country_count'] = ApplicationDetails.objects.filter(address__country=country,
                                                                              is_online_admission=True).count()

                country_list.append(raw_dict)

        elif request.user.is_program():
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,program=request.user.program).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,program=request.user.program,
                                                              first_interview=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,program=request.user.program,
                                                              first_interview_attend=True).count())
            raw_list.append(
                ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True, incomplete=True,program=request.user.program).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,

                                                              admin_approval=True, is_sponsored=False,program=request.user.program).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,
                                                              application_rejection=True,program=request.user.program).count())
            raw_list.append(ApplicationDetails.objects.filter(is_online_admission=True,program=request.user.program).count())

            scholarship_list = []
            country_list = []

            for scholarship in ScholarshipDetails.objects.all():
                raw_dict = {}
                raw_dict['scholarship_name'] = scholarship.scholarship_name
                raw_dict['scholarship_count'] = ApplicationDetails.objects.filter(
                    applicant_scholarship_rel__scholarship=scholarship).count()

                scholarship_list.append(raw_dict)

            for country in CountryDetails.objects.all():
                raw_dict = {}
                raw_dict['country_name'] = country.country_name.capitalize()
                raw_dict['country_count'] = ApplicationDetails.objects.filter(address__country=country,
                                                                              is_online_admission=True).count()

                country_list.append(raw_dict)

        elif request.user.is_supervisor():
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,supervisor=request.user).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,supervisor=request.user,
                                                              first_interview=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,supervisor=request.user,
                                                              first_interview_attend=True).count())
            raw_list.append(
                ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True, incomplete=True,supervisor=request.user).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,

                                                              admin_approval=True, is_sponsored=False,supervisor=request.user).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,
                                                              application_rejection=True,supervisor=request.user).count())
            raw_list.append(ApplicationDetails.objects.filter(is_online_admission=True,supervisor=request.user).count())

            scholarship_list = []
            country_list = []

            for scholarship in ScholarshipDetails.objects.all():
                raw_dict = {}
                raw_dict['scholarship_name'] = scholarship.scholarship_name
                raw_dict['scholarship_count'] = ApplicationDetails.objects.filter(
                    applicant_scholarship_rel__scholarship=scholarship).count()

                scholarship_list.append(raw_dict)

            for country in CountryDetails.objects.all():
                raw_dict = {}
                raw_dict['country_name'] = country.country_name.capitalize()
                raw_dict['country_count'] = ApplicationDetails.objects.filter(address__country=country,
                                                                              is_online_admission=True).count()

                country_list.append(raw_dict)

        elif request.user.is_partner():
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=False,
                                                              second_interview_approval=False, psychometric_test=False,
                                                              admin_approval=False, is_sponsored=False,
                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                              year=get_current_year(request)).count())

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=False, psychometric_test=False,
                                                              admin_approval=False, is_sponsored=False,
                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                              year=get_current_year(request)).count())

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=True, psychometric_test=False,
                                                              admin_approval=False, is_sponsored=False,
                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                              year=get_current_year(request)).count())

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=True, psychometric_test=True,
                                                              admin_approval=False, is_sponsored=False,
                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                              year=get_current_year(request)).count())

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=True, psychometric_test=True,
                                                              admin_approval=True, is_sponsored=False,
                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                              year=get_current_year(request)).count())

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=True, psychometric_test=True,
                                                              admin_approval=True, is_sponsored=True,
                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                              year=get_current_year(request)).count())

            raw_list.append(
                ApplicationDetails.objects.filter(nationality=request.user.partner_user_rel.get().address.country,
                                                  year=get_current_year(request)).count())

            scholarship_list = []
            country_list = []

            for scholarship in ScholarshipDetails.objects.all():
                raw_dict = {}
                raw_dict['scholarship_name'] = scholarship.scholarship_name
                raw_dict['scholarship_count'] = ApplicationDetails.objects.filter(
                    applicant_scholarship_rel__scholarship=scholarship,
                    nationality=request.user.partner_user_rel.get().address.country,
                    year=get_current_year(request)).count()

                scholarship_list.append(raw_dict)

            for country in CountryDetails.objects.all():
                raw_dict = {}
                raw_dict['country_name'] = country.country_name
                raw_dict['country_count'] = ApplicationDetails.objects.filter(address__country=country,
                                                                              nationality=request.user.partner_user_rel.get().address.country,
                                                                              year=get_current_year(request)).count()

                country_list.append(raw_dict)

        else:
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,
                                                              first_interview=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,
                                                              first_interview_attend=True).count())
            raw_list.append(
                ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True, incomplete=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,

                                                              admin_approval=True, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, is_online_admission=True,
                                                              application_rejection=True).count())
            raw_list.append(ApplicationDetails.objects.filter(is_online_admission=True).count())

            scholarship_list = []
            country_list = []

            for scholarship in ScholarshipDetails.objects.all():
                raw_dict = {}
                raw_dict['scholarship_name'] = scholarship.scholarship_name
                raw_dict['scholarship_count'] = ApplicationDetails.objects.filter(
                    applicant_scholarship_rel__scholarship=scholarship).count()

                scholarship_list.append(raw_dict)

            for country in CountryDetails.objects.all():
                raw_dict = {}
                raw_dict['country_name'] = country.country_name.capitalize()
                raw_dict['country_count'] = ApplicationDetails.objects.filter(address__country=country,is_online_admission=True).count()

                country_list.append(raw_dict)

        if User.objects.all():
            registration_flag = User.objects.filter()[0].registration_switch
            submission_switch = User.objects.filter()[0].submission_switch
        else:
            registration_flag = False
            submission_switch = False

        return render(request, "template_university_dashboard.html",
                      {'user': user, 'raw_list': raw_list, 'scholarship_list': json.dumps(scholarship_list),
                       'country_list': json.dumps(country_list),'registration_flag':registration_flag,'submission_switch':submission_switch})


def template_signup(request):
    form = signUpForm()
    return render(request, 'signup.html', {'form': form})


def template_signin(request):
    country_list = CountryDetails.objects.all()
    form = loginForm()

    if request.user.is_authenticated:
        dashboard_path = request.user.get_dashboard_path()
        return redirect(dashboard_path)

    # return render(request, "template_login.html", {'form': form})
    return render(request, "template_login.html", {'form': form, 'country_list': country_list})

@registration_required
@transaction.atomic
def user_signup(request):
    signup_form = signUpForm(request.POST)
    if request.method == 'POST':
        if signup_form.is_valid():
            user = ''
            try:
                user = signup_form.save()

                try:
                    admin_rec = User.objects.filter(role__name='Admin')[0]

                    user.registration_switch = admin_rec.registration_switch
                    user.submission_switch = admin_rec.submission_switch
                    user.psyc_switch = admin_rec.psyc_switch
                    user.agreements_switch = admin_rec.agreements_switch
                    user.semester_switch = admin_rec.semester_switch
                    user.program_switch = admin_rec.program_switch
                    user.save()
                except:
                    pass

                user.role.add(UserRole.objects.get(name=request.POST['role']))
                if str(request.POST['role']) not in ["Accountant"]:
                    try:
                        country = CountryDetails.objects.get(id=request.POST['country'])
                        address = AddressDetails.objects.create(country=country)
                    except:
                        pass

                    if request.POST['role'] == "Student":
                        user.is_active = False
                        user.save()
                        student_obj = StudentDetails.objects.create(user=user)
                        subject = 'Account Activation - Online Admission System'
                        message = 'Thank you for registering with us. In order to activate your account please click button below.'
                        send_signup_email_to_applicant(student_obj.user.email, student_obj.user.email, subject, message,student_obj.user.first_name, user.id)
                        messages.info(request,"The activation link is sent to your email id. ")

                    if request.POST['role'] == "Agent":
                        user.is_active = False
                        user.save()
                        agent_id = 'AG0000' + str(user.id)
                        AgentIDDetails.objects.create(user=user,agent_id = agent_id)
                        student_obj = StudentDetails.objects.create(user=user)
                        subject = 'Account Activation - Online Admission System'
                        message = 'Thank you for registering with us. In order to activate your account please click button below.'
                        send_signup_email_to_applicant(student_obj.user.email, student_obj.user.email, subject, message,student_obj.user.first_name, user.id)
                        messages.info(request,"The activation link is sent to your email id. ")

                    if request.POST['role'] == "Partner":
                        PartnerDetails.objects.create(user=user, address=address)

                    if request.POST['role'] == "Parent":
                        GuardianDetails.objects.create(user=user, address=address)

                    if request.POST['role'] == "Donor":
                        organisation = request.POST.get('organisation')
                        DonorDetails.objects.create(user=user, address=address, organisation=organisation)

            except Exception as e:
                if user:
                    user.delete()
                messages.success(request, str(e))
            if request.POST['role'] == 'Agent':
                return redirect('/agent/')
            else:
                return redirect('/')
        else:
            # print(signup_form.errors)
            for error_msg in signup_form.errors:
                for msg in signup_form.errors[error_msg]:
                    messages.error(request, msg)
        if request.POST.get('admin_page'):
            return redirect('/accounts/template_manage_user/')
        if request.POST['role'] == 'Agent':
            return redirect('/agent/')
        else:
            return redirect('/')


# @csrf_exempt
def user_signin(request):
    form_data = request.POST
    if request.POST:
        form = loginForm(request.POST or None)
        request.session['form_data'] = form_data
        try:
            # YearDetails.objects.get(id=year_id)
            request.session['selected_year'] = YearDetails.objects.get(active_year=True).id
        except:
            request.session['selected_year'] = ''
    else:
        form = loginForm(request.session.get('form_data'))

    if form.is_valid():
        try:
            if User.objects.filter(username = request.POST['username']).exists():
                user_obj = User.objects.get(username = request.POST['username'])
                student_obj = StudentDetails.objects.get(user=user_obj)
                success = user_obj.check_password(request.POST['password'])
                if success:
                    if not user_obj.is_active:
                        subject = 'Account Activation - Online Admission System'
                        message = 'Thank you for registering with us. In order to activate your account please click button below.'
                        send_signup_email_to_applicant(student_obj.user.email, student_obj.user.email, subject, message,
                                                       student_obj.user.first_name, user_obj.id)
                        messages.info(request, "The activation link is sent to your email id. ")
                        return redirect('/')
        except:
            pass
        user = form.login(request)
        if user:
            login(request, user)
            dashboard_path = user.get_dashboard_path()
            return redirect(dashboard_path)
        else:
            messages.error(request, "Enter valid email and password.")
            if request.POST.get('role') == 'Tanseeq Student':
                return redirect('/tanseeq/')
            return redirect('/')



@user_login_required
def user_signout(request):
    tanseeq_role = ['Tanseeq Student', 'Tanseeq Admin']
    agent_role = ['Agent']
    if request.user.role.all():
        if request.user.role.filter(name__in = agent_role):
            logout(request)
            return redirect('/agent/')
        elif request.user.role.filter(name__in = tanseeq_role):
            logout(request)
            return redirect('/tanseeq/')
        else:
            logout(request)
            return redirect('/')
    else:
        logout(request)
        return redirect('/')


@user_login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST)
        password_data = {}
        if form.is_valid():
            password_data['current_password'] = form.cleaned_data['current_password']
            password_data['password'] = form.cleaned_data['password']
            password_data['password1'] = form.cleaned_data['password1']
            user = authenticate(username=request.user.username, password=password_data['current_password'])
            if user:
                user.set_password(password_data['password1'])
                user.encoded_pwd= None
                user.is_active = True
                user.save()
                user = authenticate(username=user.username, password=password_data['password1'])
                if user is not None:
                    login(request, user)
                    dashboard_path = user.get_dashboard_path()
                    return HttpResponseRedirect(dashboard_path)
            else:
                context = {}
                context['form'] = form
                context['message'] = "Invalid Current Password"
                if request.user.is_agent():
                    context['my_template'] = 'template_agent_base.html'
                elif request.user.is_agent_recruiter():
                    context['my_template'] = 'template_recruiter_base.html'
                else:
                    context['my_template'] = 'template_base_page.html'
                return render(request, 'template_change_password.html', context)

        elif not request.POST:
            password_data = json.loads(request.body)
            if 'current_password' in password_data:
                if not 'password' in password_data or not 'password1' in password_data:
                    return HttpResponse(json.dumps({'message': 'New Password is necessary'}),
                                        content_type="application/json")
                elif password_data['password'] != password_data['password1']:
                    return HttpResponse(json.dumps({'message': 'The Passwords did not match'}),
                                        content_type="application/json")

                user = authenticate(username=request.user.username, password=password_data['current_password'])
                if user:
                    if user.is_blocked:
                        return HttpResponseRedirect('/accounts/user_blocked/')
                    user.set_password(password_data['password1'])
                    user.is_active = True
                    user.save()
                    user = authenticate(username=user.username, password=password_data['password1'])
                    if user is not None:
                        login(request, user)
                        dashboard_path = user.get_dashboard_path()
                        return HttpResponseRedirect(dashboard_path)
                else:
                    return HttpResponse(json.dumps({'message': 'Invalid current password'}),
                                        content_type="application/json")
            elif not 'current_password' in password_data:
                return HttpResponse(json.dumps({'message': 'Current Password is necessary'}),
                                    content_type="application/json")

            return HttpResponse(json.dumps({'message': 'Unknown error occurred'}), content_type="application/json")

        else:
            context = {}
            context.update(csrf(request))
            context['form'] = form
            context['message'] = "Please correct the following field:"
            ChangePasswordForm(data=request.GET)
            if request.user.is_agent():
                context['my_template'] = 'template_agent_base.html'
            elif request.user.is_agent_recruiter():
                context['my_template'] = 'template_recruiter_base.html'
            else:
                context['my_template'] = 'template_base_page.html'
            return render(request, 'template_change_password.html', context)
    else:
        context = {}
        context.update(csrf(request))
        form = ChangePasswordForm()
        context['form'] = form
        if request.user.is_agent():
            context['my_template'] = 'template_agent_base.html'
        elif request.user.is_agent_recruiter():
            context['my_template'] = 'template_recruiter_base.html'
        else:
            context['my_template'] = 'template_base_page.html'
        return render(request, 'template_change_password.html', context)


def template_manage_user(request):
    country_list = CountryDetails.objects.all()
    user_recs = User.objects.filter().exclude(role__name='Admin')
    return render(request, 'template_manage_user.html',
                  {'country_list': country_list, 'user_recs': user_recs})


def account_activate(request, user_id):
    try:
        user_rec = User.objects.get(id=user_id)
        if not user_rec.is_active:
            User.objects.filter(id=user_id).update(is_active=True)
            messages.success(request, "Account activated. You can login now.")
        else:
            messages.error(request, "Account already activated. You can login now.")
    except:
        messages.error(request, "Invalid operation.")
    return redirect('/')


import shutil
from student.models import *


@transaction.atomic
def delete_user(request, user_id):
    try:
        user_rec = User.objects.get(id=user_id)

        if user_rec.is_student():
            if user_rec.get_application:
                app_id = user_rec.get_application.id
                if not user_rec.get_application.is_submitted:
                    try:
                        application_obj = ApplicationDetails.objects.get(id=app_id)

                        object_path = str(application_obj.first_name) + '_' + str(application_obj.id)
                        object_path = settings.MEDIA_ROOT + os.path.join('reports/' + str(object_path))
                        if os.path.exists(str(object_path)):
                            shutil.rmtree(object_path)

                        AddressDetails.objects.filter(id=application_obj.address.id).delete()
                        AddressDetails.objects.filter(id=application_obj.permanent_address.id).delete()

                        ApplicationHistoryDetails.objects.filter(applicant_id=app_id).delete()
                        SiblingDetails.objects.filter(applicant_id=app_id).delete()
                        AcademicQualificationDetails.objects.filter(applicant_id=app_id).delete()
                        EnglishQualificationDetails.objects.filter(applicant_id=app_id).delete()
                        CurriculumDetails.objects.filter(applicant_id=app_id).delete()
                        ExperienceDetails.objects.filter(applicant_id=app_id).delete()
                        ScholarshipSelectionDetails.objects.filter(applicant_id=app_id).delete()
                        ApplicantAboutDetails.objects.filter(applicant_id=app_id).delete()
                        StudentNotifications.objects.filter(applicant_id=app_id).delete()
                        ApplicationDetails.objects.filter(id=app_id).delete()

                        StudentDetails.objects.filter(user=user_rec).delete()
                        User.objects.filter(id=user_rec.id).delete()
                        messages.success(request, "Student deleted successfully.")
                    except:
                        messages.warning(request,
                                         "This student cannot be deleted.")
                else:
                    messages.warning(request,
                                     "This student cannot be deleted as his/her application is already submitted.")

            else:
                try:
                    StudentDetails.objects.filter(user=user_rec).delete()
                    User.objects.filter(id=user_rec.id).delete()
                    messages.success(request, "Student deleted successfully.")
                except:
                    messages.warning(request, "This student cannot be deleted.")

        elif user_rec.is_partner():
            try:
                PartnerDetails.objects.filter(user=user_rec).delete()
                User.objects.filter(id=user_rec.id).delete()
                messages.success(request, "Partner deleted successfully.")
            except:
                messages.warning(request, "This parent cannot be deleted. Its instance is used in other tables")

        elif user_rec.is_donor():
            try:
                DonorDetails.objects.filter(user=user_rec).delete()
                User.objects.filter(id=user_rec.id).delete()
                messages.success(request, "Donor deleted successfully.")
            except:
                messages.warning(request, "This donor cannot be deleted.  As students are mapped to this donor")

        elif user_rec.is_parent():
            try:
                GuardianDetails.objects.filter(user=user_rec).delete()
                User.objects.filter(id=user_rec.id).delete()
                messages.success(request, "Parent deleted successfully.")
            except:
                messages.warning(request, "This parent cannot be deleted. As students are mapped to this parent")

        elif user_rec.is_accountant():
            try:
                User.objects.filter(id=user_rec.id).delete()
                messages.success(request, "Accountant deleted successfully.")
            except:
                messages.warning(request, "This accountant cannot be deleted. Its instance is used in other tables.")

        else:
            try:
                User.objects.filter(id=user_rec.id).delete()
                messages.success(request, "User deleted successfully.")
            except:
                messages.warning(request, "Record not deleted.")
    except:
        messages.warning(request, "Record not deleted.")
    return redirect('/accounts/staff_settings')


def update_switch(request):
    if request.method == 'POST':
        val_dict = request.POST
        if request.user.is_superuser or request.user.is_system_admin:

            if 'switch_type' in val_dict and val_dict['switch_type'] == 'is_registration_switch':
                # try:
                #     current_acd_year = YearDetails.objects.get(active_year=True)
                #     end_date = current_acd_year.end_date
                #     todayDate = date.today()
                #     if end_date <= todayDate:
                #         acadmic_flag = 'date_over'
                #         return HttpResponse(json.dumps({'flag': acadmic_flag}))
                # except:
                #     acadmic_flag = 'date_over'
                #     return HttpResponse(json.dumps({'flag': acadmic_flag}))

                User.objects.filter().update(registration_switch=(json.loads(val_dict['switch'])))

            if 'switch_type' in val_dict and val_dict['switch_type'] == 'is_submission_switch':
                # try:
                #     current_acd_year = YearDetails.objects.get(active_year=True)
                #     end_date = current_acd_year.end_date
                #     todayDate = date.today()
                #     if end_date <= todayDate:
                #         acadmic_flag = 'date_over'
                #         return HttpResponse(json.dumps({'flag': acadmic_flag}))
                # except:
                #     acadmic_flag = 'date_over'
                #     return HttpResponse(json.dumps({'flag': acadmic_flag}))

                User.objects.filter().update(submission_switch=(json.loads(val_dict['switch'])))



            if 'switch_type' in val_dict and val_dict['switch_type'] == 'is_psyc_switch':
                User.objects.filter().update(psyc_switch=(json.loads(val_dict['switch'])))

                if val_dict['switch'] == 'true':
                    application_ids = ApplicationDetails.objects.filter(year=get_current_year(),
                                                                        is_submitted=True).values_list('id')
                    application_notification(application_ids,
                                             'Now you can take your psychometric test.')

            if 'switch_type' in val_dict and val_dict['switch_type'] == 'is_agreements_switch':
                User.objects.filter().update(agreements_switch=(json.loads(val_dict['switch'])))

            if 'switch_type' in val_dict and val_dict['switch_type'] == 'is_semester_switch':
                User.objects.filter().update(semester_switch=(json.loads(val_dict['switch'])))

            if 'switch_type' in val_dict and val_dict['switch_type'] == 'is_program_switch':
                User.objects.filter().update(program_switch=(json.loads(request.POST['switch'])))

    return HttpResponse(json.dumps({'flag': json.loads(request.POST['switch'])}))


def CheckActiveYear(request):
    print("1 hour complter---------------------------------------")
    year_rec = YearDetails.objects.filter(active_year=True)
    if year_rec:
        current_acd_year = YearDetails.objects.get(active_year=True)
        all_academicyr_recs = YearDetails.objects.all()
        end_date = current_acd_year.end_date
        todayDate = date.today()
        if end_date == todayDate:
            YearDetails.objects.filter().update(base_date=False)
            YearDetails.objects.filter(id=current_acd_year.id).update(active_year=False)
        else:
            for academicyr_rec in all_academicyr_recs:
                if academicyr_rec:
                    acd_year = academicyr_rec.start_date - current_acd_year.end_date
                    if acd_year.days > 0:
                        next_acd_year_obj = academicyr_rec
                        if next_acd_year_obj.start_date == todayDate:
                            YearDetails.objects.filter().update(base_date = False)
                            YearDetails.objects.filter().update(active_year=False)
                            YearDetails.objects.filter(id=next_acd_year_obj.id).update(active_year=True,base_date = True)
        return HttpResponse('')
    else:
        current_acd_year = YearDetails.objects.get(base_date=True)
        all_academicyr_recs = YearDetails.objects.all()
        todayDate = date.today()
        for academicyr_rec in all_academicyr_recs:
            if academicyr_rec:
                acd_year = academicyr_rec.start_date - current_acd_year.end_date
                if acd_year.days > 0:
                    next_acd_year_obj = academicyr_rec
                    if next_acd_year_obj.start_date == todayDate:
                        YearDetails.objects.filter().update(base_date=False)
                        YearDetails.objects.filter().update(active_year=False)
                        YearDetails.objects.filter(id=next_acd_year_obj.id).update(active_year=True,base_date = True)
        return HttpResponse('')


class AuthRequiredMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/")
        return None


def staff_settings(request):
    country_list = CountryDetails.objects.all()
    role_name_list = ['Admin','Student','Donor','Partner','Parent','System Admin']
    user_recs = User.objects.filter().exclude(role__name__in=role_name_list)
    return render(request, 'staff_settings.html',
                  {'country_list': country_list, 'user_recs': user_recs})

def add_staff(request):
    country_list = CountryDetails.objects.all()
    system_settings_list = ['Manage Language', 'Manage Currency', 'Manage Country', 'Manage Study Mode', 'Manage Study Level','Manage Study Type','Manage Student Mode', 'Manage Learning Centers', 'Manage Faculties', 'Link Faculty to User']
    user_settings_list = ['Manage Group', 'Manage Users']
    university_settings_list = ['Manage Universities', 'Manage University Partner', 'Link University to User', 'Manage Program', 'Manage Campus','Link Campus to User', 'Manage Department', 'Link Department to User']
    academic_settings_list = ['Manage Year', 'Manage Semester', 'Manage Activity', 'Manage Calendar']
    module_settings_list = ['Manage Applicant Documents', 'Approving Applicant Details','Payment Settings']
    if request.method == 'POST':
        faculty = request.POST.get('faculty',None)
        program = request.POST.get('program',None)
        supervisor_faculty = request.POST.get('supervisor_faculty',None)
        if supervisor_faculty:
            faculty = supervisor_faculty
        supervisor_program = request.POST.get('supervisor_program', None)
        if supervisor_program:
            program = supervisor_program
        university = request.POST.get('university')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')
        country = request.POST.get('country')
        residential_address = request.POST.get('address')
        status = request.POST.get('status')
        permission_list = request.POST.getlist('checks[]')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            country_obj = CountryDetails.objects.get(id = country)
            staff_dict = {
                # 'first_name': first_name,
                # 'last_name': last_name,
                'email': email,
                'role': role,
                'country': country_obj.id,
                'country_name': country_obj.country_name,
                'residential_address': residential_address,
                'status': status,
                'system_settings_list': system_settings_list,
                'user_settings_list': user_settings_list,
                'university_settings_list': university_settings_list,
                'academic_settings_list': academic_settings_list,
                'module_settings_list': module_settings_list,
                'permission_list': permission_list
            }
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists.")
                return render(request, 'add_staff.html',{'country_list':country_list,'staff_dict':staff_dict})

            staff_obj = User.objects.create(email = email,username = email,password = make_password(password),is_active = status,university_id = university,faculty_id = faculty,program_id = program)
            staff_obj.role.add(UserRole.objects.get(name=role))
            try:
                country = CountryDetails.objects.get(id=country)
                address = AddressDetails.objects.create(country=country,residential_address = residential_address)
                staff_obj.address = address
            except:
                pass
            staff_obj.save()

            system_check = any(item in system_settings_list for item in permission_list)
            user_check = any(item in user_settings_list for item in permission_list)
            university_check = any(item in university_settings_list for item in permission_list)
            academic_check = any(item in academic_settings_list for item in permission_list)
            module_check = any(item in module_settings_list for item in permission_list)
            if system_check is True:
                permission_list.append('System Settings')
            if user_check is True:
                permission_list.append('User Settings')
            if university_check is True:
                permission_list.append('University Settings')
            if academic_check is True:
                permission_list.append('Academic Settings')
            if module_check is True:
                permission_list.append('Application Settings')

            for rec in permission_list:
                permission_obj = PersmissionDetails.objects.create(permission=rec)
                staff_obj.permission.add(permission_obj)
            messages.success(request, "Record saved.")
        except Exception as e:
            print(e)
            messages.warning(request, "Record not saved.")
        return redirect('/accounts/staff_settings/')
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                       is_partner_university=False).order_by('-id')
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    staff_dict = {
        'first_name': '',
        'last_name': '',
        'email': '',
        'role': '',
        'country': '',
        'residential_address': '',
        'status': True,
        'system_settings_list': system_settings_list,
        'user_settings_list': user_settings_list,
        'university_settings_list': university_settings_list,
        'academic_settings_list': academic_settings_list,
        'module_settings_list': module_settings_list,
        'permission_list': [],
        'university_recs':university_recs,
        'university_type_recs':university_type_recs

    }
    return render(request, 'add_staff.html', {'country_list':country_list,'staff_dict':staff_dict})

def delete_staff(request):
    if request.method == 'POST':
        staff_delete_id = request.POST.get('staff_delete_id')
        try:
            User.objects.filter(id=staff_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/accounts/staff_settings/')

def edit_staff(request, staff_id=None):
    country_list = CountryDetails.objects.all()
    user_obj = User.objects.get(id=staff_id)
    system_settings_list = ['Manage Language', 'Manage Currency', 'Manage Country', 'Manage Study Mode', 'Manage Study Level','Manage Study Type','Manage Student Mode', 'Manage Learning Centers', 'Manage Faculties', 'Link Faculty to User']
    user_settings_list = ['Manage Group', 'Manage Users']
    university_settings_list = ['Manage Universities', 'Manage University Partner', 'Link University to User', 'Manage Program', 'Manage Campus','Link Campus to User','Manage Department', 'Link Department to User']
    academic_settings_list = ['Manage Year', 'Manage Semester', 'Manage Activity', 'Manage Calendar']
    module_settings_list = ['Manage Applicant Documents','Approving Applicant Details','Payment Settings']
    if request.method == 'POST':
        faculty = request.POST.get('faculty', None)
        program = request.POST.get('program', None)

        supervisor_faculty = request.POST.get('supervisor_faculty', None)
        if supervisor_faculty:
            faculty = supervisor_faculty
        supervisor_program = request.POST.get('supervisor_program', None)
        if supervisor_program:
            program = supervisor_program

        university = request.POST.get('university')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')
        country = request.POST.get('country')
        residential_address = request.POST.get('address')
        status = request.POST.get('status')
        permission_list = request.POST.getlist('checks[]')

        if status == 'on':
            status = True
        else:
            status = False
        try:

            country_obj = CountryDetails.objects.get(id=country)
            user_obj = {
                'id': user_obj.id,
                # 'first_name': first_name,
                # 'last_name': last_name,
                'email': email,
                'role': role,
                'country': country_obj.id,
                'country_name': country_obj.country_name,
                'residential_address': residential_address,
                'status': status,
                'system_settings_list': system_settings_list,
                'user_settings_list': user_settings_list,
                'university_settings_list': university_settings_list,
                'academic_settings_list': academic_settings_list,
                'module_settings_list': module_settings_list,
                'permission_list': permission_list
            }
            if User.objects.filter(~Q(id=staff_id), email=email).exists():
                messages.warning(request, "Email already exists.")
                return render(request, 'edit_staff.html',{'country_list':country_list,'user_obj':user_obj})

            user = User.objects.get(id=staff_id)
            try:
                country = CountryDetails.objects.get(id=country)
                address = AddressDetails.objects.create(country=country, residential_address=residential_address)
                user.address = address
            except:
                pass
            user.role.clear()
            user.role.add(UserRole.objects.get(name=role))
            if faculty:
                user.faculty_id = faculty
            if program:
                user.program_id = program
            user.university_id = university
            user.email = email
            if password:
                user.set_password(password)
            user.username = email
            user.is_active = status
            user.save()



            system_check = any(item in system_settings_list for item in permission_list)
            user_check = any(item in user_settings_list for item in permission_list)
            university_check = any(item in university_settings_list for item in permission_list)
            academic_check = any(item in academic_settings_list for item in permission_list)
            module_check = any(item in module_settings_list for item in permission_list)
            if system_check is True:
                permission_list.append('System Settings')
            if user_check is True:
                permission_list.append('User Settings')
            if university_check is True:
                permission_list.append('University Settings')
            if academic_check is True:
                permission_list.append('Academic Settings')
            if module_check is True:
                permission_list.append('Application Settings')

            if permission_list:
                user.permission.clear()

            for rec in permission_list:
                permission_obj = PersmissionDetails.objects.create(permission=rec)
                user.permission.add(permission_obj)

            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/accounts/staff_settings/')
    # if user_obj.university:
    #     if user_obj.university.is_partner_university == False:
    #         university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,is_partner_university = False).order_by('-id')
    #     else:
    #         university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
    #                                                        is_partner_university=True).order_by('-id')
    # else:
    #     university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
    #                                                            is_partner_university=False).order_by('-id')
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                       university_type_id=user_obj.university.university_type.id).order_by(
        '-id')
    is_faculty = False
    if user_obj.role.all():
        if user_obj.role.all()[0].name == 'Faculty':
            is_faculty = True

    is_program = False
    if user_obj.role.all():
        if user_obj.role.all()[0].name == 'Program':
            is_program = True

    is_supervisor = False
    if user_obj.role.all():
        if user_obj.role.all()[0].name == 'Supervisor':
            is_supervisor = True

    faculty_list = []
    faculty_ids = []
    if is_faculty == True:
        if user_obj.university:
            faculty_recs = ProgramDetails.objects.filter(university_id=user_obj.university.id)
            for rec in faculty_recs:
                if not rec.faculty.id in faculty_ids:
                    raw_dict = {}
                    raw_dict['id'] = rec.faculty.id
                    raw_dict['faculty'] = rec.faculty.faculty_name
                    faculty_ids.append(rec.faculty.id)
                    faculty_list.append(raw_dict)

    program_list = []
    if is_program == True:
        if user_obj.university:
            program_recs = ProgramDetails.objects.filter(university_id=user_obj.university.id,is_delete=False)
            for rec in program_recs:
                raw_dict = {}
                raw_dict['id'] = rec.id
                raw_dict['program'] = rec.program_name
                program_list.append(raw_dict)

    supervisor_faculty_list = []
    supervisor_faculty_ids = []
    if is_supervisor == True:
        if user_obj.university:
            faculty_recs = ProgramDetails.objects.filter(university_id=user_obj.university.id)
            for rec in faculty_recs:
                if not rec.faculty.id in supervisor_faculty_ids:
                    raw_dict = {}
                    raw_dict['id'] = rec.faculty.id
                    raw_dict['faculty'] = rec.faculty.faculty_name
                    supervisor_faculty_ids.append(rec.faculty.id)
                    supervisor_faculty_list.append(raw_dict)

    supervisor_program_list = []
    program_recs = []
    if is_supervisor == True:
        if user_obj.faculty:
            program_recs = ProgramDetails.objects.filter(university_id=user_obj.university.id, faculty_id = user_obj.faculty_id,is_delete=False)
        for rec in program_recs:
            raw_dict = {}
            raw_dict['id'] = rec.id
            raw_dict['program'] = rec.program_name
            supervisor_program_list.append(raw_dict)

    university_type_recs = UniversityTypeDetails.objects.filter(status=True)

    user_obj = {
        'id': user_obj.id,
        # 'first_name': user_obj.first_name,
        # 'last_name': user_obj.last_name,
        'email': user_obj.email,
        'role': user_obj.role.all()[0].name,
        'country': user_obj.address.country.id if user_obj.address.country else None,
        'country_name': user_obj.address.country.country_name if user_obj.address.country else None,
        'residential_address': user_obj.address.residential_address if user_obj.address.country else None,
        'status': user_obj.is_active,
        'system_settings_list': system_settings_list,
        'user_settings_list': user_settings_list,
        'university_settings_list': university_settings_list,
        'academic_settings_list': academic_settings_list,
        'module_settings_list': module_settings_list,
        'permission_list':user_obj.permission.values_list('permission',flat=True),
        'university_recs':university_recs,
        'university':user_obj.university,
        'is_faculty':is_faculty,
        'faculty_id':user_obj.faculty.id if user_obj.faculty else None,
        'faculty':user_obj.faculty.faculty_name if user_obj.faculty else None,
        'faculty_list':faculty_list,
        'is_program':is_program,
        'program_id': user_obj.program.id if user_obj.program else None,
        'program': user_obj.program.program_name if user_obj.program else None,
        'program_list': program_list,
        'university_type_recs':university_type_recs,
        'is_supervisor':is_supervisor,
        'supervisor_program_list':supervisor_program_list,
        'supervisor_faculty_list':supervisor_faculty_list,

    }
    return render(request, "edit_staff.html", {'user_obj': user_obj,'country_list':country_list})


def get_user_permission(request):
    access_list = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            system_settings_list = ['Manage Language', 'Manage Currency', 'Manage Country', 'Manage Study Mode',
                                    'Manage Study Level', 'Manage Study Type', 'Manage Student Mode','Manage Learning Centers',
                                    'Manage Faculties', 'Link Faculty to User','System Settings']
            user_settings_list = ['Manage Group', 'Manage Users','User Settings']
            university_settings_list = ['Manage Universities', 'Manage University Partner', 'Link University to User',
                                        'Manage Program','Manage Program Fee', 'Manage Campus', 'Link Campus to User', 'Manage Department',
                                        'Link Department to User','University Settings']
            academic_settings_list = ['Manage Year', 'Manage Semester', 'Manage Activity', 'Manage Calendar','Academic Settings']
            module_settings_list = ['Manage Applicant Documents', 'Approving Applicant Details','Payment Settings','Application Settings']
            access_list = system_settings_list + user_settings_list + university_settings_list + academic_settings_list + module_settings_list
        else:
            access_list = request.user.permission.values_list('permission', flat=True)
    return {'access_list': access_list}

def get_email_exists(request):
    user_id = request.POST.get('user_id', None)
    email = request.POST.get('email', None)
    email_exists = False
    if user_id:
        if User.objects.filter(email=email.strip()).exclude(id = user_id).exists():
            email_exists = True
        else:
            email_exists = False
        return JsonResponse(email_exists, safe=False)
    else:
        if User.objects.filter(email=email.strip()).exists():
            email_exists = True
        else:
            email_exists = False
        return JsonResponse(email_exists, safe=False)



def get_university_exists(request):
    user_id = request.POST.get('user_id', None)
    university = request.POST.get('university', None)
    university_exists = False
    if user_id:
        if User.objects.filter(university_id=university.strip()).exclude(id = user_id).exists():
            university_exists = True
        else:
            university_exists = False
        return JsonResponse(university_exists, safe=False)
    else:
        if User.objects.filter(university_id=university.strip()).exists():
            university_exists = True
        else:
            university_exists = False
        return JsonResponse(university_exists, safe=False)



def get_faculty_from_account_type(request):
    faculty_list = []
    faculty_ids = []
    account_type = request.POST.get('account_type', None)
    university = request.POST.get('university', None)
    faculty_recs = ProgramDetails.objects.all()
    if university:
        faculty_recs = faculty_recs.filter(university_id = university)
        for rec in faculty_recs:
            if not rec.faculty.id in faculty_ids:
                raw_dict = {}
                raw_dict['id'] = rec.faculty.id
                raw_dict['faculty'] = rec.faculty.faculty_name
                faculty_ids.append(rec.faculty.id)
                faculty_list.append(raw_dict)
        return JsonResponse(faculty_list, safe=False)
    else:
        return JsonResponse(faculty_list, safe=False)

def get_program_from_account_type(request):
    program_list = []
    account_type = request.POST.get('account_type', None)
    university = request.POST.get('university', None)
    program_recs = ProgramDetails.objects.filter(is_delete=False).order_by('-id')
    if university:
        program_recs = program_recs.filter(university_id = university)
        for rec in program_recs:
            raw_dict = {}
            raw_dict['id'] = rec.id
            raw_dict['program'] = rec.program_name
            program_list.append(raw_dict)
        return JsonResponse(program_list, safe=False)
    else:
        return JsonResponse(program_list, safe=False)

def get_working_experience(request):
    form_vals = {}
    if request.user.role.all().filter(name__in=[request.user.STUDENT]).exists():
        try:
            applicaton_obj = request.user.student_user_rel.get().student_applicant_rel.get(year__active_year=True)
            form_vals['working_experience'] = True if applicaton_obj.employement_history_rel.all() else False
            return form_vals
        except:
            form_vals['working_experience'] = False
            return form_vals
    else:
        return None


def get_program_from_faculty(request):
    program_list = []
    account_type = request.POST.get('account_type', None)
    university = request.POST.get('university', None)
    faculty_id = request.POST.get('faculty_id', None)
    program_recs = ProgramDetails.objects.filter(is_delete=False).order_by('-id')
    if faculty_id:
         program_recs = ProgramDetails.objects.filter(faculty_id = faculty_id).order_by('-id')
    if university:
        program_recs = program_recs.filter(university_id = university)
        for rec in program_recs:
            raw_dict = {}
            raw_dict['id'] = rec.id
            raw_dict['program'] = rec.program_name
            program_list.append(raw_dict)
        return JsonResponse(program_list, safe=False)
    else:
        return JsonResponse(program_list, safe=False)

def agent_login(request):
    country_list = CountryDetails.objects.all()
    is_agent = True
    form = loginForm()
    if request.user.is_authenticated:
        dashboard_path = request.user.get_dashboard_path()
        return redirect(dashboard_path)
    context = {
        'form':form,
        'country_list':country_list,
        'is_agent':is_agent,
    }
    return render(request, "template_login.html",context)


def tanseeq_student_login(request):
    is_tanseeq_student = True
    form = loginForm()
    if request.user.is_authenticated:
        dashboard_path = request.user.get_dashboard_path()
        return redirect(dashboard_path)
    context = {
        'form':form,
        'is_tanseeq_student':is_tanseeq_student,
    }
    return render(request, "template_login.html",context)



def edit_agent(request, agent_id=None):
    user_obj = User.objects.get(id = agent_id)
    agent_obj = ''
    if AgentIDDetails.objects.filter(user_id = agent_id).exists():
        agent_obj = AgentIDDetails.objects.get(user_id = agent_id)
    if request.method == 'POST':
        photo = request.FILES.get('photo',None)
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name',None)
        agent_email = request.POST.get('agent_email',None)

        if User.objects.filter(email = agent_email).exclude(id = user_obj.id).exists():
            messages.warning(request, "Email already exists.")
            return redirect('/accounts/edit_agent/'+str(agent_id))
        if AgentAttachementDetails.objects.filter(agent_profile_id=agent_obj.id).exists():
            attachment_obj = AgentAttachementDetails.objects.get(agent_profile_id=agent_obj.id)
        else:
            if (photo is not None):
                attachment_obj = AgentAttachementDetails.objects.create(agent_profile_id=agent_obj.id)
        if photo:
            attachment_obj.image = photo
            attachment_obj.save()
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.username = agent_email
        user_obj.email = agent_email
        user_obj.save()
        messages.success(request, "Record saved.")
        return redirect('/accounts/edit_agent/'+str(agent_id))
    else:
        context = {}
        if request.user.is_agent():
            context['my_template'] = 'template_agent_base.html'
        else:
            context['my_template'] = 'template_base_page.html'
        attachment_obj = None
        if AgentAttachementDetails.objects.filter(agent_profile_id=agent_obj.id).exists():
            attachment_obj = AgentAttachementDetails.objects.get(agent_profile_id=agent_obj.id)
        context['agent_id'] = agent_id
        context['user_obj'] = user_obj
        context['agent_obj'] = agent_obj
        context['attachment_obj'] = attachment_obj
        return render(request, "agent_details.html",context)


def agent_recruiter_settings(request):
    context = {
        'agent_recruiter_recs': User.objects.filter(role__name = 'Agent Recruiter')
    }
    return render(request, 'agent_recruiter_settings.html',context)


def add_agent_recruiter(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email', None)
            country = request.POST.get('country', None)
            role = request.POST.get('role', None)
            password = request.POST.get('password', None)
            address = request.POST.get('address', None)
            status = request.POST.get('status')
            if status == 'on':
                status = True
            else:
                status = False
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists.")
                return redirect('/accounts/agent_recruiter_settings/')

            user_obj = User.objects.create(email=email, username=email, password=make_password(password), is_active=status)
            user_obj.role.add(UserRole.objects.get(name=role))
            country = CountryDetails.objects.get(id=country)
            address = AddressDetails.objects.create(country=country, residential_address=address)
            user_obj.address = address
            user_obj.save()
            messages.success(request, "Record saved.")
            return redirect('/accounts/agent_recruiter_settings/')
        except Exception as e:
            messages.warning(request, str(e.args[0]))
            return redirect('/accounts/agent_recruiter_settings/')
    else:
        context = {
            'country_list': CountryDetails.objects.all(),
        }
        return render(request, 'add_agent_recruiter.html',context)


def edit_agent_recruiter(request, recruiter_id=None):
    user_obj = User.objects.get(id=recruiter_id)
    if request.method == 'POST':
        try:
            email = request.POST.get('email', None)
            country = request.POST.get('country', None)
            role = request.POST.get('role', None)
            password = request.POST.get('password', None)
            address = request.POST.get('address', None)
            status = request.POST.get('status')
            if status == 'on':
                status = True
            else:
                status = False
            if User.objects.filter(email=email).exclude(id = user_obj.id).exists():
                messages.warning(request, "Email already exists.")
                return redirect('/accounts/agent_recruiter_settings/')
            user_obj.email = email
            user_obj.username = email
            user_obj.is_active = status
            user_obj.email = email
            if password:
                user_obj.set_password(password)
            country = CountryDetails.objects.get(id=country)
            address = AddressDetails.objects.create(country=country, residential_address=address)
            user_obj.address = address
            user_obj.save()
            messages.success(request, "Record saved.")
            return redirect('/accounts/agent_recruiter_settings/')
        except Exception as e:
            messages.warning(request, str(e.args[0]))
            return redirect('/accounts/agent_recruiter_settings/')
    else:
        context = {
            'country_list': CountryDetails.objects.all(),
            'user_obj': user_obj,
        }
        return render(request, 'edit_agent_recruiter.html', context)