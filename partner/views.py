from django.shortcuts import render, redirect
from masters.models import *
from student.models import *
from partner.models import *
import json
from django.contrib import messages
from django.http import JsonResponse
from common.utils import send_email_to_applicant, application_notification, export_pdf
from django.db.models import Max, Q


# Create your views here.

def template_registered_application(request):
    if request.user.is_super_admin():
        applicant_recs = ApplicationDetails.objects.filter(is_submitted=True)
        university_recs = UniversityDetails.objects.all()
    else:
        applicant_recs = ApplicationDetails.objects.filter(address__country=request.user.partner_user_rel.get().country,
                                                           is_submitted=True)
        university_recs = UniversityDetails.objects.filter(country=request.user.partner_user_rel.get().country)
    country_recs = CountryDetails.objects.all()
    degree_recs = DegreeDetails.objects.all()

    return render(request, 'template_registered_application.html',
                  {'applicant_recs': applicant_recs, 'country_recs': country_recs, 'university_recs': university_recs,
                   'degree_recs': degree_recs})


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
        request.session['form_data'] = request.POST
        university = request.POST.get('university')
        degree = request.POST.get('degree')
        nationality = request.POST.get('nationality')
        country = request.POST.get('country')
    else:

        form_data = request.session.get('form_data')

        university = form_data.get('university')
        degree = form_data.get('degree')
        nationality = form_data.get('nationality')
        country = form_data.get('country')

    try:

        if request.user.is_super_admin():
            applicant_recs = ApplicationDetails.objects.filter(
                Q(is_submitted=True), filter_country(country), filter_nationality(nationality),
                filter_degree(degree),
                filter_university(university))

            university_recs = UniversityDetails.objects.all()
        else:
            applicant_recs = ApplicationDetails.objects.filter(
                Q(address__country=request.user.partner_user_rel.get().country,
                  is_submitted=True), filter_nationality(nationality),
                filter_degree(degree),
                filter_university(university))

            university_recs = UniversityDetails.objects.filter(country=request.user.partner_user_rel.get().country)

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
            applicant_recs = ApplicationDetails.objects.filter(is_submitted=True)
        else:
            applicant_recs = ApplicationDetails.objects.filter(
                address__country=request.user.partner_user_rel.get().country,
                is_submitted=True)
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
    application_id = request.POST.get('application_rec')

    accept_interview = request.POST.get('accept_interview')
    reject_interview = request.POST.get('reject_interview')

    try:
        application_obj = ApplicationDetails.objects.get(id=application_id)

        if accept_interview == None and reject_interview == None:
            application_obj.application_rejection = False
            application_obj.save()
            messages.success(request, "This application rejection is canceled.")
            return redirect('/partner/template_approving_application/')

        if application_obj.application_rejection:
            messages.success(request, "This Application Is Already Rejected.")
            return redirect('/partner/template_approving_application/')

        if reject_interview:
            application_obj.application_rejection = True
            application_obj.save()

            subject = 'Application Rejected'
            message = 'Your application has rejected.'

            send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                    application_obj.first_name)

            application_notification(application_obj.id, 'Application Rejected')

            # if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
            #                                                 status='Application Rejected').exists():
            ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                     status='Application Rejected',
                                                     remark='Your application has rejected.')
            messages.success(request, "Application Rejected.")
            return redirect('/partner/template_approving_application/')

        if accept_interview:
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

                    subject = 'First Interview Call'
                    message = 'You are requested to come down for the first interview time at-' + str(
                        time) + ' on ' + str(date) + ' at ' + str(venue) + '. \n \n Thanks and Regards \n \n XYZ'

                    send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                            application_obj.first_name)
                    application_notification(application_obj.id,
                                             'You are requested to come down for the first interview. Check your mail for more updates.')

                    if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
                                                                    status='First Interview Call').exists():
                        ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                                 status='First Interview Call',
                                                                 remark='You are requested to come down for the first interview.')

                    messages.success(request, "Record Updated.")
                    return redirect('/partner/template_approving_application/')
                else:
                    messages.warning(request, "Please Fill The First Interview Call Details.")
                    return redirect('/partner/template_approving_application/')

            elif not application_obj.first_interview_attend:

                application_obj.first_interview_attend = True
                application_obj.save()

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
                messages.success(request, "Record Updated.")
                return redirect('/partner/template_approving_application/')

            elif not application_obj.first_interview_approval:

                application_obj.first_interview_approval = True
                application_obj.save()

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
                messages.success(request, "Record Updated.")
                return redirect('/partner/template_approving_application/')


            elif not application_obj.psychometric_test:
                application_obj.psychometric_test = True
                application_obj.save()

                subject = 'Psychometric Test Update'
                message = 'You have submitted the Psychometric Test result.'

                send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                        application_obj.first_name)
                application_notification(application_obj.id,
                                         'You have submitted Psychometric test result.')

                if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
                                                                status='Psychometric Test').exists():
                    ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                             status='Psychometric Test',
                                                             remark='You have submitted Psychometric test result. Please wait for the further updates.')
                messages.success(request, "Record Updated.")
                return redirect('/partner/template_approving_application/')

            elif not application_obj.second_interview_attend:
                application_obj.second_interview_attend = True
                application_obj.save()

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
                messages.success(request, "Record Updated.")
                return redirect('/partner/template_approving_application/')

            elif not application_obj.second_interview_approval:
                application_obj.second_interview_approval = True
                application_obj.save()

                subject = 'Second Interview Approval'
                message = 'You have cleared the second round of interview.'

                send_email_to_applicant(request.user.email, application_obj.email, subject, message,
                                        application_obj.first_name)
                application_notification(application_obj.id,
                                         'You have cleared the second round of interview.')

                if not ApplicationHistoryDetails.objects.filter(applicant_id=application_obj,
                                                                status='Second Interview Approval').exists():
                    ApplicationHistoryDetails.objects.create(applicant_id=application_obj,
                                                             status='Second Interview Approval',
                                                             remark='You have cleared your second interview. Please wait for the further updates.')
                messages.success(request, "Record Updated.")
                return redirect('/partner/template_approving_application/')

            elif not application_obj.admin_approval:
                scholarship_fee = request.POST.get('scholarship_fee')
                if scholarship_fee != '':
                    application_obj.admin_approval = True
                    application_obj.scholarship_fee = scholarship_fee
                    application_obj.save()

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
        request.session['form_data'] = request.POST
        application_status = request.POST.get('application_status')
    else:
        form_data = request.session.get('form_data')
        application_status = form_data.get('application_status')

    applicant_recs = ''

    try:
        if request.user.is_system_admin:
            if application_status == 'First Interview':
                applicant_recs = ApplicationDetails.objects.filter(
                    is_submitted=True, first_interview=True)

            elif application_status == 'First Interview attended':
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, first_interview_attend=True)

            elif application_status == 'First Interview approval':
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, first_interview_approval=True)

            elif application_status == 'Psychometric Test':
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, psychometric_test=True)

            elif application_status == 'Second Interview attended':
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, second_interview_attend=True)

            elif application_status == 'Second Interview approval':
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, second_interview_approval=True)

            elif application_status == 'Admin approval':
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True, admin_approval=True)
            else:
                applicant_recs = ApplicationDetails.objects.filter(is_submitted=True)

        else:

            if application_status == 'First Interview':
                applicant_recs = ApplicationDetails.objects.filter(
                    address__country=request.user.partner_user_rel.get().country,
                    is_submitted=True, first_interview=True)

            elif application_status == 'First Interview attended':
                applicant_recs = ApplicationDetails.objects.filter(
                    address__country=request.user.partner_user_rel.get().country,
                    is_submitted=True, first_interview_attend=True)

            elif application_status == 'First Interview approval':
                applicant_recs = ApplicationDetails.objects.filter(
                    address__country=request.user.partner_user_rel.get().country,
                    is_submitted=True, first_interview_approval=True)

            elif application_status == 'Psychometric Test':
                applicant_recs = ApplicationDetails.objects.filter(
                    address__country=request.user.partner_user_rel.get().country,
                    is_submitted=True, psychometric_test=True)

            elif application_status == 'Second Interview attended':
                applicant_recs = ApplicationDetails.objects.filter(
                    address__country=request.user.partner_user_rel.get().country,
                    is_submitted=True, second_interview_attend=True)

            elif application_status == 'Second Interview approval':
                applicant_recs = ApplicationDetails.objects.filter(
                    address__country=request.user.partner_user_rel.get().country,
                    is_submitted=True, second_interview_approval=True)

            elif application_status == 'Admin approval':
                applicant_recs = ApplicationDetails.objects.filter(
                    address__country=request.user.partner_user_rel.get().country,
                    is_submitted=True, admin_approval=True)
            else:
                applicant_recs = ApplicationDetails.objects.filter(
                    address__country=request.user.partner_user_rel.get().country,
                    is_submitted=True)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))

    return render(request, 'template_approving_application.html',
                  {'applicant_recs': applicant_recs, 'application_status': application_status})


def template_student_progress_history(request):
    applicant_recs = ''
    try:
        if request.user.is_super_admin():
            applicant_recs = ApplicationDetails.objects.filter(is_submitted=True)
        else:
            applicant_recs = ApplicationDetails.objects.filter(
                address__country=request.user.partner_user_rel.get().country,
                is_submitted=True)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))

    return render(request, 'template_student_progress_history.html',
                  {'applicant_recs': applicant_recs})


def filter_application_history(request):
    if request.POST:
        request.session['form_data'] = request.POST
        application = request.POST.get('application')
    else:
        form_data = request.session.get('form_data')
        application = form_data.get('application')

    try:
        if request.user.is_super_admin():
            applicant_recs = ApplicationDetails.objects.filter(is_submitted=True)
            application_history_recs = ApplicationDetails.objects.get(id=application).applicant_history_rel.all()
            application_obj = ApplicationDetails.objects.get(id=application)

        # elif request.user.is_donor():
        #     stud = []
        #     for obj in StudentDonorMapping.objects.filter(donor__user=request.user):
        #         stud.append(StudentDetails.objects.get(id=obj.student.id))
        #
        #     applicant_recs = ApplicationDetails.objects.filter(student__in=stud,
        #                                                        address__country=request.user.donor_user_rel.get().country,
        #                                                        is_sponsored=True)
        #     application_obj = ApplicationDetails.objects.get(id=application)
        #     application_history_recs = ApplicationDetails.objects.get(id=application).applicant_history_rel.all()

        else:
            applicant_recs = ApplicationDetails.objects.filter(
                address__country=request.user.partner_user_rel.get().country, is_submitted=True)
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
            appliaction_ids = ApplicationDetails.objects.filter(is_submitted=True).values_list('id')
        else:
            appliaction_ids = ApplicationDetails.objects.filter(
                address__country=request.user.partner_user_rel.get().country,
                is_submitted=True).values_list('id')
        psychometric_obj = ApplicantPsychometricTestDetails.objects.filter(applicant_id__in=appliaction_ids)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, 'template_psychometric_test_report.html',
                  {'psychometric_obj': psychometric_obj})


def template_link_student_program(request):
    if request.user.is_super_admin():
        applicant_recs = ApplicationDetails.objects.filter(is_submitted=True)
        university_recs = UniversityDetails.objects.filter()
    else:
        applicant_recs = ApplicationDetails.objects.filter(address__country=request.user.partner_user_rel.get().country,
                                                           is_submitted=True)
        university_recs = UniversityDetails.objects.filter(country=request.user.partner_user_rel.get().country)

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
            program_recs = ProgramDetails.objects.filter(
                university=applicant_rec.applicant_scholarship_rel.get().university,
                degree_type=applicant_rec.applicant_scholarship_rel.get().course_applied.degree_type)

            temp_dict['program_recs'] = program_recs
            temp_dict['applicant_rec'] = applicant_rec
            temp_dict['flag'] = True

        rec_list.append(temp_dict)

    country_recs = CountryDetails.objects.all()
    degree_recs = DegreeDetails.objects.all()
    program_recs = ProgramDetails.objects.all()

    return render(request, 'template_link_student_program.html',
                  {'applicant_recs': applicant_recs, 'country_recs': country_recs, 'university_recs': university_recs,
                   'degree_recs': degree_recs, 'semester_recs': semester_recs, 'rec_list': rec_list,
                   'program_recs': program_recs})


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
        messages.warning(request, "Records is already saved")
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
        application_list = []
        application_id = []
        if request.user.is_super_admin():
            application_recs = ApplicantAcademicProgressDetails.objects.all().order_by('-last_updated')
            for application in application_recs:
                if application.applicant_id.id not in application_id:
                    application_list.append(application)
                    application_id.append(application.applicant_id.id)
        else:
            application_recs = ApplicantAcademicProgressDetails.objects.filter(
                applicant_id__address__country=request.user.partner_user_rel.get().country).order_by('-last_updated')
            for application in application_recs:
                if application.applicant_id.id not in application_id:
                    application_list.append(application)
                    application_id.append(application.applicant_id.id)


    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, 'template_academic_progress.html',
                  {'application_recs': application_list})


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
        if request.user.is_super_admin():
            # attendance_rec = ApplicantDevelopmentProgramDetails.objects.filter(applicant_id__year=YearDetails.objects.get(active_year=True))
            # attended_rec = ApplicantDevelopmentProgramDetails.objects.filter(applicant_id__year=YearDetails.objects.get(active_year=True)).values_list('applicant_id',flat=1)
            # not_attended_recs = ApplicationDetails.objects.filter(~Q(id__in=attended_rec),year=YearDetails.objects.get(active_year=True))
            # StudentModuleMapping.objects.filter(~Q(applicant_id__in=attended_rec),year=YearDetails.objects.get(active_year=True),module__module='')

            all_modules = StudentModuleMapping.objects.filter(applicant_id__year=YearDetails.objects.get(active_year=True))
        else:
            # attendance_rec = ApplicantDevelopmentProgramDetails.objects.filter(applicant_id__year=YearDetails.objects.get(active_year=True),applicant_id__address__country=request.user.partner_user_rel.get().country)
            # attended_rec = ApplicantDevelopmentProgramDetails.objects.filter(applicant_id__year=YearDetails.objects.get(active_year=True),applicant_id__address__country=request.user.partner_user_rel.get().country).values_list('applicant_id', flat=1)
            # not_attended_recs = ApplicationDetails.objects.filter(~Q(id__in=attended_rec),year=YearDetails.objects.get(active_year=True))

            all_modules = StudentModuleMapping.objects.filter(applicant_id__address__country=request.user.partner_user_rel.get().country,applicant_id__year=YearDetails.objects.get(active_year=True))

        attended_list = []
        not_attended_list = []

        for rec in all_modules:
            program_dict = {}
            if ApplicantDevelopmentProgramDetails.objects.filter(applicant_id=rec.applicant_id,module=rec.module.module).exists():
                certificate_rec = ApplicantDevelopmentProgramDetails.objects.get(applicant_id=rec.applicant_id,module=rec.module.module)
                program_dict['name'] = rec.applicant_id.first_name + ' ' + rec.applicant_id.last_name if rec.applicant_id.last_name else ''
                program_dict['country'] = rec.applicant_id.address.country.country_name
                program_dict['degree'] = rec.degree.degree_name
                program_dict['program'] =rec.program.program_name
                program_dict['module'] =rec.module.module.module_name
                program_dict['semester'] =rec.module.semester.semester_name
                program_dict['certificate'] =certificate_rec.certificate_document

                attended_list.append(program_dict)

            else:
                program_dict['name'] = rec.applicant_id.first_name + ' ' + rec.applicant_id.last_name if rec.applicant_id.last_name else ''
                program_dict['country'] = rec.applicant_id.address.country.country_name
                program_dict['degree'] = rec.degree.degree_name
                program_dict['program'] = rec.program.program_name
                program_dict['module'] = rec.module.module.module_name
                program_dict['semester'] = rec.module.semester.semester_name
                program_dict['certificate'] = ''

                not_attended_list.append(program_dict)


    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_attendance_report/')

    return render(request, "template_attendance_report.html",
                  {'attended_recs': attended_list,'not_attended_recs':not_attended_list})


def export_academic_progress_details(request):
    try:
        progress_list = []
        column_names = ['Name', 'Session', 'Date', 'Semester', 'Transcript', 'GPA Minimum', 'GPA Maximum',
                        'Grade Minimum', 'Grade Maximum']
        progress_list.append(column_names)
        app_id = request.POST.get('export')
        progress_rec = ApplicantAcademicProgressDetails.objects.filter(applicant_id=app_id)
        for rec in progress_rec:
            temp_list = []
            temp_list.append(str(rec.applicant_id.first_name + ' ' + rec.applicant_id.last_name))
            temp_list.append(str(rec.year.year_name))
            temp_list.append(str(rec.date))
            temp_list.append(str(rec.semester.semester_name))
            temp_list.append(str(rec.transcript_document))
            temp_list.append(str(rec.gpa_scored))
            temp_list.append(str(rec.gpa_from))
            temp_list.append(str(rec.cgpa_scored))
            temp_list.append(str(rec.cgpa_from))
            progress_list.append(temp_list)

        return export_pdf('export_skill_entry', progress_list)
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_academic_progress/')
