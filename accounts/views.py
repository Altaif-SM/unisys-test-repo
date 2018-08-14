from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from accounts.decoratars import user_login_required, registration_required
from accounts.forms import loginForm, signUpForm
from accounts.service import *
from accounts.models import UserRole
from student.models import StudentDetails, ApplicationDetails, ScholarshipSelectionDetails
from masters.models import AddressDetails, CountryDetails, ScholarshipDetails, GuardianDetails, EmailTemplates, \
    YearDetails
from partner.models import PartnerDetails
from donor.models import DonorDetails
import json
from common.utils import *
from accounts.service import UserService


# Create your views here.

def index(request):
    return render(request, "index.html")


@user_login_required
def home(request):
    if request.user.is_authenticated:
        user = request.user

        raw_list = []

        if request.user.is_super_admin():

            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=False,
                                                              second_interview_approval=False, psychometric_test=False,
                                                              admin_approval=False, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=False, psychometric_test=False,
                                                              admin_approval=False, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=True, psychometric_test=False,
                                                              admin_approval=False, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=True, psychometric_test=True,
                                                              admin_approval=False, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=True, psychometric_test=True,
                                                              admin_approval=True, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=True, psychometric_test=True,
                                                              admin_approval=True, is_sponsored=True).count())
            raw_list.append(ApplicationDetails.objects.filter().count())

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
                raw_dict['country_name'] = country.country_name
                raw_dict['country_count'] = ApplicationDetails.objects.filter(address__country=country).count()

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
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=False,
                                                              second_interview_approval=False, psychometric_test=False,
                                                              admin_approval=False, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=False, psychometric_test=False,
                                                              admin_approval=False, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=True, psychometric_test=False,
                                                              admin_approval=False, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=True, psychometric_test=True,
                                                              admin_approval=False, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=True, psychometric_test=True,
                                                              admin_approval=True, is_sponsored=False).count())
            raw_list.append(ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                              second_interview_approval=True, psychometric_test=True,
                                                              admin_approval=True, is_sponsored=True).count())
            raw_list.append(ApplicationDetails.objects.filter().count())

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
                raw_dict['country_name'] = country.country_name
                raw_dict['country_count'] = ApplicationDetails.objects.filter(address__country=country).count()

                country_list.append(raw_dict)

        # if user.is_superuser:
        return render(request, "template_admin_dashboard.html",
                      {'user': user, 'raw_list': raw_list, 'scholarship_list': json.dumps(scholarship_list),
                       'country_list': json.dumps(country_list)})


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
                        # student_obj = StudentDetails.objects.create(user=user, address=address)
                        user.is_active = False
                        user.save()
                        student_obj = StudentDetails.objects.create(user=user)

                        # try:
                        #     email_rec = EmailTemplates.objects.get(template_for='Student Signup', is_active=True)
                        #     context = {'first_name': student_obj.user.first_name}
                        #     send_email_with_template(student_obj, context, email_rec.subject, email_rec.email_body,
                        #                              request, True)
                        # except:

                        subject = 'Signup Completed'
                        message = 'Your signup completed in NAMA. Please click on the given button to activate your account.'
                        send_signup_email_to_applicant(student_obj.user.email, student_obj.user.email, subject,
                                                           message,
                                                           student_obj.user.first_name, user.id)

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
            return redirect('/')
        else:
            # print(signup_form.errors)
            for error_msg in signup_form.errors:
                # form = signUpForm()
                for msg in signup_form.errors[error_msg]:
                    messages.success(request, msg)
        if request.POST.get('admin_page'):
            return redirect('/accounts/template_manage_user/')
        return redirect('/')
        # return render(request, 'template_manage_user.html', {'form': signup_form})
        # return render(request, 'template_login.html', {'form': signup})


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
        user = form.login(request)

        if user:
            login(request, user)
            dashboard_path = user.get_dashboard_path()
            return redirect(dashboard_path)
        else:
            messages.success(request, "Enter Valid User Name and Password.")
            return redirect('/')


        # if user:
        #     if user.is_active:
        #         login(request, user)
        #         dashboard_path = user.get_dashboard_path()
        #         return redirect(dashboard_path)
        #     else:
        #         messages.success(request,
        #                          "Please activate your account first. Activation link has been sent to your email " + str(
        #                              user.email) + '.')
        #         return redirect('/')
        # else:
        #     messages.success(request, "Enter Valid User Name and Password.")
        #     return redirect('/')


@user_login_required
def user_signout(request):
    logout(request)
    return redirect('/')


def template_manage_user(request):
    country_list = CountryDetails.objects.all()
    user_recs = User.objects.filter().exclude(role__name='Admin')
    return render(request, 'template_manage_user.html',
                  {'country_list': country_list, 'user_recs': user_recs})


def account_activate(request,user_id):
    # user_id = request.POST.get('user_id')

    try:
        user_rec = User.objects.get(id=user_id)

        if not user_rec.is_active:

            User.objects.filter(id=user_id).update(is_active=True)
            messages.success(request, "Account activated. You can login now.")
        else:
            messages.warning(request, "Account already activated. You can login now.")
    except:
        messages.warning(request, "Invalid operation.")
    return redirect('/')


def update_switch(request):
    if request.method == 'POST':
        val_dict = request.POST
        if request.user.is_superuser:
            if 'switch_type' in val_dict and val_dict['switch_type'] == 'is_registration_switch':
                User.objects.filter().update(registration_switch=(json.loads(val_dict['switch'])))

            if 'switch_type' in val_dict and val_dict['switch_type'] == 'is_submission_switch':
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
