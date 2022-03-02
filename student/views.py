from django.shortcuts import render, redirect
from masters.views import *
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

# Create your views here.
@student_login_required
def student_home(request):
    username = ''
    application_history_obj = ''
    application_id = ''
    application = ''

    try:
        first_name = request.user.first_name
        last_name = request.user.last_name if request.user.last_name else ''
        username = str(first_name) + ' ' + str(last_name)

        if ApplicationDetails.objects.filter(application_id=request.user.get_application_id).exists():
            application = request.user.get_application
            if request.user.get_application.is_submitted:
                application_history_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id,
                                                                         is_submitted=True).applicant_history_rel.all()
            else:
                application_id = request.user.get_application.id

    except Exception as e:
        username = request.user.first_name
        messages.warning(request, "Form have some error" + str(e))

    return render(request, 'student_home.html',
                  {'username': username, 'application_history_obj': application_history_obj,
                   'application_id': application_id, 'application': application})


def delete_application(request, app_id):
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

    except Exception as e:
        messages.warning(request, "An error occurred " + str(e))
    return redirect('/student/student_home/')

@student_login_required
def applicant_personal_info(request):
    country_recs = CountryDetails.objects.all()
    religion_recs = ReligionDetails.objects.all()
    student_recs = StudentDetails.objects.filter(user__is_active = True)
    agent_recs = AgentDetails.objects.filter()


    application_obj = ''

    if ApplicationDetails.objects.filter(application_id=request.user.get_application_id).exists():
        application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id)

    #if ApplicationDetails.objects.filter(id=request.user.get_application.id).exists():
    #     application_obj = ApplicationDetails.objects.get(id=request.user.get_application.id)

    return render(request, 'applicant_personal_info.html',
                  {'country_recs': country_recs, 'religion_recs': religion_recs, 'application_obj': application_obj,'student_recs':student_recs,'agent_recs':agent_recs})


def save_update_applicant_personal_info(request):
    passport_photo = request.FILES.get('passport_photo')
    pic = request.FILES.get('photo')
    same_as = request.POST.get('same_as')
    # value_check = json.loads(request.POST.get('value_check'))
    redirect_flag = False
    # from_status = from_status_check(list(value_check.values()))

    if request.POST:
        if StudentDetails.objects.filter(user=request.user):
            student = StudentDetails.objects.get(user=request.user)

            if request.POST['first_name'] and request.POST['last_name'] and request.POST['email'] != '':

                if ApplicationDetails.objects.filter(application_id=request.user.get_application_id).exists():

                    ApplicationDetails.objects.filter(application_id=request.user.get_application_id).update(
                        first_name=request.POST['first_name'],
                        middle_name=request.POST['middle_name'],
                        last_name=request.POST['last_name'],
                        surname=request.POST['surname'],
                        passport_number=request.POST.get('passport_number'),
                        email=request.POST['email'])

                    application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id)

                    AddressDetails.objects.filter(id=application_obj.address.id).update(
                        country_id=request.POST['country'],
                        mobile=request.POST['mobile'],
                        whats_app=request.POST['whats_app'],
                        country_code=request.POST['country_code'],
                        district=request.POST['district'],
                        post_code=request.POST['post_code'],
                        residential_address=request.POST['permanent_residential_address'],
                        street=request.POST['permanent_street'])

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
                                                                            year=current_year)

                        address_obj = AddressDetails.objects.create(country_id=request.POST['country'],
                                                                    mobile=request.POST['mobile'],
                                                                    whats_app=request.POST['whats_app'],
                                                                    country_code=request.POST['country_code'],
                                                                    district=request.POST['district'],
                                                                    post_code=request.POST['post_code'],
                                                                    residential_address=request.POST['permanent_residential_address'],
                                                                    street=request.POST['permanent_street'])

                        application_id = get_application_id(application_obj)
                        application_obj.application_id = application_id
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
                return redirect('/student/applicant_personal_info/')

    if redirect_flag:
        messages.success(request, "Record saved")
        return redirect('/student/applicant_intake_info/')
    else:
        messages.warning(request, "Please fill proper form")
        return redirect('/student/applicant_personal_info/')


def applicant_family_info(request):
    country_recs = AllCountries.objects.all()
    path = ''
    application_obj = ''
    sibling_obj = ''
    if ApplicationDetails.objects.filter(application_id=request.user.get_application_id).exists():
        application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id)
        path = base_path(application_obj)
        if SiblingDetails.objects.filter(applicant_id=application_obj).exists():
            sibling_obj = SiblingDetails.objects.filter(applicant_id=application_obj)


    return render(request, 'applicant_family_info.html',{'country_recs': country_recs, 'application_obj': application_obj, 'path': path,'sibling_obj_rec': sibling_obj})


def save_update_applicant_family_info(request):
    redirect_flag = False
    if request.POST:
        try:

            try:
                mother_pay_slip = request.FILES['mother_pay_slip']
            except Exception as e:
                mother_pay_slip = ''

            try:
                father_pay_slip = request.FILES.get('father_pay_slip')

            except:
                father_pay_slip = ''

            father_pay_slip_text = request.POST.get('father_pay_slip_text')

            sibling_count = request.POST.get('sibling_count')
            mother_pay_slip_text = request.POST.get('mother_pay_slip_text')

            if StudentDetails.objects.filter(user=request.user):

                ApplicationDetails.objects.filter(application_id=request.user.get_application_id).update(
                    mother_name=request.POST['mother_name'],
                    mother_income=request.POST['mother_income'],
                    mother_nationality=request.POST['mother_nationality'],
                    mother_occupation=request.POST['mother_occupation'],
                    mother_telephone_home=request.POST['mother_telephone_home'],
                    mother_dob=request.POST['mother_dob'] if request.POST['mother_dob'] else None,
                    mother_email=request.POST['mother_email'],
                    mother_home_address=request.POST['mother_home_address'],

                    father_name=request.POST['father_name'],
                    father_income=request.POST['father_income'],
                    father_nationality=request.POST['father_nationality'],
                    father_occupation=request.POST['father_occupation'],
                    father_telephone_home=request.POST['father_telephone_home'],
                    father_dob=request.POST['father_dob'] if request.POST['father_dob'] else None,
                    father_email=request.POST['father_email'],
                    father_home_address =request.POST['father_home_address'] )


                application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id)

                mother_slip = str(mother_pay_slip)

                if mother_pay_slip:
                    object_path = media_path(application_obj)
                    handle_uploaded_file(str(object_path) + '/' + mother_slip, mother_pay_slip)
                    application_obj.mother_pay_slip = mother_slip

                if not mother_pay_slip_text:
                    application_obj.mother_pay_slip = ''

                if father_pay_slip:
                    object_path = media_path(application_obj)
                    father_slip = str(father_pay_slip)
                    handle_uploaded_file(str(object_path) + '/' + father_slip, father_pay_slip)
                    application_obj.father_pay_slip = father_slip

                if not father_pay_slip_text:
                    application_obj.father_pay_slip = ''

                application_obj.save()





                for x in range(int(sibling_count)):
                    try:
                        x = x + 1
                        if request.POST['sibling_id_' + str(x)]:
                            SiblingDetails.objects.filter(id=request.POST['sibling_id_' + str(x)]).update(sibling_name=request.POST['sibling_' + str(x)],sibling_age=request.POST['age_' + str(x)],sibling_status=request.POST['status_' + str(x)])
                        else:
                            SiblingDetails.objects.create(sibling_name=request.POST['sibling_' + str(x)],
                                                          sibling_age=request.POST['age_' + str(x)],
                                                          sibling_status=request.POST['status_' + str(x)],
                                                          applicant_id=application_obj)
                    except:
                        pass

                redirect_flag = True

            if redirect_flag:
                messages.success(request, "Record saved")
                return redirect('/student/applicant_family_mother_sibling_info/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/student/applicant_family_info/')


def applicant_family_mother_sibling_info(request):
    country_recs = AllCountries.objects.all()
    path = ''

    application_obj = ''

    if ApplicationDetails.objects.filter(application_id=request.user.get_application_id).exists():
        application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id)
        path = base_path(application_obj)

    return render(request, 'applicant_family_mother_sibling_info.html',
                  {'country_recs': country_recs, 'application_obj': application_obj,"path":path})


def save_update_applicant_family_mother_sibling_info(request):
    redirect_flag = False

    if request.POST:
        try:
            try:
                wife_pay_slip = request.FILES.get('wife_pay_slip')

            except Exception as e:
                wife_pay_slip = ''

            wife_pay_slip_text = request.POST.get('wife_pay_slip_text')

            if StudentDetails.objects.filter(user=request.user):

                ApplicationDetails.objects.filter(application_id=request.user.get_application_id).update(wife_name=request.POST['wife_name'],
                    wife_income=request.POST['wife_income'],
                    wife_nationality=request.POST['wife_nationality'],
                    wife_occupation=request.POST['wife_occupation'],
                    wife_telephone_home=request.POST['wife_telephone_home'],
                    wife_dob=request.POST['wife_dob'] if request.POST['wife_dob'] else None,
                    wife_email=request.POST['wife_email'],
                    wife_home_address=request.POST['wife_home_address'])



                application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id)

                if wife_pay_slip:
                    object_path = media_path(application_obj)

                    wife_slip = str(wife_pay_slip)
                    handle_uploaded_file(str(object_path) + '/' + wife_slip, wife_pay_slip)
                    application_obj.wife_pay_slip = wife_slip

                if not wife_pay_slip_text:
                    application_obj.wife_pay_slip = ''



                application_obj.save()

                redirect_flag = True

            if redirect_flag:
                messages.success(request, "Record saved")
                return redirect('/student/applicant_academic_english_qualification/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/student/applicant_family_mother_sibling_info/')


def applicant_academic_english_qualification(request):
    year_recs = YearDetails.objects.all()
    qualification_obj = ''
    english_obj = ''
    arab_obj = ''
    passing_year_recs = PassingYear.objects.filter().order_by('-year')
    country_recs = CountryDetails.objects.all()
    english_competency_test_recs = EnglishCompetencyTestDetails.objects.all()
    arab_competency_test_recs = ArabCompetencyTestDetails.objects.all()

    try:
        application_obj = request.user.get_application
    except Exception as e :
        messages.warning(request, "Please fill the personal details first.")
        return redirect('/student/applicant_personal_info/')

    try:
        if request.user.get_application:
            # if not request.user.get_application.is_submitted:
            # application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id,
            #                                           is_submitted=False)
            if AcademicQualificationDetails.objects.filter(applicant_id=request.user.get_application).exists():
                qualification_obj = AcademicQualificationDetails.objects.filter(
                    applicant_id=request.user.get_application)

            if EnglishQualificationDetails.objects.filter(applicant_id=request.user.get_application).exists():
                english_obj = EnglishQualificationDetails.objects.filter(applicant_id=request.user.get_application)
                arab_obj = ArabQualificationDetails.objects.filter(applicant_id=request.user.get_application)
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/applicant_personal_info/')

    return render(request, 'applicant_academic_english_qualification.html',
                  {'year_recs': year_recs, 'qualification_recs': qualification_obj, 'english_recs': english_obj,'arab_recs': arab_obj,
                   'passing_year_recs': passing_year_recs, 'application_obj': application_obj,'country_recs':country_recs,'english_competency_test_recs':english_competency_test_recs,
                   'arab_competency_test_recs':arab_competency_test_recs})


def save_update_applicant_academic_english_qualification(request):
    redirect_flag = False
    academic_count = request.POST.get('academic_count')
    english_count = request.POST.get('english_count')
    arab_count = request.POST.get('arab_count')

    if request.POST:

        try:
            if StudentDetails.objects.filter(user=request.user):
                # if not request.user.get_application.is_submitted:
                try:
                    if not AcademicQualificationDetails.objects.filter(applicant_id = request.user.get_application).exists():
                        application_obj = ApplicationDetails.objects.get(id = request.user.get_application.id)
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
                                    applicant_id=request.user.get_application)

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
                                    applicant_id=request.user.get_application)

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
                                    applicant_id=request.user.get_application)
                            arab_object.save()
                        except Exception as e:
                            pass

                    redirect_flag = True
                except Exception as e:
                    messages.warning(request, "Form have some error" + str(e))
                # else:
                #     messages.success(request, "Please fill the record.")
                #     return redirect('/student/applicant_personal_info/')

                if redirect_flag:
                    messages.success(request, "Record saved")
                    return redirect('/student/applicant_credit_transfer/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/student/applicant_academic_english_qualification/')


#------ BACKUP Academic Qalification----------------

# def save_update_applicant_academic_english_qualification(request):
#     redirect_flag = False
#
#     if request.POST:
#         try:
#             a_level_result_document = request.FILES.get('a_level_result_document')
#         except Exception as e:
#             a_level_result_document = ''
#
#         try:
#             o_level_result_document = request.FILES.get('o_level_result_document')
#         except Exception as e:
#             o_level_result_document = ''
#
#         try:
#             high_school_result_document = request.FILES.get('high_school_result_document')
#         except Exception as e:
#             high_school_result_document = ''
#
#         try:
#             english_test_one_result_document = request.FILES.get('english_test_one_result_document')
#         except Exception as e:
#             english_test_one_result_document = ''
#
#         try:
#             english_test_two_result_document = request.FILES.get('english_test_two_result_document')
#         except Exception as e:
#             english_test_two_result_document = ''
#
#         a_level_result_document_text = request.POST.get('a_level_result_document_text')
#         o_level_result_document_text = request.POST.get('o_level_result_document_text')
#         high_school_result_document_text = request.POST.get('high_school_result_document_text')
#         english_test_one_result_document_text = request.POST.get('english_test_one_result_document_text')
#         english_test_two_result_document_text = request.POST.get('english_test_two_result_document_text')
#
#         try:
#             if StudentDetails.objects.filter(user=request.user):
#                 if not request.user.get_application.is_submitted:
#                     if AcademicQualificationDetails.objects.filter(applicant_id=request.user.get_application).exists():
#                         try:
#                             AcademicQualificationDetails.objects.filter(
#                                 applicant_id=request.user.get_application).update(
#                                 a_level=request.POST['a_level'],
#                                 a_level_year=request.POST['a_level_year'],
#                                 a_level_institution=request.POST['a_level_institution'],
#                                 a_level_result=request.POST['a_level_result'],
#
#                                 o_level=request.POST['o_level'],
#                                 o_level_year=request.POST['o_level_year'],
#                                 o_level_institution=request.POST['o_level_institution'],
#                                 o_level_result=request.POST['o_level_result'],
#
#                                 high_school=request.POST['high_school'],
#                                 high_school_year=request.POST['high_school_year'],
#                                 high_school_institution=request.POST['high_school_institution'],
#                                 high_school_result=request.POST['high_school_result'])
#
#                             qualification_obj = AcademicQualificationDetails.objects.get(
#                                 applicant_id=request.user.get_application)
#
#                             if a_level_result_document:
#                                 a_level_result = str(a_level_result_document)
#                                 object_path = media_path(qualification_obj.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + a_level_result, a_level_result_document)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + a_level_result),a_level_result_document)
#                                 qualification_obj.a_level_result_document = a_level_result
#
#                             if not a_level_result_document_text:
#                                 qualification_obj.a_level_result_document = ''
#
#                             if o_level_result_document:
#                                 o_level_result = str(o_level_result_document)
#                                 object_path = media_path(qualification_obj.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + o_level_result, o_level_result_document)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + o_level_result),o_level_result_document)
#                                 qualification_obj.o_level_result_document = o_level_result
#
#                             if not o_level_result_document_text:
#                                 qualification_obj.o_level_result_document = ''
#
#                             if high_school_result_document:
#                                 high_school_result = str(high_school_result_document)
#                                 object_path = media_path(qualification_obj.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + high_school_result,
#                                                      high_school_result_document)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + high_school_result),high_school_result_document)
#                                 qualification_obj.high_school_result_document = high_school_result
#
#                             if not high_school_result_document_text:
#                                 qualification_obj.high_school_result_document = ''
#
#                             qualification_obj.save()
#
#                             EnglishQualificationDetails.objects.filter(
#                                 applicant_id=request.user.get_application).update(
#                                 english_test_one=request.POST['english_test_one'],
#                                 english_test_one_year=request.POST['english_test_one_year'],
#                                 english_test_one_result=request.POST['english_test_one_result'],
#
#                                 english_test_two=request.POST['english_test_two'],
#                                 english_test_two_year=request.POST['english_test_two_year'],
#                                 english_test_two_result=request.POST['english_test_two_result'])
#
#                             english_object = EnglishQualificationDetails.objects.get(
#                                 applicant_id=request.user.get_application)
#
#                             english_test_one_result = str(english_test_one_result_document)
#                             english_test_two_result = str(english_test_two_result_document)
#
#                             if english_test_one_result_document:
#                                 object_path = media_path(english_object.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + english_test_one_result,
#                                                      english_test_one_result_document)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + english_test_one_result),english_test_one_result_document)
#                                 english_object.english_test_one_result_document = english_test_one_result
#
#                             if not english_test_one_result_document_text:
#                                 english_object.english_test_one_result_document = ''
#
#                             if english_test_two_result_document:
#                                 object_path = media_path(english_object.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + english_test_two_result,
#                                                      english_test_two_result_document)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + english_test_two_result),english_test_two_result_document)
#                                 english_object.english_test_two_result_document = english_test_two_result
#
#                             if not english_test_two_result_document_text:
#                                 english_object.english_test_two_result_document = ''
#
#                             english_object.save()
#
#                             redirect_flag = True
#                         except Exception as e:
#                             messages.warning(request, "Form have some error" + str(e))
#                     else:
#                         try:
#                             qualification_obj = AcademicQualificationDetails.objects.create(
#                                 a_level=request.POST['a_level'],
#                                 a_level_year=request.POST['a_level_year'],
#                                 a_level_result=request.POST['a_level_result'],
#                                 a_level_institution=request.POST['a_level_institution'],
#
#                                 o_level=request.POST['o_level'],
#                                 o_level_year=request.POST['o_level_year'],
#                                 o_level_result=request.POST['o_level_result'],
#                                 o_level_institution=request.POST['o_level_institution'],
#
#                                 high_school=request.POST['high_school'],
#                                 high_school_year=request.POST['high_school_year'],
#                                 high_school_result=request.POST['high_school_result'],
#                                 high_school_institution=request.POST['high_school_institution'],
#                                 applicant_id=request.user.get_application)
#
#                             if a_level_result_document:
#                                 a_level_result = str(a_level_result_document)
#
#                                 object_path = media_path(qualification_obj.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + a_level_result, a_level_result_document)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + a_level_result),a_level_result_document)
#                                 qualification_obj.a_level_result_document = a_level_result
#
#                             if not a_level_result_document_text:
#                                 qualification_obj.a_level_result_document = ''
#
#                             if o_level_result_document:
#                                 o_level_result = str(o_level_result_document)
#                                 object_path = media_path(qualification_obj.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + o_level_result, o_level_result_document)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + o_level_result),o_level_result_document)
#                                 qualification_obj.o_level_result_document = o_level_result
#
#                             if not o_level_result_document_text:
#                                 qualification_obj.o_level_result_document = ''
#
#                             if high_school_result_document:
#                                 high_school_result = str(high_school_result_document)
#                                 object_path = media_path(qualification_obj.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + high_school_result,
#                                                      high_school_result_document)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + high_school_result),high_school_result_document)
#                                 qualification_obj.high_school_result_document = high_school_result
#
#                             if not high_school_result_document_text:
#                                 qualification_obj.high_school_result_document = ''
#
#                             qualification_obj.save()
#
#                             english_object = EnglishQualificationDetails.objects.create(
#                                 english_test_one=request.POST['english_test_one'],
#                                 english_test_one_year=request.POST['english_test_one_year'],
#                                 english_test_one_result=request.POST['english_test_one_result'],
#
#                                 english_test_two=request.POST['english_test_two'],
#                                 english_test_two_year=request.POST['english_test_two_year'],
#                                 english_test_two_result=request.POST['english_test_two_result'],
#                                 applicant_id=request.user.get_application,
#                             )
#
#                             if english_test_one_result_document:
#                                 english_test_one_result = str(english_test_one_result_document)
#                                 object_path = media_path(english_object.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + english_test_one_result,
#                                                      english_test_one_result_document)
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + english_test_one_result),english_test_two_result_document)
#
#                                 english_object.english_test_one_result_document = english_test_one_result
#
#                             if not english_test_one_result_document_text:
#                                 english_object.english_test_one_result_document = ''
#
#                             if english_test_two_result_document:
#                                 english_test_two_result = str(english_test_two_result_document)
#                                 object_path = media_path(english_object.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + english_test_two_result,
#                                                      english_test_two_result_document)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + english_test_two_result),english_test_two_result_document)
#                                 english_object.english_test_two_result_document = english_test_two_result
#
#                             if not english_test_two_result_document_text:
#                                 english_object.english_test_two_result_document = ''
#
#                             english_object.save()
#
#                             redirect_flag = True
#                         except Exception as e:
#                             messages.warning(request, "Form have some error" + str(e))
#                 else:
#                     messages.success(request, "Please fill the record.")
#                     return redirect('/student/applicant_personal_info/')
#
#                 if redirect_flag:
#                     messages.success(request, "Record saved")
#                     return redirect('/student/applicant_curriculum_experience_info/')
#         except Exception as e:
#             messages.warning(request, "Form have some error" + str(e))
#
#         messages.warning(request, "Please fill proper form")
#     return redirect('/student/applicant_academic_english_qualification/')


def applicant_curriculum_experience_info(request):
    year_recs = YearDetails.objects.all()
    curriculum_obj = ''
    experience_obj = ''
    application_obj = ''

    passing_year_recs = PassingYear.objects.all()
    country_recs = CountryDetails.objects.all()
    try:
        application_obj = request.user.get_application
        if request.user.get_application:
            # if not request.user.get_application.is_submitted:
            # application_obj = ApplicationDetails.objects.get(student=student, is_submitted=False)
            if CurriculumDetails.objects.filter(applicant_id=request.user.get_application).exists():
                curriculum_obj = CurriculumDetails.objects.filter(applicant_id=request.user.get_application)

            if PostgraduateDetails.objects.filter(applicant_id=request.user.get_application).exists():
                experience_obj = PostgraduateDetails.objects.filter(applicant_id=request.user.get_application)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/applicant_personal_info/')
    return render(request, 'applicant_curriculum_experience_info.html',
                  {'year_recs': year_recs, 'experience_recs': experience_obj, 'curriculum_recs': curriculum_obj,
                   'passing_year_recs': passing_year_recs, 'application_obj': application_obj,'country_recs':country_recs})


def save_update_applicant_curriculum_experience_info(request):
    redirect_flag = False

    curriculum_count = request.POST.get('curriculum_count')
    experience_count = request.POST.get('experience_count')

    if request.POST:
        try:
            if StudentDetails.objects.filter(user=request.user):
                student = StudentDetails.objects.filter(user=request.user)[0]
                # if not request.user.get_application.is_submitted:
                # application_obj = ApplicationDetails.objects.get(student=student, is_submitted=False)

                # for x in range(int(curriculum_count)):
                #     try:
                #         x = x + 1
                #
                #         curriculum_result_document = request.FILES.get('curriculum_result_document_' + str(x))
                #         curriculum_result_document_text = request.POST.get(
                #             'curriculum_result_document_text_' + str(x))
                #
                #         if request.POST.get('curriculum_obj_' + str(x)):
                #             CurriculumDetails.objects.filter(
                #                 id=request.POST['curriculum_obj_' + str(x)]).update(
                #                 curriculum_name=request.POST['curriculum_name_' + str(x)],
                #                 curriculum_year=request.POST['curriculum_year_' + str(x)])
                #
                #             curriculum_obj = CurriculumDetails.objects.filter(
                #                 id=request.POST['curriculum_obj_' + str(x)])[0]
                #
                #         else:
                #             curriculum_obj = CurriculumDetails.objects.create(
                #                 curriculum_name=request.POST['curriculum_name_' + str(x)],
                #                 curriculum_year=request.POST['curriculum_year_' + str(x)],
                #                 applicant_id=request.user.get_application)
                #
                #         if curriculum_result_document:
                #             result_document = str(curriculum_result_document)
                #
                #             object_path = media_path(curriculum_obj.applicant_id)
                #             handle_uploaded_file(str(object_path) + '/' + result_document,
                #                                  curriculum_result_document)
                #
                #             curriculum_obj.curriculum_result_document = result_document
                #
                #         if not curriculum_result_document_text:
                #             curriculum_obj.curriculum_result_document = ''
                #
                #         curriculum_obj.save()
                #     except Exception as e:
                #         pass

                for count in range(int(experience_count)):
                    try:
                        count = count + 1

                        # work_experience_document = request.FILES.get('work_experience_document_' + str(count))
                        # work_experience_document_text = request.POST.get(
                        #     'work_experience_document_text_' + str(count))

                        if request.POST.get('experience_obj_' + str(count)):

                            PostgraduateDetails.objects.filter(id=request.POST['experience_obj_' + str(count)]).update(
                                qualification_name=request.POST['qualification_name_' + str(count)],
                                license_certificate_no=request.POST['license_' + str(count)],
                                professional_body=request.POST['professional_body_' + str(count)],
                                awarded_date=request.POST['awarded_date_' + str(count)] if request.POST[
                                    'awarded_date_' + str(count)] else None,
                                expiration_date=request.POST['expiration_date_' + str(count)] if request.POST[
                                    'expiration_date_' + str(count)] else None,
                                agency_name_no=request.POST['agency_name_no_' + str(count)],
                                country=request.POST['country_' + str(count)] if request.POST[
                                    'country_' + str(count)] else None,

                            )

                            experience_object = PostgraduateDetails.objects.filter(
                                id=request.POST['experience_obj_' + str(count)])[0]

                        else:
                            experience_object = PostgraduateDetails.objects.create(
                                qualification_name=request.POST['qualification_name_' + str(count)],
                                license_certificate_no=request.POST['license_' + str(count)],
                                professional_body=request.POST['professional_body_' + str(count)],
                                awarded_date=request.POST['awarded_date_' + str(count)] if request.POST[
                                    'awarded_date_' + str(count)] else None,
                                expiration_date=request.POST['expiration_date_' + str(count)] if request.POST[
                                    'expiration_date_' + str(count)] else None,
                                agency_name_no=request.POST['agency_name_no_' + str(count)],
                                country=request.POST['country_' + str(count)] if request.POST[
                                    'country_' + str(count)] else None,
                                applicant_id=request.user.get_application)

                        # if work_experience_document:
                        #     work_experience = str(work_experience_document)
                        #     object_path = media_path(experience_object.applicant_id)
                        #     handle_uploaded_file(str(object_path) + '/' + work_experience,
                        #                          work_experience_document)
                        #
                        #     experience_object.work_experience_document = work_experience
                        #
                        # if not work_experience_document_text:
                        #     experience_object.work_experience_document_one = ''

                        experience_object.save()
                    except Exception as e:
                        pass

                redirect_flag = True

            # else:
            #     messages.success(request, "Please fill the record.")
            #     return redirect('/student/applicant_personal_info/')

            if redirect_flag:
                messages.success(request, "Record saved")
                return redirect('/student/applicant_employement_history_info/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/student/applicant_scholarship_about_yourself_info/')




#------------ Backup for static save of Experiance and Curriculam ---------------------

# def save_update_applicant_curriculum_experience_info(request):
#     redirect_flag = False
#
#     if request.POST:
#         try:
#             try:
#                 curriculum_result_document_one = request.FILES.get('curriculum_result_document_one')
#                 curriculum_result_document_two = request.FILES.get('curriculum_result_document_two')
#                 curriculum_result_document_three = request.FILES.get('curriculum_result_document_three')
#
#                 work_experience_document_one = request.FILES.get('work_experience_document_one')
#                 work_experience_document_two = request.FILES.get('work_experience_document_two')
#
#             except Exception as e:
#                 curriculum_result_document_one = ''
#                 curriculum_result_document_two = ''
#                 curriculum_result_document_three = ''
#
#                 work_experience_document_one = ''
#                 work_experience_document_two = ''
#
#             curriculum_result_document_one_text = request.POST.get('curriculum_result_document_one_text')
#             curriculum_result_document_two_text = request.POST.get('curriculum_result_document_two_text')
#             curriculum_result_document_three_text = request.POST.get('curriculum_result_document_three_text')
#
#             work_experience_document_one_text = request.POST.get('work_experience_document_one_text')
#             work_experience_document_two_text = request.POST.get('work_experience_document_two_text')
#
#             if StudentDetails.objects.filter(user=request.user):
#                 student = StudentDetails.objects.filter(user=request.user)[0]
#                 if not request.user.get_application.is_submitted:
#                     # application_obj = ApplicationDetails.objects.get(student=student, is_submitted=False)
#                     if CurriculumDetails.objects.filter(applicant_id=request.user.get_application).exists():
#                         try:
#                             CurriculumDetails.objects.filter(applicant_id=request.user.get_application).update(
#                                 curriculum_name_one=request.POST['curriculum_name_one'],
#                                 curriculum_year_one=request.POST['curriculum_year_one'],
#
#                                 curriculum_name_two=request.POST['curriculum_name_two'],
#                                 curriculum_year_two=request.POST['curriculum_year_two'],
#
#                                 curriculum_name_three=request.POST['curriculum_name_three'],
#                                 curriculum_year_three=request.POST['curriculum_year_three'])
#
#                             curriculum_obj = CurriculumDetails.objects.get(
#                                 applicant_id=request.user.get_application)
#
#                             if curriculum_result_document_one:
#                                 curriculum_result_one = str(curriculum_result_document_one)
#                                 object_path = media_path(curriculum_obj.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + curriculum_result_one,
#                                                      curriculum_result_document_one)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_one),curriculum_result_document_one)
#                                 curriculum_obj.curriculum_result_document_one = curriculum_result_one
#
#                             if not curriculum_result_document_one_text:
#                                 curriculum_obj.curriculum_result_document_one = ''
#
#                             if curriculum_result_document_two:
#                                 curriculum_result_two = str(curriculum_result_document_two)
#                                 object_path = media_path(curriculum_obj.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + curriculum_result_two,
#                                                      curriculum_result_document_two)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_two),curriculum_result_document_two)
#                                 curriculum_obj.curriculum_result_document_two = curriculum_result_two
#
#                             if not curriculum_result_document_two_text:
#                                 curriculum_obj.curriculum_result_document_two = ''
#
#                             if curriculum_result_document_three:
#                                 curriculum_result_three = str(curriculum_result_document_three)
#                                 object_path = media_path(curriculum_obj.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + curriculum_result_three,
#                                                      curriculum_result_document_three)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_three),curriculum_result_document_three)
#                                 curriculum_obj.curriculum_result_document_three = curriculum_result_three
#
#                             if not curriculum_result_document_three_text:
#                                 curriculum_obj.curriculum_result_document_three = ''
#
#                             curriculum_obj.save()
#
#                             ExperienceDetails.objects.filter(applicant_id=request.user.get_application).update(
#                                 work_experience_one=request.POST['work_experience_one'],
#                                 from_date_one=request.POST['from_date_one'] if request.POST['from_date_one'] else None,
#                                 to_date_one=request.POST['to_date_one'] if request.POST['to_date_one'] else None,
#                                 experience_one_current=True if request.POST.get('experience_one_current') else False,
#
#                                 work_experience_two=request.POST['work_experience_two'],
#                                 from_date_two=request.POST['from_date_two'] if request.POST['from_date_two'] else None,
#                                 to_date_two=request.POST['to_date_two'] if request.POST['to_date_two'] else None,
#                                 experience_two_current=True if request.POST.get('experience_two_current') else False,
#                             )
#
#                             try:
#
#                                 experience_object = ExperienceDetails.objects.get(
#                                     applicant_id=request.user.get_application)
#                             except:
#                                 experience_object = ExperienceDetails.objects.create(
#                                     work_experience_one=request.POST['work_experience_one'],
#                                     from_date_one=request.POST['from_date_one'] if request.POST[
#                                         'from_date_one'] else None,
#                                     to_date_one=request.POST['to_date_one'] if request.POST['to_date_one'] else None,
#                                     experience_one_current=True if request.POST.get(
#                                         'experience_one_current') else False,
#
#                                     work_experience_two=request.POST['work_experience_two'],
#                                     from_date_two=request.POST['from_date_two'] if request.POST[
#                                         'from_date_two'] else None,
#                                     to_date_two=request.POST['to_date_two'] if request.POST['to_date_two'] else None,
#                                     experience_two_current=True if request.POST.get(
#                                         'experience_two_current') else False,
#                                     applicant_id=request.user.get_application)
#
#                             if work_experience_document_one:
#                                 work_experience_one = str(work_experience_document_one)
#                                 object_path = media_path(experience_object.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + work_experience_one,
#                                                      work_experience_document_one)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + work_experience_one),work_experience_document_one)
#                                 experience_object.work_experience_document_one = work_experience_one
#
#                             if not work_experience_document_one_text:
#                                 experience_object.work_experience_document_one = ''
#
#                             if work_experience_document_two:
#                                 work_experience_two = str(work_experience_document_two)
#                                 object_path = media_path(experience_object.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + work_experience_two,
#                                                      work_experience_document_two)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + work_experience_two),work_experience_document_two)
#                                 experience_object.work_experience_document_two = work_experience_two
#
#                             if not work_experience_document_two_text:
#                                 experience_object.work_experience_document_two = ''
#
#                             experience_object.save()
#
#                             redirect_flag = True
#                         except Exception as e:
#                             messages.warning(request, "Form have some error" + str(e))
#                     else:
#                         try:
#                             curriculum_obj = CurriculumDetails.objects.create(
#                                 curriculum_name_one=request.POST['curriculum_name_one'],
#                                 curriculum_year_one=request.POST['curriculum_year_one'],
#
#                                 curriculum_name_two=request.POST['curriculum_name_two'],
#                                 curriculum_year_two=request.POST['curriculum_year_two'],
#
#                                 curriculum_name_three=request.POST['curriculum_name_three'],
#                                 curriculum_year_three=request.POST['curriculum_year_three'],
#                                 applicant_id=request.user.get_application)
#
#                             if curriculum_result_document_one:
#                                 curriculum_result_one = str(curriculum_result_document_one)
#                                 object_path = media_path(curriculum_obj.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + curriculum_result_one,
#                                                      curriculum_result_document_one)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_one),curriculum_result_document_one)
#                                 curriculum_obj.curriculum_result_document_one = curriculum_result_one
#
#                             if not curriculum_result_document_one_text:
#                                 curriculum_obj.curriculum_result_document_one = ''
#
#                             if curriculum_result_document_two:
#                                 curriculum_result_two = str(curriculum_result_document_two)
#                                 object_path = media_path(curriculum_obj.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + curriculum_result_two,
#                                                      curriculum_result_document_two)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_two),curriculum_result_document_two)
#                                 curriculum_obj.curriculum_result_document_two = curriculum_result_two
#
#                             if not curriculum_result_document_two_text:
#                                 curriculum_obj.curriculum_result_document_two = ''
#
#                             if curriculum_result_document_three:
#                                 curriculum_result_three = str(curriculum_result_document_three)
#                                 object_path = media_path(curriculum_obj.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + curriculum_result_three,
#                                                      curriculum_result_document_three)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_three),curriculum_result_document_three)
#                                 curriculum_obj.curriculum_result_document_three = curriculum_result_three
#
#                             if not curriculum_result_document_three_text:
#                                 curriculum_obj.curriculum_result_document_three = ''
#
#                             curriculum_obj.save()
#
#                             experience_object = ExperienceDetails.objects.create(
#                                 work_experience_one=request.POST['work_experience_one'],
#                                 from_date_one=request.POST['from_date_one'] if request.POST['from_date_one'] else None,
#                                 to_date_one=request.POST['to_date_one'] if request.POST['to_date_one'] else None,
#                                 experience_one_current=True if request.POST.get('experience_one_current') else False,
#
#                                 work_experience_two=request.POST['work_experience_two'],
#                                 from_date_two=request.POST['from_date_two'] if request.POST['from_date_two'] else None,
#                                 to_date_two=request.POST['to_date_two'] if request.POST['to_date_two'] else None,
#                                 experience_two_current=True if request.POST.get('experience_two_current') else False,
#                                 applicant_id=request.user.get_application)
#
#                             if work_experience_document_one:
#                                 work_experience_one = str(work_experience_document_one)
#                                 object_path = media_path(experience_object.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + work_experience_one,
#                                                      work_experience_document_one)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + work_experience_one),work_experience_document_one)
#                                 experience_object.work_experience_document_one = work_experience_one
#
#                             if not work_experience_document_one_text:
#                                 experience_object.work_experience_document_one = ''
#
#                             if work_experience_document_two:
#                                 work_experience_two = str(work_experience_document_two)
#                                 object_path = media_path(experience_object.applicant_id)
#                                 handle_uploaded_file(str(object_path) + '/' + work_experience_two,
#                                                      work_experience_document_two)
#
#                                 # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + work_experience_two),work_experience_document_two)
#                                 experience_object.work_experience_document_two = work_experience_two
#
#                             if not work_experience_document_two_text:
#                                 experience_object.work_experience_document_two = ''
#
#                             experience_object.save()
#
#                             redirect_flag = True
#                         except Exception as e:
#                             messages.warning(request, "Form have some error" + str(e))
#                 else:
#                     messages.success(request, "Please fill the record.")
#                     return redirect('/student/applicant_personal_info/')
#
#                 if redirect_flag:
#                     messages.success(request, "Record saved")
#                     return redirect('/student/applicant_scholarship_about_yourself_info/')
#         except Exception as e:
#             messages.warning(request, "Form have some error" + str(e))
#
#         messages.warning(request, "Please fill proper form")
#     return redirect('/student/applicant_scholarship_about_yourself_info/')


def applicant_scholarship_about_yourself_info(request):
    scholarship_recs = ScholarshipDetails.objects.all()
    degree_obj = DegreeDetails.objects.all()
    university_obj = UniversityDetails.objects.all()
    course_recs = ProgramDetails.objects.all()
    terms_condition_recs = UploadTermCondition.objects.all()

    scholarship_obj = ''
    about_obj = ''
    application_obj = ''

    try:
         request.user.get_application
    except Exception as e:
        messages.warning(request, "Please fill the personal details first...")
        return redirect('/student/applicant_personal_info/')

    try:
        if request.user.get_application:
            # if not request.user.get_application.is_submitted:
            application_obj = request.user.get_application

            if ScholarshipSelectionDetails.objects.filter(applicant_id=request.user.get_application).exists():
                scholarship_obj = ScholarshipSelectionDetails.objects.get(applicant_id=request.user.get_application)

            if ApplicantAboutDetails.objects.filter(applicant_id=request.user.get_application).exists():
                about_obj = ApplicantAboutDetails.objects.get(applicant_id=request.user.get_application)
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return render(request, 'applicant_scholarship_about_yourself_info.html',
                  {'scholarship_recs': scholarship_recs, 'scholarship_obj': scholarship_obj, 'about_obj': about_obj,
                   'university_obj': university_obj, 'degree_obj': degree_obj, 'course_recs': course_recs,
                   'application_obj': application_obj,'terms_condition_recs':terms_condition_recs})


def get_degrees(request):
    finalDict = []
    course_applied = request.POST.get('course_applied', None)

    program_rec = ProgramDetails.objects.get(id=course_applied)
    degree_detail_rec = DegreeDetails.objects.filter(degree_type=program_rec.degree_type)

    for rec in degree_detail_rec:
        degree_data = {'name': rec.degree_name.title(), 'id': rec.id,
                       'university': program_rec.university.university_name.title(),
                       'university_id': program_rec.university.id}
        finalDict.append(degree_data)

    return JsonResponse(finalDict, safe=False)


def save_update_applicant_scholarship_about_yourself_info(request):
    try:
        admission_letter_document = request.FILES.get('admission_letter_document')
    except:
        admission_letter_document = ''

    redirect_flag = False
    admission_letter_document_text = request.POST.get('admission_letter_document_text')

    if request.POST:
        try:
            if StudentDetails.objects.filter(user=request.user):
                if not request.user.get_application.is_submitted:
                    # application_obj = ApplicationDetails.objects.get(student=student, is_submitted=False)
                    if ScholarshipSelectionDetails.objects.filter(applicant_id=request.user.get_application).exists():
                        try:
                            ScholarshipSelectionDetails.objects.filter(
                                applicant_id=request.user.get_application).update(
                                scholarship_id=request.POST['scholarship'],
                                course_applied_id=request.POST['course_applied'],
                                degree_id=request.POST['degree_applied'],
                                university_id=request.POST['university'])

                            scholarship_obj = ScholarshipSelectionDetails.objects.get(
                                applicant_id=request.user.get_application)

                            if admission_letter_document:
                                admission_letter = str(admission_letter_document)
                                object_path = media_path(scholarship_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + admission_letter,
                                                     admission_letter_document)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + admission_letter),admission_letter_document)
                                scholarship_obj.admission_letter_document = admission_letter

                            if not admission_letter_document_text:
                                scholarship_obj.admission_letter_document = ''
                            scholarship_obj.save()

                            ApplicantAboutDetails.objects.filter(applicant_id=request.user.get_application).update(
                                about_yourself=request.POST['about_yourself'])

                            redirect_flag = True
                        except Exception as e:
                            messages.warning(request, "Form have some error" + str(e))
                    else:
                        try:
                            scholarship_obj = ScholarshipSelectionDetails.objects.create(
                                scholarship_id=request.POST['scholarship'],
                                course_applied_id=request.POST['course_applied'],
                                degree_id=request.POST['degree_applied'],
                                university_id=request.POST['university'],
                                applicant_id=request.user.get_application)

                            if admission_letter_document:
                                admission_letter = str(admission_letter_document)
                                object_path = media_path(scholarship_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + admission_letter,
                                                     admission_letter_document)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + admission_letter),admission_letter_document)
                                scholarship_obj.admission_letter_document = admission_letter

                            if not admission_letter_document_text:
                                scholarship_obj.admission_letter_document = ''
                            scholarship_obj.save()

                            ApplicantAboutDetails.objects.create(
                                about_yourself=request.POST['about_yourself'],
                                applicant_id=request.user.get_application)

                            redirect_flag = True
                        except Exception as e:
                            messages.warning(request, "Form have some error" + str(e))
                else:
                    messages.success(request, "Please fill the record.")
                    return redirect('/student/applicant_personal_info/')

                if redirect_flag:
                    messages.success(request, "Record saved")
                    return redirect('/student/my_application/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/student/applicant_scholarship_about_yourself_info/')


def my_application(request):
    try:
        application_obj = request.user.get_application
        siblings_obj = application_obj.sibling_applicant_rel.all() if application_obj.sibling_applicant_rel.all() else ''
        qualification_obj = application_obj.academic_applicant_rel.all() if application_obj.academic_applicant_rel.all() else ''
        english_obj = application_obj.english_applicant_rel.all() if application_obj.english_applicant_rel.all() else ''
        arabic_recs = application_obj.arab_applicant_rel.all() if application_obj.arab_applicant_rel.all() else ''
        curriculum_obj = application_obj.curriculum_applicant_rel.all() if application_obj.curriculum_applicant_rel.all() else ''
        applicant_experience_obj = application_obj.applicant_experience_rel.all() if application_obj.applicant_experience_rel.all() else ''
        scholarship_obj = application_obj.applicant_scholarship_rel.get() if application_obj.applicant_scholarship_rel.all() else ''
        about_obj = application_obj.applicant_about_rel.get() if application_obj.applicant_about_rel.all() else ''
        postgraduate_recs = application_obj.applicant_postgraduate_rel.all() if application_obj.applicant_postgraduate_rel.all() else ''
        employement_history_recs = application_obj.employement_history_rel.all() if application_obj.employement_history_rel.all() else ''
        addition_info_obj = application_obj.applicant_addition_info.get() if application_obj.applicant_addition_info.all() else ''
        attachement_obj = application_obj.applicant_attachement_rel.all() if application_obj.applicant_attachement_rel.all() else ''

        return render(request, 'my_application.html',
                      {'siblings_obj': siblings_obj, 'application_obj': application_obj,
                       'qualification_recs': qualification_obj, 'english_recs': english_obj,
                       'curriculum_recs': curriculum_obj,
                       'applicant_experience_recs': applicant_experience_obj,
                       'scholarship_obj': scholarship_obj, 'about_obj': about_obj,'attachement_obj':attachement_obj,'postgraduate_recs':postgraduate_recs,
                       'employement_history_recs':employement_history_recs,'addition_info_obj':addition_info_obj,'attachement_obj':attachement_obj,
                       'arabic_recs':arabic_recs})

    except Exception as e:
        messages.warning(request, "Please Fill The Application Form First ... ")
        return redirect("/")

@submission_required
def submit_application(request):
    try:
        app_id = request.POST.get('app_id')
        application_obj = ApplicationDetails.objects.get(id=app_id)
        if not application_obj.university:
            messages.warning(request,"Please fill the Intake Information section before submitting the application.")
            return redirect('/student/applicant_intake_info/')
        if not AcademicQualificationDetails.objects.filter(applicant_id=request.user.get_application):
            messages.warning(request, "Please fill the Academic Qualification section before submitting the application.")
            return redirect('/student/applicant_academic_english_qualification/')
        if not AdditionInformationDetails.objects.filter(application_id=request.user.get_application):
            messages.warning(request, "Please fill the Additional Information section before submitting the application.")
            return redirect('/student/applicant_additional_information/')
        if not ApplicantAttachementDetails.objects.filter(applicant_id=request.user.get_application):
            messages.warning(request, "Please upload required Attachement section before submitting the application.")
            return redirect('/student/applicant_attachment_submission/')
        else:
            document_recs = DocumentDetails.objects.all()
            attachment_obj = ApplicantAttachementDetails.objects.get(applicant_id=request.user.get_application)
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
                attachement_count = DocumentDetails.objects.filter(doc_required = 'Yes').exclude(document_name='Research').count()

            if not attachement_count == document_count:
                messages.warning(request, "Please upload required Attachement section before submitting the application.")
                return redirect('/student/applicant_attachment_submission/')

        if application_obj.is_submitted == False:
            progress_counter = application_obj.progress_counter
            progress_counter = progress_counter + 10
            application_obj.progress_counter = progress_counter
            application_obj.save()

        ApplicationDetails.objects.filter(application_id=request.user.get_application_id).update(is_submitted=True,is_online_admission = True)
        ApplicationHistoryDetails.objects.create(applicant_id=request.user.get_application,
                                                 status='Application Submitted',
                                                 remark='Your application is submitted and your University will be notified on further updates regarding your applications.')

        # try:
        #     email_rec = EmailTemplates.objects.get(template_for='Student Application Submission',
        #                                            is_active=True)
        #     context = {'first_name': application_obj.first_name}
        #     send_email_with_template(application_obj, context, email_rec.subject, email_rec.email_body,
        #                              request)
        # except:
        #     subject = 'Student Application Submission'
        #     message = 'This mail is to notify that you have submitted application. We will update you application related info soon.'
        #
        #     send_email_to_applicant(request.user.email, application_obj.email, subject, message,
        #                             application_obj.first_name)

        application_notification(request.user.get_application.id,
                                 'You have successfully submitted your application.')
        admin_notification(request.user.get_application.id,
                           str(request.user.get_application.get_full_name()) + ' have submitted application.')

        messages.success(request, "Application submitted successfully.")

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/student/student_home/')


@psycho_test_required
def applicant_psychometric_test(request):
    try:
         request.user.get_application
    except Exception as e:
        messages.warning(request, "Please fill the personal details first...")
        return redirect('/student/applicant_personal_info/')

    try:
        psychometric_test_obj = ''
        if request.user.get_application:
            if request.user.get_application.is_submitted:
                if ApplicantPsychometricTestDetails.objects.filter(applicant_id=request.user.get_application).exists():
                    psychometric_test_obj = ApplicantPsychometricTestDetails.objects.get(
                        applicant_id=request.user.get_application)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/student_home/')
    return render(request, 'applicant_psychometric_test.html', {'psychometric_test_obj': psychometric_test_obj})


@psycho_test_required
def save_psychometric_test(request):
    try:
        test_result_document = request.FILES.get('test_result_document')
    except:
        test_result_document = ''

    try:
        test_result_document_text = request.POST.get('test_result_document_text')
        result = request.POST.get('result')

        if ApplicantPsychometricTestDetails.objects.filter(applicant_id=request.user.get_application).exists():
            ApplicantPsychometricTestDetails.objects.filter(
                applicant_id=request.user.get_application).update(result=result)

            psychometric_test_obj = ApplicantPsychometricTestDetails.objects.get(
                applicant_id=request.user.get_application)
        else:
            psychometric_test_obj = ApplicantPsychometricTestDetails.objects.create(
                applicant_id=request.user.get_application, result=result)

        if not ApplicationHistoryDetails.objects.filter(applicant_id=request.user.get_application,
                                                        status='Psychometric Test Submitted').exists():
            ApplicationHistoryDetails.objects.create(applicant_id=request.user.get_application,
                                                     status='Psychometric Test Submitted',
                                                     remark='You have submitted Psychometric Test. Please wait for the further updates.')

        if test_result_document:
            test_result = str(test_result_document)
            object_path = media_path(psychometric_test_obj.applicant_id)
            handle_uploaded_file(str(object_path) + '/' + test_result, test_result_document)

            # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + test_result),test_result_document)
            psychometric_test_obj.test_result_document = test_result

        if not test_result_document_text:
            psychometric_test_obj.test_result_document = ''

        psychometric_test_obj.save()

        messages.success(request, "Test Result submitted successfully.")

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/student/applicant_psychometric_test/')


@agreements_required
def applicant_agreement_submission(request):

    try:
       request.user.get_application
    except Exception as e:
        messages.warning(request, "Please fill the personal details first...")
        return redirect('/student/applicant_personal_info/')

    try:
        agreement_submission_obj = ''
        if request.user.get_application:
            if request.user.get_application.is_submitted:
                if ApplicantAgreementDetails.objects.filter(applicant_id=request.user.get_application).exists():
                    agreement_submission_obj = ApplicantAgreementDetails.objects.get(
                        applicant_id=request.user.get_application)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/student_home/')
    return render(request, 'applicant_agreement_submission.html',
                  {'agreement_submission_obj': agreement_submission_obj})


@agreements_required
def save_agreement_submission(request):
    try:
        four_parties_agreements = request.FILES.get('four_parties_agreements')
        education_loan_agreements = request.FILES.get('education_loan_agreements')
    except:
        four_parties_agreements = ''
        education_loan_agreements = ''

    try:

        four_parties_agreements_text = request.POST.get('four_parties_agreements_text')
        education_loan_agreements_text = request.POST.get('education_loan_agreements_text')

        if ApplicantAgreementDetails.objects.filter(applicant_id=request.user.get_application).exists():
            agreement_obj = ApplicantAgreementDetails.objects.get(
                applicant_id=request.user.get_application)
        else:
            agreement_obj = ApplicantAgreementDetails.objects.create(
                applicant_id=request.user.get_application)
            application_notification(request.user.get_application.id,
                                     'You have submitted agreements.')
            ApplicationHistoryDetails.objects.create(applicant_id=request.user.get_application,
                                                     status='Agreements submitted.',
                                                     remark='You have submitted agreements. Please wait for the further updates.')

        if four_parties_agreements:
            parties_agreements = str(four_parties_agreements)
            object_path = media_path(agreement_obj.applicant_id)
            handle_uploaded_file(str(object_path) + '/' + parties_agreements, four_parties_agreements)

            # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + parties_agreements),four_parties_agreements)
            agreement_obj.four_parties_agreement_document = parties_agreements

        if not four_parties_agreements_text:
            agreement_obj.four_parties_agreement_document = ''

        agreement_obj.save()

        if education_loan_agreements:
            education_agreements = str(education_loan_agreements)
            object_path = media_path(agreement_obj.applicant_id)
            handle_uploaded_file(str(object_path) + '/' + education_agreements, education_loan_agreements)

            # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + education_agreements),education_loan_agreements)
            agreement_obj.education_loan_agreement_document = education_agreements

        if not education_loan_agreements_text:
            agreement_obj.education_loan_agreement_document = ''

        agreement_obj.save()

        messages.success(request, "Agreement submitted successfully.")

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/student/applicant_agreement_submission/')


@dev_program_required
def applicant_program_certificate_submission(request):

    try:
       request.user.get_application
    except Exception as e:
        messages.warning(request, "Please fill the personal details first...")
        return redirect('/student/applicant_personal_info/')

    try:
        module_recs = ''
        certificate_recs = ''
        if request.user.get_application:
            if request.user.get_application.is_submitted:
                module_recs = StudentModuleMapping.objects.filter(applicant_id=request.user.get_application)
                # module_recs = ScholarshipSelectionDetails.objects.filter(applicant_id=request.user.get_application)
                certificate_recs = ApplicantDevelopmentProgramDetails.objects.filter(
                    applicant_id=request.user.get_application)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/student_home/')
    return render(request, 'applicant_program_certificate_submission.html',
                  {'module_recs': module_recs, 'certificate_recs': certificate_recs})


@dev_program_required
def save_applicant_program_certificate_submission(request):
    try:
        certificate_document = request.FILES['certificate_document']
    except:
        certificate_document = ''

    try:
        module = request.POST.get('module')

        agreement_obj = ApplicantDevelopmentProgramDetails.objects.create(
            applicant_id=request.user.get_application, module_id=module)

        if certificate_document:
            certificate = str(certificate_document)
            object_path = media_path(agreement_obj.applicant_id)
            handle_uploaded_file(str(object_path) + '/' + certificate, certificate_document)

            # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + certificate),certificate_document)
            agreement_obj.certificate_document = certificate
            agreement_obj.save()

        messages.success(request, "Certificate submitted successfully.")

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/student/applicant_program_certificate_submission/')


def delete_applicant_program_certificate_submission(request):
    program_id = request.POST.get('program_id')
    try:
        ApplicantDevelopmentProgramDetails.objects.filter(id=program_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


@semester_required
def applicant_academic_progress(request):
    try:
        semester_recs = ''
        year_recs = ''
        progress_recs = ''
        applicant_semester = ''
        application_degree_type = ''
        degree_name = ''
        try:
            request.user.get_application
        except Exception as e:
            messages.warning(request, "Please fill the personal details first...")
            return redirect('/student/applicant_personal_info/')

        if request.user.get_application:
            if request.user.get_application.is_submitted:
                application_degree_type = request.user.get_application.applicant_scholarship_rel.get().degree.degree_type.degree_name
                if application_degree_type == 'masters (course work)':
                    degree_name = 'course_work'

                elif application_degree_type == 'phd':
                    degree_name = 'phd'

                else:
                    degree_name = 'degree'

                year_recs = YearDetails.objects.all()
                semester_recs = SemesterDetails.objects.all()

                if request.user.get_application.semester:
                    applicant_semester = request.user.get_application.semester.id
                else:
                    applicant_semester = ''


                progress_recs = ApplicantAcademicProgressDetails.objects.filter(
                    applicant_id=request.user.get_application)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/student_home/')
    return render(request, 'applicant_academic_progress.html',
                  {'degree_name': degree_name, 'semester_recs': semester_recs, 'year_recs': year_recs,
                   'progress_recs': progress_recs, 'applicant_semester': applicant_semester})


@semester_required
def save_applicant_academic_progress(request):
    try:
        transcript_document = request.FILES['transcript_document']
    except:
        transcript_document = ''

    year = request.POST.get('year')
    date = request.POST.get('date')
    semester = request.POST.get('semester_name')

    gpa_scored = request.POST.get('gpa_scored')
    gpa_from = request.POST.get('gpa_from')

    cgpa_scored = request.POST.get('cgpa_scored')
    cgpa_from = request.POST.get('cgpa_from')

    result = request.POST.get('result')
    try:
        progress_obj = ApplicantAcademicProgressDetails.objects.create(year_id=year,
                                                                       date=date if date else None,
                                                                       semester_id=semester,
                                                                       gpa_scored=gpa_scored,
                                                                       gpa_from=gpa_from,
                                                                       cgpa_scored=cgpa_scored,
                                                                       cgpa_from=cgpa_from,
                                                                       applicant_id=request.user.get_application,
                                                                       result=result)

        if transcript_document:
            transcript = str(transcript_document)
            object_path = media_path(progress_obj.applicant_id)
            handle_uploaded_file(str(object_path) + '/' + transcript, transcript_document)

            # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + transcript),transcript_document)
            progress_obj.transcript_document = transcript
            progress_obj.save()
        messages.success(request, "Record saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/student/applicant_academic_progress/')


def applicant_progress_history(request):
    username = ''
    application_history_obj = ''
    try:
        username = request.user.get_full_name()
        if ApplicationDetails.objects.filter(application_id=request.user.get_application_id,
                                             is_submitted=True).exists():
            application_history_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id,
                                                                     is_submitted=True).applicant_history_rel.all()
    except Exception as e:
        username = request.user.first_name
        messages.warning(request, "Form have some error" + str(e))

    return render(request, 'applicant_progress_history.html',
                  {'application_history_obj': application_history_obj, 'username': username})


def save_other_university(request):
    university_name = request.POST.get('other_university_name')
    country_id = request.POST.get('other_university_country')
    try:
        if not UniversityDetails.objects.filter(university_name=university_name.lower(),
                                                country_id=country_id).exists():
            UniversityDetails.objects.create(university_name=university_name.lower(), country_id=country_id)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "University added.")
    except:
        messages.warning(request, "University not added.")
    return redirect('/student/applicant_scholarship_about_yourself_info/')

# import os
# from django.conf import settings
# from django.http import HttpResponse
# from django.template import Context
# from django.template.loader import get_template
# import datetime
# from xhtml2pdf import pisa


# def generate_PDF(request):
#     year_recs = YearDetails.objects.all()
#     curriculum_obj = ''
#     experience_obj = ''
#
#     student = StudentDetails.objects.filter(user=request.user)[0]
#     if ApplicationDetails.objects.filter(student=student).exists():
#         application_obj = ApplicationDetails.objects.get(student=student)
#         if CurriculumDetails.objects.filter(applicant_id=application_obj).exists():
#             curriculum_obj = CurriculumDetails.objects.get(applicant_id=application_obj)
#
#         if ExperienceDetails.objects.filter(applicant_id=application_obj).exists():
#             experience_obj = ExperienceDetails.objects.get(applicant_id=application_obj)
#
#     template = get_template('applicant_curriculum_experience_info.html')
#     Context = ({'year_recs': year_recs, 'experience_obj': experience_obj, 'curriculum_obj': curriculum_obj})
#     html = template.render(Context)
#
#     file = open('test.pdf', "w+b")
#     pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
#             encoding='utf-8')
#
#     file.seek(0)
#     pdf = file.read()
#     file.close()
#     return HttpResponse(pdf, 'application/pdf')



#========================Import_Student_Apllication=========================
from accounts.models import UserRole
def import_student_application(request):
    redirect_flag = False

    try:
        file_recs = request.FILES['excel'].get_records()
        for file_rec in file_recs:
            same_as = file_rec['Same as Present Address'].lower()
            if not User.objects.filter(email__iexact=file_rec['Email']).exists():
                try:
                    nationality_obj = CountryDetails.objects.get(country_name__iexact=file_rec['Nationality'])
                except Exception as e:
                    messages.warning(request, "Nationality Not Found" +"for applicant"+str(file_rec['Email']))
                    continue

                try:
                    country_obj = CountryDetails.objects.get(country_name__iexact=file_rec['Country'])
                except Exception as e:
                    messages.warning(request, "Country Not Found" +"for applicant"+str(file_rec['Email']))
                    continue

                try:
                    permanent_country_obj = CountryDetails.objects.get(country_name__iexact=file_rec['Permanent Country'])
                except Exception as e:
                    messages.warning(request, "CountryDetails Not Found" +"for applicant"+str(file_rec['Email']))
                    continue

                try:
                    scholarshipDetails_obj = ScholarshipDetails.objects.get(scholarship_name__iexact=file_rec['Scholarship Applied'])
                except Exception as e:
                    messages.warning(request, "ScholarshipDetails Not Found" +"for applicant"+str(file_rec['Email']))
                    continue

                try:
                    programDetails_obj = ProgramDetails.objects.get(program_name__iexact=file_rec['Course Applied'])
                except Exception as e:
                    messages.warning(request, "Program Details Not Found" +"for applicant"+str(file_rec['Email']))
                    continue
                try:
                    degree_details_obj = DegreeDetails.objects.get(degree_name__iexact=file_rec['Degree'])
                except Exception as e:
                    messages.warning(request, "Degree Details Not Found" +"for applicant"+str(file_rec['Email']))
                    continue
                try:
                    UniversityDetails_obj = UniversityDetails.objects.get(university_name__iexact=file_rec['University'])
                except Exception as e:
                    messages.warning(request, "University Details Not Found" +"for applicant"+str(file_rec['Email']))
                    continue

                try:
                    academicyear_obj = YearDetails.objects.get(year_name=file_rec['Academic Year'])
                except Exception as e:
                    messages.warning(request, "Year Details Not Found"+"for applicant"+str(file_rec['Email']))
                    continue

                user = User.objects.create(first_name=file_rec['First Name'],last_name=file_rec['Last Name'],username=file_rec['Email'],email=file_rec['Email'],password= make_password('redbytes123'),is_active=True,
                registration_switch=True,submission_switch=True,psyc_switch=True,agreements_switch=True,semester_switch=True,program_switch=True)

                user.role.add(UserRole.objects.get(name='Student'))
                student = StudentDetails.objects.create(user=user)

                #current_year = YearDetails.objects.get(active_year=True)

                application_obj = ApplicationDetails.objects.create(first_name=file_rec['First Name'],last_name=file_rec['Last Name'],birth_date=file_rec['DOB'],
                                                                    gender=file_rec['Gender'],
                                                                    nationality_id=nationality_obj.id,
                                                                    passport_number=file_rec['Passport no.'],telephone_hp=file_rec['Telphone no (HP)'],
                                                                    email=file_rec['Email'],
                                                                    student=student,
                                                                    year_id=academicyear_obj.id)

                address_obj = AddressDetails.objects.create(country_id=country_obj.id,street=file_rec['Premise/Sub-Locality'],state=file_rec['State/Province'],district=file_rec['District'],
                                                            post_code=file_rec['Postcode'],sub_locality=file_rec['Sub-Locality'],
                                                            residential_address=file_rec['Residential/Postal Address'])

                if same_as=="yes":
                    address_obj.is_same = True
                    address_obj.save()
                    application_obj.permanent_address = address_obj
                else:
                    permanent_address_obj = AddressDetails.objects.create(country_id=permanent_country_obj.id,street=file_rec['Permanent Premise/Sub-Locality'],
                        state=file_rec['Permanent State/Province'],district=file_rec['Permanent District'],post_code=file_rec['Permanent Postcode'],
                        sub_locality=file_rec['Permanent Sub-Locality'],residential_address=file_rec['Permanent Residential/Postal Address'])

                    application_obj.permanent_address = permanent_address_obj

                application_id = specfic_year_get_application_id(application_obj,file_rec['Academic Year'])

                application_obj.application_id = application_id
                application_obj.address = address_obj
                application_obj.save()

                scholarship_obj = ScholarshipSelectionDetails.objects.create(scholarship_id=scholarshipDetails_obj.id,course_applied_id=programDetails_obj.id,degree_id=degree_details_obj.id,university_id=UniversityDetails_obj.id,applicant_id_id=application_obj.id)

                ApplicantAboutDetails.objects.create(about_yourself=file_rec['About Yourself'],applicant_id_id=application_obj.id)

                agreement_obj = ApplicantAgreementDetails.objects.create(applicant_id_id=application_obj.id)

                psychometric_test_obj = ApplicantPsychometricTestDetails.objects.create(applicant_id_id=application_obj.id, result=file_rec['Psychometric Test Result'])

                if not ApplicationHistoryDetails.objects.filter(applicant_id_id=application_obj.id,status='Application Submitted').exists():

                    ApplicationHistoryDetails.objects.create(applicant_id_id=application_obj.id,status='Agreements submitted.',remark='You have submitted agreements. Please wait for the further updates.')

                redirect_flag = True

            else:
                messages.warning(request,"email already exists"+str(file_rec['Email']))
                continue


        if redirect_flag:
            messages.success(request, "Record saved")


    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/student/import_applicant_records_tile/')


def import_applicant_qualification_info(request):
    try:
        redirect_flag = False

        file_recs = request.FILES['student_qualification_rec'].get_records()

        for file_rec in file_recs:
            try:
                user_obj = User.objects.get(email=file_rec['Email'])
            except Exception as e:
                messages.warning(request, "User Not Found" + str(e))
                continue

            try:
                applicant_application = get_application_specfic_year(user_obj,file_rec['Academic year'])

            except Exception as e:
                messages.warning(request, "Some Error occured..." + str(e))
                continue



            english_object = EnglishQualificationDetails.objects.create(english_test=file_rec['English Competency Test'],
             english_test_year=file_rec['Year'],
             english_test_result=file_rec['Result'],
             applicant_id_id=applicant_application.id)

            redirect_flag = True

        if redirect_flag:
            messages.success(request, "Record saved")

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/student/import_applicant_records_tile/')


def import_applicant_donor_mapping(request):
    try:
        redirect_flag = False
        file_recs = request.FILES['applicant_donor_mapping'].get_records()
        for file_rec in file_recs:
            try:
                user_obj = User.objects.get(email=file_rec['Applicant email'])
            except Exception as e:
                messages.warning(request, "User Not Found" + str(e))
                continue
            try:
                donor_user = User.objects.get(email=file_rec['Donor email'])
                donor = DonorDetails.objects.get(user=donor_user.id)
            except Exception as e:
                messages.warning(request, "Donor not Found" + str(e))
                continue
            try:
                applicant_application = get_application_specfic_year(user_obj,file_rec['Academic year'])

            except Exception as e:
                messages.warning(request, "Some Error occured..." + str(e))
                continue

            application_obj = ApplicationDetails.objects.filter(id=applicant_application.id).update(is_submitted=True, first_interview=True,first_interview_attend=True, first_interview_approval=True, psychometric_test=True,
                second_interview_attend=True,
                second_interview_approval=True, admin_approval=True,scholarship_fee=file_rec['Scholarship Total'] )

            applicant_appliation_id = applicant_application.id

            # application_history start================================

            if not ApplicationHistoryDetails.objects.filter(applicant_id_id=applicant_appliation_id,
                                                            status='Application Submitted').exists():
                ApplicationHistoryDetails.objects.create(applicant_id_id=applicant_appliation_id,
                                                         status='Application Submitted',
                                                         remark='Your application is submitted and your institution will be notified on further updates regarding your applications.')

            if not ApplicationHistoryDetails.objects.filter(applicant_id_id=applicant_appliation_id,
                                                            status='First Interview Call').exists():
                ApplicationHistoryDetails.objects.create(applicant_id_id=applicant_appliation_id,
                                                         status='First Interview Call',
                                                         remark='You are requested to come down for the first interview.')

            if not ApplicationHistoryDetails.objects.filter(applicant_id_id=applicant_appliation_id,
                                                            status='First Interview Attended').exists():
                ApplicationHistoryDetails.objects.create(applicant_id_id=applicant_appliation_id,
                                                         status='First Interview Attended',
                                                         remark='You have attended first interview. Please wait for the further updates.')

            if not ApplicationHistoryDetails.objects.filter(applicant_id_id=applicant_appliation_id,
                                                            status='First Interview Approval').exists():
                ApplicationHistoryDetails.objects.create(applicant_id_id=applicant_appliation_id,
                                                         status='First Interview Approval',
                                                         remark='You have cleared your first interview. Please wait for the further updates.')

            if not ApplicationHistoryDetails.objects.filter(applicant_id_id=applicant_appliation_id,
                                                            status='Psychometric Test').exists():
                ApplicationHistoryDetails.objects.create(applicant_id_id=applicant_appliation_id,
                                                         status='Psychometric Test',
                                                         remark='You have submitted Psychometric test result. Please wait for the further updates.')

            if not ApplicationHistoryDetails.objects.filter(applicant_id_id=applicant_appliation_id,
                                                            status='Second Interview Attended').exists():
                ApplicationHistoryDetails.objects.create(applicant_id_id=applicant_appliation_id,
                                                         status='Second Interview Attended',
                                                         remark='You have attended second interview. Please wait for the further updates.')

            if not ApplicationHistoryDetails.objects.filter(applicant_id_id=applicant_appliation_id,
                                                            status='Second Interview Approval').exists():
                ApplicationHistoryDetails.objects.create(applicant_id_id=applicant_appliation_id,
                                                         status='Second Interview Approval',
                                                         remark='You have cleared your second interview. Please wait for the further updates.')

            if not ApplicationHistoryDetails.objects.filter(applicant_id_id=applicant_appliation_id,
                                                            status='Admin Approval').exists():
                ApplicationHistoryDetails.objects.create(applicant_id_id=applicant_appliation_id,
                                                         status='Admin Approval',
                                                         remark='Your application have been approved by the admin. Please wait for the further updates.')

            #========application_history end==================

            #====mapping applicant with donor#==============
            application_rec = ApplicationDetails.objects.get(id=applicant_application.id)
            application_rec.is_sponsored = True
            application_rec.save()

            if not StudentDonorMapping.objects.filter(donor=donor, applicant_id=application_rec).exists():
                StudentDonorMapping.objects.create(student=application_rec.student, donor=donor, applicant_id=application_rec)
            redirect_flag = True

        if redirect_flag:
            messages.success(request, "Record saved")



    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/student/import_applicant_records_tile/')


def import_applicant_records_tile(request):

    return render(request,'import_applicant_records_tile.html')

def export_templates(request):
    return render(request, 'export_templates.html')

def export_applicant_info_template(request):
    rows = []
    column_names = ["Academic Year", "First Name", "Last Name", "DOB", "Gender", "Nationality","Passport no.","Email","Telphone no (HP)","Country","Residential/Postal Address",
                    "Premise/Sub-Locality","Sub-Locality","District","Postcode","State/Province","Same as Present Address","Permanent Country","Permanent Residential/Postal Address","Permanent Premise/Sub-Locality",
                    "Permanent Sub-Locality","Permanent District","Permanent Postcode","Permanent State/Province","Scholarship Applied","Course Applied","Degree","University",
                    "About Yourself","Psychometric Test Result"]
    return export_users_xls('Applicant_details_template', column_names, rows)

def export_applicant_donor_mapping(request):
    rows = []
    column_names = ["Academic year", "Applicant email", "Donor email", "Scholarship Total"]
    return export_users_xls('Link_student_donor_template', column_names, rows)


def export_applicant_qualification_template(request):
    rows = []
    column_names = ["Academic year", "Email", "English Competency Test", "Year","Result"]
    return export_users_xls('Academic_info_template', column_names, rows)



def get_degrees_from_universities(request):

    finalDict = []
    university_id = request.POST.get('university_id', None)
    program_rec = ProgramDetails.objects.filter(university_id=university_id)
    for rec in program_rec:

        degree_type_id = DegreeTypeDetails.objects.get(id=rec.degree_type.id)

        degree_detail_rec = DegreeDetails.objects.filter(degree_type=degree_type_id.id)

        for degree_name in degree_detail_rec:
            if not any(d['id'] == degree_name.id  for d in finalDict):
                raw_dict = {}
                raw_dict['name']=degree_name.degree_name.title() +" " +"("+str(degree_name.degree_type.degree_name.title())+")"
                raw_dict['id']=degree_name.id
                finalDict.append(raw_dict)


    return JsonResponse(finalDict, safe=False)



def get_courses_from_degrees(request):

    finalDict = []

    university_id = request.POST.get('university_id', None)
    degree_type_id = request.POST.get('degree_applied_id', None)

    degree_details_obj = DegreeDetails.objects.get(id=degree_type_id).degree_type

    program_rec = ProgramDetails.objects.filter(university_id=university_id,degree_type = degree_details_obj.id)

    for rec in program_rec:

        raw_dict = {}
        raw_dict['name']=rec.program_name
        raw_dict['id']=rec.id
        finalDict.append(raw_dict)
    return JsonResponse(finalDict, safe=False)



def applicant_employement_history_info(request):
    country_recs = CountryDetails.objects.all()
    employement_history_obj = ''
    employement_history_count = 0
    try:
        application_obj = request.user.get_application
        if request.user.get_application:
            if EmployementHistoryDetails.objects.filter(applicant_id=request.user.get_application).exists():
                employement_history_obj = EmployementHistoryDetails.objects.filter(applicant_id=request.user.get_application)
                employement_history_count = employement_history_obj.count()
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/applicant_personal_info/')
    return render(request, 'applicant_employement_history_info.html',
                  {'employement_history_obj': employement_history_obj,'application_obj': application_obj,'country_recs':country_recs,'employement_history_count':employement_history_count})


def save_update_applicant_employement_history_info(request):
    if request.POST:
        redirect_flag = False
        experience_count = request.POST.get('experience_count')
        try:
            if StudentDetails.objects.filter(user=request.user):
                EmployementHistoryDetails.objects.filter(applicant_id=request.user.get_application).delete()
                for count in range(int(experience_count)):
                    try:
                        count = count + 1
                        working_criteria = False
                        if request.POST['working_criteria_' + str(count)] == 'Previous':
                            working_criteria = False
                        else:
                            working_criteria = True
                        if request.POST.get('no_experience') == 'on':
                            no_experience = True
                        else:
                            no_experience = False
                        EmployementHistoryDetails.objects.create(
                            no_experience=no_experience,
                            working_criteria=working_criteria,
                            employer_name=request.POST['employer_name_' + str(count)],
                            working_status=request.POST['working_status_' + str(count)],
                            designation=request.POST['designation_' + str(count)],
                            from_date=request.POST['from_date_' + str(count)] if request.POST['from_date_' + str(count)] else None,
                            to_date=request.POST['to_date_' + str(count)] if request.POST['to_date_' + str(count)] else None,
                            applicant_id=request.user.get_application)
                    except Exception as e:
                        pass
                redirect_flag = True
                if redirect_flag:
                    messages.success(request, "Record saved")
                    return redirect('/student/applicant_additional_information/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/student/applicant_employement_history_info/')


def applicant_additional_information(request):
    campus_recs = CampusBranchesDetails.objects.all()
    country_recs = AllCountries.objects.all()
    student_recs = StudentDetails.objects.filter(user__is_active=True)
    agent_recs = AgentDetails.objects.filter()
    path = ''
    application_obj = ''
    sibling_obj = ''

    try:
        application_obj = request.user.get_application
    except Exception as e :
        messages.warning(request, "Please fill the personal details first.")
        return redirect('/student/applicant_personal_info/')

    if AdditionInformationDetails.objects.filter(application_id=request.user.get_application).exists():
        application_obj = AdditionInformationDetails.objects.get(application_id=request.user.get_application)
        # path = base_path(application_obj)
        # if SiblingDetails.objects.filter(applicant_id=application_obj).exists():
        #     sibling_obj = SiblingDetails.objects.filter(applicant_id=application_obj)


    return render(request, 'applicant_additional_info.html', {'country_recs': country_recs, 'application_obj': application_obj, 'path': path, 'sibling_obj_rec': sibling_obj, 'student_recs':student_recs, 'agent_recs':agent_recs,'campus_recs':campus_recs})

def save_update_applicant_additional_info(request):
    redirect_flag = False
    if request.POST:
        try:

            if StudentDetails.objects.filter(user=request.user):
                if AdditionInformationDetails.objects.filter(application_id = request.user.get_application).exists():
                    AdditionInformationDetails.objects.filter(application_id = request.user.get_application).update(
                        ken_name=request.POST['ken_name'],
                        ken_id=request.POST['ken_id'],
                        ken_relationship=request.POST['ken_relationship'],
                        ken_tel_no=request.POST['ken_tel_no'],
                        ken_email=request.POST['ken_email'],
                        about_know=request.POST['about_know'] if request.POST['about_know'] else None,
                        campus_id=request.POST['campus'] if request.POST['campus'] else None,
                        )
                    if request.POST['is_sponsored'] == 'Yes':
                        AdditionInformationDetails.objects.filter(application_id=request.user.get_application).update(
                            sponsore_organisation=request.POST['sponsore_organisation'],
                            sponsore_address=request.POST['sponsore_address'],
                            sponsore_email=request.POST['sponsore_email'],
                            sponsore_contact=request.POST['sponsore_contact'],
                            is_sponsored=True
                        )
                    else:
                        AdditionInformationDetails.objects.filter(application_id=request.user.get_application).update(
                            sponsore_organisation='',
                            sponsore_address='',
                            sponsore_email='',
                            sponsore_contact='',
                            is_sponsored=False
                        )
                else:
                    if request.POST['ken_name'] != '' or request.POST['ken_id'] != '' or request.POST['ken_relationship'] != '' or request.POST['ken_tel_no'] != '' or request.POST['ken_email'] != '' or request.POST['about_know'] != '' or request.POST['campus'] != '' or request.POST['is_sponsored'] != 'No':
                        application_obj = ApplicationDetails.objects.get(id=request.user.get_application.id)
                        progress_counter = application_obj.progress_counter
                        progress_counter = progress_counter + 20
                        application_obj.progress_counter = progress_counter
                        application_obj.save()

                        AdditionInformationDetails.objects.create(application_id=request.user.get_application,ken_name=request.POST['ken_name'],
                            ken_id=request.POST['ken_id'],
                            ken_relationship=request.POST['ken_relationship'],
                            ken_tel_no=request.POST['ken_tel_no'],
                            ken_email=request.POST['ken_email'],
                            about_know=request.POST['about_know'] if request.POST['about_know'] else None,
                            campus_id=request.POST['campus'] if request.POST['campus'] else None)
                        if request.POST['is_sponsored'] == 'Yes':
                            AdditionInformationDetails.objects.filter(application_id=request.user.get_application).update(
                                sponsore_organisation=request.POST['sponsore_organisation'],
                                sponsore_address=request.POST['sponsore_address'],
                                sponsore_email=request.POST['sponsore_email'],
                                sponsore_contact=request.POST['sponsore_contact'],
                                is_sponsored=True
                            )
                        else:
                            AdditionInformationDetails.objects.filter(application_id=request.user.get_application).update(
                                sponsore_organisation='',
                                sponsore_address='',
                                sponsore_email='',
                                sponsore_contact='',
                                is_sponsored=False
                            )
                redirect_flag = True
            if redirect_flag:
                messages.success(request, "Record saved")
                return redirect('/student/applicant_attachment_submission/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/student/applicant_additional_information/')


def applicant_attachment_submission(request):
    application_obj = ''
    try:
        application_obj = request.user.get_application
    except Exception as e :
        messages.warning(request, "Please fill the personal details first.")
        return redirect('/student/applicant_personal_info/')
    try:
        attachment_obj = ''
        if request.user.get_application:
            # if request.user.get_application.is_submitted:
            if ApplicantAttachementDetails.objects.filter(applicant_id=request.user.get_application).exists():
                attachment_obj = ApplicantAttachementDetails.objects.get(
                    applicant_id=request.user.get_application)
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/student_home/')
    document_recs = DocumentDetails.objects.all()
    return render(request, 'applicant_attachment_submission.html',
                  {'attachment_obj': attachment_obj,'document_recs':document_recs,'application_obj':application_obj})


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

        if ApplicantAttachementDetails.objects.filter(applicant_id=request.user.get_application).exists():
            attachment_obj = ApplicantAttachementDetails.objects.get(
                applicant_id=request.user.get_application)
        else:
            if (passport_photo is not None) or (photo is not None) or (level_result_document is not None) or (transcript_document is not None) or (english_test_result_document is not None) or (arab_test_result_document is not None) or (recommendation_letter is not None):
                if not ApplicantAttachementDetails.objects.filter(applicant_id=request.user.get_application).exists():
                    application_obj = ApplicationDetails.objects.get(id=request.user.get_application.id)
                    progress_counter = application_obj.progress_counter
                    progress_counter = progress_counter + 10
                    application_obj.progress_counter = progress_counter
                    application_obj.save()
                attachment_obj = ApplicantAttachementDetails.objects.create(
                    applicant_id=request.user.get_application)
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
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/student/applicant_declaration/')

def applicant_declaration(request):
    application_obj = ''
    try:
        application_obj = request.user.get_application
    except Exception as e :
        messages.warning(request, "Please fill the personal details first.")
        return redirect('/student/applicant_personal_info/')
    try:
        if request.user.get_application:
            application_obj = request.user.get_application
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return render(request, 'applicant_declaration.html', {'application_obj':application_obj})


def application_offer_letter_pdf(request, app_id):
    try:
        application_obj = ApplicationDetails.objects.get(id=app_id)
        if application_obj.first_interview_attend:
            header_path = ''
            if application_obj.university.university_logo:
                # header_path = settings.MEDIA_ROOT + 'university_logo.png'
                header_path = application_obj.university.university_logo.path
            created_on = application_obj.created_on.strftime("%d %B %Y")
            registration_number = int(application_obj.created_on.timestamp())
            current_date = datetime.datetime.now().strftime("%d %B %Y")
            student_id = hex(binascii.crc32(str(app_id).encode()))[2:]
            template = get_template('application_offer_letter_pdf.html')
            Context = ({ 'application_obj': application_obj, 'header_path':header_path,'current_date':current_date,'student_id':student_id,'created_on':created_on,'registration_number':registration_number})
            html = template.render(Context)
            file = open('test.pdf', "w+b")
            pisa.CreatePDF(html.encode('utf-8'), dest=file,encoding='utf-8')
            file.seek(0)
            pdf = file.read()
            file.close()
            return HttpResponse(pdf, 'application/pdf')
        else:
            header_path = ''
            if application_obj.university.university_logo:
                # header_path = settings.MEDIA_ROOT + 'university_logo.png'
                header_path = application_obj.university.university_logo.path
            created_on = application_obj.created_on.strftime("%d %B %Y")
            registration_number = int(application_obj.created_on.timestamp())
            current_date = datetime.datetime.now().strftime("%d %B %Y")
            student_id = hex(binascii.crc32(str(app_id).encode()))[2:]
            template = get_template('application_conditional_letter_pdf.html')
            Context = ({'application_obj': application_obj, 'header_path': header_path, 'current_date': current_date,
                        'student_id': student_id, 'created_on': created_on, 'registration_number': registration_number})
            html = template.render(Context)
            file = open('test.pdf', "w+b")
            pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
            file.seek(0)
            pdf = file.read()
            file.close()
            return HttpResponse(pdf, 'application/pdf')
    except:
        return redirect('/student/application_offer_letter/')


def application_offer_letter(request):
    try:
        application_obj = request.user.get_application
        return render(request, 'applicant_offer_letter.html', {'application_obj': application_obj})
    except Exception as e:
        messages.warning(request, "Please Fill The Application Form First ... ")
        return redirect("/")



@student_login_required
def applicant_intake_info(request):
    religion_recs = ReligionDetails.objects.all()
    student_recs = StudentDetails.objects.filter(user__is_active = True)
    year_recs = ''
    semester_recs = ''

    program_recs = ProgramDetails.objects.filter(is_delete=False).order_by('-id')
    faculty_recs = FacultyDetails.objects.filter(status=True).order_by('-id')
    study_type_list = ['International', 'University Main']
    study_mode_list = ['Online', 'On Campus']
    study_mode_list_2 = ['Online', 'On Campus']
    study_mode_list_3 = ['Online', 'On Campus']
    study_level_list = ['Undergraduate', 'Postgraduate']
    study_type_recs = StudyTypeDetails.objects.all()
    study_level_recs = StudyLevelDetails.objects.filter().order_by('-id')
    study_level_recs_2 = StudyLevelDetails.objects.filter().order_by('-id')
    study_level_recs_3 = StudyLevelDetails.objects.filter().order_by('-id')
    try:
        application_obj = request.user.get_application
    except Exception as e :
        messages.warning(request, "Please fill the personal details first.")
        return redirect('/student/applicant_personal_info/')

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

    if ApplicationDetails.objects.filter(application_id=request.user.get_application_id).exists():
        application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id)
        if application_obj.faculty:
             department_recs = application_obj.faculty.department.all()

        if application_obj.faculty_2:
             department_2_recs = application_obj.faculty_2.department.all()

        if application_obj.faculty_3:
             department_3_recs = application_obj.faculty_3.department.all()

    if application_obj:
        if application_obj.university:
            country_learning_recs = LearningCentersDetails.objects.filter(university_id=application_obj.university.id)
            for rec in country_learning_recs:
                raw_dict = {}
                if rec.country.id not in duplicate_country_ids:
                    raw_dict['id'] = rec.country.id
                    raw_dict['country_name'] = rec.country.country_name
                    duplicate_country_ids.append(rec.country.id)
                    country_recs.append(raw_dict)


        program_recs = ProgramDetails.objects.filter(is_delete=False)
        if application_obj.study_level:
            program_recs = program_recs.filter(study_level_id=application_obj.study_level.id)
        if application_obj.study_mode:
            for rec in program_recs:
                for mode in rec.study_mode.filter(study_mode=application_obj.study_mode):
                    faculty_list.append(rec)

        program_recs_2 = ProgramDetails.objects.filter(is_delete=False)
        if application_obj.study_level_2:
            program_recs_2 = program_recs_2.filter(study_level_id=application_obj.study_level_2.id)
        if application_obj.study_mode_2:
            for rec in program_recs_2:
                for mode in rec.study_mode.filter(study_mode=application_obj.study_mode_2):
                    faculty_2_list.append(rec)

        program_recs_3 = ProgramDetails.objects.filter(is_delete=False)
        if application_obj.study_level_3:
            program_recs_3 = program_recs_3.filter(study_level_id=application_obj.study_level_3.id)
        if application_obj.study_mode_3:
            for rec in program_recs_3:
                for mode in rec.study_mode.filter(study_mode=application_obj.study_mode_3):
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

        if application_obj.study_level:
            program_recs = program_recs.filter(study_level_id=application_obj.study_level.id)

        if application_obj.faculty:
            program_recs = program_recs.filter(faculty_id=application_obj.faculty.id)

        if application_obj.department:
            program_recs = program_recs.filter(department_id=application_obj.department.id)

        if application_obj.study_mode:
            for rec in program_recs:
                for mode in rec.study_mode.filter(study_mode=application_obj.study_mode):
                    program_list.append(rec)

        if program_list:
            for rec in program_recs:
                raw_dict = {}
                raw_dict['id'] = rec.id
                raw_dict['program'] = rec.program_name
                program_final_list.append(raw_dict)

        program_2_recs = ProgramDetails.objects.filter(is_delete=False)
        if application_obj.university:
            program_2_recs = program_2_recs.filter(university_id=application_obj.university.id)

        if application_obj.study_level_2:
            program_2_recs = program_2_recs.filter(study_level_id=application_obj.study_level_2.id)

        if application_obj.faculty_2:
            program_2_recs = program_2_recs.filter(faculty_id=application_obj.faculty_2.id)

        if application_obj.department_2:
            program_2_recs = program_2_recs.filter(department_id=application_obj.department_2.id)

        if application_obj.study_mode_2:
            for rec in program_2_recs:
                for mode in rec.study_mode.filter(study_mode=application_obj.study_mode_2):
                    program_2_list.append(rec)

        if program_2_list:
            for rec in program_2_recs:
                raw_dict = {}
                raw_dict['id'] = rec.id
                raw_dict['program'] = rec.program_name
                program_2_final_list.append(raw_dict)

        program_3_recs = ProgramDetails.objects.filter(is_delete=False)
        if application_obj.university:
            program_3_recs = program_3_recs.filter(university_id=application_obj.university.id)

        if application_obj.study_level_2:
            program_3_recs = program_3_recs.filter(study_level_id=application_obj.study_level_3.id)

        if application_obj.faculty_3:
            program_3_recs = program_3_recs.filter(faculty_id=application_obj.faculty_3.id)

        if application_obj.department_3:
            program_3_recs = program_3_recs.filter(department_id=application_obj.department_3.id)

        if application_obj.study_mode_3:
            for rec in program_3_recs:
                for mode in rec.study_mode.filter(study_mode=application_obj.study_mode_3):
                    program_3_list.append(rec)

        if program_3_list:
            for rec in program_3_recs:
                raw_dict = {}
                raw_dict['id'] = rec.id
                raw_dict['program'] = rec.program_name
                program_3_final_list.append(raw_dict)



        if application_obj.university:
            year_recs = SemesterDetails.objects.filter(university_id = application_obj.university.id)
            if application_obj.university.is_partner_university == True:
                university_recs = UniversityDetails.objects.filter(is_delete=False,
                                                                   is_partner_university=True).order_by('-id')
            else:
                university_recs = UniversityDetails.objects.filter(is_delete=False,
                                                                   is_partner_university=False).order_by('-id')
        else:
            university_recs = UniversityDetails.objects.filter(is_delete=False,
                                                               is_partner_university=False).order_by('-id')
        if application_obj.university and application_obj.academic_year:
            semester_recs = SemesterDetails.objects.filter(university_id = application_obj.university.id,year_id = application_obj.academic_year.id)

        if application_obj.learning_country:
            learning_centre_recs = LearningCentersDetails.objects.filter(country_id=application_obj.learning_country.id,university_id=application_obj.university.id)
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


    return render(request, 'intake_details.html',{'country_recs': country_recs, 'religion_recs': religion_recs, 'application_obj': application_obj,'student_recs':student_recs,'agent_recs':agent_recs,'year_recs':year_recs,'semester_recs':semester_recs,
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
                                                  })


def get_learning_centre_from_country(request):
    finalDict = []
    country_id = request.POST.get('country_id', None)
    university = request.POST.get('university', None)
    learning_centre_recs = LearningCentersDetails.objects.filter(country_id=country_id,university_id = university)
    for rec in learning_centre_recs:
        raw_dict = {}
        raw_dict['learning_centre_name']=rec.lc_name
        raw_dict['id']=rec.id
        finalDict.append(raw_dict)
    return JsonResponse(finalDict, safe=False)



def get_university_from_type(request):
    finalDict = []
    university_type = request.POST.get('university_type', None)
    if university_type == 'Main':
        university_recs = UniversityDetails.objects.filter(is_delete=False, is_partner_university=False).order_by('-id')
    else:
        university_recs = UniversityDetails.objects.filter(is_delete=False, is_partner_university=True).order_by('-id')
    for rec in university_recs:
        raw_dict = {}
        raw_dict['university_name']=rec.university_name
        raw_dict['id']=rec.id
        finalDict.append(raw_dict)
    return JsonResponse(finalDict, safe=False)


def save_update_applicant_intake_info(request):
    if request.POST:
        try:
            application_id = request.POST['application_id']
            application_obj = ApplicationDetails.objects.get(id = application_id)
            if not application_obj.university:
                progress_counter = application_obj.progress_counter
                progress_counter = progress_counter + 20
                application_obj.progress_counter = progress_counter
                application_obj.save()

            if request.POST.get('learning_centre'):
                application_obj.learning_centre_id = request.POST.get('learning_centre')
            application_obj.academic_year_id = request.POST.get('year')
            application_obj.program_id = request.POST.get('program')
            application_obj.campus_id = request.POST.get('campus')
            application_obj.faculty_id = request.POST.get('faculty')
            application_obj.university_id = request.POST.get('university')
            application_obj.semester_id = request.POST.get('semester')
            application_obj.study_mode = request.POST.get('study_mode')
            application_obj.study_level_id = request.POST.get('study_level')
            application_obj.department_id = request.POST.get('department',None)
            application_obj.program_mode_id = request.POST.get('program_mode')

            application_obj.study_mode_2 = request.POST.get('study_mode_2',None)
            application_obj.study_level_2_id = request.POST.get('study_level_2',None)
            application_obj.faculty_2_id = request.POST.get('faculty_2',None)
            application_obj.department_2_id = request.POST.get('department_2', None)
            application_obj.program_2_id = request.POST.get('program_2',None)
            application_obj.program_mode_2_id = request.POST.get('program_mode_2',None)

            application_obj.study_mode_3 = request.POST.get('study_mode_3', None)
            application_obj.study_level_3_id = request.POST.get('study_level_3', None)
            application_obj.faculty_3_id = request.POST.get('faculty_3', None)
            application_obj.department_3_id = request.POST.get('department_3', None)
            application_obj.program_3_id = request.POST.get('program_3', None)
            application_obj.program_mode_3_id = request.POST.get('program_mode_3', None)




            if request.POST.get('country'):
                application_obj.learning_country_id = request.POST.get('country')
            application_obj.intake_flag = True
            application_obj.save()
            redirect_flag = True
            if redirect_flag:
                messages.success(request, "Record saved")
                return redirect('/student/applicant_academic_english_qualification/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))
    return redirect('/student/applicant_intake_info/')


def get_branch_campus_from_program(request):
    finalDict = []
    program_id = request.POST.get('program_id', None)
    program_obj = ProgramDetails.objects.get(id=program_id)
    for rec in program_obj.campus.all():
        raw_dict = {}
        raw_dict['campus_name']=rec.campus.campus_name
        raw_dict['id']=rec.campus.id
        finalDict.append(raw_dict)
    faculty_list = []
    faculty_dict = {}
    faculty_dict['id'] = program_obj.faculty.id
    faculty_dict['faculty_name'] = program_obj.faculty.faculty_name
    faculty_list.append(faculty_dict)
    main_list = finalDict + faculty_list
    return JsonResponse(main_list,safe=False)


def applicant_credit_transfer(request):
    try:
        credit_transfer_recs = ''
        credit_transfer_count = 0
        application_obj = request.user.get_application
        if request.user.get_application:
            if CreditTransferDetails.objects.filter(applicant_id=request.user.get_application).exists():
                credit_transfer_recs = CreditTransferDetails.objects.filter(applicant_id=request.user.get_application)
                credit_transfer_count = CreditTransferDetails.objects.filter(applicant_id=request.user.get_application).count()
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/applicant_personal_info/')
    return render(request, 'applicant_credit_transfer.html',
                  {'credit_transfer_recs': credit_transfer_recs,
                   'application_obj': application_obj,'credit_transfer_count':credit_transfer_count})

def save_credit_transfer(request):
    redirect_flag = False
    experience_count = request.POST.get('experience_count')
    if request.POST:
        try:
            if StudentDetails.objects.filter(user=request.user):
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
                            )
                        else:
                            CreditTransferDetails.objects.create(
                                course_code=request.POST['course_code_' + str(count)],
                                course_title=request.POST['course_title_' + str(count)],
                                credit_hours=request.POST['credit_hours_' + str(count)],
                                grade=request.POST['grade_' + str(count)],
                                institution=request.POST['institution_' + str(count)],
                                applicant_id=request.user.get_application
                            )
                    except Exception as e:
                        pass
                redirect_flag = True
            if redirect_flag:
                messages.success(request, "Record saved")
                return redirect('/student/applicant_employement_history_info/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))
        messages.warning(request, "Please fill proper form")
    return redirect('/student/applicant_credit_transfer/')