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
    YearDetails
from partner.models import PartnerDetails
from donor.models import DonorDetails
import json
from common.utils import *
from django.template.context_processors import csrf
from accounts.service import UserService
from datetime import date
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

                        messages.info(request,"The activation link is sent to your email id ... ")

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
                    messages.error(request, msg)
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
            messages.error(request, "Enter Valid User Name and Password.")
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
            return render(request, 'template_change_password.html', context)
    else:
        context = {}
        context.update(csrf(request))
        form = ChangePasswordForm()
        context['form'] = form
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
    return redirect('/accounts/template_manage_user')


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