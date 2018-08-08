from django.shortcuts import render, redirect
from masters.models import *
from student.models import *
from partner.models import *
import json
from django.contrib import messages
from django.http import JsonResponse
from common.utils import *
from django.db.models import Max, Q


# Create your views here.
from student.views import applicant_academic_english_qualification


def partner_home(request):
    username = ''
    try:
        username = request.user.first_name

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))

    return render(request, 'partner_home.html', {'username': username})


def template_registered_application(request):
    if request.user.is_super_admin():
        applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, year=get_current_year(request))
        university_recs = UniversityDetails.objects.all()
    else:
        applicant_recs = ApplicationDetails.objects.filter(
            nationality=request.user.partner_user_rel.get().address.country,
            is_submitted=True, year=get_current_year(request))
        university_recs = UniversityDetails.objects.filter(country=request.user.partner_user_rel.get().address.country)
    country_recs = CountryDetails.objects.all()
    degree_recs = DegreeDetails.objects.all()

    return render(request, 'template_registered_application.html',
                  {'applicant_recs': applicant_recs, 'country_recs': country_recs, 'university_recs': university_recs,
                   'degree_recs': degree_recs})


def export_registered_application(request):
    if request.user.is_super_admin():
        applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, year=get_current_year(request))
    else:
        applicant_recs = ApplicationDetails.objects.filter(
            nationality=request.user.partner_user_rel.get().address.country,
            is_submitted=True, year=get_current_year(request))

    rows = []
    for application in applicant_recs:
        temp_list = []
        temp_list.append(application.get_full_name())
        temp_list.append(application.nationality.country_name.title() if application.nationality else '')
        temp_list.append(application.address.country.country_name.title())
        temp_list.append(application.applicant_scholarship_rel.all()[0].university.university_name.title())
        temp_list.append(application.applicant_scholarship_rel.all()[0].degree.degree_name.title())
        temp_list.append(application.applicant_scholarship_rel.all()[0].course_applied.program_name.title())
        rows.append(temp_list)

    cloumns = ['Student Name', 'Nationality', 'Country', 'University', 'Degree', 'Course']

    return export_wraped_column_xls('registered_application', cloumns, rows)


def template_applicant_all_details(request, app_id):
    application_obj = ApplicationDetails.objects.get(id=app_id)
    siblings_obj = application_obj.sibling_applicant_rel.all() if application_obj.sibling_applicant_rel.all() else ''
    qualification_obj = application_obj.academic_applicant_rel.get() if application_obj.academic_applicant_rel.all() else ''
    english_obj = application_obj.english_applicant_rel.get() if application_obj.english_applicant_rel.all() else ''
    curriculum_obj = application_obj.curriculum_applicant_rel.get() if application_obj.curriculum_applicant_rel.all() else ''
    applicant_experience_obj = application_obj.applicant_experience_rel.get() if application_obj.applicant_experience_rel.all() else ''
    scholarship_obj = application_obj.applicant_scholarship_rel.get() if application_obj.applicant_scholarship_rel.all() else ''

    return render(request, 'template_applicant_all_details.html',
                  {'siblings_obj': siblings_obj, 'application_obj': application_obj,
                   'qualification_obj': qualification_obj, 'english_obj': english_obj,
                   'curriculum_obj': curriculum_obj,
                   'applicant_experience_obj': applicant_experience_obj,
                   'scholarship_obj': scholarship_obj})


def filter_nationality(field):
    if field != '':
        return Q(nationality_id=field)
    else:
        return Q()  # Dummy filter


def filter_degree(degree):
    if degree != '':
        return Q(applicant_scholarship_rel__course_applied_id=degree)
    else:
        return Q()  # Dummy filter


def filter_university(university):
    if university != '':
        return Q(applicant_scholarship_rel__university_id=university)
    else:
        return Q()  # Dummy filter


def filter_country(country):
    if country != '':
        return Q(address__country_id=country)
    else:
        return Q()  # Dummy filter


def filter_registered_application(request):
    if request.POST:
        request.session['registered_application_form_data'] = request.POST
        university = request.POST.get('university')
        degree = request.POST.get('degree')
        nationality = request.POST.get('nationality')
        country = request.POST.get('country')
    else:

        form_data = request.session.get('registered_application_form_data')

        university = form_data.get('university')
        degree = form_data.get('degree')
        nationality = form_data.get('nationality')
        country = form_data.get('country')

    try:

        if request.user.is_super_admin():
            applicant_recs = ApplicationDetails.objects.filter(
                Q(is_submitted=True), filter_country(country), filter_nationality(nationality),
                filter_degree(degree),
                filter_university(university), year=get_current_year(request))

            university_recs = UniversityDetails.objects.all()
        else:
            applicant_recs = ApplicationDetails.objects.filter(
                Q(nationality=request.user.partner_user_rel.get().address.country,
                  is_submitted=True), filter_nationality(nationality),
                filter_degree(degree),
                filter_university(university), year=get_current_year(request))

            university_recs = UniversityDetails.objects.filter(
                country=request.user.partner_user_rel.get().address.country)

        country_recs = CountryDetails.objects.all()
        degree_recs = DegreeDetails.objects.all()

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, 'template_registered_application.html',
                  {'applicant_recs': applicant_recs, 'country_recs': country_recs, 'university_recs': university_recs,
                   'degree_recs': degree_recs})


def template_approving_application(request):
    applicant_recs = ''
    try:
        if request.user.is_super_admin():
            applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, year=get_current_year(request))
        else:
            applicant_recs = ApplicationDetails.objects.filter(
                nationality=request.user.partner_user_rel.get().address.country,
                is_submitted=True, year=get_current_year(request))
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))

    return render(request, 'template_approving_application.html',
                  {'applicant_recs': applicant_recs})


# def change_application_status(request):
#     data_value = json.loads(request.POST.get('data_value'))
#
#     try:
#
#         # messages_success = False
#
#         for application in data_value:
#
#             # getting application object for flag validations
#             application_obj = ApplicationDetails.objects.get(id=application['application_id'])
#
#             if not application_obj.first_interview:
#                 if application['flags']['id_first']:
#                     application_obj.first_interview = True
#                     application_obj.save()
#
#                     subject = 'First Interview Call'
#                     message = 'You are requested to come down for the first interview on 17th Aug, 2018 at Abc Hall, Dubai. \n \n Thanks and Regards \n \n XYZ'
#
#                     send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                             application_obj.first_name)
#
#                     if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
#                                                                     status='First Interview Call').exists():
#                         ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
#                                                                  status='First Interview Call',
#                                                                  remark='You are requested to come down for the first interview.')
#                 else:
#                     continue
#
#             if not application_obj.first_interview_attend:
#                 if application['flags']['id_first'] and application['flags']['id_first_interview_attend']:
#                     application_obj.first_interview_attend = True
#                     application_obj.save()
#
#                     subject = 'First Interview Attended'
#                     message = 'This mail is to notify that you have attended first interview. We will update you about the result soon.'
#
#                     send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                             application_obj.first_name)
#
#                     if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
#                                                                     status='First Interview Attended').exists():
#                         ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
#                                                                  status='First Interview Attended',
#                                                                  remark='You have attended first interview. Please wait for the further updates.')
#                 else:
#                     continue
#
#             if not application_obj.first_interview_approval:
#                 if application['flags']['id_first'] and application['flags']['id_first_interview_attend'] and \
#                         application['flags'][
#                             'id_first_interview_approval']:
#                     application_obj.first_interview_approval = True
#                     application_obj.save()
#
#                     subject = 'First Interview Approval'
#                     message = 'You have cleared the first round of interview. Please Upload the Psychometric test result.'
#
#                     send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                             application_obj.first_name)
#
#                     if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
#                                                                     status='First Interview Approval').exists():
#                         ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
#                                                                  status='First Interview Approval',
#                                                                  remark='You have cleared your first interview. Please wait for the further updates.')
#                 else:
#                     continue
#
#             if not application_obj.psychometric_test:
#
#                 if application['flags']['id_first'] and application['flags']['id_first_interview_attend'] and \
#                         application['flags'][
#                             'id_first_interview_approval'] and application['flags']['id_test']:
#                     application_obj.psychometric_test = True
#                     application_obj.save()
#
#                     subject = 'Psychometric Test Update'
#                     message = 'You have submitted the Psychometric Test result.'
#
#                     send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                             application_obj.first_name)
#
#                     if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
#                                                                     status='Psychometric Test').exists():
#                         ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
#                                                                  status='Psychometric Test',
#                                                                  remark='You have submitted Psychometric test result. Please wait for the further updates.')
#                 else:
#                     continue
#
#             if not application_obj.second_interview_attend:
#                 if application['flags']['id_first'] and application['flags']['id_first_interview_attend'] and \
#                         application['flags'][
#                             'id_first_interview_approval'] and application['flags']['id_test'] and application['flags'][
#                     'id_second_interview_attend']:
#                     application_obj.second_interview_attend = True
#                     application_obj.save()
#
#                     subject = 'Second Interview Attended'
#                     message = 'This mail is to notify that you have attended second interview. We will update you about the result soon.'
#
#                     send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                             application_obj.first_name)
#
#                     if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
#                                                                     status='Second Interview Attended').exists():
#                         ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
#                                                                  status='Second Interview Attended',
#                                                                  remark='You have attended second interview. Please wait for the further updates.')
#                 else:
#                     continue
#
#             else:
#                 continue
#
#             if not application_obj.second_interview_approval:
#                 if application['flags']['id_first'] and application['flags']['id_first_interview_attend'] and \
#                         application['flags'][
#                             'id_first_interview_approval'] and application['flags']['id_test'] and application['flags'][
#                     'id_second_interview_attend'] and application['flags']['id_second_interview_approval']:
#                     application_obj.second_interview_approval = True
#                     application_obj.save()
#
#                     subject = 'Second Interview Approval'
#                     message = 'You have cleared the second round of interview.'
#
#                     send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                             application_obj.first_name)
#
#                     if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
#                                                                     status='Second Interview Approval').exists():
#                         ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
#                                                                  status='Second Interview Approval',
#                                                                  remark='You have cleared your second interview. Please wait for the further updates.')
#                 else:
#                     continue
#
#             if request.user.is_super_admin():
#                 if not application_obj.admin_approval:
#                     if application['flags']['id_first'] and application['flags']['id_first_interview_attend'] and \
#                             application['flags']['id_first_interview_approval'] and application['flags']['id_test'] and \
#                             application['flags'][
#                                 'id_second_interview_attend'] and application['flags'][
#                         'id_second_interview_approval'] and \
#                             application['flags']['id_admin']:
#
#                         if application['flags']['id_scholarship_fee'] != '':
#                             application_obj.admin_approval = True
#                             application_obj.scholarship_fee = application['flags']['id_scholarship_fee']
#                             application_obj.save()
#
#                             subject = 'Admin Approval'
#                             message = 'Congrats... Your application has got final approval by the admin.'
#
#                             send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                                     application_obj.first_name)
#
#                             if not ApplicationHistoryDetails.objects.filter(
#                                     applicant_id_id=application['application_id'],
#                                     status='Admin Approval').exists():
#                                 ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
#                                                                          status='Admin Approval',
#                                                                          remark='Your application have been approved by the admin. Please wait for the further updates.')
#                     else:
#                         continue
#
#
#     except Exception as e:
#         messages.warning(request, "Form have some error" + str(e))
#
#         # ApplicationDetails.objects.filter(id=application['application_id']).update(
#         #     first_interview=application['flags']['id_first'],
#         #     first_interview_attend=application['flags']['id_first_interview_attend'],
#         #     first_interview_approval=application['flags']['id_first_interview_approval'],
#         #     psychometric_test=application['flags']['id_test'],
#         #     second_interview_attend=application['flags']['id_second_interview_attend'],
#         #     second_interview_approval=application['flags']['id_second_interview_approval'],
#         #     admin_approval=application['flags']['id_admin'],
#         # )
#     return redirect('/partner/template_approving_application/')

def template_application_approval_details(request, app_id):
    try:
        application_rec = ApplicationDetails.objects.get(id=app_id)
        approval_messages = ''

        if application_rec.application_rejection:
            messages.warning(request, "This application has been rejected.")
            # return redirect('/partner/template_approving_application/')

        flag_schedule = False
        admin_flag = False

        final_approval = True

        if not application_rec.first_interview:
            approval_messages = 'First Interview Call'
            flag_schedule = True
            final_approval = False

        elif not application_rec.first_interview_attend:
            approval_messages = 'First Interview Attended'
            final_approval = False

        elif not application_rec.first_interview_approval:
            approval_messages = 'First Interview Approval'
            final_approval = False

        elif not application_rec.psychometric_test:
            if not ApplicantPsychometricTestDetails.objects.filter(applicant_id=application_rec).exists():
                messages.warning(request, "This applicant has not submitted psychometric test.")
                return redirect('/partner/template_approving_application/')

            approval_messages = 'Psychometric Test'
            # flag_test = True
            final_approval = False

        elif not application_rec.second_interview_attend:
            approval_messages = 'Second Interview Attended'
            final_approval = False

        elif not application_rec.second_interview_approval:
            approval_messages = 'Second Interview Approval'
            final_approval = False

        elif not application_rec.admin_approval:
            if not ApplicantAgreementDetails.objects.filter(applicant_id=application_rec).exists():
                messages.warning(request, "This applicant has not submitted agreements.")
                return redirect('/partner/template_approving_application/')

            approval_messages = 'Admin Approval'
            final_approval = False
            admin_flag = True

            if not request.user.is_super_admin():
                messages.warning(request, "Final approval can done only by admin")
                return redirect('/partner/template_approving_application/')

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_approving_application/')

    return render(request, "template_application_approval_details.html",
                  {'application_rec': application_rec, 'approval_messages': approval_messages,
                   'flag_schedule': flag_schedule, 'admin_flag': admin_flag, 'final_approval': final_approval})


def change_application_status(request):
    try:
        check_ids = json.loads(request.POST.get('check_ids'))
        interview_type = request.POST.get('interview_type')

        for application in check_ids:

            # getting application object for flag validations
            application_obj = ApplicationDetails.objects.get(id=application)

            if interview_type == 'First Interview':

                if not application_obj.first_interview:
                    time = request.POST.get('time')
                    date = request.POST.get('date')
                    venue = request.POST.get('venue')

                    if not time == '' or date == '' or venue == '':

                        application_obj.first_interview = True
                        application_obj.interview_time = time
                        application_obj.interview_date = date
                        application_obj.interview_venue = venue
                        application_obj.save()

                        try:
                            email_rec = EmailTemplates.objects.get(template_for='First Interview Call',
                                                                   is_active=True)
                            context = {'first_name': application_obj.first_name, 'time': time, 'venue': venue,
                                       'date': date}
                            send_email_with_template(application_obj, context, email_rec.subject,
                                                     email_rec.email_body,
                                                     request)
                        except:
                            subject = 'First Interview Call'
                            message = 'You are requested to come down for the first interview time at-' + str(
                                time) + ' on ' + str(date) + ' at ' + str(
                                venue) + '. \n \n Thanks and Regards \n \n XYZ'

                            send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                                    application_obj.first_name)

                        application_notification(application_obj.id,
                                                 'You are requested to come down for the first interview. Check your mail for more updates.')

                        if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
                                                                        status='First Interview Call').exists():
                            ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                                     status='First Interview Call',
                                                                     remark='You are requested to come down for the first interview.')

                    else:
                        continue
                else:
                    continue

            elif interview_type == 'First Interview attended':

                if application_obj.first_interview:

                    if not application_obj.first_interview_attend:
                        application_obj.first_interview_attend = True
                        application_obj.save()

                        try:
                            email_rec = EmailTemplates.objects.get(template_for='First Interview Attend',
                                                                   is_active=True)
                            context = {'first_name': application_obj.first_name}
                            send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body,
                                                     request)
                        except:
                            subject = 'First Interview Attended'
                            message = 'This mail is to notify that you have attended first interview. We will update you about the result soon.'

                            send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                                    application_obj.first_name)

                        application_notification(application_obj.id, 'You have attended first interview.')

                        if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
                                                                        status='First Interview Attended').exists():
                            ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                                     status='First Interview Attended',
                                                                     remark='You have attended first interview. Please wait for the further updates.')
                    else:
                        continue
                else:
                    continue

            elif interview_type == 'First Interview approval':
                if application_obj.first_interview_attend:
                    if not application_obj.first_interview_approval:
                        application_obj.first_interview_approval = True
                        application_obj.save()

                        try:
                            email_rec = EmailTemplates.objects.get(template_for='First Interview Approval',
                                                                   is_active=True)
                            context = {'first_name': application_obj.first_name}
                            send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body,
                                                     request)
                        except:
                            subject = 'First Interview Approval'
                            message = 'You have cleared the first round of interview. Please Upload the Psychometric test result. For test please visit at https://www.surveymonkey.com/ and perform test.'
                            send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                                    application_obj.first_name)

                        application_notification(application_obj.id,
                                                 'You have cleared your first interview. For more updates please check your mail.')

                        if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
                                                                        status='First Interview Approval').exists():
                            ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                                     status='First Interview Approval',
                                                                     remark='You have cleared your first interview. Please wait for the further updates.')
                    else:
                        continue
                else:
                    continue

            elif interview_type == 'Psychometric Test':
                if application_obj.first_interview_approval:
                    if not application_obj.psychometric_test:

                        if ApplicantPsychometricTestDetails.objects.filter(applicant_id=application_obj).exists():

                            application_obj.psychometric_test = True
                            application_obj.save()

                            try:
                                email_rec = EmailTemplates.objects.get(template_for='Psychometric Test', is_active=True)
                                context = {'first_name': application_obj.first_name}
                                send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body,
                                                         request)
                            except:
                                subject = 'Psychometric Test Update'
                                message = 'You have submitted the Psychometric Test result.'
                                send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                                        application_obj.first_name)

                            application_notification(application_obj.id, 'You have submitted Psychometric test result.')

                            if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
                                                                            status='Psychometric Test').exists():
                                ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                                         status='Psychometric Test',
                                                                         remark='You have submitted Psychometric test result. Please wait for the further updates.')
                        else:
                            continue
                    else:
                        continue
                else:
                    continue

            elif interview_type == 'Second Interview attended':

                if application_obj.psychometric_test:
                    if not application_obj.second_interview_attend:
                        application_obj.second_interview_attend = True
                        application_obj.save()

                        try:
                            email_rec = EmailTemplates.objects.get(template_for='Second Interview Attend',
                                                                   is_active=True)
                            context = {'first_name': application_obj.first_name}
                            send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body,
                                                     request)
                        except:
                            subject = 'Second Interview Attended'
                            message = 'This mail is to notify that you have attended second interview. We will update you about the result soon.'

                            send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                                    application_obj.first_name)

                        application_notification(application_obj.id,
                                                 'You have attended second interview. We will update you about the result soon.')

                        if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
                                                                        status='Second Interview Attended').exists():
                            ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                                     status='Second Interview Attended',
                                                                     remark='You have attended second interview. Please wait for the further updates.')
                    else:
                        continue
                else:
                    continue

            elif interview_type == 'Second Interview approval':
                if application_obj.second_interview_attend:
                    if not application_obj.second_interview_approval:
                        application_obj.second_interview_approval = True
                        application_obj.save()

                        try:
                            email_rec = EmailTemplates.objects.get(template_for='Second Interview Approval',
                                                                   is_active=True)
                            context = {'first_name': application_obj.first_name}
                            send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body,
                                                     request)
                        except:
                            subject = 'Second Interview Approval'
                            message = 'You have cleared the second round of interview.'
                            send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                                    application_obj.first_name)
                        application_notification(application_obj.id, 'You have cleared the second round of interview.')

                        if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
                                                                        status='Second Interview Approval').exists():
                            ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                                     status='Second Interview Approval',
                                                                     remark='You have cleared your second interview. Please wait for the further updates.')
                    else:
                        continue
                else:
                    continue

            elif interview_type == 'Admin approval':
                if request.user.is_super_admin():
                    if application_obj.second_interview_approval:
                        if not application_obj.admin_approval:
                            scholarship_fee = request.POST.get('scholarship_fee')
                            if scholarship_fee != '':
                                application_obj.admin_approval = True
                                application_obj.scholarship_fee = scholarship_fee
                                application_obj.save()

                                try:
                                    email_rec = EmailTemplates.objects.get(template_for='Admin Approval',
                                                                           is_active=True)
                                    context = {'first_name': application_obj.first_name}
                                    send_email_with_template(application_obj, context, email_rec.subject,
                                                             email_rec.email_body,
                                                             request)
                                except:
                                    subject = 'Admin Approval'
                                    message = 'Congrats... Your application has got final approval by the admin.'

                                    send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                                            application_obj.first_name)

                                application_notification(application_obj.id,
                                                         'Congrats... Your application has got final approval by the admin.')

                                if not ApplicationHistoryDetails.objects.filter(
                                        applicant_id=application_obj,
                                        status='Admin Approval').exists():
                                    ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                                             status='Admin Approval',
                                                                             remark='Your application have been approved by the admin. Please wait for the further updates.')
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue

            elif interview_type == 'Reject':
                if not application_obj.application_rejection:
                    application_obj.application_rejection = True
                    application_obj.save()

                    try:
                        email_rec = EmailTemplates.objects.get(template_for='Application Rejected', is_active=True)
                        context = {'first_name': application_obj.first_name}
                        send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body,
                                                 request)
                    except:
                        subject = 'Application Rejected'
                        message = 'Your application has rejected.'

                        send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                                application_obj.first_name)

                    application_notification(application_obj.id, 'Application Rejected')

                    ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                             status='Application Rejected',
                                                             remark='Your application has rejected.')
                else:
                    continue
            else:
                continue

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/partner/template_approving_application/')


# def change_application_status(request):
#     application_id = request.POST.get('application_rec')
#
#     accept_interview = request.POST.get('accept_interview')
#     reject_interview = request.POST.get('reject_interview')
#
#     try:
#         application_obj = ApplicationDetails.objects.get(id=application_id)
#
#         if accept_interview == None and reject_interview == None:
#             application_obj.application_rejection = False
#             application_obj.save()
#             messages.success(request, "This application rejection is canceled.")
#             return redirect('/partner/template_approving_application/')
#
#         if application_obj.application_rejection:
#             messages.success(request, "This Application Is Already Rejected.")
#             return redirect('/partner/template_approving_application/')
#
#         if reject_interview:
#             application_obj.application_rejection = True
#             application_obj.save()
#
#             try:
#                 email_rec = EmailTemplates.objects.get(template_for='Application Rejected', is_active=True)
#                 context = {'first_name': application_obj.first_name}
#                 send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body, request)
#             except:
#                 subject = 'Application Rejected'
#                 message = 'Your application has rejected.'
#
#                 send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                         application_obj.first_name)
#
#             application_notification(application_obj.id, 'Application Rejected')
#
#             ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
#                                                      status='Application Rejected',
#                                                      remark='Your application has rejected.')
#             messages.success(request, "Application Rejected.")
#             return redirect('/partner/template_approving_application/')
#
#         if accept_interview:
#             if not application_obj.first_interview:
#                 time = request.POST.get('time')
#                 date = request.POST.get('date')
#                 venue = request.POST.get('venue')
#
#                 if not time == '' or date == '' or venue == '':
#
#                     application_obj.first_interview = True
#                     application_obj.interview_time = time
#                     application_obj.interview_date = date
#                     application_obj.interview_venue = venue
#                     application_obj.save()
#
#                     try:
#                         email_rec = EmailTemplates.objects.get(template_for='First Interview Call', is_active=True)
#                         context = {'first_name': application_obj.first_name, 'time': time, 'venue': venue, 'date': date}
#                         send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body,
#                                                  request)
#                     except:
#                         subject = 'First Interview Call'
#                         message = 'You are requested to come down for the first interview time at-' + str(
#                             time) + ' on ' + str(date) + ' at ' + str(venue) + '. \n \n Thanks and Regards \n \n XYZ'
#
#                         send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                                 application_obj.first_name)
#
#                     application_notification(application_obj.id,
#                                              'You are requested to come down for the first interview. Check your mail for more updates.')
#
#                     if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
#                                                                     status='First Interview Call').exists():
#                         ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
#                                                                  status='First Interview Call',
#                                                                  remark='You are requested to come down for the first interview.')
#
#                     messages.success(request, "Record Updated.")
#                     return redirect('/partner/template_approving_application/')
#                 else:
#                     messages.warning(request, "Please Fill The First Interview Call Details.")
#                     return redirect('/partner/template_approving_application/')
#
#             elif not application_obj.first_interview_attend:
#
#                 application_obj.first_interview_attend = True
#                 application_obj.save()
#
#                 try:
#                     email_rec = EmailTemplates.objects.get(template_for='First Interview Attend', is_active=True)
#                     context = {'first_name': application_obj.first_name}
#                     send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body, request)
#                 except:
#                     subject = 'First Interview Attended'
#                     message = 'This mail is to notify that you have attended first interview. We will update you about the result soon.'
#
#                     send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                             application_obj.first_name)
#
#                 application_notification(application_obj.id, 'You have attended first interview.')
#
#                 if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
#                                                                 status='First Interview Attended').exists():
#                     ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
#                                                              status='First Interview Attended',
#                                                              remark='You have attended first interview. Please wait for the further updates.')
#                 messages.success(request, "Record Updated.")
#                 return redirect('/partner/template_approving_application/')
#
#             elif not application_obj.first_interview_approval:
#
#                 application_obj.first_interview_approval = True
#                 application_obj.save()
#
#                 try:
#                     email_rec = EmailTemplates.objects.get(template_for='First Interview Approval', is_active=True)
#                     context = {'first_name': application_obj.first_name}
#                     send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body, request)
#                 except:
#                     subject = 'First Interview Approval'
#                     message = 'You have cleared the first round of interview. Please Upload the Psychometric test result. For test please visit at https://www.surveymonkey.com/ and perform test.'
#                     send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                             application_obj.first_name)
#
#                 application_notification(application_obj.id,
#                                          'You have cleared your first interview. For more updates please check your mail.')
#
#                 if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
#                                                                 status='First Interview Approval').exists():
#                     ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
#                                                              status='First Interview Approval',
#                                                              remark='You have cleared your first interview. Please wait for the further updates.')
#                 messages.success(request, "Record Updated.")
#                 return redirect('/partner/template_approving_application/')
#
#
#             elif not application_obj.psychometric_test:
#                 application_obj.psychometric_test = True
#                 application_obj.save()
#
#                 try:
#                     email_rec = EmailTemplates.objects.get(template_for='Psychometric Test', is_active=True)
#                     context = {'first_name': application_obj.first_name}
#                     send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body, request)
#                 except:
#                     subject = 'Psychometric Test Update'
#                     message = 'You have submitted the Psychometric Test result.'
#                     send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                             application_obj.first_name)
#
#                 application_notification(application_obj.id, 'You have submitted Psychometric test result.')
#
#                 if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
#                                                                 status='Psychometric Test').exists():
#                     ApplicationHistoryDetails.objects.create(applicant_id=application_obj, status='Psychometric Test',
#                                                              remark='You have submitted Psychometric test result. Please wait for the further updates.')
#                 messages.success(request, "Record Updated.")
#                 return redirect('/partner/template_approving_application/')
#
#             elif not application_obj.second_interview_attend:
#                 application_obj.second_interview_attend = True
#                 application_obj.save()
#
#                 try:
#                     email_rec = EmailTemplates.objects.get(template_for='Second Interview Attend', is_active=True)
#                     context = {'first_name': application_obj.first_name}
#                     send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body, request)
#                 except:
#                     subject = 'Second Interview Attended'
#                     message = 'This mail is to notify that you have attended second interview. We will update you about the result soon.'
#
#                     send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                             application_obj.first_name)
#
#                 application_notification(application_obj.id,
#                                          'You have attended second interview. We will update you about the result soon.')
#
#                 if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
#                                                                 status='Second Interview Attended').exists():
#                     ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
#                                                              status='Second Interview Attended',
#                                                              remark='You have attended second interview. Please wait for the further updates.')
#                 messages.success(request, "Record Updated.")
#                 return redirect('/partner/template_approving_application/')
#
#             elif not application_obj.second_interview_approval:
#                 application_obj.second_interview_approval = True
#                 application_obj.save()
#
#                 try:
#                     email_rec = EmailTemplates.objects.get(template_for='Second Interview Approval', is_active=True)
#                     context = {'first_name': application_obj.first_name}
#                     send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body, request)
#                 except:
#                     subject = 'Second Interview Approval'
#                     message = 'You have cleared the second round of interview.'
#                     send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                             application_obj.first_name)
#                 application_notification(application_obj.id, 'You have cleared the second round of interview.')
#
#                 if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
#                                                                 status='Second Interview Approval').exists():
#                     ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
#                                                              status='Second Interview Approval',
#                                                              remark='You have cleared your second interview. Please wait for the further updates.')
#
#                 messages.success(request, "Record Updated.")
#                 return redirect('/partner/template_approving_application/')
#
#             elif not application_obj.admin_approval:
#                 scholarship_fee = request.POST.get('scholarship_fee')
#                 if scholarship_fee != '':
#                     application_obj.admin_approval = True
#                     application_obj.scholarship_fee = scholarship_fee
#                     application_obj.save()
#
#                     try:
#                         email_rec = EmailTemplates.objects.get(template_for='Admin Approval', is_active=True)
#                         context = {'first_name': application_obj.first_name}
#                         send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body,
#                                                  request)
#                     except:
#                         subject = 'Admin Approval'
#                         message = 'Congrats... Your application has got final approval by the admin.'
#
#                         send_email_to_applicant(request.user.email, application_obj.email, subject, message,
#                                                 application_obj.first_name)
#
#                     application_notification(application_obj.id,
#                                              'Congrats... Your application has got final approval by the admin.')
#
#                     if not ApplicationHistoryDetails.objects.filter(
#                             applicant_id=application_obj,
#                             status='Admin Approval').exists():
#                         ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
#                                                                  status='Admin Approval',
#                                                                  remark='Your application have been approved by the admin. Please wait for the further updates.')
#                     messages.success(request, "Record Updated.")
#                     return redirect('/partner/template_approving_application/')
#
#     except Exception as e:
#         messages.warning(request, "Form have some error" + str(e))
#
#     return redirect('/partner/template_approving_application/')
#
#


def change_final_application_status(request):
    application_id = request.POST.get('application_rec')

    accept_interview = request.POST.get('accept_interview')
    # reject_interview = request.POST.get('reject_interview')

    try:
        application_obj = ApplicationDetails.objects.get(id=application_id)

        if accept_interview:
            if not application_obj.admin_approval:
                scholarship_fee = request.POST.get('scholarship_fee')
                if scholarship_fee != '':
                    application_obj.admin_approval = True
                    application_obj.scholarship_fee = scholarship_fee
                    application_obj.save()

                    try:
                        email_rec = EmailTemplates.objects.get(template_for='Admin Approval', is_active=True)
                        context = {'first_name': application_obj.first_name}
                        send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body,
                                                 request)
                    except:
                        subject = 'Admin Approval'
                        message = 'Congrats... Your application has got final approval by the admin.'

                        send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                                application_obj.first_name)

                    application_notification(application_obj.id,
                                             'Congrats... Your application has got final approval by the admin.')

                    if not ApplicationHistoryDetails.objects.filter(
                            applicant_id=application_obj,
                            status='Admin Approval').exists():
                        ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                                 status='Admin Approval',
                                                                 remark='Your application have been approved by the admin. Please wait for the further updates.')
                    messages.success(request, "Record Updated.")
                    return redirect('/partner/template_approving_application/')

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))

    return redirect('/partner/template_approving_application/')


def filter_application_status(request):
    if request.POST:
        request.session['application_status_form_data'] = request.POST
        application_status = request.POST.get('application_status')
    else:
        form_data = request.session.get('application_status_form_data')
        application_status = form_data.get('application_status')

    applicant_recs = ''

    try:
        if request.user.is_superuser:
            if application_status == 'First Interview':
                applicant_recs = ApplicationDetails.objects.filter(
                    is_submitted=True, first_interview=True, year=get_current_year(request))

            elif application_status == 'First Interview attended':
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, first_interview_attend=True,
                                                                   year=get_current_year(request))

            elif application_status == 'First Interview approval':
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True,
                                                                   year=get_current_year(request))

            elif application_status == 'Psychometric Test':
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, psychometric_test=True,
                                                                   year=get_current_year(request))

            elif application_status == 'Second Interview attended':
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, second_interview_attend=True,
                                                                   year=get_current_year(request))

            elif application_status == 'Second Interview approval':
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, second_interview_approval=True,
                                                                   year=get_current_year(request))

            elif application_status == 'Admin approval':
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, admin_approval=True,
                                                                   year=get_current_year(request))
            else:
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, year=get_current_year(request))

        else:

            if application_status == 'First Interview':
                applicant_recs = ApplicationDetails.objects.filter(
                    nationality=request.user.partner_user_rel.get().address.country,
                    is_submitted=True, first_interview=True, year=get_current_year(request))

            elif application_status == 'First Interview attended':
                applicant_recs = ApplicationDetails.objects.filter(
                    nationality=request.user.partner_user_rel.get().address.country,
                    is_submitted=True, first_interview_attend=True, year=get_current_year(request))

            elif application_status == 'First Interview approval':
                applicant_recs = ApplicationDetails.objects.filter(
                    nationality=request.user.partner_user_rel.get().address.country,
                    is_submitted=True, first_interview_approval=True, year=get_current_year(request))

            elif application_status == 'Psychometric Test':
                applicant_recs = ApplicationDetails.objects.filter(
                    nationality=request.user.partner_user_rel.get().address.country,
                    is_submitted=True, psychometric_test=True, year=get_current_year(request))

            elif application_status == 'Second Interview attended':
                applicant_recs = ApplicationDetails.objects.filter(
                    nationality=request.user.partner_user_rel.get().address.country,
                    is_submitted=True, second_interview_attend=True, year=get_current_year(request))

            elif application_status == 'Second Interview approval':
                applicant_recs = ApplicationDetails.objects.filter(
                    nationality=request.user.partner_user_rel.get().address.country,
                    is_submitted=True, second_interview_approval=True, year=get_current_year(request))

            elif application_status == 'Admin approval':
                applicant_recs = ApplicationDetails.objects.filter(
                    nationality=request.user.partner_user_rel.get().address.country,
                    is_submitted=True, admin_approval=True, year=get_current_year(request))
            else:
                applicant_recs = ApplicationDetails.objects.filter(
                    nationality=request.user.partner_user_rel.get().address.country,
                    is_submitted=True, year=get_current_year(request))

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))

    return render(request, 'template_approving_application.html',
                  {'applicant_recs': applicant_recs, 'application_status': application_status})


def template_student_progress_history(request):
    applicant_recs = ''
    try:
        if request.user.is_super_admin():
            applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, year=get_current_year(request))
        else:
            applicant_recs = ApplicationDetails.objects.filter(
                nationality=request.user.partner_user_rel.get().address.country,
                is_submitted=True, year=get_current_year(request))

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))

    return render(request, 'template_student_progress_history.html',
                  {'applicant_recs': applicant_recs})


def filter_application_history(request):
    if request.POST:
        request.session['application_history_form_data'] = request.POST
        application = request.POST.get('application')
    else:
        form_data = request.session.get('application_history_form_data')
        application = form_data.get('application')

    try:
        if request.user.is_super_admin():
            applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, year=get_current_year(request))
            application_history_recs = ApplicationDetails.objects.get(id=application).applicant_history_rel.all()
            application_obj = ApplicationDetails.objects.get(id=application)
        else:
            applicant_recs = ApplicationDetails.objects.filter(
                nationality=request.user.partner_user_rel.get().address.country, is_submitted=True,
                year=get_current_year(request))
            application_obj = ApplicationDetails.objects.get(id=application)

            application_history_recs = ApplicationDetails.objects.get(id=application).applicant_history_rel.all()

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, 'template_student_progress_history.html',
                  {'applicant_recs': applicant_recs, 'application_history_recs': application_history_recs,
                   'application_obj': application_obj})


def template_psychometric_test_report(request):
    try:
        if request.user.is_super_admin():
            appliaction_recs = ApplicationDetails.objects.filter(is_submitted=True, year=get_current_year(request),
                                                                 first_interview_approval=True)
        else:
            appliaction_recs = ApplicationDetails.objects.filter(year=get_current_year(request),
                                                                 first_interview_approval=True,
                                                                 nationality=request.user.partner_user_rel.get().address.country,
                                                                 is_submitted=True)

        attended_list = []

        for rec in appliaction_recs:
            program_dict = {}
            program_dict['name'] = rec.get_full_name()
            program_dict['country'] = rec.address.country.country_name

            if ApplicantPsychometricTestDetails.objects.filter(applicant_id=rec.id).exists():
                psychometric_rec = ApplicantPsychometricTestDetails.objects.get(applicant_id=rec.id)

                program_dict['result'] = psychometric_rec.result
                program_dict['test_result_document'] = psychometric_rec.test_result_document

            else:
                program_dict['result'] = ''
                program_dict['test_result_document'] = ''

            program_dict['application'] = rec

            attended_list.append(program_dict)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, 'template_psychometric_test_report.html', {'attended_list': attended_list})


def filter_psychometric_test_report(request):
    try:
        if request.POST:
            request.session['psychometric_test'] = request.POST
            filter = request.POST.get('filter')
        else:
            form_data = request.session.get('psychometric_test')
            filter = form_data.get('filter')

        if request.user.is_super_admin():
            appliaction_recs = ApplicationDetails.objects.filter(is_submitted=True, year=get_current_year(request),
                                                                 first_interview_approval=True)
        else:
            appliaction_recs = ApplicationDetails.objects.filter(year=get_current_year(request),
                                                                 first_interview_approval=True,
                                                                 nationality=request.user.partner_user_rel.get().address.country,
                                                                 is_submitted=True)

        filter_rec = {}

        attended_list = []

        for rec in appliaction_recs:

            if filter == 'examined':
                if ApplicantPsychometricTestDetails.objects.filter(applicant_id=rec.id).exists():
                    psychometric_rec = ApplicantPsychometricTestDetails.objects.get(applicant_id=rec.id)

                    program_dict = {}
                    program_dict['name'] = rec.get_full_name()
                    program_dict['country'] = rec.address.country.country_name
                    program_dict['application'] = rec

                    program_dict['result'] = psychometric_rec.result
                    program_dict['test_result_document'] = psychometric_rec.test_result_document
                    filter_rec['value'] = 'examined'
                    filter_rec['name'] = 'Examined'

                    attended_list.append(program_dict)

            elif filter == 'not_examined':
                if not ApplicantPsychometricTestDetails.objects.filter(applicant_id=rec.id).exists():
                    program_dict = {}
                    program_dict['name'] = rec.get_full_name()
                    program_dict['country'] = rec.address.country.country_name
                    program_dict['application'] = rec

                    program_dict['result'] = ''
                    program_dict['test_result_document'] = ''
                    filter_rec['value'] = 'not_examined'
                    filter_rec['name'] = 'Not Examined'
                    attended_list.append(program_dict)

            else:
                program_dict = {}
                program_dict['name'] = rec.get_full_name()
                program_dict['country'] = rec.address.country.country_name
                program_dict['application'] = rec

                if ApplicantPsychometricTestDetails.objects.filter(applicant_id=rec.id).exists():
                    psychometric_rec = ApplicantPsychometricTestDetails.objects.get(applicant_id=rec.id)

                    program_dict['result'] = psychometric_rec.result
                    program_dict['test_result_document'] = psychometric_rec.test_result_document

                else:
                    program_dict['result'] = ''
                    program_dict['test_result_document'] = ''
                filter_rec['value'] = 'all'
                filter_rec['name'] = 'All'

                attended_list.append(program_dict)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, 'template_psychometric_test_report.html',
                  {'attended_list': attended_list, 'filter_rec': filter_rec})


def template_link_student_program(request):
    if request.user.is_super_admin():
        applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, year=get_current_year(request))
        university_recs = UniversityDetails.objects.filter()
    else:
        applicant_recs = ApplicationDetails.objects.filter(
            nationality=request.user.partner_user_rel.get().address.country,
            year=get_current_year(request), is_submitted=True)
        university_recs = UniversityDetails.objects.filter(country=request.user.partner_user_rel.get().address.country)

    module_recs = ModuleDetails.objects.all()

    rec_list = []

    semester_recs = SemesterDetails.objects.all()

    for applicant_rec in applicant_recs:
        temp_dict = {}

        if StudentModuleMapping.objects.filter(applicant_id=applicant_rec).exists():
            module_obj = StudentModuleMapping.objects.filter(applicant_id=applicant_rec)

            temp_dict['program'] = module_obj[0].program
            temp_dict['module'] = module_obj
            temp_dict['semester'] = module_obj[0].module.semester
            temp_dict['applicant_rec'] = module_obj[0].applicant_id
            temp_dict['flag'] = False

        else:
            temp_dict['program'] = applicant_rec.applicant_scholarship_rel.get().course_applied
            temp_dict['module'] = ''
            temp_dict['semester'] = ''
            temp_dict['applicant_rec'] = applicant_rec
            temp_dict['flag'] = True

        rec_list.append(temp_dict)

    country_recs = CountryDetails.objects.all()
    degree_recs = DegreeDetails.objects.all()
    modules_recs = ModuleDetails.objects.all()
    program_recs = DevelopmentProgram.objects.filter(year=YearDetails.objects.get(active_year=1))

    return render(request, 'template_link_student_program.html',
                  {'applicant_recs': applicant_recs, 'country_recs': country_recs, 'university_recs': university_recs,
                   'degree_recs': degree_recs, 'semester_recs': semester_recs, 'rec_list': rec_list,
                   'program_recs': program_recs, 'modules_recs': modules_recs})


def get_semester_modules(request):
    finalDict = []
    semester = request.POST.get('semester_id', None)

    modules_recs = DevelopmentProgram.objects.filter(year=YearDetails.objects.get(active_year=1), semester_id=semester)
    module_id = []

    for rec in modules_recs:
        if rec.id not in module_id:
            module_id.append(rec.id)
            module_data = {'id': rec.id, 'module_name': rec.module.module_name.title()}
            finalDict.append(module_data)
    return JsonResponse(finalDict, safe=False)


def save_student_program(request):
    try:
        data_value = json.loads(request.POST.get('data_value'))
    except Exception as e:
        messages.warning(request, "No record updated.")
        return redirect('/partner/template_link_student_program/')

    try:
        for application in data_value:
            if not StudentModuleMapping.objects.filter(applicant_id_id=application['applicant_id']).exists():
                flag_module_assigned = False
                for module in application['applicant_module']:
                    StudentModuleMapping.objects.create(program_id=application['applicant_program'],
                                                        degree_id=application['degree'],
                                                        applicant_id_id=application['applicant_id'],
                                                        module_id=module)
                    flag_module_assigned = True
                if flag_module_assigned:
                    application_notification(application['applicant_id'],
                                             'Some modules have assigned to your.')

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/partner/template_link_student_program/')


def template_academic_progress(request):
    try:
        scholarship_type = ScholarshipDetails.objects.all()
        application_list = []
        application_id = []
        if request.user.is_super_admin():
            application_recs = ApplicantAcademicProgressDetails.objects.filter(
                applicant_id__year=get_current_year(request), ).order_by('-last_updated')
            for application in application_recs:
                if application.applicant_id.id not in application_id:
                    application_list.append(application)
                    application_id.append(application.applicant_id.id)
        else:
            application_recs = ApplicantAcademicProgressDetails.objects.filter(
                applicant_id__year=get_current_year(request),
                applicant_id__nationality=request.user.partner_user_rel.get().address.country).order_by(
                '-last_updated')
            for application in application_recs:
                if application.applicant_id.id not in application_id:
                    application_list.append(application)
                    application_id.append(application.applicant_id.id)


    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_academic_progress/')

    return render(request, 'template_academic_progress.html',
                  {'application_recs': application_list, 'scholarship_type': scholarship_type})


def filter_academic_progress(request):
    if request.POST:
        request.session['academic_progress_form_data'] = request.POST
        scholarship = request.POST.get('scholarship')
        export = request.POST.get('export')
    else:
        form_data = request.session.get('academic_progress_form_data')
        scholarship = form_data.get('scholarship')
        export = form_data.get('export')

    try:
        scholarship_type = ScholarshipDetails.objects.all()
        scholarship_obj = ScholarshipDetails.objects.get(id=scholarship)
        application_list = []
        application_id = []

        applicant_ids = ScholarshipSelectionDetails.objects.filter(scholarship_id=scholarship).values_list(
            'applicant_id')
        if request.user.is_super_admin():
            application_recs = ApplicantAcademicProgressDetails.objects.filter(applicant_id__in=applicant_ids,
                                                                               applicant_id__year=get_current_year(
                                                                                   request)).order_by(
                '-last_updated')
            # for application in application_recs:
            #     if application.applicant_id.id not in application_id:
            #         application_list.append(application)
            #         application_id.append(application.applicant_id.id)
        else:
            application_recs = ApplicantAcademicProgressDetails.objects.filter(applicant_id__in=applicant_ids,
                                                                               applicant_id__year=get_current_year(
                                                                                   request),
                                                                               applicant_id__nationality=request.user.partner_user_rel.get().address.country).order_by(
                '-last_updated')
        for application in application_recs:
            if application.applicant_id.id not in application_id:
                application_list.append(application)
                application_id.append(application.applicant_id.id)

        if export:
            rows = []
            export_application_id = []

            for application in application_recs:
                temp_list = []
                if application.applicant_id.id not in export_application_id:
                    temp_list.append(application.applicant_id.get_full_name())
                    temp_list.append(application.applicant_id.address.country.country_name.title())
                    temp_list.append(
                        application.applicant_id.applicant_scholarship_rel.all()[0].university.university_name.title())
                    temp_list.append(
                        application.applicant_id.applicant_scholarship_rel.all()[0].degree.degree_name.title())
                    temp_list.append(
                        application.applicant_id.applicant_scholarship_rel.all()[0].course_applied.program_name.title())
                    temp_list.append(application.semester.semester_name.title())
                    temp_list.append(application.gpa_scored)
                    temp_list.append(application.cgpa_scored)
                    temp_list.append(application.date)
                    temp_list.append(application.transcript_document)
                    rows.append(temp_list)

                    export_application_id.append(application.applicant_id.id)

            column_names = ['Student Name', 'Country', 'University', 'Degree', 'Program', 'Semester', 'GPA', 'CGPA',
                            'Date', 'PDF']
            return export_wraped_column_xls('academic_progress_details', column_names, rows)


    except Exception as e:

        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_academic_progress/')

    return render(request, 'template_academic_progress.html',
                  {'application_recs': application_list, 'scholarship_type': scholarship_type,
                   'scholarship_obj': scholarship_obj})


def export_academic_progress_details(request):
    try:
        progress_list = []
        column_names = ['Name', 'Session', 'Date', 'Semester', 'Transcript', 'GPA Minimum', 'GPA Maximum',
                        'Grade Minimum', 'Grade Maximum']
        progress_list.append(column_names)
        app_id = request.POST.get('export')
        progress_rec = ApplicantAcademicProgressDetails.objects.filter(applicant_id=app_id,
                                                                       applicant_id__year=get_current_year(request))
        for rec in progress_rec:
            temp_list = []
            temp_list.append(str(rec.applicant_id.applicant_id.get_full_name()))
            temp_list.append(str(rec.year.year_name))
            temp_list.append(str(rec.date))
            temp_list.append(str(rec.semester.semester_name))
            temp_list.append(str(rec.transcript_document))
            temp_list.append(str(rec.gpa_scored))
            temp_list.append(str(rec.gpa_from))
            temp_list.append(str(rec.cgpa_scored))
            temp_list.append(str(rec.cgpa_from))
            progress_list.append(temp_list)

        return export_pdf('academic_progress_details', progress_list)
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_academic_progress/')


def template_academic_progress_details(request, app_id):
    try:
        progress_rec = ApplicantAcademicProgressDetails.objects.filter(applicant_id=app_id)
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_academic_progress/')

    return render(request, "template_academic_progress_details.html",
                  {'progress_recs': progress_rec})


def template_attendance_report(request):
    try:
        # modules_recs = ModuleDetails.objects.all()
        if request.user.is_super_admin():
            all_modules = StudentModuleMapping.objects.filter(
                applicant_id__year=get_current_year(request))
        else:
            all_modules = StudentModuleMapping.objects.filter(
                applicant_id__nationality=request.user.partner_user_rel.get().address.country,
                applicant_id__year=get_current_year(request))

        attended_list = []
        not_attended_list = []

        for rec in all_modules:
            program_dict = {}
            if ApplicantDevelopmentProgramDetails.objects.filter(applicant_id=rec.applicant_id,
                                                                 module=rec.module).exists():
                certificate_rec = ApplicantDevelopmentProgramDetails.objects.get(applicant_id=rec.applicant_id,
                                                                                 module=rec.module)
                program_dict[
                    'name'] = rec.applicant_id.get_full_name()
                program_dict['country'] = rec.applicant_id.address.country.country_name
                program_dict['degree'] = rec.degree.degree_name
                program_dict['program'] = rec.module.name
                program_dict['module'] = rec.module.module.module_name
                program_dict['semester'] = rec.module.semester.semester_name
                program_dict['certificate'] = certificate_rec.certificate_document

                attended_list.append(program_dict)

            else:
                program_dict[
                    'name'] = rec.applicant_id.get_full_name()
                program_dict['country'] = rec.applicant_id.address.country.country_name
                program_dict['degree'] = rec.degree.degree_name
                program_dict['program'] = rec.module.name
                program_dict['module'] = rec.module.module.module_name
                program_dict['semester'] = rec.module.semester.semester_name
                program_dict['certificate'] = ''

                not_attended_list.append(program_dict)


    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, "template_attendance_report.html",
                  {'attended_recs': attended_list, 'not_attended_recs': not_attended_list})


def filter_attendance_report(request):
    if request.POST:
        request.session['attendance_report'] = request.POST
        modules = request.POST.get('modules')
    else:
        form_data = request.session.get('attendance_report')
        modules = form_data.get('modules')

    try:

        if modules == 'All':
            return redirect('/partner/template_attendance_report/')

        # modules_recs = ModuleDetails.objects.all()
        # module_obj = ModuleDetails.objects.get(id=modules)
        if request.user.is_super_admin():
            all_modules = StudentModuleMapping.objects.filter(applicant_id__year=get_current_year(request))
        else:
            all_modules = StudentModuleMapping.objects.filter(
                applicant_id__nationality=request.user.partner_user_rel.get().address.country,
                applicant_id__year=get_current_year(request))

        attended_list = []
        not_attended_list = []

        for rec in all_modules:
            program_dict = {}
            if ApplicantDevelopmentProgramDetails.objects.filter(applicant_id=rec.applicant_id,
                                                                 module=rec.module).exists():
                certificate_rec = ApplicantDevelopmentProgramDetails.objects.get(applicant_id=rec.applicant_id,
                                                                                 module=rec.module)
                program_dict[
                    'name'] = rec.applicant_id.get_full_name()
                program_dict['country'] = rec.applicant_id.address.country.country_name
                program_dict['degree'] = rec.degree.degree_name
                program_dict['program'] = rec.module.name
                program_dict['module'] = rec.module.module.module_name
                program_dict['semester'] = rec.module.semester.semester_name
                program_dict['certificate'] = certificate_rec.certificate_document

                attended_list.append(program_dict)

            else:
                program_dict[
                    'name'] = rec.applicant_id.get_full_name()
                program_dict['country'] = rec.applicant_id.address.country.country_name
                program_dict['degree'] = rec.degree.degree_name
                program_dict['program'] = rec.module.name
                program_dict['module'] = rec.module.module.module_name
                program_dict['semester'] = rec.module.semester.semester_name
                program_dict['certificate'] = ''

                not_attended_list.append(program_dict)

        filter_obj = {}

        if modules == 'attended':
            filter_obj['value'] = 'attended'
            filter_obj['name'] = 'Attended'
            return render(request, "template_attendance_report.html",
                          {'attended_recs': attended_list, 'filter_obj': filter_obj})
        else:
            filter_obj['value'] = 'not_attended'
            filter_obj['name'] = 'Not Attended'

            return render(request, "template_attendance_report.html",
                          {'not_attended_recs': not_attended_list, 'filter_obj': filter_obj})


    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_attendance_report/')


def template_accepted_students(request):
    try:
        scholarship_type = ScholarshipDetails.objects.all()
        application_list = []
        # application_id = []
        if request.user.is_super_admin():
            application_ids = ApplicationDetails.objects.filter(admin_approval=True,
                                                                year=get_current_year(request)).values_list('id')

        else:
            application_ids = ApplicationDetails.objects.filter(
                nationality=request.user.partner_user_rel.get().address.country,
                year=get_current_year(request)).values_list('id')
        scholarship_recs = ScholarshipSelectionDetails.objects.filter(applicant_id__in=application_ids)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_accepted_students/')

    return render(request, 'template_accepted_students.html',
                  {'scholarship_recs': scholarship_recs, 'scholarship_type': scholarship_type})


def template_link_students_donor(request):
    try:
        donor_recs = DonorDetails.objects.all()
        if request.user.is_super_admin():
            application_ids = ApplicationDetails.objects.filter(admin_approval=True,
                                                                year=get_current_year(request)).values_list('id')

        else:
            application_ids = ApplicationDetails.objects.filter(
                nationality=request.user.partner_user_rel.get().address.country,
                year=get_current_year(request)).values_list('id')
        scholarship_recs = ScholarshipSelectionDetails.objects.filter(applicant_id__in=application_ids)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_link_students_donor/')

    return render(request, 'template_link_students_donor.html',
                  {'scholarship_recs': scholarship_recs, 'donor_recs': donor_recs})


def save_students_donor_linking(request):
    try:
        data_value = json.loads(request.POST.get('data_value'))

        for rec in data_value:
            if StudentDonorMapping.objects.filter(student_id=rec['student'], applicant_id_id=rec['applicant']).exists():
                StudentDonorMapping.objects.filter(student_id=rec['student'], applicant_id_id=rec['applicant']).update(
                    donor_id=rec['donor'])
            else:
                StudentDonorMapping.objects.create(student_id=rec['student'], applicant_id_id=rec['applicant'],
                                                   donor_id=rec['donor'])

        messages.success(request, "Record Saved")

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/partner/template_link_students_donor/')


def template_donor_students_linking(request):
    try:
        donor_recs = DonorDetails.objects.all()
        if request.user.is_super_admin():
            applicant_ids = StudentDonorMapping.objects.filter(
                applicant_id__year=get_current_year(request)).values_list(
                'applicant_id', flat=1)
            application_ids = ApplicationDetails.objects.filter(id__in=applicant_ids).values_list('id', flat=1)

        else:
            applicant_ids = StudentDonorMapping.objects.filter(applicant_id__year=get_current_year(request),
                                                               applicant_id__nationality=request.user.partner_user_rel.get().address.country).values_list(
                'applicant_id', flat=1)
            application_ids = ApplicationDetails.objects.filter(id__in=applicant_ids).values_list('id', flat=1)

        scholarship_recs = ScholarshipSelectionDetails.objects.filter(applicant_id__in=application_ids)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_donor_students_linking/')

    return render(request, 'template_donor_students_linking.html',
                  {'scholarship_recs': scholarship_recs, 'donor_recs': donor_recs})


def filter_donor_student_linking(request):
    if request.POST:
        request.session['donor_student_linking'] = request.POST
        donor = request.POST.get('donor')
    else:
        form_data = request.session.get('donor_student_linking')
        donor = form_data.get('donor')

    try:

        donor_recs = DonorDetails.objects.all()
        donor_obj = ''
        if request.user.is_super_admin():
            if donor == 'All':
                applicant_ids = StudentDonorMapping.objects.filter(
                    applicant_id__year=get_current_year(request)).values_list(
                    'applicant_id', flat=1)
            else:
                donor_obj = DonorDetails.objects.get(id=donor)
                applicant_ids = StudentDonorMapping.objects.filter(applicant_id__year=get_current_year(request),
                                                                   donor_id=donor).values_list('applicant_id', flat=1)
            application_ids = ApplicationDetails.objects.filter(id__in=applicant_ids).values_list('id', flat=1)

        else:
            if donor == 'All':
                applicant_ids = StudentDonorMapping.objects.filter(applicant_id__year=get_current_year(request),
                                                                   applicant_id__nationality=request.user.partner_user_rel.get().address.country).values_list(
                    'applicant_id', flat=1)
            else:
                donor_obj = DonorDetails.objects.get(id=donor)
                applicant_ids = StudentDonorMapping.objects.filter(applicant_id__year=get_current_year(request),
                                                                   donor_id=donor,
                                                                   applicant_id__nationality=request.user.partner_user_rel.get().address.country).values_list(
                    'applicant_id', flat=1)
            application_ids = ApplicationDetails.objects.filter(id__in=applicant_ids).values_list('id', flat=1)

        scholarship_recs = ScholarshipSelectionDetails.objects.filter(applicant_id__in=application_ids)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_donor_students_linking/')

    return render(request, 'template_donor_students_linking.html',
                  {'scholarship_recs': scholarship_recs, 'donor_recs': donor_recs, 'donor_obj': donor_obj})


def template_student_agreement(request):
    try:
        if request.user.is_super_admin():
            all_applications = ApplicationDetails.objects.filter(year=get_current_year(request))
        else:
            all_applications = ApplicationDetails.objects.filter(
                nationality=request.user.partner_user_rel.get().address.country,
                year=get_current_year(request))

        attended_list = []
        not_attended_list = []

        for rec in all_applications:
            program_dict = {}

            if ApplicantAgreementDetails.objects.filter(applicant_id=rec).exists():

                agreement_rec = ApplicantAgreementDetails.objects.get(applicant_id=rec)
                program_dict['name'] = rec.get_full_name()
                program_dict['country'] = rec.address.country.country_name
                program_dict['four_parties'] = agreement_rec.four_parties_agreement_document
                program_dict['education_loan'] = agreement_rec.education_loan_agreement_document
                program_dict['application'] = rec

                attended_list.append(program_dict)

            else:
                program_dict['name'] = rec.get_full_name()
                program_dict['country'] = rec.address.country.country_name
                program_dict['four_parties'] = ''
                program_dict['education_loan'] = ''
                program_dict['application'] = rec

                not_attended_list.append(program_dict)


    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, "template_student_agreement.html",
                  {'attended_recs': attended_list, 'not_attended_recs': not_attended_list})


def filter_student_agreement(request):
    try:
        if request.POST:
            request.session['student_agreement'] = request.POST
            filter = request.POST.get('filter')
        else:
            form_data = request.session.get('student_agreement')
            filter = form_data.get('filter')

        if request.user.is_super_admin():
            all_applications = ApplicationDetails.objects.filter(year=get_current_year(request))
        else:
            all_applications = ApplicationDetails.objects.filter(
                nationality=request.user.partner_user_rel.get().address.country,
                year=get_current_year(request))

        filter_rec = {}

        attended_list = []
        not_attended_list = []

        for rec in all_applications:

            if filter == 'submitted':
                if ApplicantAgreementDetails.objects.filter(applicant_id=rec).exists():
                    program_dict = {}
                    agreement_rec = ApplicantAgreementDetails.objects.get(applicant_id=rec)
                    program_dict['name'] = rec.get_full_name()
                    program_dict['country'] = rec.address.country.country_name
                    program_dict['four_parties'] = agreement_rec.four_parties_agreement_document
                    program_dict['education_loan'] = agreement_rec.education_loan_agreement_document
                    program_dict['application'] = rec

                    attended_list.append(program_dict)

                    filter_rec['value'] = 'submitted'
                    filter_rec['name'] = 'Submitted'

            elif filter == 'not_submitted':
                if not ApplicantAgreementDetails.objects.filter(applicant_id=rec).exists():
                    program_dict = {}

                    program_dict['name'] = rec.get_full_name()
                    program_dict['country'] = rec.address.country.country_name
                    program_dict['four_parties'] = ''
                    program_dict['education_loan'] = ''
                    program_dict['application'] = rec

                    not_attended_list.append(program_dict)

                    filter_rec['value'] = 'not_submitted'
                    filter_rec['name'] = 'Not Submitted'

            else:
                program_dict = {}
                program_dict['name'] = rec.get_full_name()
                program_dict['country'] = rec.address.country.country_name
                program_dict['application'] = rec

                if ApplicantAgreementDetails.objects.filter(applicant_id=rec).exists():

                    agreement_rec = ApplicantAgreementDetails.objects.get(applicant_id=rec)
                    program_dict['four_parties'] = agreement_rec.four_parties_agreement_document
                    program_dict['education_loan'] = agreement_rec.education_loan_agreement_document

                    attended_list.append(program_dict)

                else:
                    program_dict['four_parties'] = ''
                    program_dict['education_loan'] = ''

                    not_attended_list.append(program_dict)
                filter_rec['value'] = 'all'
                filter_rec['name'] = 'All'

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, "template_student_agreement.html",
                  {'filter_rec': filter_rec, 'attended_recs': attended_list, 'not_attended_recs': not_attended_list})


def template_semester_result(request):
    try:
        scholarship_type = ScholarshipDetails.objects.all()
        application_list = []
        application_id = []
        if request.user.is_super_admin():
            application_recs = ApplicantAcademicProgressDetails.objects.filter(
                applicant_id__year=get_current_year(request), ).order_by('-last_updated')
            for application in application_recs:
                if application.applicant_id.id not in application_id:
                    application_list.append(application)
                    application_id.append(application.applicant_id.id)
        else:
            application_recs = ApplicantAcademicProgressDetails.objects.filter(
                applicant_id__year=get_current_year(request),
                applicant_id__nationality=request.user.partner_user_rel.get().address.country).order_by(
                '-last_updated')
            for application in application_recs:
                if application.applicant_id.id not in application_id:
                    application_list.append(application)
                    application_id.append(application.applicant_id.id)


    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_academic_progress/')

    return render(request, 'template_semester_result.html',
                  {'application_recs': application_list, 'scholarship_type': scholarship_type})


# import os
# from django.conf import settings
# from django.http import HttpResponse
# from django.template import Context
# from django.template.loader import get_template
# import datetime
# from xhtml2pdf import pisa
#
#
# def generate_student_details_pdf(request,app_id):
#     year_recs = YearDetails.objects.all()
#     curriculum_obj = ''
#     experience_obj = ''
#
#     application_obj = ApplicationDetails.objects.get(id=app_id)
#     siblings_obj = application_obj.sibling_applicant_rel.all() if application_obj.sibling_applicant_rel.all() else ''
#     qualification_obj = application_obj.academic_applicant_rel.get() if application_obj.academic_applicant_rel.all() else ''
#     english_obj = application_obj.english_applicant_rel.get() if application_obj.english_applicant_rel.all() else ''
#     curriculum_obj = application_obj.curriculum_applicant_rel.get() if application_obj.curriculum_applicant_rel.all() else ''
#     applicant_experience_obj = application_obj.applicant_experience_rel.get() if application_obj.applicant_experience_rel.all() else ''
#     scholarship_obj = application_obj.applicant_scholarship_rel.get() if application_obj.applicant_scholarship_rel.all() else ''
#
#     template = get_template('template_applicant_all_details.html')
#     Context = ({'siblings_obj': siblings_obj, 'application_obj': application_obj,
#                    'qualification_obj': qualification_obj, 'english_obj': english_obj,
#                    'curriculum_obj': curriculum_obj,
#                    'applicant_experience_obj': applicant_experience_obj,
#                    'scholarship_obj': scholarship_obj})
#     html = template.render(Context)
#     response = HttpResponse(html)
#     output_file_name= 'fffffffff'
#
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=' + str(output_file_name) + '.pdf'
#
#     return response


# file = open('test.pdf', "w+b")
# pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
#         encoding='utf-8')
#
# file.seek(0)
# pdf = file.read()
# file.close()
# return HttpResponse(pdf, 'application/pdf')


def donar_student_linking_export(request):
    try:
        if request.POST:
            request.session['donor_student_linking'] = request.POST
            donor = request.POST.get('donor')

        else:
            form_data = request.session.get('donor_student_linking')
            donor = form_data.get('donor')

        try:
            if donor == "":
                donor = "All"
            rows = []
            donor_recs = DonorDetails.objects.all()
            donor_obj = ''
            if request.user.is_super_admin():
                if donor == 'All':
                    applicant_ids = StudentDonorMapping.objects.filter(
                        applicant_id__year=get_current_year(request)).values_list('applicant_id', flat=1)
                else:
                    donor_obj = DonorDetails.objects.get(id=donor)
                    applicant_ids = StudentDonorMapping.objects.filter(applicant_id__year=get_current_year(request),
                                                                       donor_id=donor).values_list('applicant_id',
                                                                                                   flat=1)
                application_ids = ApplicationDetails.objects.filter(id__in=applicant_ids).values_list('id', flat=1)

            else:
                if donor == 'All':
                    applicant_ids = StudentDonorMapping.objects.filter(applicant_id__year=get_current_year(request),
                                                                       applicant_id__nationality=request.user.partner_user_rel.get().address.country).values_list(
                        'applicant_id', flat=1)
                else:
                    donor_obj = DonorDetails.objects.get(id=donor)
                    applicant_ids = StudentDonorMapping.objects.filter(applicant_id__year=get_current_year(request),
                                                                       donor_id=donor,
                                                                       applicant_id__nationality=request.user.partner_user_rel.get().address.country).values_list(
                        'applicant_id', flat=1)
                application_ids = ApplicationDetails.objects.filter(id__in=applicant_ids).values_list('id', flat=1)

            scholarship_recs = ScholarshipSelectionDetails.objects.filter(applicant_id__in=application_ids)
            for rec in scholarship_recs:
                rec_list = []
                rec_list.append(rec.applicant_id.get_full_name())
                rec_list.append(rec.applicant_id.nationality.country_name)
                rec_list.append(rec.applicant_id.address.country.country_name)
                rec_list.append(rec.university.university_name)
                rec_list.append(rec.course_applied.degree_name)
                if rec.applicant_id.applicant_module_rel.all():
                    rec.append(rec.applicant_id.applicant_module_rel.all()[0].program.program_name)
                else:
                    rec_list.append("")

                rows.append(rec_list)


        except Exception as e:
            return redirect('/partner/template_donor_students_linking/')

        column_names = ["Student Name", "Nationality", "Country", "University ", "Degree", "Program"]

        return export_wraped_column_xls('DonorStudentLinking', column_names, rows)
    except:
        return redirect('/partner/template_donor_students_linking/')


def template_link_students_parent(request):
    students_recs = ApplicationDetails.objects.filter(admin_approval=True, year=get_current_year(request))

    # students_recs = StudentDetails.objects.filter(id__in=studs)
    parents_recs = GuardianDetails.objects.all()
    return render(request, "template_link_student_to_parent.html",
                  {'students_recs': students_recs, 'parents_recs': parents_recs})


def save_students_parent_linking(request):
    try:
        data_value = json.loads(request.POST.get('data_value'))

        for rec in data_value:
            if GuardianStudentMapping.objects.filter(student_id=rec['student']).exists():
                GuardianStudentMapping.objects.filter(student_id=rec['student']).update(
                    guardian_id=rec['parent'])
            else:
                GuardianStudentMapping.objects.create(student_id=rec['student'],
                                                      guardian_id=rec['parent'])

        messages.success(request, "Record Saved")

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/partner/template_link_students_parent/')


def application_all_details_pdf(request, app_id):
    try:
        year_recs = YearDetails.objects.all()
        curriculum_obj = ''
        experience_obj = ''

        x = 14

        application_obj = ApplicationDetails.objects.get(id=app_id)
        report_path = settings.MEDIA_ROOT + str('reports/') + str(application_obj.first_name) + '_' + str(
            application_obj.id) + '/'

        siblings_obj = application_obj.sibling_applicant_rel.all() if application_obj.sibling_applicant_rel.all() else ''
        qualification_obj = application_obj.academic_applicant_rel.get() if application_obj.academic_applicant_rel.all() else ''
        english_obj = application_obj.english_applicant_rel.get() if application_obj.english_applicant_rel.all() else ''
        curriculum_obj = application_obj.curriculum_applicant_rel.get() if application_obj.curriculum_applicant_rel.all() else ''
        applicant_experience_obj = application_obj.applicant_experience_rel.get() if application_obj.applicant_experience_rel.all() else ''
        scholarship_obj = application_obj.applicant_scholarship_rel.get() if application_obj.applicant_scholarship_rel.all() else ''

        template = get_template('application_all_details_pdf.html')
        Context = ({'report_path': report_path, 'application_obj': application_obj, 'siblings_obj': siblings_obj,
                    'qualification_obj': qualification_obj, 'english_obj': english_obj,
                    'curriculum_obj': curriculum_obj, 'applicant_experience_obj': applicant_experience_obj,
                    'scholarship_obj': scholarship_obj, 'x': x})
        html = template.render(Context)

        file = open('test.pdf', "w+b")
        pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                    encoding='utf-8')

        file.seek(0)
        pdf = file.read()
        file.close()
        return HttpResponse(pdf, 'application/pdf')
    except:
        return redirect('/partner/template_applicant_all_details/' + str(app_id))
