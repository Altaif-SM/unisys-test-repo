from django.shortcuts import render, redirect
from masters.views import *
from agents.models import *
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from common.utils import get_application_id
from payments.models import *
from django.views import View
import stripe
from accounts.decoratars import student_login_required, psycho_test_required, semester_required, registration_required, \
    dev_program_required, agreements_required, submission_required
import os
import shutil
from django.contrib.auth.hashers import make_password
import datetime
import uuid
import binascii
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import cgi, html
cgi.escape = html.escape

def dashboard(request):
    try:
        del request.session['form_data']
    except:
        pass
    agent_obj = AgentIDDetails.objects.get(user=request.user)
    history_recs = AgentProfileHistoryDetails.objects.filter(agent_id=agent_obj.id)
    context = {
        'history_recs':history_recs
    }
    return render(request, 'agent_dashboard.html',context)

# Create your views here.
def personal_info(request):
    if request.method == 'POST':
        try:
            agent_id = request.POST.get('agent_id', None)
            first_name = request.POST.get('first_name',None)
            last_name = request.POST.get('last_name',None)
            mobile = request.POST.get('mobile',None)
            country_code = request.POST.get('country_code',None)
            whats_app = request.POST.get('whats_app',None)
            country = request.POST.get('country',None)
            nationality = request.POST.get('nationality',None)
            post_code = request.POST.get('post_code',None)
            address_line_1 = request.POST.get('address_line_1',None)
            address_line_2 = request.POST.get('address_line_2',None)
            city = request.POST.get('city',None)
            agent_obj = AgentIDDetails.objects.get(agent_id= agent_id)
            agent_obj.user.first_name = first_name
            agent_obj.user.last_name = last_name
            agent_obj.mobile = mobile
            agent_obj.country_code = country_code
            agent_obj.whats_app = whats_app
            agent_obj.country_id = country
            agent_obj.nationality_id = nationality
            agent_obj.post_code = post_code
            agent_obj.address_line_1 = address_line_1
            agent_obj.address_line_2 = address_line_2
            agent_obj.city = city
            agent_obj.save()
            messages.success(request, "Record saved")
            return redirect('/agents/corporate_info/')
        except:
            return redirect('/agents/personal_info/')
    else:
        try:
            del request.session['form_data']
        except:
            pass
        context = {
            'country_recs':CountryDetails.objects.all(),
            'agent_obj':AgentIDDetails.objects.get(user=request.user)

        }
        return render(request,'agent_personal_info.html',context)

def corporate_info(request):
    agent_obj = AgentIDDetails.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            agent_id = request.POST.get('agent_id', None)
            company_name = request.POST.get('company_name',None)
            company_registration_no = request.POST.get('company_registration_no',None)
            email = request.POST.get('email',None)
            country = request.POST.get('country',None)
            telephone = request.POST.get('telephone',None)
            website_url = request.POST.get('website_url',None)
            address = request.POST.get('address',None)
            if CorporateDetails.objects.filter(agent_profile_id = agent_id).exists():
                CorporateDetails.objects.filter(agent_profile_id = agent_id).update(
                    company_name=company_name,
                    company_registration_no=company_registration_no,
                    email=email,
                    country_id=country,
                    telephone=telephone,
                    website_url=website_url,
                    address=address,
                )
            else:
                CorporateDetails.objects.create(agent_profile_id = agent_id,
                                                company_name = company_name,
                                                company_registration_no = company_registration_no,
                                                email = email,
                                                country_id = country,
                                                telephone = telephone,
                                                website_url = website_url,
                                                address = address,
                                                )
            messages.success(request, "Record saved")
            # return redirect('/payments/payment_details/'+str(agent_obj.user.id))
            return redirect('/agents/attachment/')
        except:
            return redirect('/agents/corporate_info/')

    else:
        corporate_obj = None
        if CorporateDetails.objects.filter(agent_profile_id = agent_obj.id).exists():
            corporate_obj = CorporateDetails.objects.get(agent_profile_id = agent_obj.id)
        context = {
            'country_recs':CountryDetails.objects.all(),
            'corporate_obj':corporate_obj,
            'agent_obj':agent_obj
        }
        return render(request,'corporate_info.html',context)


def attachment(request):
    agent_obj = AgentIDDetails.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            passport_photo = request.FILES.get('passport_photo')
            photo = request.FILES.get('photo')
            company_registration = request.FILES.get('company_registration')
            license_certificate = request.FILES.get('license_certificate')
        except:
            passport_photo = ''
            photo = ''
            company_registration = ''
            license_certificate = ''

        try:

            if AgentAttachementDetails.objects.filter(agent_profile_id=agent_obj.id).exists():
                attachment_obj = AgentAttachementDetails.objects.get(agent_profile_id=agent_obj.id)
            else:
                if (passport_photo is not None) or (photo is not None) or (company_registration is not None) or (license_certificate is not None):
                    attachment_obj = AgentAttachementDetails.objects.create(agent_profile_id=agent_obj.id)

            if passport_photo:
                attachment_obj.passport_image = passport_photo
                attachment_obj.save()

            if photo:
                attachment_obj.image = photo
                attachment_obj.save()

            if company_registration:
                attachment_obj.company_registration = company_registration
                attachment_obj.save()

            if license_certificate:
                attachment_obj.license_certificate = license_certificate
                attachment_obj.save()

            messages.success(request, "Attachment submitted successfully.")
            return redirect('/agents/declaration/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))
        return redirect('/agents/attachment/')

    else:
        attachment_obj = None
        if AgentAttachementDetails.objects.filter(agent_profile_id = agent_obj.id).exists():
            attachment_obj = AgentAttachementDetails.objects.get(agent_profile_id = agent_obj.id)
        context = {
            'attachment_obj':attachment_obj,
            'agent_obj':agent_obj
        }
        return render(request,'attachement.html',context)

def declaration(request):
    agent_obj = AgentIDDetails.objects.get(user=request.user)
    first_name = agent_obj.user.first_name
    last_name = agent_obj.user.last_name
    if request.method == 'POST':
        try:
            AgentIDDetails.objects.filter(id = agent_obj.id).update(is_submitted = True)
            AgentProfileHistoryDetails.objects.create(agent_id=agent_obj.id,
                                                     status='Application Submitted',
                                                     remark='Hi, ' + first_name + ' ' + last_name + ' your application is submitted and AGENT RECRUITER  will be notified on further updates regarding your applications.')

            messages.success(request, "Record saved")
            return redirect('/agents/dashboard/')
        except:
            return redirect('/agents/declaration/')
    else:
        context = {
            'agent_obj':agent_obj
        }
        return render(request,'declaration.html',context)


def recruiter_dashboard(request):
    history_recs = AgentProfileHistoryDetails.objects.filter(agent_recruiter_id = request.user.id)
    context = {
        'history_recs': history_recs
    }
    return render(request, 'recruiter_dashboard.html',context)


def recruiter_approved_application(request):
    if request.method == 'POST':
        try:
            check_ids = json.loads(request.POST.get('check_ids'))
            recruiter_type = request.POST.get('recruiter_type',None)
            reject_comment = request.POST.get('reject_comment',None)
            for agent_id in check_ids:
                if request.user.is_agent_recruiter():
                    agent_obj = AgentIDDetails.objects.get(id=agent_id)
                    if recruiter_type == 'APPROVED':
                        agent_obj.application_status = 'APPROVED'
                        agent_obj.save()
                        AgentProfileHistoryDetails.objects.create(agent_id=agent_obj.id,
                                                                  status=recruiter_type,
                                                                  remark='Hi, ' + agent_obj.user.first_name + ' ' + agent_obj.user.last_name + ' your application has been APPROVED by AGENT RECRUITER.')

                        AgentProfileHistoryDetails.objects.create(agent_recruiter_id=request.user.id,
                                                                  status=recruiter_type,
                                                                  remark=agent_obj.user.first_name + ' ' + agent_obj.user.last_name + ' application has been ' + recruiter_type + ' .')
                        messages.success(request, agent_obj.user.first_name.title() + " application status changed.")

                        messages.success(request,agent_obj.user.first_name.title() + " application status changed.")
                    elif recruiter_type == 'REJECTED':
                        agent_obj.application_status = 'REJECTED'
                        agent_obj.reject_comment = reject_comment
                        agent_obj.save()
                        AgentProfileHistoryDetails.objects.create(agent_id=agent_obj.id,
                                                                  status=recruiter_type,
                                                                  remark='Hi, ' + agent_obj.user.first_name + ' ' + agent_obj.user.last_name + ' your application has been REJECTED by AGENT RECRUITER.')

                        AgentProfileHistoryDetails.objects.create(agent_recruiter_id=request.user.id,
                                                                  status=recruiter_type,
                                                                  remark= agent_obj.user.first_name + ' ' + agent_obj.user.last_name + ' application has been ' + recruiter_type + ' .')
                        messages.success(request, agent_obj.user.first_name.title() + " application status changed.")
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))
        return redirect('/agents/recruiter_approved_application/')
    else:
        context = {
            'agent_recs':AgentIDDetails.objects.filter(is_submitted= True)
        }
        return render(request, 'recruiter_approved_application.html', context)

def agent_application_details(request, agent_id):
    agent_obj = AgentIDDetails.objects.get(id=agent_id)
    attachement_details = agent_obj.attachement_agent_rel.get() if agent_obj.attachement_agent_rel.all() else None
    corporate_details = agent_obj.corporate_agent_rel.get() if agent_obj.corporate_agent_rel.all() else None
    payment_agent_details = True if agent_obj.payment_agent_rel.all() else False
    context = {
        'agent_obj': agent_obj,
        'attachement_details': attachement_details,
        'corporate_details': corporate_details,
        'payment_agent_details': payment_agent_details,
    }
    return render(request, 'agent_application_details.html', context)


def referral_fee_topup(request):
    accepted_applicants = ''
    context = {}
    try:
        if request.user.is_agent():
            accepted_applicants = ApplicationDetails.objects.filter(is_submitted=True, agent_id = request.user.id,
                                                                    year=get_current_year(request),
                                                                    )
            context['my_template'] = 'template_agent_base.html'
        else:
            accepted_applicants = ApplicationDetails.objects.filter(is_submitted=True,
                                                                 year=get_current_year(request), is_accepted=True,
                                                                 ).exclude(is_offer_accepted = True)
            context['my_template'] = 'template_base_page.html'

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return render(request, 'referral_fee_topup.html',{'accepted_applicants': accepted_applicants,'context':context})

def applicant_personal_info(request, user_id):
    country_recs = CountryDetails.objects.all()
    religion_recs = ReligionDetails.objects.all()
    student_recs = StudentDetails.objects.filter(user__is_active = True)
    agent_recs = AgentDetails.objects.filter()
    application_obj = ''
    agent_obj = ''
    session_email = None

    if ApplicationDetails.objects.filter(student__user_id = user_id).exists():
        user_obj = User.objects.get(id = user_id)
        if user_obj.is_student():
            session_email = user_obj.email
            request.session['form_data'] = {'email': user_obj.email}
    else:
        if request.session.get('form_data'):
            form_data = request.session.get('form_data')
            session_email = form_data.get('email')



    if User.objects.filter(email=session_email).exists():
        user = User.objects.get(email=session_email)
    else:
        user = None

    if ApplicationDetails.objects.filter(email=session_email).exists():
        application_obj = ApplicationDetails.objects.get(email=session_email)
        if application_obj.agent_id:
            agent_obj = AgentIDDetails.objects.get(user_id=request.user.id)
    context = {
        'country_recs':country_recs,
        'religion_recs':religion_recs,
        'application_obj':application_obj,
        'student_recs':student_recs,
        'agent_recs':agent_recs,
        'agent_obj':agent_obj,
        'user':user,
    }
    return render(request, 'agent_applicant_personal_info.html',context )

def save_update_applicant_personal_info(request):
    redirect_flag = False
    if request.POST:
        request.session['form_data'] = request.POST
        if request.session.get('form_data'):
            form_data = request.session.get('form_data')
            session_email = form_data.get('email')

        if not User.objects.filter(email = session_email).exists():
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                                       username=request.POST['email'], email=request.POST['email'],
                                       password=make_password('123456'), is_active=True,
                                       registration_switch=True, submission_switch=True, psyc_switch=True,
                                       agreements_switch=True, semester_switch=True, program_switch=True)
            user.role.add(UserRole.objects.get(name='Student'))
            StudentDetails.objects.create(user=user)
        else:
            user = User.objects.get(email = session_email)
        if StudentDetails.objects.filter(user=user):
            student = StudentDetails.objects.get(user=user)
            if request.POST['first_name'] and request.POST['passport_number']:
                if ApplicationDetails.objects.filter(application_id=user.get_application_id).exists():
                    ApplicationDetails.objects.filter(application_id=user.get_application_id).update(
                        first_name=request.POST['first_name'],
                        middle_name=request.POST['middle_name'],
                        last_name=request.POST['last_name'],
                        surname=request.POST['surname'],
                        passport_number=request.POST.get('passport_number'),
                        email=request.POST['email'],
                        agent_id = request.user.id)
                    application_obj = ApplicationDetails.objects.get(application_id=user.get_application_id)
                    if application_obj.address:
                        AddressDetails.objects.filter(id=application_obj.address.id).update(
                            country_id=request.POST['country'],
                            nationality_id=request.POST['nationality'],
                            mobile=request.POST['mobile'],
                            whats_app=request.POST['whats_app'],
                            country_code=request.POST['country_code'],
                            district=request.POST['district'],
                            post_code=request.POST['post_code'],
                            residential_address=request.POST['permanent_residential_address'],
                            street=request.POST['permanent_street'])
                    else:
                        address_obj = AddressDetails.objects.create(country_id=request.POST['country'],
                                                                    nationality_id=request.POST['nationality'],
                                                                    mobile=request.POST['mobile'],
                                                                    whats_app=request.POST['whats_app'],
                                                                    country_code=request.POST['country_code'],
                                                                    district=request.POST['district'],
                                                                    post_code=request.POST['post_code'],
                                                                    residential_address=request.POST[
                                                                        'permanent_residential_address'],
                                                                    street=request.POST['permanent_street'])
                        application_obj.address = address_obj
                    application_obj.save()
                    redirect_flag = True
                else:
                    try:
                        current_year = YearDetails.objects.get(active_year=True)
                        application_obj = ApplicationDetails.objects.create(first_name=request.POST['first_name'],
                                                                            middle_name=request.POST['middle_name'],
                                                                            last_name=request.POST['last_name'],
                                                                            surname=request.POST['surname'],
                                                                            passport_number=request.POST.get('passport_number'),
                                                                            email=request.POST['email'],
                                                                            student=student,
                                                                            year=current_year,
                                                                            agent_id = request.user.id)
                        application_id = get_application_id(application_obj)
                        application_obj.application_id = application_id
                        application_obj.save()
                        address_obj = AddressDetails.objects.create(country_id=request.POST['country'],
                                                                    nationality_id=request.POST['nationality'],
                                                                    mobile=request.POST['mobile'],
                                                                    whats_app=request.POST['whats_app'],
                                                                    country_code=request.POST['country_code'],
                                                                    district=request.POST['district'],
                                                                    post_code=request.POST['post_code'],
                                                                    residential_address=request.POST['permanent_residential_address'],
                                                                    street=request.POST['permanent_street'])

                        application_obj.progress_counter = 20
                        application_obj.address = address_obj
                        application_obj.save()
                        redirect_flag = True
                    except Exception as e:
                        messages.warning(request, "Form have some error" + str(e))
                try:
                    application_obj.save()
                except Exception as e:
                    messages.warning(request, "Form have some error" + str(e))
            else:
                messages.success(request, "Please fill mandatory fields")
                if user:
                    return redirect('/agents/applicant_personal_info/' + str(user.id))
                else:
                    return redirect('/agents/applicant_personal_info/' + str(request.user.id))

    if redirect_flag:
        messages.success(request, "Record saved")
        return redirect('/agents/applicant_intake_info/')
    else:
        messages.warning(request, "Please fill proper form")
        if user:
            return redirect('/agents/applicant_personal_info/'+str(user.id))
        else:
            return redirect('/agents/applicant_personal_info/'+str(request.user.id))

def applicant_intake_info(request):
    religion_recs = ReligionDetails.objects.all()
    student_recs = StudentDetails.objects.filter(user__is_active = True)
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    type_recs = TypeDetails.objects.filter(status=True).exclude(type__in = ['Community Colleage', 'Colleage'])
    year_recs = ''
    semester_recs = ''
    university_recs =''
    program_recs = ProgramDetails.objects.filter(is_delete=False).order_by('-id')
    faculty_recs = FacultyDetails.objects.filter(status=True).order_by('-id')
    study_type_list = ['International', 'University Main']
    study_mode_list = StudyTypeDetails.objects.all()
    study_mode_list_2 = StudyTypeDetails.objects.filter().exclude(study_type = 'Research')
    study_mode_list_3 = StudyTypeDetails.objects.filter().exclude(study_type = 'Research')
    study_level_list = ['Undergraduate', 'Postgraduate']
    study_type_recs = StudyTypeDetails.objects.all()
    study_level_recs = StudyLevelDetails.objects.filter().order_by('-id')
    study_level_recs_2 = StudyLevelDetails.objects.filter().order_by('-id')
    study_level_recs_3 = StudyLevelDetails.objects.filter().order_by('-id')

    session_email = None
    if request.session.get('form_data'):
        form_data = request.session.get('form_data')
        session_email = form_data.get('email')

    if User.objects.filter(email=session_email).exists():
        user = User.objects.get(email=session_email)
    else:
        user = None

    try:
        application_obj = user.get_application
    except Exception as e :
        messages.warning(request, "Please fill the personal details first.")
        if user:
            return redirect('/agents/applicant_personal_info/'+str(user.id))
        else:
            return redirect('/agents/applicant_personal_info/'+str(request.user.id))

    agent_recs = AgentDetails.objects.filter()

    application_obj = ''
    learning_centre_list = []
    campus_list = []
    department_recs = []
    department_2_recs = []
    department_3_recs = []

    faculty_final_list = []
    faculty_list = []
    faculty_ids = []

    faculty_2_final_list = []
    faculty_2_list = []
    faculty_2_ids = []

    faculty_3_final_list = []
    faculty_3_list = []
    faculty_3_ids = []



    program_final_list = []
    program_list = []

    program_2_final_list = []
    program_2_list = []

    program_3_final_list = []
    program_3_list = []

    country_recs = []
    duplicate_country_ids = []

    learning_centre_recs = []
    research_details = ''
    supervisor_list = ''
    attachment_obj = None
    if ApplicantAttachementDetails.objects.filter(applicant_id=user.get_application).exists():
        attachment_obj = ApplicantAttachementDetails.objects.get(applicant_id=user.get_application)

    country_recs = CountryDetails.objects.all()
    if not user == None :
        if ApplicationDetails.objects.filter(application_id=user.get_application_id).exists():
            application_obj = ApplicationDetails.objects.get(application_id=user.get_application_id)
            if application_obj.faculty:
                 department_recs = application_obj.faculty.department.all()

            if application_obj.faculty_2:
                 department_2_recs = application_obj.faculty_2.department.all()

            if application_obj.faculty_3:
                 department_3_recs = application_obj.faculty_3.department.all()

    if application_obj:

        if ResearchDetails.objects.filter(application_id=user.get_application).exists():
            research_details = ResearchDetails.objects.get(application_id=user.get_application)

        if research_details:
            role_name_list = ['Supervisor']
            users_recs = User.objects.filter(role__name__in=role_name_list)
            if application_obj.university:
                supervisor_list = users_recs.filter(university_id=application_obj.university.id, role__name__in=role_name_list)
            if application_obj.faculty:
                supervisor_list = users_recs.filter(faculty_id=application_obj.faculty.id, role__name__in=role_name_list)
            if application_obj.program:
                supervisor_list = users_recs.filter(program_id=application_obj.program.id, role__name__in=role_name_list)

        program_recs = ProgramDetails.objects.filter(is_delete=False)
        if application_obj.program_mode:
            program_recs = program_recs.filter(study_type_id=application_obj.program_mode.id,study_level_id=application_obj.study_level.id)
            for rec in program_recs:
                faculty_list.append(rec)

        program_recs_2 = ProgramDetails.objects.filter(is_delete=False)
        if application_obj.program_mode_2:
            program_recs_2 = program_recs_2.filter(study_type_id=application_obj.program_mode_2.id,study_level_id=application_obj.study_level.id)
            for rec in program_recs_2:
                faculty_2_list.append(rec)

        program_recs_3 = ProgramDetails.objects.filter(is_delete=False)
        if application_obj.program_mode_3:
            program_recs_3 = program_recs_3.filter(study_type_id=application_obj.program_mode_3.id,study_level_id=application_obj.study_level.id)
            for rec in program_recs_3:
                faculty_3_list.append(rec)


        if faculty_list:
            for rec in faculty_list:
                if not rec.faculty.id in faculty_ids:
                    raw_dict = {}
                    if application_obj.university.id == rec.university.id:
                        raw_dict['id'] = rec.faculty.id
                        raw_dict['faculty'] = rec.faculty.faculty_name
                        faculty_ids.append(rec.faculty.id)
                        faculty_final_list.append(raw_dict)

        if faculty_2_list:
            for rec in faculty_2_list:
                if not rec.faculty.id in faculty_2_ids:
                    raw_dict = {}
                    if application_obj.university.id == rec.university.id:
                        raw_dict['id'] = rec.faculty.id
                        raw_dict['faculty'] = rec.faculty.faculty_name
                        faculty_2_ids.append(rec.faculty.id)
                        faculty_2_final_list.append(raw_dict)

        if faculty_3_list:
            for rec in faculty_3_list:
                if not rec.faculty.id in faculty_3_ids:
                    raw_dict = {}
                    if application_obj.university.id == rec.university.id:
                        raw_dict['id'] = rec.faculty.id
                        raw_dict['faculty'] = rec.faculty.faculty_name
                        faculty_3_ids.append(rec.faculty.id)
                        faculty_3_final_list.append(raw_dict)


        program_recs = ProgramDetails.objects.filter(is_delete=False)
        if application_obj.university:
            program_recs = program_recs.filter(university_id=application_obj.university.id)

        if application_obj.program_mode:
            program_recs = program_recs.filter(study_type_id=application_obj.program_mode.id)

        if application_obj.faculty:
            program_recs = program_recs.filter(faculty_id=application_obj.faculty.id)

        for rec in program_recs:
            try:
                raw_dict = {}
                raw_dict['id'] = rec.id
                raw_dict['program'] = rec.program_name
                program_final_list.append(raw_dict)
            except:
                pass

        program_2_recs = ProgramDetails.objects.filter(is_delete=False)
        if application_obj.university:
            program_2_recs = program_2_recs.filter(university_id=application_obj.university.id)

        if application_obj.program_mode_2:
            program_2_recs = program_2_recs.filter(study_type_id=application_obj.program_mode_2.id)

        if application_obj.faculty_2:
            program_2_recs = program_2_recs.filter(faculty_id=application_obj.faculty_2.id)

        for rec in program_2_recs:
            try:
                raw_dict = {}
                raw_dict['id'] = rec.id
                raw_dict['program'] = rec.program_name
                program_2_final_list.append(raw_dict)
            except:
                pass

        program_3_recs = ProgramDetails.objects.filter(is_delete=False)
        if application_obj.university:
            program_3_recs = program_3_recs.filter(university_id=application_obj.university.id)

        if application_obj.program_mode_3:
            program_3_recs = program_3_recs.filter(study_type_id=application_obj.program_mode_3.id)

        if application_obj.faculty_3:
            program_3_recs = program_3_recs.filter(faculty_id=application_obj.faculty_3.id)

        for rec in program_3_recs:
            try:
                raw_dict = {}
                raw_dict['id'] = rec.id
                raw_dict['program'] = rec.program_name
                program_3_final_list.append(raw_dict)
            except:
                pass



        if application_obj.university:
            year_recs = SemesterDetails.objects.filter(university_id = application_obj.university.id,study_level_id = application_obj.study_level.id)
            try:
                university_recs = UniversityDetails.objects.filter(is_delete=False,
                                                                   university_type_id=application_obj.university_type.id,type_id=application_obj.type.id).order_by('-id')
            except:
                pass
        if application_obj.university and application_obj.academic_year:
            # semester_recs = SemesterDetails.objects.filter(university_id = application_obj.university.id,year_id = application_obj.academic_year.id,study_level_id = application_obj.study_level.id)
            semester_recs = SemesterDetails.objects.filter(university_id = application_obj.university.id,year_id = application_obj.academic_year.id)

        if application_obj.university:
            learning_centre_recs = LearningCentersDetails.objects.filter(university_id=application_obj.university.id)
            for rec in learning_centre_recs:
                raw_dict = {}
                raw_dict['learning_centre_name'] = rec.lc_name
                raw_dict['id'] = rec.id
                learning_centre_list.append(raw_dict)
        if application_obj.program:
            campus_recs = application_obj.program.campus.all()
            for rec in campus_recs:
                raw_dict = {}
                raw_dict['campus_name'] = rec.campus.campus_name
                raw_dict['id'] = rec.campus.id
                campus_list.append(raw_dict)

    else:
        university_recs = UniversityDetails.objects.filter(is_delete=False, is_partner_university=False).order_by('-id')


    return render(request, 'agent_intake_details.html',{'country_recs': country_recs, 'religion_recs': religion_recs, 'application_obj': application_obj,'student_recs':student_recs,'agent_recs':agent_recs,'year_recs':year_recs,'semester_recs':semester_recs,
                                                  'learning_centre_recs':learning_centre_recs,'university_recs':university_recs,'learning_centre_list':learning_centre_list,'program_recs':program_recs,'campus_list':campus_list,'study_type_list':study_type_list,'study_mode_list':study_mode_list,'study_level_list':study_level_list,'faculty_recs':faculty_recs,
                                                  'department_recs':department_recs,'study_type_recs':study_type_recs,'study_level_recs':study_level_recs,'faculty_final_list':faculty_final_list,'program_final_list':program_final_list,
                                                  'study_mode_list_2':study_mode_list_2,
                                                  'study_level_recs_2':study_level_recs_2,
                                                  'faculty_2_final_list':faculty_2_final_list,
                                                  'department_2_recs':department_2_recs,
                                                  'program_2_final_list':program_2_final_list,
                                                  'study_mode_list_3':study_mode_list_3,
                                                  'study_level_recs_3':study_level_recs_3,
                                                  'faculty_3_final_list':faculty_3_final_list,
                                                  'department_3_recs':department_3_recs,
                                                  'program_3_final_list':program_3_final_list,
                                                  'university_type_recs':university_type_recs,
                                                  'type_recs':type_recs,
                                                  'supervisor_list':supervisor_list,
                                                  'research_details':research_details,
                                                        'user': user,
                                                        "attachment_obj":attachment_obj,
                                                  })

def save_update_applicant_intake_info(request):
    if request.POST:
        try:
            application_id = request.POST['application_id']
            research_proposal = request.FILES.get('research_proposal', None)
            application_obj = ApplicationDetails.objects.get(id = application_id)
            user = User.objects.get(email = application_obj.email)
            if not application_obj.university:
                progress_counter = application_obj.progress_counter
                progress_counter = progress_counter + 20
                application_obj.progress_counter = progress_counter
                application_obj.save()

            application_obj.learning_centre_id = request.POST.get('learning_centre',None)
            application_obj.academic_year_id = request.POST.get('year',None)
            application_obj.program_id = request.POST.get('program',None)
            application_obj.campus_id = request.POST.get('campus',None)
            application_obj.faculty_id = request.POST.get('faculty',None)
            application_obj.university_id = request.POST.get('university',None)
            application_obj.semester_id = request.POST.get('semester',None)
            application_obj.study_mode = request.POST.get('study_mode',None)
            application_obj.study_level_id = request.POST.get('program_level',None)
            application_obj.department_id = request.POST.get('department',None)
            application_obj.program_mode_id = request.POST.get('study_level',None)

            application_obj.study_mode_2 = request.POST.get('study_mode_2',None)
            # application_obj.study_level_2_id = request.POST.get('study_level_2',None)
            application_obj.faculty_2_id = request.POST.get('faculty_2',None)
            application_obj.department_2_id = request.POST.get('department_2', None)
            application_obj.program_2_id = request.POST.get('program_2',None)
            application_obj.program_mode_2_id = request.POST.get('study_level_2',None)

            application_obj.study_mode_3 = request.POST.get('study_mode_3', None)
            # application_obj.study_level_3_id = request.POST.get('study_level_3', None)
            application_obj.faculty_3_id = request.POST.get('faculty_3', None)
            application_obj.department_3_id = request.POST.get('department_3', None)
            application_obj.program_3_id = request.POST.get('program_3', None)
            application_obj.program_mode_3_id = request.POST.get('study_level_3', None)
            # if request.POST.get('country'):
            application_obj.learning_country_id = request.POST.get('country',None)
            application_obj.university_type_id = request.POST.get('university_type',None)
            application_obj.acceptance_avg = request.POST.get('acceptance_avg',None)
            application_obj.type_id = request.POST.get('type',None)
            application_obj.intake_flag = True
            application_obj.save()

            study_type_obj = StudyTypeDetails.objects.get(id = request.POST.get('study_level',None))
            if study_type_obj.study_type == 'Research':
                supervisor = request.POST.get('supervisor', None)
                research_title = request.POST.get('research_title', None)
                project_outline = request.POST.get('project_outline', None)
                data_collection = request.POST.get('data_collection', None)
                data_analysis = request.POST.get('data_analysis', None)
                progress_date = request.POST.get('progress_date', None)
                problems_encountered = request.POST.get('problems_encountered', None)
                program_research = request.POST.get('program', None)
                faculty = request.POST.get('faculty', None)
                university = request.POST.get('university', None)

                if ResearchDetails.objects.filter(application_id=user.get_application).exists():
                    research_details = ResearchDetails.objects.get(application_id=user.get_application)
                    research_details.supervisor_id = supervisor
                    research_details.research_title = research_title
                    research_details.project_outline = project_outline
                    research_details.data_collection = data_collection
                    research_details.data_analysis = data_analysis
                    research_details.progress_date = progress_date
                    research_details.problems_encountered = problems_encountered
                    research_details.program_research_id = program_research
                    research_details.faculty_id = faculty
                    research_details.university_id = university
                    research_details.save()
                else:
                    ResearchDetails.objects.create(application_id=user.get_application,supervisor_id = supervisor,
                                                   research_title = research_title,
                                                   project_outline = project_outline,
                                                   data_collection = data_collection,
                                                   data_analysis = data_analysis,
                                                   progress_date = progress_date,
                                                   problems_encountered = problems_encountered,
                                                   program_research_id = program_research,
                                                   faculty_id = faculty,
                                                   university_id = university,

                                                   )
                if ApplicantAttachementDetails.objects.filter(applicant_id=user.get_application).exists():
                    attachment_obj = ApplicantAttachementDetails.objects.get(applicant_id=user.get_application)
                else:
                    if (research_proposal is not None):
                        attachment_obj = ApplicantAttachementDetails.objects.create(applicant_id=user.get_application)
                if research_proposal:
                    attachment_obj.research_proposal = research_proposal
                    attachment_obj.save()

            else:
                ResearchDetails.objects.filter(application_id=user.get_application).filter().delete()
                ApplicantAttachementDetails.objects.filter(applicant_id=user.get_application).filter().delete()

            redirect_flag = True
            if redirect_flag:
                messages.success(request, "Record saved")
                return redirect('/agents/applicant_academic_english_qualification/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))
    return redirect('/agents/applicant_intake_info/')



def applicant_academic_english_qualification(request):
    year_recs = YearDetails.objects.all()
    qualification_obj = ''
    english_obj = ''
    arab_obj = ''
    passing_year_recs = PassingYear.objects.filter().order_by('-year')
    country_recs = CountryDetails.objects.all()
    english_competency_test_recs = EnglishCompetencyTestDetails.objects.all()
    arab_competency_test_recs = ArabCompetencyTestDetails.objects.all()

    session_email = None
    if request.session.get('form_data'):
        form_data = request.session.get('form_data')
        session_email = form_data.get('email')

    if User.objects.filter(email=session_email).exists():
        user = User.objects.get(email=session_email)
    else:
        user = None

    try:
        application_obj = user.get_application
    except Exception as e :
        messages.warning(request, "Please fill the personal details first.")
        if user:
            return redirect('/agents/applicant_personal_info/'+str(user.id))
        else:
            return redirect('/agents/applicant_personal_info/'+str(request.user.id))

    try:
        if user.get_application:
            # if not request.user.get_application.is_submitted:
            # application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id,
            #                                           is_submitted=False)
            if AcademicQualificationDetails.objects.filter(applicant_id=user.get_application).exists():
                qualification_obj = AcademicQualificationDetails.objects.filter(
                    applicant_id=user.get_application)

            if EnglishQualificationDetails.objects.filter(applicant_id=user.get_application).exists():
                english_obj = EnglishQualificationDetails.objects.filter(applicant_id=user.get_application)
                arab_obj = ArabQualificationDetails.objects.filter(applicant_id=user.get_application)
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        if user:
            return redirect('/agents/applicant_personal_info/'+str(user.id))
        else:
            return redirect('/agents/applicant_personal_info/'+str(request.user.id))

    return render(request, 'agent_applicant_academic_english_qualification.html',
                  {'year_recs': year_recs, 'qualification_recs': qualification_obj, 'english_recs': english_obj,'arab_recs': arab_obj,
                   'passing_year_recs': passing_year_recs, 'application_obj': application_obj,'country_recs':country_recs,'english_competency_test_recs':english_competency_test_recs,
                   'arab_competency_test_recs':arab_competency_test_recs,'user':user})


def save_update_applicant_academic_english_qualification(request):
    redirect_flag = False
    academic_count = request.POST.get('academic_count')
    english_count = request.POST.get('english_count')
    arab_count = request.POST.get('arab_count')
    application_id = request.POST.get('application_id')
    application_obj = ApplicationDetails.objects.get(id=application_id)
    user = User.objects.get(email=application_obj.email)

    if request.POST:

        try:
            if StudentDetails.objects.filter(user=user):
                # if not request.user.get_application.is_submitted:
                try:
                    if not AcademicQualificationDetails.objects.filter(applicant_id = user.get_application).exists():
                        application_obj = ApplicationDetails.objects.get(id = user.get_application.id)
                        progress_counter = application_obj.progress_counter
                        progress_counter = progress_counter + 20
                        application_obj.progress_counter = progress_counter
                        application_obj.save()

                    for x in range(int(academic_count)):
                        try:
                            x = x + 1

                            level_result_document = request.FILES.get('level_result_document' + str(x))
                            level_result_document_text = request.POST.get('level_result_document_text' + str(x))

                            if request.POST.get('academic_id_' + str(x)):
                                AcademicQualificationDetails.objects.filter(
                                    id=request.POST['academic_id_' + str(x)]).update(
                                    country_id=request.POST['country' + str(x)],
                                    major=request.POST['major' + str(x)],
                                    degree=request.POST['degree' + str(x)],
                                    level_year=request.POST['level_year' + str(x)],
                                    level_result=request.POST['level_result' + str(x)],
                                    level_institution=request.POST['level_institution' + str(x)])

                                if request.POST['degree' + str(x)] == 'OTHERS':
                                    AcademicQualificationDetails.objects.filter(
                                        id=request.POST['academic_id_' + str(x)]).update(
                                        other_degree=request.POST['other_rec' + str(x)])

                                qualification_obj = AcademicQualificationDetails.objects.filter(
                                    id=request.POST['academic_id_' + str(x)])[0]

                            else:
                                qualification_obj = AcademicQualificationDetails.objects.create(
                                    # level=request.POST['level' + str(x)],
                                    level_year=request.POST['level_year' + str(x)],
                                    country_id=request.POST['country' + str(x)],
                                    major=request.POST['major' + str(x)],
                                    degree=request.POST['degree' + str(x)],
                                    level_result=request.POST['level_result' + str(x)],
                                    level_institution=request.POST['level_institution' + str(x)],
                                    applicant_id=user.get_application)

                                if request.POST['degree' + str(x)] == 'OTHERS':
                                    qualification_obj.other_degree = request.POST['other_rec' + str(x)]
                                    qualification_obj.save()


                            if level_result_document:
                                level_result = str(level_result_document)

                                object_path = media_path(qualification_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + level_result,
                                                     level_result_document)

                                qualification_obj.level_result_document = level_result

                            if not level_result_document_text:
                                qualification_obj.level_result_document = ''

                            qualification_obj.save()
                        except Exception as e:
                            pass

                    for count in range(int(english_count)):
                        try:
                            count = count + 1

                            english_test_result_document = request.FILES.get(
                                'english_test_result_document_' + str(count))
                            english_test_result_document_text = request.POST.get(
                                'english_test_result_document_text_' + str(count))

                            if request.POST.get('english_obj_' + str(count)):
                                EnglishQualificationDetails.objects.filter(
                                    id=request.POST['english_obj_' + str(count)]).update(
                                    english_test=request.POST['english_test_' + str(count)],
                                    english_competency_test_id=request.POST['english_competency_test_' + str(count)],
                                    # english_test_year=request.POST['english_test_year_' + str(count)],
                                    english_test_result=request.POST['english_test_result_' + str(count)])

                                english_object = EnglishQualificationDetails.objects.filter(
                                    id=request.POST['english_obj_' + str(count)])[0]

                            else:
                                english_object = EnglishQualificationDetails.objects.create(
                                    english_test=request.POST['english_test_' + str(count)],
                                    english_competency_test_id=request.POST['english_competency_test_' + str(count)],
                                    # english_test_year=request.POST['english_test_year_' + str(count)],
                                    english_test_result=request.POST['english_test_result_' + str(count)],
                                    applicant_id=user.get_application)

                            if english_test_result_document:
                                english_test_result = str(english_test_result_document)
                                object_path = media_path(english_object.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + english_test_result,
                                                     english_test_result_document)

                                english_object.english_test_result_document = english_test_result

                            if not english_test_result_document_text:
                                english_object.english_test_result_document = ''

                            english_object.save()
                        except Exception as e:
                            pass

                    for count in range(int(arab_count)):
                        try:
                            count = count + 1
                            if request.POST.get('arab_obj_' + str(count)):
                                ArabQualificationDetails.objects.filter(
                                    id=request.POST['arab_obj_' + str(count)]).update(
                                    arab_test=request.POST['arab_test_' + str(count)],
                                    arab_competency=request.POST['arab_competency_test_' + str(count)],
                                    arab_test_result=request.POST['arab_test_result_' + str(count)])

                                arab_object = ArabQualificationDetails.objects.filter(
                                    id=request.POST['arab_obj_' + str(count)])[0]
                            else:
                                arab_object = ArabQualificationDetails.objects.create(
                                    arab_test=request.POST['arab_test_' + str(count)],
                                    arab_competency=request.POST['arab_competency_test_' + str(count)],
                                    arab_test_result=request.POST['arab_test_result_' + str(count)],
                                    applicant_id=user.get_application)
                            arab_object.save()
                        except Exception as e:
                            pass

                    redirect_flag = True
                except Exception as e:
                    messages.warning(request, "Form have some error" + str(e))
                if redirect_flag:
                    messages.success(request, "Record saved")
                    return redirect('/agents/applicant_credit_transfer/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/agents/applicant_academic_english_qualification/')

def applicant_credit_transfer(request):
    try:
        credit_transfer_recs = ''
        credit_transfer_count = 0

        session_email = None
        if request.session.get('form_data'):
            form_data = request.session.get('form_data')
            session_email = form_data.get('email')

        if User.objects.filter(email=session_email).exists():
            user = User.objects.get(email=session_email)
        else:
            user = None

        application_obj = user.get_application
        if user.get_application:
            if CreditTransferDetails.objects.filter(applicant_id=user.get_application).exists():
                credit_transfer_recs = CreditTransferDetails.objects.filter(applicant_id=user.get_application)
                credit_transfer_count = CreditTransferDetails.objects.filter(applicant_id=user.get_application).count()
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        if user:
            return redirect('/agents/applicant_personal_info/'+str(user.id))
        else:
            return redirect('/agents/applicant_personal_info/'+str(request.user.id))
    return render(request, 'agent_applicant_credit_transfer.html',
                  {'credit_transfer_recs': credit_transfer_recs,
                   'application_obj': application_obj,'credit_transfer_count':credit_transfer_count,'user':user})

def save_credit_transfer(request):
    redirect_flag = False
    experience_count = request.POST.get('experience_count')
    application_id = request.POST.get('application_id')
    application_obj = ApplicationDetails.objects.get(id=application_id)
    user = User.objects.get(email=application_obj.email)
    if request.POST:
        try:
            if StudentDetails.objects.filter(user=user):
                for count in range(int(experience_count)):
                    try:
                        count = count + 1
                        if request.POST.get('credit_transfer_obj_' + str(count)):
                            CreditTransferDetails.objects.filter(id=request.POST['credit_transfer_obj_' + str(count)]).update(
                                course_code=request.POST['course_code_' + str(count)],
                                course_title=request.POST['course_title_' + str(count)],
                                credit_hours=request.POST['credit_hours_' + str(count)],
                                grade=request.POST['grade_' + str(count)],
                                institution=request.POST['institution_' + str(count)],
                                program_study_status=request.POST['program_study_status_' + str(count)],
                            )
                        else:
                            CreditTransferDetails.objects.create(
                                course_code=request.POST['course_code_' + str(count)],
                                course_title=request.POST['course_title_' + str(count)],
                                credit_hours=request.POST['credit_hours_' + str(count)],
                                grade=request.POST['grade_' + str(count)],
                                institution=request.POST['institution_' + str(count)],
                                program_study_status=request.POST['program_study_status_' + str(count)],
                                applicant_id=user.get_application

                            )
                    except Exception as e:
                        pass
                redirect_flag = True
            if redirect_flag:
                messages.success(request, "Record saved")
                return redirect('/agents/applicant_credit_transfer_attachement/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))
        messages.warning(request, "Please fill proper form")
    return redirect('/agents/applicant_credit_transfer/')


def applicant_credit_transfer_attachement(request):
    session_email = None
    if request.session.get('form_data'):
        form_data = request.session.get('form_data')
        session_email = form_data.get('email')

    if User.objects.filter(email=session_email).exists():
        user = User.objects.get(email=session_email)
    else:
        user = None

    try:
        application_obj = user.get_application
    except Exception as e:
        messages.warning(request, "Please fill the personal details first.")
        if user:
            return redirect('/agents/applicant_personal_info/'+str(user.id))
        else:
            return redirect('/agents/applicant_personal_info/'+str(request.user.id))
    try:
        credit_transfer_attachment_obj = ''
        if user.get_application:
            if CreditTransferAttachmentDetails.objects.filter(applicant_id=user.get_application).exists():
                credit_transfer_attachment_obj = CreditTransferAttachmentDetails.objects.get(
                    applicant_id=user.get_application)
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/agents/dashboard/')
    return render(request, 'agent_applicant_credit_transfer_attachement.html',
                  {'credit_transfer_attachment_obj': credit_transfer_attachment_obj,
                   'application_obj': application_obj,'user':user})

def save_credit_transfer_attachement(request):
    try:
        grading_scheme = request.FILES.get('grading_scheme')
        module_syllabus = request.FILES.get('module_syllabus')
        status_verification_letter = request.FILES.get('status_verification_letter')
        application_id = request.POST.get('application_id')
        application_obj = ApplicationDetails.objects.get(id=application_id)
        user = User.objects.get(email=application_obj.email)
    except:
        grading_scheme = ''
        module_syllabus = ''
        status_verification_letter = ''

    try:

        if CreditTransferAttachmentDetails.objects.filter(applicant_id=user.get_application).exists():
            credit_transfer_attachment_obj = CreditTransferAttachmentDetails.objects.get(
                applicant_id=user.get_application)
        else:
            if (grading_scheme is not None) or (module_syllabus is not None) or (status_verification_letter is not None):
                credit_transfer_attachment_obj = CreditTransferAttachmentDetails.objects.create(
                    applicant_id=user.get_application)
        if grading_scheme:
            credit_transfer_attachment_obj.grading_scheme = grading_scheme
            credit_transfer_attachment_obj.save()

        if module_syllabus:
            credit_transfer_attachment_obj.module_syllabus = module_syllabus
            credit_transfer_attachment_obj.save()

        if status_verification_letter:
            credit_transfer_attachment_obj.status_verification_letter = status_verification_letter
            credit_transfer_attachment_obj.save()

        messages.success(request, "Attachment submitted successfully.")

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/agents/applicant_employement_history_info/')

def applicant_employement_history_info(request):
    session_email = None
    if request.session.get('form_data'):
        form_data = request.session.get('form_data')
        session_email = form_data.get('email')

    if User.objects.filter(email=session_email).exists():
        user = User.objects.get(email=session_email)
    else:
        user = None

    try:
        application_obj = user.get_application
    except Exception as e :
        messages.warning(request, "Please fill the personal details first.")
        if user:
            return redirect('/agents/applicant_personal_info/'+str(user.id))
        else:
            return redirect('/agents/applicant_personal_info/'+str(request.user.id))

    country_recs = CountryDetails.objects.all()
    employement_history_obj = ''
    employement_history_count = 0
    try:
        application_obj = user.get_application
        if user.get_application:
            if EmployementHistoryDetails.objects.filter(applicant_id=user.get_application).exists():
                employement_history_obj = EmployementHistoryDetails.objects.filter(applicant_id=user.get_application)
                employement_history_count = employement_history_obj.count()
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        if user:
            return redirect('/agents/applicant_personal_info/'+str(user.id))
        else:
            return redirect('/agents/applicant_personal_info/'+str(request.user.id))
    return render(request, 'agent_applicant_employement_history_info.html',
                  {'employement_history_obj': employement_history_obj,'application_obj': application_obj,'country_recs':country_recs,'employement_history_count':employement_history_count,'user':user})


def save_update_applicant_employement_history_info(request):
    if request.POST:
        redirect_flag = False
        experience_count = request.POST.get('experience_count')
        application_id = request.POST.get('application_id')
        application_obj = ApplicationDetails.objects.get(id=application_id)
        user = User.objects.get(email=application_obj.email)
        try:
            if StudentDetails.objects.filter(user=user):
                # EmployementHistoryDetails.objects.filter(applicant_id=request.user.get_application).delete()
                for count in range(int(experience_count)):
                    try:
                        count = count + 1

                        working_criteria = None
                        if request.POST['working_criteria_' + str(count)] == 'Previous':
                            working_criteria = 'Previous'
                        else:
                            working_criteria = 'Current'

                        if request.POST.get('no_experience') == 'on':
                            no_experience = True
                        else:
                            no_experience = False

                        if request.POST['employement_history_obj_' + str(count)]:
                            employee_history_obj = EmployementHistoryDetails.objects.get(id = request.POST['employement_history_obj_' + str(count)])
                            EmployementHistoryDetails.objects.filter(id = request.POST['employement_history_obj_' + str(count)]).update(no_experience=no_experience,
                                working_criteria=working_criteria,
                                employer_name=request.POST['employer_name_' + str(count)],
                                working_status=request.POST['working_status_' + str(count)],
                                designation=request.POST['designation_' + str(count)],
                                from_date=request.POST['from_date_' + str(count)] if request.POST[
                                    'from_date_' + str(count)] else None,
                                to_date=request.POST['to_date_' + str(count)] if request.POST[
                                    'to_date_' + str(count)] else None,
                                )
                            working_experience = request.FILES.get('working_experience_' + str(count))
                            if working_experience:
                                employee_history_obj.working_experience = working_experience
                                employee_history_obj.save()
                        else:
                            employee_history_obj = EmployementHistoryDetails.objects.create(
                                no_experience=no_experience,
                                working_criteria=working_criteria,
                                employer_name=request.POST['employer_name_' + str(count)],
                                working_status=request.POST['working_status_' + str(count)],
                                designation=request.POST['designation_' + str(count)],
                                from_date=request.POST['from_date_' + str(count)] if request.POST['from_date_' + str(count)] else None,
                                to_date=request.POST['to_date_' + str(count)] if request.POST['to_date_' + str(count)] else None,
                                applicant_id=user.get_application)

                            working_experience = request.FILES.get('working_experience_' + str(count))
                            if working_experience:
                                employee_history_obj.working_experience = working_experience
                                employee_history_obj.save()



                    except Exception as e:
                        pass
                redirect_flag = True
                if redirect_flag:
                    messages.success(request, "Record saved")
                    return redirect('/agents/applicant_additional_information/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/agents/applicant_employement_history_info/')


def applicant_additional_information(request):
    campus_recs = CampusBranchesDetails.objects.all()
    country_recs = AllCountries.objects.all()
    student_recs = StudentDetails.objects.filter(user__is_active=True)
    agent_recs = AgentDetails.objects.filter()
    agents = User.objects.filter(role__name = 'Agent')
    path = ''
    sibling_obj = ''
    application_obj = ''

    session_email = None
    if request.session.get('form_data'):
        form_data = request.session.get('form_data')
        session_email = form_data.get('email')

    if User.objects.filter(email=session_email).exists():
        user = User.objects.get(email=session_email)
    else:
        user = None

    try:
        app_obj = user.get_application
    except Exception as e :
        messages.warning(request, "Please fill the personal details first.")
        if user:
            return redirect('/agents/applicant_personal_info/'+str(user.id))
        else:
            return redirect('/agents/applicant_personal_info/'+str(request.user.id))

    if AdditionInformationDetails.objects.filter(application_id=user.get_application).exists():
        application_obj = AdditionInformationDetails.objects.get(application_id=user.get_application)


    return render(request, 'agent_applicant_additional_info.html', {'country_recs': country_recs, 'application_obj': application_obj, 'path': path, 'sibling_obj_rec': sibling_obj, 'student_recs':student_recs, 'agent_recs':agent_recs,'campus_recs':campus_recs,
                                                              'agents':agents,'app_obj':app_obj,'user':user})

def save_update_applicant_additional_info(request):
    redirect_flag = False
    if request.POST:
        try:
            application_id = request.POST.get('application_id')
            application_obj = ApplicationDetails.objects.get(id=application_id)
            user = User.objects.get(email=application_obj.email)
            if StudentDetails.objects.filter(user=user):
                if AdditionInformationDetails.objects.filter(application_id = user.get_application).exists():
                    AdditionInformationDetails.objects.filter(application_id = user.get_application).update(
                        recruitment_agents=request.POST['recruitment_agents'],
                        ken_name=request.POST['ken_name'],
                        ken_id=request.POST['ken_id'],
                        ken_relationship=request.POST['ken_relationship'],
                        ken_tel_no=request.POST['ken_tel_no'],
                        ken_email=request.POST['ken_email'],
                        about_know=request.POST['about_know'] if request.POST['about_know'] else None,
                        campus_id=request.POST['campus'] if request.POST['campus'] else None,
                        )
                    if request.POST['is_sponsored'] == 'Yes':
                        AdditionInformationDetails.objects.filter(application_id=user.get_application).update(
                            sponsore_organisation=request.POST['sponsore_organisation'],
                            sponsore_address=request.POST['sponsore_address'],
                            sponsore_email=request.POST['sponsore_email'],
                            sponsore_contact=request.POST['sponsore_contact'],
                            is_sponsored=True
                        )
                    else:
                        AdditionInformationDetails.objects.filter(application_id=user.get_application).update(
                            sponsore_organisation='',
                            sponsore_address='',
                            sponsore_email='',
                            sponsore_contact='',
                            is_sponsored=False
                        )
                else:
                    if request.POST['ken_name'] != '' or request.POST['ken_id'] != '' or request.POST['ken_relationship'] != '' or request.POST['ken_tel_no'] != '' or request.POST['ken_email'] != '' or request.POST['about_know'] != '' or request.POST['campus'] != '' or request.POST['is_sponsored'] != 'No':
                        application_obj = ApplicationDetails.objects.get(id=user.get_application.id)
                        progress_counter = application_obj.progress_counter
                        progress_counter = progress_counter + 20
                        application_obj.progress_counter = progress_counter
                        application_obj.save()

                        AdditionInformationDetails.objects.create(application_id=user.get_application,ken_name=request.POST['ken_name'],recruitment_agents = request.POST['recruitment_agents'],
                            ken_id=request.POST['ken_id'],
                            ken_relationship=request.POST['ken_relationship'],
                            ken_tel_no=request.POST['ken_tel_no'],
                            ken_email=request.POST['ken_email'],
                            about_know=request.POST['about_know'] if request.POST['about_know'] else None,
                            campus_id=request.POST['campus'] if request.POST['campus'] else None,

                                                                  )
                        if request.POST['is_sponsored'] == 'Yes':
                            AdditionInformationDetails.objects.filter(application_id=user.get_application).update(
                                sponsore_organisation=request.POST['sponsore_organisation'],
                                sponsore_address=request.POST['sponsore_address'],
                                sponsore_email=request.POST['sponsore_email'],
                                sponsore_contact=request.POST['sponsore_contact'],
                                is_sponsored=True
                            )
                        else:
                            AdditionInformationDetails.objects.filter(application_id=user.get_application).update(
                                sponsore_organisation='',
                                sponsore_address='',
                                sponsore_email='',
                                sponsore_contact='',
                                is_sponsored=False
                            )
                redirect_flag = True
            if redirect_flag:
                messages.success(request, "Record saved")
                return redirect('/agents/checkout/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/agents/applicant_additional_information/')


def checkout(request):
    try:
        session_email = None
        if request.session.get('form_data'):
            form_data = request.session.get('form_data')
            session_email = form_data.get('email')

        if User.objects.filter(email=session_email).exists():
            user = User.objects.get(email=session_email)
        else:
            user = None

        application_obj = ApplicationDetails.objects.get(email = session_email)

        if ApplicationDetails.objects.filter(application_id=user.get_application_id).exists():
            application_obj = ApplicationDetails.objects.get(application_id=user.get_application_id)
        payement_obj = None
        if PaymentDetails.objects.filter(university_id = application_obj.university.id).exists():
            payement_obj = PaymentDetails.objects.get(university_id = application_obj.university.id)
        if payement_obj == None:
            return render(request, 'agent_no_university_fee.html',{'application_obj':application_obj,'user':user})
        order_obj = None
        if ApplicationFeeDetails.objects.filter(application_id=user.get_application.id).exists():
            order_obj = ApplicationFeeDetails.objects.get(application_id_id=user.get_application.id)
        return render(request, 'agent_checkout.html', {'application_obj': application_obj, 'payement_obj': payement_obj,'order_obj':order_obj,'user':user})
    except Exception as e:
        messages.warning(request, "Please fill the personal details first.")
        if user:
            return redirect('/agents/applicant_personal_info/'+str(user.id))
        else:
            return redirect('/agents/applicant_personal_info/'+str(request.user.id))

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = settings.SERVER_HOST_NAME
        session_email = None
        if request.session.get('form_data'):
            form_data = request.session.get('form_data')
            session_email = form_data.get('email')

        if User.objects.filter(email=session_email).exists():
            user = User.objects.get(email=session_email)
        else:
            user = None

        application_obj = user.get_application
        payement_obj = 1000
        if PaymentDetails.objects.filter(university_id=application_obj.university.id).exists():
            payement_obj = PaymentDetails.objects.get(university_id=application_obj.university.id)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(float(payement_obj.amount)*100),
                            'product_data': {
                                'name': 'Online Admission',
                                'images': ['http://unisys.online/static/images/university_logo.png'],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='payment',
                success_url=YOUR_DOMAIN + 'agents/stripe_checkout_success/session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + 'agents/checkout/',
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return str(e)

def stripe_checkout_success(request, session_id):
    session_email = None
    if request.session.get('form_data'):
        form_data = request.session.get('form_data')
        session_email = form_data.get('email')

    if User.objects.filter(email=session_email).exists():
        user = User.objects.get(email=session_email)
    else:
        user = None
    ApplicationFeeDetails.objects.create(application_id=user.get_application)
    return redirect('/agents/checkout/')

def applicant_attachment_submission(request):
    session_email = None
    if request.session.get('form_data'):
        form_data = request.session.get('form_data')
        session_email = form_data.get('email')

    if User.objects.filter(email=session_email).exists():
        user = User.objects.get(email=session_email)
    else:
        user = None
    try:
        application_obj = user.get_application
    except Exception as e :
        messages.warning(request, "Please fill the personal details first.")
        if user:
            return redirect('/agents/applicant_personal_info/'+str(user.id))
        else:
            return redirect('/agents/applicant_personal_info/'+str(request.user.id))
    try:
        attachment_obj = ''
        if user.get_application:
            if ApplicantAttachementDetails.objects.filter(applicant_id=user.get_application).exists():
                attachment_obj = ApplicantAttachementDetails.objects.get(
                    applicant_id=user.get_application)
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/agents/dashboard/')
    document_recs = DocumentDetails.objects.all()
    return render(request, 'agent_applicant_attachment_submission.html',
                  {'attachment_obj': attachment_obj,'document_recs':document_recs,'application_obj':application_obj,'user':user})


def save_attachement_submission(request):
    try:
        passport_photo = request.FILES.get('passport_photo')
        photo = request.FILES.get('photo')
        level_result_document = request.FILES.get('level_result_document')
        transcript_document = request.FILES.get('transcript_document')
        english_test_result_document = request.FILES.get('english_test_result_document')
        arab_test_result_document = request.FILES.get('arab_test_result_document')
        recommendation_letter = request.FILES.get('recommendation_letter')
        research_proposal = request.FILES.get('research_proposal')
    except:
        passport_photo = ''
        photo = ''
        level_result_document = ''
        transcript_document = ''
        english_test_result_document = ''
        arab_test_result_document = ''
        recommendation_letter = ''
        research_proposal = ''

    try:
        application_id = request.POST.get('application_id')
        application_obj = ApplicationDetails.objects.get(id=application_id)
        user = User.objects.get(email=application_obj.email)

        if ApplicantAttachementDetails.objects.filter(applicant_id=user.get_application).exists():
            attachment_obj = ApplicantAttachementDetails.objects.get(
                applicant_id=user.get_application)
        else:
            if (passport_photo is not None) or (photo is not None) or (level_result_document is not None) or (transcript_document is not None) or (english_test_result_document is not None) or (arab_test_result_document is not None) or (recommendation_letter is not None):
                if not ApplicantAttachementDetails.objects.filter(applicant_id=user.get_application).exists():
                    application_obj = ApplicationDetails.objects.get(id=user.get_application.id)
                    progress_counter = application_obj.progress_counter
                    progress_counter = progress_counter + 10
                    application_obj.progress_counter = progress_counter
                    application_obj.save()
                attachment_obj = ApplicantAttachementDetails.objects.create(
                    applicant_id=user.get_application)
        if passport_photo:
            attachment_obj.passport_image = passport_photo
            attachment_obj.save()

        if photo:
            attachment_obj.image = photo
            attachment_obj.save()

        if level_result_document:
            attachment_obj.level_result_document = level_result_document
            attachment_obj.save()

        if transcript_document:
            attachment_obj.transcript_document = transcript_document
            attachment_obj.save()

        if english_test_result_document:
            attachment_obj.english_test_result_document = english_test_result_document
            attachment_obj.save()

        if arab_test_result_document:
            attachment_obj.arab_test_result_document = arab_test_result_document
            attachment_obj.save()

        if recommendation_letter:
            attachment_obj.recommendation_letter = recommendation_letter
            attachment_obj.save()

        if research_proposal:
            attachment_obj.research_proposal = research_proposal
            attachment_obj.save()
        messages.success(request, "Attachment submitted successfully.")
    except Exception as e:
        print(str(e))
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/agents/applicant_declaration/')


def applicant_declaration(request):
    session_email = None
    if request.session.get('form_data'):
        form_data = request.session.get('form_data')
        session_email = form_data.get('email')

    if User.objects.filter(email=session_email).exists():
        user = User.objects.get(email=session_email)
    else:
        user = None

    try:
        application_obj = user.get_application
    except Exception as e :
        messages.warning(request, "Please fill the personal details first.")
        if user:
            return redirect('/agents/applicant_personal_info/'+str(user.id))
        else:
            return redirect('/agents/applicant_personal_info/'+str(request.user.id))
    try:
        if user.get_application:
            application_obj = user.get_application
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return render(request, 'agent_applicant_declaration.html', {'application_obj':application_obj,'user':user})

def submit_application(request):
    try:
        app_id = request.POST.get('app_id')
        application_obj = ApplicationDetails.objects.get(id=app_id)
        user = User.objects.get(id=application_obj.student.user.id)
        if not application_obj.university:
            messages.warning(request,"Please fill the Intake Information section before submitting the application.")
            return redirect('/agents/applicant_intake_info/')
        if not AcademicQualificationDetails.objects.filter(applicant_id=user.get_application):
            messages.warning(request, "Please fill the Academic Qualification section before submitting the application.")
            return redirect('/agents/applicant_academic_english_qualification/')
        if not AdditionInformationDetails.objects.filter(application_id=user.get_application):
            messages.warning(request, "Please fill the Additional Information section before submitting the application.")
            return redirect('/agents/applicant_additional_information/')
        if not ApplicantAttachementDetails.objects.filter(applicant_id=user.get_application):
            messages.warning(request, "Please upload required Attachement section before submitting the application.")
            return redirect('/agents/applicant_attachment_submission/')
        else:
            document_recs = DocumentDetails.objects.all()
            attachment_obj = ApplicantAttachementDetails.objects.get(applicant_id=user.get_application)
            document_count = 0
            if document_recs[0].doc_required == 'Yes':
                if attachment_obj.image:
                    document_count = document_count + 1
            if document_recs[1].doc_required == 'Yes':
                if attachment_obj.passport_image:
                    document_count = document_count + 1
            if document_recs[2].doc_required == 'Yes':
                if attachment_obj.level_result_document:
                    document_count = document_count + 1
            if document_recs[3].doc_required == 'Yes':
                if attachment_obj.transcript_document:
                    document_count = document_count + 1
            if document_recs[4].doc_required == 'Yes':
                if attachment_obj.english_test_result_document:
                    document_count = document_count + 1
            if document_recs[5].doc_required == 'Yes':
                if attachment_obj.arab_test_result_document:
                    document_count = document_count + 1
            if document_recs[6].doc_required == 'Yes':
                if attachment_obj.recommendation_letter:
                    document_count = document_count + 1

            if application_obj.program_mode.study_type == 'Research':
                attachement_count = DocumentDetails.objects.filter(doc_required='Yes').count()
                if document_recs[7].doc_required == 'Yes':
                    if attachment_obj.research_proposal:
                        document_count = document_count + 1
            else:
                attachement_count = DocumentDetails.objects.filter(doc_required = 'Yes').exclude(document_name='Research Proposal').count()

            if not attachement_count == document_count:
                messages.warning(request, "Please upload required Attachement section before submitting the application.")
                return redirect('/agents/applicant_attachment_submission/')

        if application_obj.is_submitted == False:
            progress_counter = application_obj.progress_counter
            progress_counter = progress_counter + 10
            application_obj.progress_counter = progress_counter
            application_obj.save()

        ApplicationDetails.objects.filter(application_id=user.get_application_id).update(is_submitted=True,is_online_admission = True)
        ApplicationHistoryDetails.objects.create(applicant_id=user.get_application,
                                                 status='Application Submitted',
                                                 remark='Your application is submitted and your University will be notified on further updates regarding your applications.')


        application_notification(user.get_application.id,
                                 'You have successfully submitted your application.')
        admin_notification(user.get_application.id,
                           str(user.get_application.get_full_name()) + ' have submitted application.')

        messages.success(request, "Application submitted successfully.")

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/partner/approved_application/')