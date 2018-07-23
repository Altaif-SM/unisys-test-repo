from django.db.models import Q
from django.shortcuts import render, redirect
from masters.models import StudentDonorMapping, CountryDetails, DegreeDetails, UniversityDetails
from student.models import ApplicationDetails, ApplicationHistoryDetails, StudentDetails
import json
from django.contrib import messages


# Create your views here.
def template_donor_dashboard(request):
    return render(request, "template_donor_dashboard.html")


def template_student_selection(request):
    country_recs = CountryDetails.objects.all()
    university_recs = UniversityDetails.objects.filter(country=request.user.donor_user_rel.get().country)
    degree_recs = DegreeDetails.objects.all()

    stud = []
    for obj in StudentDonorMapping.objects.filter(donor__user=request.user):
        stud.append(StudentDetails.objects.get(id=obj.student.id))

    application_records = ApplicationDetails.objects.filter(student__in=stud, admin_approval=True)
    return render(request, "template_student_selection.html",
                  {"application_records": application_records, 'country_recs': country_recs,
                   'university_recs': university_recs,
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


def filter_student_selection(request):
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

        stud = []
        for obj in StudentDonorMapping.objects.filter(donor__user=request.user):
            stud.append(StudentDetails.objects.get(id=obj.student.id))

        application_records = ApplicationDetails.objects.filter(Q(student__in=stud),
                                                                Q(
                                                                    address__country=request.user.donor_user_rel.get().country,
                                                                    admin_approval=True),
                                                                filter_nationality(nationality),
                                                                filter_degree(degree),
                                                                filter_university(university))

        country_recs = CountryDetails.objects.all()
        university_recs = UniversityDetails.objects.filter(country=request.user.donor_user_rel.get().country)
        degree_recs = DegreeDetails.objects.all()

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, 'template_student_selection.html',
                  {'application_records': application_records, 'country_recs': country_recs,
                   'university_recs': university_recs,
                   'degree_recs': degree_recs})


def template_student_details(request, app_id):
    application_rec = ApplicationDetails.objects.get(id=app_id)
    return render(request, "template_student_details.html", {'application_rec': application_rec})


def template_student_reports(request):
    country_recs = CountryDetails.objects.all()
    university_recs = UniversityDetails.objects.filter(country=request.user.donor_user_rel.get().country)
    degree_recs = DegreeDetails.objects.all()

    stud = []
    for obj in StudentDonorMapping.objects.filter(donor__user=request.user):
        stud.append(StudentDetails.objects.get(id=obj.student.id))

    application_records = ApplicationDetails.objects.filter(student__in=stud,
                                                            is_sponsored=True)

    return render(request, "template_student_reports.html",
                  {"application_records": application_records, 'country_recs': country_recs,
                   'university_recs': university_recs,
                   'degree_recs': degree_recs})


def filter_student_report(request):
    if request.POST:
        request.session['form_data'] = request.POST
        university = request.POST.get('university')
        degree = request.POST.get('degree')
        country = request.POST.get('country')
    else:

        form_data = request.session.get('form_data')

        university = form_data.get('university')
        degree = form_data.get('degree')
        country = form_data.get('country')

    try:

        stud = []
        for obj in StudentDonorMapping.objects.filter(donor__user=request.user):
            stud.append(StudentDetails.objects.get(id=obj.student.id))

        application_records = ApplicationDetails.objects.filter(Q(student__in=stud),
                                                                Q(
                                                                    address__country=request.user.donor_user_rel.get().country,
                                                                    is_sponsored=True), filter_nationality(country),
                                                                filter_degree(degree),
                                                                filter_university(university))

        country_recs = CountryDetails.objects.all()
        university_recs = UniversityDetails.objects.filter(country=request.user.donor_user_rel.get().country)
        degree_recs = DegreeDetails.objects.all()

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, 'template_student_reports.html',
                  {'application_records': application_records, 'country_recs': country_recs,
                   'university_recs': university_recs,
                   'degree_recs': degree_recs})


def template_application_progress_history(request):
    applicant_recs = ''
    try:
        if request.user.is_super_admin():
            applicant_recs = ApplicationDetails.objects.filter(is_sponsored=True)
        else:
            stud = []
            for obj in StudentDonorMapping.objects.filter(donor__user=request.user):
                stud.append(StudentDetails.objects.get(id=obj.student.id))

            applicant_recs = ApplicationDetails.objects.filter(student__in=stud,
                                                               address__country=request.user.donor_user_rel.get().country,
                                                               is_sponsored=True)
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
            applicant_recs = ApplicationDetails.objects.filter(is_sponsored=True)
            application_history_recs = ApplicationDetails.objects.get(id=application).applicant_history_rel.all()
            application_obj = ApplicationDetails.objects.get(id=application)
        else:
            stud = []
            for obj in StudentDonorMapping.objects.filter(donor__user=request.user):
                stud.append(StudentDetails.objects.get(id=obj.student.id))

            applicant_recs = ApplicationDetails.objects.filter(student__in=stud,
                                                               address__country=request.user.donor_user_rel.get().country,
                                                               is_sponsored=True)
            application_obj = ApplicationDetails.objects.get(id=application)

            application_history_recs = ApplicationDetails.objects.get(id=application).applicant_history_rel.all()

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/partner/template_registered_application/')

    return render(request, 'template_student_progress_history.html',
                  {'applicant_recs': applicant_recs, 'application_history_recs': application_history_recs,
                   'application_obj': application_obj})


def template_my_payments(request):

    stud = StudentDonorMapping.objects.filter(donor__user=request.user).values("student")
    student_list = StudentDetails.objects.filter(id__in=stud)

    return render(request, "template_my_payments.html", {'student_list': student_list})


def template_students_receipts(request):

    debit_total = 0
    outstanding_total = 0


    stud = StudentDonorMapping.objects.filter(donor__user=request.user).values("student")
    student_list = StudentDetails.objects.filter(id__in=stud).distinct()


    student_list_rec = []

    for obj in student_list:

        raw_dict = {}
        raw_dict_one = {}
        approval_amount = 0
        credit_total = 0
        outstanding_amount = 0
        application_list = []
        for application_obj in obj.student_applicant_rel.all():

            if application_obj.rel_donor_receipt_voucher.all():
                approval_amount = application_obj.scholarship_fee

                raw_dict['application_rec'] = application_obj
                for voucher_obj in application_obj.rel_student_payment_receipt_voucher.all():

                    raw_dict['voucher_rec'] = voucher_obj
                    if voucher_obj.voucher_type == "credit":
                        credit_total += float(voucher_obj.voucher_amount)

                outstanding_amount = float(approval_amount) - float(credit_total)

                raw_dict['approval_amount'] = float(approval_amount)
                raw_dict['credit_total'] = float(credit_total)
                raw_dict['outstanding_amount'] = float(outstanding_amount)
                student_list_rec.append(raw_dict)

        debit_total += float(credit_total)
        outstanding_total += float(outstanding_amount)

    return render(request, "template_students_receipts.html", {'voucher_record': student_list_rec, 'debit_total': debit_total, 'outstanding_total': outstanding_total})


def approve_sponsorship(request):
    application_rec = ApplicationDetails.objects.get(id=request.POST['app_id'])
    application_rec.is_sponsored = True
    application_rec.save()
    return render(request, "template_student_details.html", {'application_rec': application_rec})
