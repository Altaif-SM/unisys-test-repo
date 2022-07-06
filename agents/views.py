from django.shortcuts import render, redirect
from masters.views import *
from agents.models import *
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from common.utils import get_application_id
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