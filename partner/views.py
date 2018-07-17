from django.shortcuts import render, redirect
from masters.models import *
from student.models import *
from partner.models import *
import json
from django.contrib import messages


# Create your views here.

def template_registered_application(request):
    applicant_recs = ApplicationDetails.objects.filter(address__country=request.user.partner_user_rel.get().country,
                                                       is_submitted=True)
    country_recs = CountryDetails.objects.all()
    university_recs = UniversityDetails.objects.filter(country=request.user.partner_user_rel.get().country)
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


def filter_registered_application(request):
    if request.POST:
        request.session['form_data'] = request.POST
        university = request.POST.get('university')
        degree = request.POST.get('degree')
        nationality = request.POST.get('nationality')
    else:

        form_data = request.session.get('form_data')

        university = form_data.get('university')
        degree = form_data.get('degree')
        nationality = form_data.get('nationality')

    try:

        applicant_recs = ApplicationDetails.objects.filter(
            Q(address__country=request.user.partner_user_rel.get().country,
              is_submitted=True), filter_nationality(nationality),
            filter_degree(degree),
            filter_university(university))

        country_recs = CountryDetails.objects.all()
        university_recs = UniversityDetails.objects.filter(country=request.user.partner_user_rel.get().country)
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


def change_application_status(request):
    data_value = json.loads(request.POST.get('data_value'))

    try:

        for application in data_value:

            # getting application object for falg validations
            application_obj = ApplicationDetails.objects.get(id=application['application_id'])

            # validations on flag
            if application['flags']['id_first']:
                application_obj.first_interview = True
                application_obj.save()

                if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
                                                                status='First Interview Call').exists():
                    ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
                                                             status='First Interview Call',
                                                             remark='You are requested to come down for the first interview.')
            else:
                continue

            if application['flags']['id_first'] and application['flags']['id_first_interview_attend']:
                application_obj.first_interview_attend = True
                application_obj.save()

                if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
                                                                status='First Interview Attended').exists():
                    ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
                                                             status='First Interview Attended',
                                                             remark='You have attended first interview. Please wait for the further updates.')
            else:
                continue

            if application['flags']['id_first'] and application['flags']['id_first_interview_attend'] and \
                    application['flags'][
                        'id_first_interview_approval']:
                application_obj.first_interview_approval = True
                application_obj.save()

                if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
                                                                status='First Interview Approval').exists():
                    ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
                                                             status='First Interview Approval',
                                                             remark='You have cleared your first interview. Please wait for the further updates.')
            else:
                continue

            if application['flags']['id_first'] and application['flags']['id_first_interview_attend'] and \
                    application['flags'][
                        'id_first_interview_approval'] and application['flags']['id_test']:
                application_obj.psychometric_test = True
                application_obj.save()

                if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
                                                                status='Psychometric Test').exists():
                    ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
                                                             status='Psychometric Test',
                                                             remark='You have submitted Psychometric test result. Please wait for the further updates.')
            else:
                continue

            if application['flags']['id_first'] and application['flags']['id_first_interview_attend'] and \
                    application['flags'][
                        'id_first_interview_approval'] and application['flags']['id_test'] and application['flags'][
                'id_second_interview_attend']:
                application_obj.second_interview_attend = True
                application_obj.save()

                if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
                                                                status='Second Interview Attended').exists():
                    ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
                                                             status='Second Interview Attended',
                                                             remark='You have attended second interview. Please wait for the further updates.')
            else:
                continue

            if application['flags']['id_first'] and application['flags']['id_first_interview_attend'] and \
                    application['flags'][
                        'id_first_interview_approval'] and application['flags']['id_test'] and application['flags'][
                'id_second_interview_attend'] and application['flags']['id_second_interview_approval']:
                application_obj.second_interview_approval = True
                application_obj.save()

                if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
                                                                status='Second Interview Approval').exists():
                    ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
                                                             status='Second Interview Approval',
                                                             remark='You have cleared your second interview. Please wait for the further updates.')
            else:
                continue

            if request.user.is_super_admin():
                if application['flags']['id_first'] and application['flags']['id_first_interview_attend'] and \
                        application['flags']['id_first_interview_approval'] and application['flags']['id_test'] and \
                        application['flags'][
                            'id_second_interview_attend'] and application['flags']['id_second_interview_approval'] and \
                        application['flags']['id_admin']:
                    application_obj.admin_approval = True
                    application_obj.save()

                    if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application['application_id'],
                                                                    status='Admin Approval').exists():
                        ApplicationHistoryDetails.objects.create(applicant_id_id=application['application_id'],
                                                                 status='Admin Approval',
                                                                 remark='Your application have been approved by the admin. Please wait for the further updates.')
                else:
                    continue


    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))

        # ApplicationDetails.objects.filter(id=application['application_id']).update(
        #     first_interview=application['flags']['id_first'],
        #     first_interview_attend=application['flags']['id_first_interview_attend'],
        #     first_interview_approval=application['flags']['id_first_interview_approval'],
        #     psychometric_test=application['flags']['id_test'],
        #     second_interview_attend=application['flags']['id_second_interview_attend'],
        #     second_interview_approval=application['flags']['id_second_interview_approval'],
        #     admin_approval=application['flags']['id_admin'],
        # )
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
        appliaction_ids = ApplicationDetails.objects.filter(
            address__country=request.user.partner_user_rel.get().country,
            is_submitted=True).values_list('id')
        psychometric_obj = ApplicantPsychometricTestDetails.objects.filter(applicant_id__in=appliaction_ids)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, 'template_psychometric_test_report.html',
                  {'psychometric_obj': psychometric_obj})
