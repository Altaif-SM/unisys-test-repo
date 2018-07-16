from django.shortcuts import render, redirect
from masters.views import *

from django.http import HttpResponse
from django.contrib import messages
from common.utils import get_application_id


# Create your views here.

def student_home(request):
    application_history_obj = ''

    try:
        if ApplicationDetails.objects.filter(application_id=request.user.get_application_id,
                                             is_submitted=True).exists():
            application_history_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id,
                                                                     is_submitted=True).applicant_history_rel.all()
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))

    return render(request, 'student_home.html',
                  {'application_history_obj': application_history_obj})


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
    pic = request.POST.get('pic')
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
                    birth_date=request.POST['birth_date'],
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
                # application_id = get_application_id(application_obj)

                application_obj.address = address_obj
                # application_obj.application_id = application_id
                application_obj.save()

                redirect_flag = True
            else:
                try:
                    current_year = YearDetails.objects.get(active_year=True)
                    application_obj = ApplicationDetails.objects.create(first_name=request.POST['first_name'],
                                                                        middle_name=request.POST['middle_name'],
                                                                        last_name=request.POST['last_name'],
                                                                        birth_date=request.POST['birth_date'],
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

                    application_id = get_application_id(application_obj)

                    application_obj.application_id = application_id
                    application_obj.address = address_obj
                    application_obj.save()
                    redirect_flag = True
                except Exception as e:
                    messages.warning(request, "Form have some error" + str(e))

            try:
                if pic:
                    dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
                    filename = "%s_%s.%s" % (str(application_obj.id), dirname, 'png')
                    raw_file_path_and_name = os.path.join('images/' + filename)
                    data = str(pic)
                    temp_data = data.split('base64,')[1]
                    raw_data = base64.b64decode(temp_data)
                    f = open(settings.MEDIA_ROOT + raw_file_path_and_name, 'wb')
                    f.write(raw_data)
                    f.close()
                    application_obj.image = raw_file_path_and_name
                    application_obj.save()
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

    application_obj = ''

    if ApplicationDetails.objects.filter(application_id=request.user.get_application_id,
                                         is_submitted=False).exists():
        application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id,
                                                         is_submitted=False)

    return render(request, 'applicant_family_info.html',
                  {'country_recs': country_recs, 'application_obj': application_obj})


def save_update_applicant_family_info(request):
    redirect_flag = False

    if request.POST:
        try:
            try:
                wife_pay_slip = request.FILES['wife_pay_slip']
                father_pay_slip = request.FILES['father_pay_slip']
            except Exception as e:
                wife_pay_slip = ''
                father_pay_slip = ''

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
                        wife_dob=request.POST['wife_dob'],
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
                            'father_dob'],
                        father_email=request.POST[
                            'father_email'])

                    application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id)

                    if wife_pay_slip:
                        wife_slip = str(wife_pay_slip)
                        handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + wife_slip), wife_pay_slip)
                        application_obj.wife_pay_slip = wife_slip

                    if father_pay_slip:
                        father_slip = str(father_pay_slip)
                        handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + father_slip),
                                             father_pay_slip)
                        application_obj.father_pay_slip = father_slip

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
                        mother_dob=request.POST['mother_dob'],
                        mother_email=request.POST[
                            'mother_email'])

                    application_obj = request.user.get_application

                    mother_slip = str(mother_pay_slip)

                    if mother_pay_slip:
                        handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + mother_slip),
                                             mother_pay_slip)
                        application_obj.mother_pay_slip = mother_slip
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

    try:
        if request.user.get_application:
            if not request.user.get_application.is_submitted:
                # application_obj = ApplicationDetails.objects.get(application_id=request.user.get_application_id,
                #                                           is_submitted=False)
                if AcademicQualificationDetails.objects.filter(applicant_id=request.user.get_application).exists():
                    qualification_obj = AcademicQualificationDetails.objects.get(applicant_id=request.user.get_application)

                if EnglishQualificationDetails.objects.filter(applicant_id=request.user.get_application).exists():
                    english_obj = EnglishQualificationDetails.objects.get(applicant_id=request.user.get_application)
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/student/applicant_personal_info/')

    return render(request, 'applicant_academic_english_qualification.html',
                  {'year_recs': year_recs, 'qualification_obj': qualification_obj, 'english_obj': english_obj})


def save_update_applicant_academic_english_qualification(request):
    redirect_flag = False

    if request.POST:
        try:
            a_level_result_document = request.FILES['a_level_result_document']
            o_level_result_document = request.FILES['o_level_result_document']
            high_school_result_document = request.FILES['high_school_result_document']

            english_test_one_result_document = request.FILES['english_test_one_result_document']
            english_test_two_result_document = request.FILES['english_test_two_result_document']

        except Exception as e:
            a_level_result_document = ''
            o_level_result_document = ''
            high_school_result_document = ''

            english_test_one_result_document = ''
            english_test_two_result_document = ''
        try:
            if StudentDetails.objects.filter(user=request.user):
                if not request.user.get_application.is_submitted:
                    if AcademicQualificationDetails.objects.filter(applicant_id=request.user.get_application).exists():
                        try:
                            AcademicQualificationDetails.objects.filter(
                                applicant_id=request.user.get_application).update(
                                a_level=request.POST['a_level'],
                                a_level_year_id=request.POST['a_level_year'],
                                a_level_result=request.POST['a_level_result'],

                                o_level=request.POST['o_level'],
                                o_level_year_id=request.POST['o_level_year'],
                                o_level_result=request.POST['o_level_result'],

                                high_school=request.POST['high_school'],
                                high_school_year_id=request.POST['high_school_year'],
                                high_school_result=request.POST['high_school_result'])

                            qualification_obj = AcademicQualificationDetails.objects.get(
                                applicant_id=request.user.get_application)

                            if a_level_result_document:
                                a_level_result = str(a_level_result_document)
                                handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + a_level_result),
                                                     a_level_result_document)
                                qualification_obj.a_level_result_document = a_level_result

                            if o_level_result_document:
                                o_level_result = str(o_level_result_document)
                                handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + o_level_result),
                                                     o_level_result_document)
                                qualification_obj.o_level_result_document = o_level_result

                            if high_school_result_document:
                                high_school_result = str(high_school_result_document)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + high_school_result),
                                    high_school_result_document)
                                qualification_obj.high_school_result_document = high_school_result

                            qualification_obj.save()

                            EnglishQualificationDetails.objects.filter(
                                applicant_id=request.user.get_application).update(
                                english_test_one=request.POST['english_test_one'],
                                english_test_one_year_id=request.POST['english_test_one_year'],
                                english_test_one_result=request.POST['english_test_one_result'],

                                english_test_two=request.POST['english_test_two'],
                                english_test_two_year_id=request.POST['english_test_two_year'],
                                english_test_two_result=request.POST['english_test_two_result'])

                            english_object = EnglishQualificationDetails.objects.get(
                                applicant_id=request.user.get_application)

                            english_test_one_result = str(english_test_one_result_document)
                            english_test_two_result = str(english_test_two_result_document)

                            if english_test_one_result_document:
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + english_test_one_result),
                                    english_test_one_result_document)
                                english_object.english_test_one_result_document = english_test_one_result

                            if english_test_two_result_document:
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + english_test_two_result),
                                    english_test_two_result_document)
                                english_object.english_test_two_result_document = english_test_two_result

                            english_object.save()

                            redirect_flag = True
                        except Exception as e:
                            messages.warning(request, "Form have some error" + str(e))
                    else:
                        try:
                            qualification_obj = AcademicQualificationDetails.objects.create(
                                a_level=request.POST['a_level'],
                                a_level_year_id=request.POST['a_level_year'],
                                a_level_result=request.POST['a_level_result'],

                                o_level=request.POST['o_level'],
                                o_level_year_id=request.POST['o_level_year'],
                                o_level_result=request.POST['o_level_result'],

                                high_school=request.POST['high_school'],
                                high_school_year_id=request.POST['high_school_year'],
                                high_school_result=request.POST['high_school_result'],
                                applicant_id=request.user.get_application)

                            if a_level_result_document:
                                a_level_result = str(a_level_result_document)
                                handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + a_level_result),
                                                     a_level_result_document)
                                qualification_obj.a_level_result_document = a_level_result

                            if o_level_result_document:
                                o_level_result = str(o_level_result_document)
                                handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + o_level_result),
                                                     o_level_result_document)
                                qualification_obj.o_level_result_document = o_level_result

                            if high_school_result_document:
                                high_school_result = str(high_school_result_document)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + high_school_result),
                                    high_school_result_document)
                                qualification_obj.high_school_result_document = high_school_result

                            qualification_obj.save()

                            english_object = EnglishQualificationDetails.objects.create(
                                english_test_one=request.POST['english_test_one'],
                                english_test_one_year_id=request.POST['english_test_one_year'],
                                english_test_one_result=request.POST['english_test_one_result'],

                                english_test_two=request.POST['english_test_two'],
                                english_test_two_year_id=request.POST['english_test_two_year'],
                                english_test_two_result=request.POST['english_test_two_result'],
                                applicant_id=request.user.get_application,
                            )

                            if english_test_one_result_document:
                                english_test_one_result = str(english_test_one_result_document)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + english_test_one_result),
                                    english_test_two_result_document)
                                english_object.english_test_one_result_document = english_test_one_result

                            if english_test_two_result_document:
                                english_test_two_result = str(english_test_two_result_document)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + english_test_two_result),
                                    english_test_two_result_document)
                                english_object.english_test_two_result_document = english_test_two_result

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
                  {'year_recs': year_recs, 'experience_obj': experience_obj, 'curriculum_obj': curriculum_obj})


def save_update_applicant_curriculum_experience_info(request):
    redirect_flag = False

    if request.POST:
        try:
            try:
                curriculum_result_document_one = request.FILES['curriculum_result_document_one']
                curriculum_result_document_two = request.FILES['curriculum_result_document_two']
                curriculum_result_document_three = request.FILES['curriculum_result_document_three']

                work_experience_document_one = request.FILES['work_experience_document_one']
                work_experience_document_two = request.FILES['work_experience_document_two']

            except Exception as e:
                curriculum_result_document_one = ''
                curriculum_result_document_two = ''
                curriculum_result_document_three = ''

                work_experience_document_one = ''
                work_experience_document_two = ''

            if StudentDetails.objects.filter(user=request.user):
                student = StudentDetails.objects.filter(user=request.user)[0]
                if not request.user.get_application.is_submitted:
                    # application_obj = ApplicationDetails.objects.get(student=student, is_submitted=False)
                    if CurriculumDetails.objects.filter(applicant_id=request.user.get_application).exists():
                        try:
                            CurriculumDetails.objects.filter(applicant_id=request.user.get_application).update(
                                curriculum_name_one=request.POST['curriculum_name_one'],
                                curriculum_year_one_id=request.POST['curriculum_year_one'],

                                curriculum_name_two=request.POST['curriculum_name_two'],
                                curriculum_year_two_id=request.POST['curriculum_year_two'],

                                curriculum_name_three=request.POST['curriculum_name_three'],
                                curriculum_year_three_id=request.POST['curriculum_year_three'])

                            curriculum_obj = CurriculumDetails.objects.get(
                                applicant_id=request.user.get_application)

                            if curriculum_result_document_one:
                                curriculum_result_one = str(curriculum_result_document_one)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_one),
                                    curriculum_result_document_one)
                                curriculum_obj.curriculum_result_document_one = curriculum_result_one

                            if curriculum_result_document_two:
                                curriculum_result_two = str(curriculum_result_document_two)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_two),
                                    curriculum_result_document_two)
                                curriculum_obj.curriculum_result_document_two = curriculum_result_two

                            if curriculum_result_document_three:
                                curriculum_result_three = str(curriculum_result_document_three)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_three),
                                    curriculum_result_document_three)
                                curriculum_obj.curriculum_result_document_three = curriculum_result_three

                                curriculum_obj.save()

                            ExperienceDetails.objects.filter(applicant_id=request.user.get_application).update(
                                work_experience_one=request.POST['work_experience_one'],
                                from_date_one=request.POST['from_date_one'],
                                to_date_one=request.POST['to_date_one'],

                                work_experience_two=request.POST['work_experience_two'],
                                from_date_two=request.POST['from_date_two'],
                                to_date_two=request.POST['to_date_two'])

                            experience_object = ExperienceDetails.objects.get(applicant_id=request.user.get_application)

                            if work_experience_document_one:
                                work_experience_one = str(work_experience_document_one)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + work_experience_one),
                                    work_experience_document_one)
                                experience_object.work_experience_document_one = work_experience_one

                            if work_experience_document_two:
                                work_experience_two = str(work_experience_document_two)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + work_experience_two),
                                    work_experience_document_two)
                                experience_object.work_experience_document_two = work_experience_two

                            experience_object.save()

                            redirect_flag = True
                        except Exception as e:
                            messages.warning(request, "Form have some error" + str(e))
                    else:
                        try:
                            curriculum_obj = CurriculumDetails.objects.create(
                                curriculum_name_one=request.POST['curriculum_name_one'],
                                curriculum_year_one_id=request.POST['curriculum_year_one'],

                                curriculum_name_two=request.POST['curriculum_name_two'],
                                curriculum_year_two_id=request.POST['curriculum_year_two'],

                                curriculum_name_three=request.POST['curriculum_name_three'],
                                curriculum_year_three_id=request.POST['curriculum_year_three'],
                                applicant_id=request.user.get_application)

                            if curriculum_result_document_one:
                                curriculum_result_one = str(curriculum_result_document_one)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_one),
                                    curriculum_result_document_one)
                                curriculum_obj.curriculum_result_document_one = curriculum_result_one

                            if curriculum_result_document_two:
                                curriculum_result_two = str(curriculum_result_document_two)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_two),
                                    curriculum_result_document_two)
                                curriculum_obj.curriculum_result_document_two = curriculum_result_two

                            if curriculum_result_document_three:
                                curriculum_result_three = str(curriculum_result_document_three)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + curriculum_result_three),
                                    curriculum_result_document_three)
                                curriculum_obj.curriculum_result_document_three = curriculum_result_three

                                curriculum_obj.save()

                                experience_object = ExperienceDetails.objects.create(
                                    work_experience_one=request.POST['work_experience_one'],
                                    from_date_one=request.POST['from_date_one'],
                                    to_date_one=request.POST['to_date_one'],

                                    work_experience_two=request.POST['work_experience_two'],
                                    from_date_two=request.POST['from_date_two'],
                                    to_date_two=request.POST['to_date_two'],
                                    applicant_id=request.user.get_application)

                            if work_experience_document_one:
                                work_experience_one = str(work_experience_document_one)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + work_experience_one),
                                    work_experience_document_one)
                                experience_object.work_experience_document_one = work_experience_one

                            if work_experience_document_two:
                                work_experience_two = str(work_experience_document_two)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + work_experience_two),
                                    work_experience_document_two)
                                experience_object.work_experience_document_two = work_experience_two

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

    scholarship_obj = ''
    about_obj = ''

    try:
        if not request.user.get_application.is_submitted:
            if request.user.get_application:
                if ScholarshipSelectionDetails.objects.filter(applicant_id=request.user.get_application).exists():
                    scholarship_obj = ScholarshipSelectionDetails.objects.get(applicant_id=request.user.get_application)

                if ApplicantAboutDetails.objects.filter(applicant_id=request.user.get_application).exists():
                    about_obj = ApplicantAboutDetails.objects.get(applicant_id=request.user.get_application)
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return render(request, 'applicant_scholarship_about_yourself_info.html',
                  {'scholarship_recs': scholarship_recs, 'scholarship_obj': scholarship_obj, 'about_obj': about_obj,
                   'university_obj': university_obj, 'degree_obj': degree_obj})


def save_update_applicant_scholarship_about_yourself_info(request):
    try:
        admission_letter_document = request.FILES['admission_letter_document']
    except:
        admission_letter_document = ''

    redirect_flag = False

    if request.POST:
        try:
            if StudentDetails.objects.filter(user=request.user):
                student = StudentDetails.objects.filter(user=request.user)[0]
                if not request.user.get_application.is_submitted:
                    # application_obj = ApplicationDetails.objects.get(student=student, is_submitted=False)
                    if ScholarshipSelectionDetails.objects.filter(applicant_id=request.user.get_application).exists():
                        try:
                            ScholarshipSelectionDetails.objects.filter(
                                applicant_id=request.user.get_application).update(
                                scholarship_id=request.POST['scholarship'],
                                course_applied_id=request.POST['course_applied'],
                                university=request.POST['university'])

                            scholarship_obj = ScholarshipSelectionDetails.objects.get(
                                applicant_id=request.user.get_application)

                            if admission_letter_document:
                                admission_letter = str(admission_letter_document)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + admission_letter),
                                    admission_letter_document)
                                scholarship_obj.admission_letter_document = admission_letter
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
                                university_id=request.POST['university'],
                                applicant_id=request.user.get_application)

                            if admission_letter_document:
                                admission_letter = str(admission_letter_document)
                                handle_uploaded_file(
                                    settings.MEDIA_ROOT + os.path.join('reports/' + admission_letter),
                                    admission_letter_document)
                                scholarship_obj.admission_letter_document = admission_letter
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
    # path = str(settings.MEDIA_URL) + str('reports/Donors.pdf')
    # path =str('/home/redbytes/scholarship_proj/scholarship_mgmt/media/reports/Donors.pdf')
    return render(request, 'my_application.html')


def submit_application(request):

    try:
        ApplicationDetails.objects.filter(application_id=request.user.get_application_id).update(is_submitted=True)
        ApplicationHistoryDetails.objects.create(applicant_id=request.user.get_application,
                                                 status='Application Submitted',
                                                 remark='Your application is submitted and your institution will be notified on further updates regarding your applications.')

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
    return redirect('/student/student_home/')

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
