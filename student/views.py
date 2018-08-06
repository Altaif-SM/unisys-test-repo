from django.shortcuts import render, redirect
from masters.views import *
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from common.utils import get_application_id
from accounts.decoratars import student_login_required, psycho_test_required, semester_required, registration_required, \
    dev_program_required, agreements_required, submission_required
import os
import shutil


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
                   'application_id': application_id,'application':application})


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


def applicant_personal_info(request):
    country_recs = CountryDetails.objects.all()
    religion_recs = ReligionDetails.objects.all()

    application_obj = ''

    if ApplicationDetails.objects.filter(application_id=request.user.get_application_id, is_submitted=False).exists():
        application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id,
                                                         is_submitted=False)

    return render(request, 'applicant_personal_info.html',
                  {'country_recs': country_recs, 'religion_recs': religion_recs, 'application_obj': application_obj})


def save_update_applicant_personal_info(request):
    passport_photo = request.FILES.get('passport_photo')
    pic = request.FILES.get('photo')
    same_as = request.POST.get('same_as')
    redirect_flag = False

    if request.POST:
        if StudentDetails.objects.filter(user=request.user):
            student = StudentDetails.objects.get(user=request.user)

            if ApplicationDetails.objects.filter(application_id=request.user.get_application_id,
                                                 is_submitted=False).exists():

                ApplicationDetails.objects.filter(application_id=request.user.get_application_id,
                                                  is_submitted=False).update(
                    first_name=request.POST['first_name'],
                    middle_name=request.POST['middle_name'],
                    last_name=request.POST['last_name'],
                    birth_date=request.POST['birth_date'] if request.POST['birth_date'] else None,
                    gender=request.POST['gender'],
                    nationality_id=request.POST[
                        'nationality'],
                    religion_id=request.POST['religion'],
                    id_number=request.POST['id_number'],
                    passport_number=request.POST[
                        'passport_number'],
                    passport_issue_country_id=request.POST[
                        'issue_country'],
                    telephone_hp=request.POST[
                        'telephone_hp'],
                    telephone_home=request.POST[
                        'telephone_home'],
                    email=request.POST['email'])

                application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id,
                                                                 is_submitted=False)

                AddressDetails.objects.filter(id=application_obj.address.id).update(
                    country_id=request.POST['country'],
                    street=request.POST['street'],
                    state=request.POST['state'],
                    district=request.POST['district'],
                    post_code=request.POST['post_code'],
                    sub_locality=request.POST['sub_locality'],
                    residential_address=request.POST['residential_address'])

                address_obj = AddressDetails.objects.get(id=application_obj.address.id)

                if same_as:
                    try:
                        if not address_obj.is_same:
                            address_id = application_obj.permanent_address.id
                            application_obj.permanent_address = None
                            application_obj.save()
                            AddressDetails.objects.filter(id=address_id).delete()

                    except Exception as e:
                        pass

                    address_obj.is_same = True
                    application_obj.permanent_address = address_obj
                    address_obj.save()
                else:
                    if application_obj.permanent_address.is_same:
                        address_obj.is_same = False
                        address_obj.save()

                        permanent_address_obj = AddressDetails.objects.create(
                            country_id=request.POST['permanent_country'],
                            street=request.POST['permanent_street'],
                            state=request.POST['permanent_state'],
                            district=request.POST['permanent_district'],
                            post_code=request.POST['permanent_post_code'],
                            sub_locality=request.POST['permanent_sub_locality'],
                            residential_address=request.POST['permanent_residential_address'])

                        application_obj.permanent_address = permanent_address_obj

                    else:
                        AddressDetails.objects.filter(id=application_obj.permanent_address.id).update(
                            country_id=request.POST['permanent_country'],
                            street=request.POST['permanent_street'],
                            state=request.POST['permanent_state'],
                            district=request.POST['permanent_district'],
                            post_code=request.POST['permanent_post_code'],
                            sub_locality=request.POST['permanent_sub_locality'],
                            residential_address=request.POST['permanent_residential_address'])
                application_obj.save()

                redirect_flag = True
            else:
                try:
                    current_year = YearDetails.objects.get(active_year=True)
                    application_obj = ApplicationDetails.objects.create(first_name=request.POST['first_name'],
                                                                        middle_name=request.POST['middle_name'],
                                                                        last_name=request.POST['last_name'],
                                                                        birth_date=request.POST['birth_date'] if
                                                                        request.POST['birth_date'] else None,
                                                                        gender=request.POST['gender'],
                                                                        nationality_id=request.POST['nationality'],
                                                                        religion_id=request.POST['religion'],
                                                                        id_number=request.POST['id_number'],
                                                                        passport_number=request.POST['passport_number'],
                                                                        passport_issue_country_id=request.POST[
                                                                            'issue_country'],
                                                                        telephone_hp=request.POST['telephone_hp'],
                                                                        telephone_home=request.POST['telephone_home'],
                                                                        email=request.POST['email'],
                                                                        student=student,
                                                                        year=current_year)

                    address_obj = AddressDetails.objects.create(country_id=request.POST['country'],
                                                                street=request.POST['street'],
                                                                state=request.POST['state'],
                                                                district=request.POST['district'],
                                                                post_code=request.POST['post_code'],
                                                                sub_locality=request.POST['sub_locality'],
                                                                residential_address=request.POST['residential_address'])

                    if same_as:
                        address_obj.is_same = True
                        address_obj.save()
                        application_obj.permanent_address = address_obj
                    else:
                        permanent_address_obj = AddressDetails.objects.create(
                            country_id=request.POST['permanent_country'],
                            street=request.POST['permanent_street'],
                            state=request.POST['permanent_state'],
                            district=request.POST['permanent_district'],
                            post_code=request.POST['permanent_post_code'],
                            sub_locality=request.POST['permanent_sub_locality'],
                            residential_address=request.POST['permanent_residential_address'])

                        application_obj.permanent_address = permanent_address_obj

                    application_id = get_application_id(application_obj)

                    application_obj.application_id = application_id
                    application_obj.address = address_obj
                    application_obj.save()

                    redirect_flag = True
                except Exception as e:
                    messages.warning(request, "Form have some error" + str(e))

            try:
                if passport_photo:
                    object_path = media_path(application_obj)

                    passport_photo_name = str(passport_photo)
                    handle_uploaded_file(str(object_path) + '/' + passport_photo_name, passport_photo)
                    application_obj.passport_image = passport_photo_name

                # if not passport_photo:
                #     application_obj.passport_image = ''

                if pic:
                    object_path = media_path(application_obj)

                    photo = str(pic)
                    handle_uploaded_file(str(object_path) + '/' + photo, pic)
                    application_obj.image = photo

                # if not pic:
                #     application_obj.image = ''

                application_obj.save()

                # if pic:
                #     dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
                #     filename = "%s_%s.%s" % (str(application_obj.id), dirname, 'png')
                #     raw_file_path_and_name = os.path.join('images/' + filename)
                #     data = str(pic)
                #     temp_data = data.split('base64,')[1]
                #     raw_data = base64.b64decode(temp_data)
                #     f = open(settings.MEDIA_ROOT + raw_file_path_and_name, 'wb')
                #     f.write(raw_data)
                #     f.close()
                #     application_obj.image = raw_file_path_and_name
                #     application_obj.save()
            except Exception as e:
                messages.warning(request, "Form have some error" + str(e))

    if redirect_flag:
        messages.success(request, "Record saved")
        return redirect('/student/applicant_family_info/')
    else:
        messages.warning(request, "Please fill proper form")
        return redirect('/student/applicant_personal_info/')


def applicant_family_info(request):
    country_recs = CountryDetails.objects.all()
    path = ''

    application_obj = ''

    if ApplicationDetails.objects.filter(application_id=request.user.get_application_id,
                                         is_submitted=False).exists():
        application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id,
                                                         is_submitted=False)
        path = base_path(application_obj)

    return render(request, 'applicant_family_info.html',
                  {'country_recs': country_recs, 'application_obj': application_obj, 'path': path})


def save_update_applicant_family_info(request):
    redirect_flag = False

    if request.POST:
        try:
            try:
                wife_pay_slip = request.FILES.get('wife_pay_slip')

            except Exception as e:
                wife_pay_slip = ''

            try:
                father_pay_slip = request.FILES.get('father_pay_slip')

            except:
                father_pay_slip = ''

            father_pay_slip_text = request.POST.get('father_pay_slip_text')
            wife_pay_slip_text = request.POST.get('wife_pay_slip_text')

            if StudentDetails.objects.filter(user=request.user):
                if not request.user.get_application.is_submitted:

                    ApplicationDetails.objects.filter(application_id=request.user.get_application_id).update(
                        wife_name=request.POST['wife_name'],
                        wife_income=request.POST[
                            'wife_income'],
                        wife_nationality_id=request.POST[
                            'wife_nationality'],
                        wife_occupation=request.POST[
                            'wife_occupation'],
                        wife_telephone_home=request.POST[
                            'wife_telephone_home'],
                        wife_dob=request.POST['wife_dob'] if request.POST['wife_dob'] else None,
                        wife_email=request.POST[
                            'wife_email'],

                        father_name=request.POST[
                            'father_name'],
                        father_income=request.POST[
                            'father_income'],
                        father_nationality_id=request.POST[
                            'father_nationality'],
                        father_occupation=request.POST[
                            'father_occupation'],
                        father_telephone_home=request.POST[
                            'father_telephone_home'],
                        father_dob=request.POST[
                            'father_dob'] if request.POST['father_dob'] else None,
                        father_email=request.POST[
                            'father_email'])

                    application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id)

                    if wife_pay_slip:
                        object_path = media_path(application_obj)

                        wife_slip = str(wife_pay_slip)
                        handle_uploaded_file(str(object_path) + '/' + wife_slip, wife_pay_slip)
                        application_obj.wife_pay_slip = wife_slip

                    if not wife_pay_slip_text:
                        application_obj.wife_pay_slip = ''

                    if father_pay_slip:
                        object_path = media_path(application_obj)
                        father_slip = str(father_pay_slip)
                        # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + father_slip),father_pay_slip)
                        handle_uploaded_file(str(object_path) + '/' + father_slip, father_pay_slip)
                        application_obj.father_pay_slip = father_slip

                    if not father_pay_slip_text:
                        application_obj.father_pay_slip = ''

                    application_obj.save()

                    redirect_flag = True

            if redirect_flag:
                messages.success(request, "Record saved")
                return redirect('/student/applicant_family_mother_sibling_info/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/student/applicant_family_info/')


def applicant_family_mother_sibling_info(request):
    country_recs = CountryDetails.objects.all()
    application_obj = ''
    sibling_obj = ''

    if ApplicationDetails.objects.filter(application_id=request.user.get_application_id,
                                         is_submitted=False).exists():
        application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id,
                                                         is_submitted=False)
        if SiblingDetails.objects.filter(applicant_id=application_obj).exists():
            sibling_obj = SiblingDetails.objects.filter(applicant_id=application_obj)

    return render(request, 'applicant_family_mother_sibling_info.html',
                  {'country_recs': country_recs, 'application_obj': application_obj, 'sibling_obj_rec': sibling_obj})


def save_update_applicant_family_mother_sibling_info(request):
    redirect_flag = False

    if request.POST:
        sibling_count = request.POST.get('sibling_count')
        mother_pay_slip_text = request.POST.get('mother_pay_slip_text')
        try:
            try:
                mother_pay_slip = request.FILES['mother_pay_slip']
            except Exception as e:
                mother_pay_slip = ''
            if StudentDetails.objects.filter(user=request.user):
                if ApplicationDetails.objects.filter(application_id=request.user.get_application_id,
                                                     is_submitted=False).exists():

                    ApplicationDetails.objects.filter(application_id=request.user.get_application_id,
                                                      is_submitted=False).update(
                        mother_name=request.POST['mother_name'],
                        mother_income=request.POST[
                            'mother_income'],
                        mother_nationality_id=request.POST[
                            'mother_nationality'],
                        mother_occupation=request.POST[
                            'mother_occupation'],
                        mother_telephone_home=request.POST[
                            'mother_telephone_home'],
                        mother_dob=request.POST['mother_dob'] if request.POST['mother_dob'] else None,
                        mother_email=request.POST['mother_email'])

                    application_obj = request.user.get_application

                    mother_slip = str(mother_pay_slip)

                    if mother_pay_slip:
                        object_path = media_path(application_obj)

                        handle_uploaded_file(str(object_path) + '/' + mother_slip, mother_pay_slip)
                        # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + mother_slip),mother_pay_slip)
                        application_obj.mother_pay_slip = mother_slip

                    if not mother_pay_slip_text:
                        application_obj.mother_pay_slip = ''
                    application_obj.save()

                    for x in range(int(sibling_count)):
                        try:
                            x = x + 1
                            if request.POST['sibling_id_' + str(x)]:
                                SiblingDetails.objects.filter(id=request.POST['sibling_id_' + str(x)]).update(
                                    sibling_name=request.POST['sibling_' + str(x)],
                                    sibling_age=request.POST['age_' + str(x)],
                                    sibling_status=request.POST['status_' + str(x)])
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
                return redirect('/student/applicant_academic_english_qualification/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/student/applicant_family_mother_sibling_info/')


def applicant_academic_english_qualification(request):
    year_recs = YearDetails.objects.all()
    qualification_obj = ''
    english_obj = ''
    passing_year_recs = PassingYear.objects.all()

    try:
        if request.user.get_application:
            if not request.user.get_application.is_submitted:
                # application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id,
                #                                           is_submitted=False)
                if AcademicQualificationDetails.objects.filter(applicant_id=request.user.get_application).exists():
                    qualification_obj = AcademicQualificationDetails.objects.get(
                        applicant_id=request.user.get_application)

                if EnglishQualificationDetails.objects.filter(applicant_id=request.user.get_application).exists():
                    english_obj = EnglishQualificationDetails.objects.get(applicant_id=request.user.get_application)
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/applicant_personal_info/')

    return render(request, 'applicant_academic_english_qualification.html',
                  {'year_recs': year_recs, 'qualification_obj': qualification_obj, 'english_obj': english_obj,
                   'passing_year_recs': passing_year_recs})


def save_update_applicant_academic_english_qualification(request):
    redirect_flag = False

    if request.POST:
        try:
            a_level_result_document = request.FILES.get('a_level_result_document')
        except Exception as e:
            a_level_result_document = ''

        try:
            o_level_result_document = request.FILES.get('o_level_result_document')
        except Exception as e:
            o_level_result_document = ''

        try:
            high_school_result_document = request.FILES.get('high_school_result_document')
        except Exception as e:
            high_school_result_document = ''

        try:
            english_test_one_result_document = request.FILES.get('english_test_one_result_document')
        except Exception as e:
            english_test_one_result_document = ''

        try:
            english_test_two_result_document = request.FILES.get('english_test_two_result_document')
        except Exception as e:
            english_test_two_result_document = ''

        a_level_result_document_text = request.POST.get('a_level_result_document_text')
        o_level_result_document_text = request.POST.get('o_level_result_document_text')
        high_school_result_document_text = request.POST.get('high_school_result_document_text')
        english_test_one_result_document_text = request.POST.get('english_test_one_result_document_text')
        english_test_two_result_document_text = request.POST.get('english_test_two_result_document_text')

        try:
            if StudentDetails.objects.filter(user=request.user):
                if not request.user.get_application.is_submitted:
                    if AcademicQualificationDetails.objects.filter(applicant_id=request.user.get_application).exists():
                        try:
                            AcademicQualificationDetails.objects.filter(
                                applicant_id=request.user.get_application).update(
                                a_level=request.POST['a_level'],
                                a_level_year=request.POST['a_level_year'],
                                a_level_institution=request.POST['a_level_institution'],
                                a_level_result=request.POST['a_level_result'],

                                o_level=request.POST['o_level'],
                                o_level_year=request.POST['o_level_year'],
                                o_level_institution=request.POST['o_level_institution'],
                                o_level_result=request.POST['o_level_result'],

                                high_school=request.POST['high_school'],
                                high_school_year=request.POST['high_school_year'],
                                high_school_institution=request.POST['high_school_institution'],
                                high_school_result=request.POST['high_school_result'])

                            qualification_obj = AcademicQualificationDetails.objects.get(
                                applicant_id=request.user.get_application)

                            if a_level_result_document:
                                a_level_result = str(a_level_result_document)
                                object_path = media_path(qualification_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + a_level_result, a_level_result_document)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + a_level_result),a_level_result_document)
                                qualification_obj.a_level_result_document = a_level_result

                            if not a_level_result_document_text:
                                qualification_obj.a_level_result_document = ''

                            if o_level_result_document:
                                o_level_result = str(o_level_result_document)
                                object_path = media_path(qualification_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + o_level_result, o_level_result_document)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + o_level_result),o_level_result_document)
                                qualification_obj.o_level_result_document = o_level_result

                            if not o_level_result_document_text:
                                qualification_obj.o_level_result_document = ''

                            if high_school_result_document:
                                high_school_result = str(high_school_result_document)
                                object_path = media_path(qualification_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + high_school_result,
                                                     high_school_result_document)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + high_school_result),high_school_result_document)
                                qualification_obj.high_school_result_document = high_school_result

                            if not high_school_result_document_text:
                                qualification_obj.high_school_result_document = ''

                            qualification_obj.save()

                            EnglishQualificationDetails.objects.filter(
                                applicant_id=request.user.get_application).update(
                                english_test_one=request.POST['english_test_one'],
                                english_test_one_year=request.POST['english_test_one_year'],
                                english_test_one_result=request.POST['english_test_one_result'],

                                english_test_two=request.POST['english_test_two'],
                                english_test_two_year=request.POST['english_test_two_year'],
                                english_test_two_result=request.POST['english_test_two_result'])

                            english_object = EnglishQualificationDetails.objects.get(
                                applicant_id=request.user.get_application)

                            english_test_one_result = str(english_test_one_result_document)
                            english_test_two_result = str(english_test_two_result_document)

                            if english_test_one_result_document:
                                object_path = media_path(english_object.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + english_test_one_result,
                                                     english_test_one_result_document)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + english_test_one_result),english_test_one_result_document)
                                english_object.english_test_one_result_document = english_test_one_result

                            if not english_test_one_result_document_text:
                                english_object.english_test_one_result_document = ''

                            if english_test_two_result_document:
                                object_path = media_path(english_object.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + english_test_two_result,
                                                     english_test_two_result_document)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + english_test_two_result),english_test_two_result_document)
                                english_object.english_test_two_result_document = english_test_two_result

                            if not english_test_two_result_document_text:
                                english_object.english_test_two_result_document = ''

                            english_object.save()

                            redirect_flag = True
                        except Exception as e:
                            messages.warning(request, "Form have some error" + str(e))
                    else:
                        try:
                            qualification_obj = AcademicQualificationDetails.objects.create(
                                a_level=request.POST['a_level'],
                                a_level_year=request.POST['a_level_year'],
                                a_level_result=request.POST['a_level_result'],
                                a_level_institution=request.POST['a_level_institution'],

                                o_level=request.POST['o_level'],
                                o_level_year=request.POST['o_level_year'],
                                o_level_result=request.POST['o_level_result'],
                                o_level_institution=request.POST['o_level_institution'],

                                high_school=request.POST['high_school'],
                                high_school_year=request.POST['high_school_year'],
                                high_school_result=request.POST['high_school_result'],
                                high_school_institution=request.POST['high_school_institution'],
                                applicant_id=request.user.get_application)

                            if a_level_result_document:
                                a_level_result = str(a_level_result_document)

                                object_path = media_path(qualification_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + a_level_result, a_level_result_document)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + a_level_result),a_level_result_document)
                                qualification_obj.a_level_result_document = a_level_result

                            if not a_level_result_document_text:
                                qualification_obj.a_level_result_document = ''

                            if o_level_result_document:
                                o_level_result = str(o_level_result_document)
                                object_path = media_path(qualification_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + o_level_result, o_level_result_document)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + o_level_result),o_level_result_document)
                                qualification_obj.o_level_result_document = o_level_result

                            if not o_level_result_document_text:
                                qualification_obj.o_level_result_document = ''

                            if high_school_result_document:
                                high_school_result = str(high_school_result_document)
                                object_path = media_path(qualification_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + high_school_result,
                                                     high_school_result_document)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + high_school_result),high_school_result_document)
                                qualification_obj.high_school_result_document = high_school_result

                            if not high_school_result_document_text:
                                qualification_obj.high_school_result_document = ''

                            qualification_obj.save()

                            english_object = EnglishQualificationDetails.objects.create(
                                english_test_one=request.POST['english_test_one'],
                                english_test_one_year=request.POST['english_test_one_year'],
                                english_test_one_result=request.POST['english_test_one_result'],

                                english_test_two=request.POST['english_test_two'],
                                english_test_two_year=request.POST['english_test_two_year'],
                                english_test_two_result=request.POST['english_test_two_result'],
                                applicant_id=request.user.get_application,
                            )

                            if english_test_one_result_document:
                                english_test_one_result = str(english_test_one_result_document)
                                object_path = media_path(english_object.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + english_test_one_result,
                                                     english_test_one_result_document)
                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + english_test_one_result),english_test_two_result_document)

                                english_object.english_test_one_result_document = english_test_one_result

                            if not english_test_one_result_document_text:
                                english_object.english_test_one_result_document = ''

                            if english_test_two_result_document:
                                english_test_two_result = str(english_test_two_result_document)
                                object_path = media_path(english_object.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + english_test_two_result,
                                                     english_test_two_result_document)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + english_test_two_result),english_test_two_result_document)
                                english_object.english_test_two_result_document = english_test_two_result

                            if not english_test_two_result_document_text:
                                english_object.english_test_two_result_document = ''

                            english_object.save()

                            redirect_flag = True
                        except Exception as e:
                            messages.warning(request, "Form have some error" + str(e))
                else:
                    messages.success(request, "Please fill the record.")
                    return redirect('/student/applicant_personal_info/')

                if redirect_flag:
                    messages.success(request, "Record saved")
                    return redirect('/student/applicant_curriculum_experience_info/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/student/applicant_academic_english_qualification/')


def applicant_curriculum_experience_info(request):
    year_recs = YearDetails.objects.all()
    curriculum_obj = ''
    experience_obj = ''

    passing_year_recs = PassingYear.objects.all()
    try:
        if request.user.get_application:
            if not request.user.get_application.is_submitted:
                # application_obj = ApplicationDetails.objects.get(student=student, is_submitted=False)
                if CurriculumDetails.objects.filter(applicant_id=request.user.get_application).exists():
                    curriculum_obj = CurriculumDetails.objects.get(applicant_id=request.user.get_application)

                if ExperienceDetails.objects.filter(applicant_id=request.user.get_application).exists():
                    experience_obj = ExperienceDetails.objects.get(applicant_id=request.user.get_application)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/applicant_personal_info/')
    return render(request, 'applicant_curriculum_experience_info.html',
                  {'year_recs': year_recs, 'experience_obj': experience_obj, 'curriculum_obj': curriculum_obj,
                   'passing_year_recs': passing_year_recs})


def save_update_applicant_curriculum_experience_info(request):
    redirect_flag = False

    if request.POST:
        try:
            try:
                curriculum_result_document_one = request.FILES.get('curriculum_result_document_one')
                curriculum_result_document_two = request.FILES.get('curriculum_result_document_two')
                curriculum_result_document_three = request.FILES.get('curriculum_result_document_three')

                work_experience_document_one = request.FILES.get('work_experience_document_one')
                work_experience_document_two = request.FILES.get('work_experience_document_two')

            except Exception as e:
                curriculum_result_document_one = ''
                curriculum_result_document_two = ''
                curriculum_result_document_three = ''

                work_experience_document_one = ''
                work_experience_document_two = ''

            curriculum_result_document_one_text = request.POST.get('curriculum_result_document_one_text')
            curriculum_result_document_two_text = request.POST.get('curriculum_result_document_two_text')
            curriculum_result_document_three_text = request.POST.get('curriculum_result_document_three_text')

            work_experience_document_one_text = request.POST.get('work_experience_document_one_text')
            work_experience_document_two_text = request.POST.get('work_experience_document_two_text')

            if StudentDetails.objects.filter(user=request.user):
                student = StudentDetails.objects.filter(user=request.user)[0]
                if not request.user.get_application.is_submitted:
                    # application_obj = ApplicationDetails.objects.get(student=student, is_submitted=False)
                    if CurriculumDetails.objects.filter(applicant_id=request.user.get_application).exists():
                        try:
                            CurriculumDetails.objects.filter(applicant_id=request.user.get_application).update(
                                curriculum_name_one=request.POST['curriculum_name_one'],
                                curriculum_year_one=request.POST['curriculum_year_one'],

                                curriculum_name_two=request.POST['curriculum_name_two'],
                                curriculum_year_two=request.POST['curriculum_year_two'],

                                curriculum_name_three=request.POST['curriculum_name_three'],
                                curriculum_year_three=request.POST['curriculum_year_three'])

                            curriculum_obj = CurriculumDetails.objects.get(
                                applicant_id=request.user.get_application)

                            if curriculum_result_document_one:
                                curriculum_result_one = str(curriculum_result_document_one)
                                object_path = media_path(curriculum_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + curriculum_result_one,
                                                     curriculum_result_document_one)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_one),curriculum_result_document_one)
                                curriculum_obj.curriculum_result_document_one = curriculum_result_one

                            if not curriculum_result_document_one_text:
                                curriculum_obj.curriculum_result_document_one = ''

                            if curriculum_result_document_two:
                                curriculum_result_two = str(curriculum_result_document_two)
                                object_path = media_path(curriculum_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + curriculum_result_two,
                                                     curriculum_result_document_two)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_two),curriculum_result_document_two)
                                curriculum_obj.curriculum_result_document_two = curriculum_result_two

                            if not curriculum_result_document_two_text:
                                curriculum_obj.curriculum_result_document_two = ''

                            if curriculum_result_document_three:
                                curriculum_result_three = str(curriculum_result_document_three)
                                object_path = media_path(curriculum_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + curriculum_result_three,
                                                     curriculum_result_document_three)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_three),curriculum_result_document_three)
                                curriculum_obj.curriculum_result_document_three = curriculum_result_three

                            if not curriculum_result_document_three_text:
                                curriculum_obj.curriculum_result_document_three = ''

                            curriculum_obj.save()

                            ExperienceDetails.objects.filter(applicant_id=request.user.get_application).update(
                                work_experience_one=request.POST['work_experience_one'],
                                from_date_one=request.POST['from_date_one'] if request.POST['from_date_one'] else None,
                                to_date_one=request.POST['to_date_one'] if request.POST['to_date_one'] else None,
                                experience_one_current=True if request.POST.get('experience_one_current') else False,

                                work_experience_two=request.POST['work_experience_two'],
                                from_date_two=request.POST['from_date_two'] if request.POST['from_date_two'] else None,
                                to_date_two=request.POST['to_date_two'] if request.POST['to_date_two'] else None,
                                experience_two_current=True if request.POST.get('experience_two_current') else False,
                            )

                            try:

                                experience_object = ExperienceDetails.objects.get(
                                    applicant_id=request.user.get_application)
                            except:
                                experience_object = ExperienceDetails.objects.create(
                                    work_experience_one=request.POST['work_experience_one'],
                                    from_date_one=request.POST['from_date_one'] if request.POST[
                                        'from_date_one'] else None,
                                    to_date_one=request.POST['to_date_one'] if request.POST['to_date_one'] else None,
                                    experience_one_current=True if request.POST.get('experience_one_current') else False,

                                    work_experience_two=request.POST['work_experience_two'],
                                    from_date_two=request.POST['from_date_two'] if request.POST[
                                        'from_date_two'] else None,
                                    to_date_two=request.POST['to_date_two'] if request.POST['to_date_two'] else None,
                                    experience_two_current=True if request.POST.get('experience_two_current') else False,
                                    applicant_id=request.user.get_application)

                            if work_experience_document_one:
                                work_experience_one = str(work_experience_document_one)
                                object_path = media_path(experience_object.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + work_experience_one,
                                                     work_experience_document_one)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + work_experience_one),work_experience_document_one)
                                experience_object.work_experience_document_one = work_experience_one

                            if not work_experience_document_one_text:
                                experience_object.work_experience_document_one = ''

                            if work_experience_document_two:
                                work_experience_two = str(work_experience_document_two)
                                object_path = media_path(experience_object.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + work_experience_two,
                                                     work_experience_document_two)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + work_experience_two),work_experience_document_two)
                                experience_object.work_experience_document_two = work_experience_two

                            if not work_experience_document_two_text:
                                experience_object.work_experience_document_two = ''

                            experience_object.save()

                            redirect_flag = True
                        except Exception as e:
                            messages.warning(request, "Form have some error" + str(e))
                    else:
                        try:
                            curriculum_obj = CurriculumDetails.objects.create(
                                curriculum_name_one=request.POST['curriculum_name_one'],
                                curriculum_year_one=request.POST['curriculum_year_one'],

                                curriculum_name_two=request.POST['curriculum_name_two'],
                                curriculum_year_two=request.POST['curriculum_year_two'],

                                curriculum_name_three=request.POST['curriculum_name_three'],
                                curriculum_year_three=request.POST['curriculum_year_three'],
                                applicant_id=request.user.get_application)

                            if curriculum_result_document_one:
                                curriculum_result_one = str(curriculum_result_document_one)
                                object_path = media_path(curriculum_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + curriculum_result_one,
                                                     curriculum_result_document_one)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_one),curriculum_result_document_one)
                                curriculum_obj.curriculum_result_document_one = curriculum_result_one

                            if not curriculum_result_document_one_text:
                                curriculum_obj.curriculum_result_document_one = ''

                            if curriculum_result_document_two:
                                curriculum_result_two = str(curriculum_result_document_two)
                                object_path = media_path(curriculum_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + curriculum_result_two,
                                                     curriculum_result_document_two)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_two),curriculum_result_document_two)
                                curriculum_obj.curriculum_result_document_two = curriculum_result_two

                            if not curriculum_result_document_two_text:
                                curriculum_obj.curriculum_result_document_two = ''

                            if curriculum_result_document_three:
                                curriculum_result_three = str(curriculum_result_document_three)
                                object_path = media_path(curriculum_obj.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + curriculum_result_three,
                                                     curriculum_result_document_three)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_three),curriculum_result_document_three)
                                curriculum_obj.curriculum_result_document_three = curriculum_result_three

                            if not curriculum_result_document_three_text:
                                curriculum_obj.curriculum_result_document_three = ''

                            curriculum_obj.save()

                            experience_object = ExperienceDetails.objects.create(
                                work_experience_one=request.POST['work_experience_one'],
                                from_date_one=request.POST['from_date_one'] if request.POST['from_date_one'] else None,
                                to_date_one=request.POST['to_date_one'] if request.POST['to_date_one'] else None,
                                experience_one_current=True if request.POST.get('experience_one_current') else False,

                                work_experience_two=request.POST['work_experience_two'],
                                from_date_two=request.POST['from_date_two'] if request.POST['from_date_two'] else None,
                                to_date_two=request.POST['to_date_two'] if request.POST['to_date_two'] else None,
                                experience_two_current=True if request.POST.get('experience_two_current') else False,
                                applicant_id=request.user.get_application)

                            if work_experience_document_one:
                                work_experience_one = str(work_experience_document_one)
                                object_path = media_path(experience_object.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + work_experience_one,
                                                     work_experience_document_one)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + work_experience_one),work_experience_document_one)
                                experience_object.work_experience_document_one = work_experience_one

                            if not work_experience_document_one_text:
                                experience_object.work_experience_document_one = ''

                            if work_experience_document_two:
                                work_experience_two = str(work_experience_document_two)
                                object_path = media_path(experience_object.applicant_id)
                                handle_uploaded_file(str(object_path) + '/' + work_experience_two,
                                                     work_experience_document_two)

                                # handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + work_experience_two),work_experience_document_two)
                                experience_object.work_experience_document_two = work_experience_two

                            if not work_experience_document_two_text:
                                experience_object.work_experience_document_two = ''

                            experience_object.save()

                            redirect_flag = True
                        except Exception as e:
                            messages.warning(request, "Form have some error" + str(e))
                else:
                    messages.success(request, "Please fill the record.")
                    return redirect('/student/applicant_personal_info/')

                if redirect_flag:
                    messages.success(request, "Record saved")
                    return redirect('/student/applicant_scholarship_about_yourself_info/')
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.warning(request, "Please fill proper form")
    return redirect('/student/applicant_scholarship_about_yourself_info/')


def applicant_scholarship_about_yourself_info(request):
    scholarship_recs = ScholarshipDetails.objects.all()
    degree_obj = DegreeDetails.objects.all()
    university_obj = UniversityDetails.objects.all()
    course_recs = ProgramDetails.objects.all()

    scholarship_obj = ''
    about_obj = ''
    application_obj = ''

    try:
        if request.user.get_application:
            if not request.user.get_application.is_submitted:
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
                   'application_obj': application_obj})


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
    application_obj = request.user.get_application
    siblings_obj = application_obj.sibling_applicant_rel.all()
    qualification_obj = application_obj.academic_applicant_rel.get()
    english_obj = application_obj.english_applicant_rel.get()
    curriculum_obj = application_obj.curriculum_applicant_rel.get()
    applicant_experience_obj = application_obj.applicant_experience_rel.get()
    scholarship_obj = application_obj.applicant_scholarship_rel.get()

    # path = str(settings.MEDIA_URL) + str('reports/Donors.pdf')
    # path =str('/home/redbytes/scholarship_proj/scholarship_mgmt/media/reports/Donors.pdf')
    return render(request, 'my_application.html', {'siblings_obj': siblings_obj, 'application_obj': application_obj,
                                                   'qualification_obj': qualification_obj, 'english_obj': english_obj,
                                                   'curriculum_obj': curriculum_obj,
                                                   'applicant_experience_obj': applicant_experience_obj,
                                                   'scholarship_obj': scholarship_obj})


def submit_application(request):
    try:
        ApplicationDetails.objects.filter(application_id=request.user.get_application_id).update(is_submitted=True)
        ApplicationHistoryDetails.objects.create(applicant_id=request.user.get_application,
                                                 status='Application Submitted',
                                                 remark='Your application is submitted and your institution will be notified on further updates regarding your applications.')

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
        if request.user.get_application:
            if request.user.get_application.is_submitted:
                year_recs = YearDetails.objects.all()
                semester_recs = SemesterDetails.objects.all()

                progress_recs = ApplicantAcademicProgressDetails.objects.filter(
                    applicant_id=request.user.get_application)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/student_home/')
    return render(request, 'applicant_academic_progress.html',
                  {'semester_recs': semester_recs, 'year_recs': year_recs, 'progress_recs': progress_recs})


@semester_required
def save_applicant_academic_progress(request):
    try:
        transcript_document = request.FILES['transcript_document']
    except:
        transcript_document = ''

    year = request.POST.get('year')
    date = request.POST.get('date')
    semester = request.POST.get('semester')

    gpa_scored = request.POST.get('gpa_scored')
    gpa_from = request.POST.get('gpa_from')

    cgpa_scored = request.POST.get('cgpa_scored')
    cgpa_from = request.POST.get('cgpa_from')
    try:
        progress_obj = ApplicantAcademicProgressDetails.objects.create(year_id=year,
                                                                       date=date if date else None,
                                                                       semester_id=semester,
                                                                       gpa_scored=gpa_scored,
                                                                       gpa_from=gpa_from,
                                                                       cgpa_scored=cgpa_scored,
                                                                       cgpa_from=cgpa_from,
                                                                       applicant_id=request.user.get_application)

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
        username = request.user.get_application.get_full_name()
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
