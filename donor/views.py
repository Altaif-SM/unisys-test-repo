from django.db.models import Q
from django.shortcuts import render, redirect
from masters.models import StudentDonorMapping, CountryDetails, DegreeDetails, UniversityDetails, ProgramDetails
from student.models import ApplicationDetails, ApplicationHistoryDetails, StudentDetails
import json
from django.contrib import messages
from common.utils import *
from accounting.models import DonorReceiptVoucher
from django.db.models import Sum
from accounts.decoratars import user_login_required
from donor.models import DonorDetails

# Create your views here.
def template_donor_dashboard(request):
    return render(request, "template_donor_dashboard.html")


def template_student_selection(request):
    country_recs = CountryDetails.objects.all()
    university_recs = UniversityDetails.objects.all()
    degree_recs = DegreeDetails.objects.all()
    program_recs = ProgramDetails.objects.all()
    # stud = []
    # for obj in StudentDonorMapping.objects.filter(donor__user=request.user):
    #     stud.append(StudentDetails.objects.get(id=obj.student.id))

    stud = StudentDetails.objects.all()
    application_records = ApplicationDetails.objects.filter(student__in=stud, admin_approval=True,year=get_current_year())
    return render(request, "template_student_selection.html",
                  {"application_records": application_records, 'country_recs': country_recs,
                   'university_recs': university_recs,'program_recs': program_recs,
                   'degree_recs': degree_recs})


def filter_nationality(field):
    if field != '':
        return Q(nationality_id=field)
    else:
        return Q()  # Dummy filter


def filter_degree(degree):
    if degree != '':
        return Q(applicant_scholarship_rel__degree_id=degree)
    else:
        return Q()  # Dummy filter


def filter_university(university):
    if university != '':
        return Q(applicant_scholarship_rel__university_id=university)
    else:
        return Q()  # Dummy filter

def filter_program(program):
    if program != '':
        return Q(applicant_scholarship_rel__course_applied_id=program)
    else:
        return Q()  # Dummy filter


def filter_student_selection(request):
    if request.POST:
        request.session['form_data'] = request.POST
        university = request.POST.get('university')
        degree = request.POST.get('degree')
        nationality = request.POST.get('nationality')
        country = request.POST.get('country')
        program = request.POST.get('program')
    else:

        form_data = request.session.get('form_data')

        university = form_data.get('university')
        country = form_data.get('country')
        degree = form_data.get('degree')
        nationality = form_data.get('nationality')
        program = form_data.get('program')

    try:

        # stud = []
        # for obj in StudentDonorMapping.objects.filter(donor__user=request.user):
        #     stud.append(StudentDetails.objects.get(id=obj.student.id))
        stud = StudentDetails.objects.all()

        if country:
            stud = stud.filter(address__country=country)

        application_records = ApplicationDetails.objects.filter(Q(student__in=stud),filter_nationality(nationality),
                                                                filter_degree(degree),filter_program(program),
                                                                filter_university(university), admin_approval=True,year=get_current_year())

        country_recs = CountryDetails.objects.all()
        university_recs = UniversityDetails.objects.all()
        degree_recs = DegreeDetails.objects.all()
        program_recs = ProgramDetails.objects.all()

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/donor/template_student_selection/')

    return render(request, 'template_student_selection.html',
                  {'application_records': application_records, 'country_recs': country_recs,
                   'university_recs': university_recs,'program_recs': program_recs,
                   'degree_recs': degree_recs})


def template_student_details(request, app_id):
    application_obj = ApplicationDetails.objects.get(id=app_id)
    siblings_obj = application_obj.sibling_applicant_rel.all() if application_obj.sibling_applicant_rel.all() else ''
    qualification_obj = application_obj.academic_applicant_rel.get() if application_obj.academic_applicant_rel.all() else ''
    english_obj = application_obj.english_applicant_rel.get() if application_obj.english_applicant_rel.all() else ''
    curriculum_obj = application_obj.curriculum_applicant_rel.get() if application_obj.curriculum_applicant_rel.all() else ''
    applicant_experience_obj = application_obj.applicant_experience_rel.get() if application_obj.applicant_experience_rel.all() else ''
    scholarship_obj = application_obj.applicant_scholarship_rel.get() if application_obj.applicant_scholarship_rel.all() else ''

    return render(request, 'template_student_details.html',
                  {'siblings_obj': siblings_obj, 'application_obj': application_obj,
                   'qualification_obj': qualification_obj, 'english_obj': english_obj,
                   'curriculum_obj': curriculum_obj,
                   'applicant_experience_obj': applicant_experience_obj,
                   'scholarship_obj': scholarship_obj})


def template_student_reports(request):
    country_recs = CountryDetails.objects.all()
    university_recs = UniversityDetails.objects.all()
    degree_recs = DegreeDetails.objects.all()
    program_recs = ProgramDetails.objects.all()

    stud = []
    for obj in StudentDonorMapping.objects.filter(donor__user=request.user,applicant_id__year=get_current_year()):
        stud.append(StudentDetails.objects.get(id=obj.student.id))

    application_records = ApplicationDetails.objects.filter(student__in=stud,
                                                            is_sponsored=True)

    return render(request, "template_student_reports.html",
                  {"application_records": application_records, 'country_recs': country_recs,
                   'university_recs': university_recs, 'program_recs': program_recs,
                   'degree_recs': degree_recs})


def filter_student_report(request):
    if request.POST:
        request.session['form_data'] = request.POST
        university = request.POST.get('university')
        degree = request.POST.get('degree')
        country = request.POST.get('country')
        program = request.POST.get('program')
    else:

        form_data = request.session.get('form_data')

        university = form_data.get('university')
        degree = form_data.get('degree')
        country = form_data.get('country')
        program = form_data.get('program')

    try:
        stud = []
        student_list = StudentDonorMapping.objects.filter(donor__user=request.user,applicant_id__year=get_current_year())
        if country:
            student_list = student_list.filter(student__address__country=country)

        for obj in student_list:
            stud.append(StudentDetails.objects.get(id=obj.student.id))

        application_records = ApplicationDetails.objects.filter(Q(student__in=stud),
                                                                Q(is_sponsored=True),
                                                                filter_degree(degree),
                                                                filter_program(program),
                                                                filter_university(university),year=get_current_year())

        country_recs = CountryDetails.objects.all()
        university_recs = UniversityDetails.objects.all()
        degree_recs = DegreeDetails.objects.all()
        program_recs = ProgramDetails.objects.all()

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/donor/template_student_reports/')

    return render(request, 'template_student_reports.html',
                  {'application_records': application_records, 'country_recs': country_recs,
                   'university_recs': university_recs,'program_recs': program_recs,
                   'degree_recs': degree_recs})


def template_application_progress_history(request):
    applicant_recs = ''
    try:
        if request.user.is_super_admin():
            applicant_recs = ApplicationDetails.objects.filter(is_submitted=True,year=get_current_year())
        else:
            stud = []
            for obj in StudentDonorMapping.objects.filter(donor__user=request.user,applicant_id__year=get_current_year()):
                stud.append(StudentDetails.objects.get(id=obj.student.id))

            applicant_recs = ApplicationDetails.objects.filter(student__in=stud,is_submitted=True,
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
            applicant_recs = ApplicationDetails.objects.filter(is_sponsored=True,year=get_current_year())
            application_history_recs = ApplicationDetails.objects.get(id=application).applicant_history_rel.all()
            application_obj = ApplicationDetails.objects.get(id=application)
        else:
            stud = []
            for obj in StudentDonorMapping.objects.filter(donor__user=request.user,applicant_id__year=get_current_year()):
                stud.append(StudentDetails.objects.get(id=obj.student.id))

            applicant_recs = ApplicationDetails.objects.filter(student__in=stud,
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

    stud = StudentDonorMapping.objects.filter(donor__user=request.user,applicant_id__year=get_current_year()).values("student")
    # student_list = StudentDetails.objects.filter(id__in=stud)
    student_list = ApplicationDetails.objects.filter(student_id__in=stud, is_sponsored=True)

    return render(request, "template_my_payments.html", {'student_list': student_list})


def template_students_receipts(request):

    debit_total = 0
    outstanding_total = 0


    stud = StudentDonorMapping.objects.filter(donor__user=request.user,applicant_id__year=get_current_year()).values("student")
    # student_list = StudentDetails.objects.filter(id__in=stud).distinct()
    student_list = ApplicationDetails.objects.filter(student_id__in=stud, is_sponsored=True).distinct()


    student_list_rec = []

    for application_obj in student_list:

        raw_dict = {}
        raw_dict_one = {}
        approval_amount = 0
        credit_total = 0
        outstanding_amount = 0
        application_list = []
        # for application_obj in obj.student_applicant_rel.all():

        if application_obj.rel_donor_receipt_voucher.all():
            approval_amount = application_obj.scholarship_fee

            raw_dict['application_rec'] = application_obj
            for voucher_obj in application_obj.rel_donor_receipt_voucher.all():

                raw_dict['voucher_rec'] = voucher_obj
                if voucher_obj.voucher_type == "debit":
                    credit_total += float(voucher_obj.voucher_amount)

            outstanding_amount = float(approval_amount) - float(credit_total)

            raw_dict['approval_amount'] = float(approval_amount)
            raw_dict['credit_total'] = float(credit_total)
            raw_dict['outstanding_amount'] = float(outstanding_amount)
            student_list_rec.append(raw_dict)

        debit_total += float(credit_total)
        outstanding_total += float(outstanding_amount)

    return render(request, "template_students_receipts.html", {'voucher_record': student_list_rec, 'debit_total': debit_total, 'outstanding_total': outstanding_total})

@user_login_required
def approve_sponsorship(request):
    application_rec = ApplicationDetails.objects.get(id=request.POST['app_id'])
    application_rec.is_sponsored = True
    application_rec.save()

    donor = DonorDetails.objects.get(user=request.user)

    StudentDonorMapping.objects.create(student=application_rec.student, donor=donor, applicant_id=application_rec)

    return render(request, "template_student_details.html", {'application_obj':application_rec})


def donor_receipt_report_export(request):
    try:
        debit_total = 0
        outstanding_total = 0
        stud = StudentDonorMapping.objects.filter(donor__user=request.user,applicant_id__year=get_current_year()).values("student")
        student_list = ApplicationDetails.objects.filter(student_id__in=stud, is_sponsored=True).distinct()
        rows = []
        for application_obj in student_list:
            rec_list =[]
            credit_total = 0
            outstanding_amount = 0
            rec_list.append(application_obj.student_id)
            rec_list.append(application_obj.get_full_name())
            if application_obj.rel_donor_receipt_voucher.all():
                approval_amount = application_obj.scholarship_fee
                for voucher_obj in application_obj.rel_student_payment_receipt_voucher.all():
                    if voucher_obj.voucher_type == "credit":
                        credit_total += float(voucher_obj.voucher_amount)
                outstanding_amount = float(approval_amount) - float(credit_total)
                rec_list.append(float(approval_amount))
                rec_list.append(float(credit_total))
                rec_list.append(float(outstanding_amount))
                rows.append(rec_list)
            debit_total += float(credit_total)
            outstanding_total += float(outstanding_amount)
        column_names = ["Student id", "Student Name", "Scholorship Fee", "Debit", "Balance",]
        return export_wraped_column_xls('DonorReceiptReport', column_names, rows)
    except:
        return redirect('/donar/template_students_receipts/')


def student_payment_report_export(request):
    try:
        val_dict = request.POST
        student_id = val_dict['student_id']
        rows =[]
        application_rec = ApplicationDetails.objects.filter(student_id=student_id, is_sponsored=True,year=get_current_year())
        voucher_record = DonorReceiptVoucher.objects.filter(application__in=application_rec)
        balance_total = DonorReceiptVoucher.objects.filter(voucher_type="debit",application__in=application_rec).values("voucher_amount").aggregate(total_credit=Sum('voucher_amount'))
        for rec in voucher_record:
            rec_list = []
            if rec.voucher_number!="":
                rec_list.append(rec.voucher_number)
            else:
                rec_list.append("")

            if rec.voucher_description !="":
                rec_list.append(rec.voucher_description)
            else:
                rec_list.append("")

            if rec.voucher_amount!="":
                rec_list.append(rec.voucher_amount)
            else:
                rec_list.append("")

            rows.append(rec_list)
        #rec_len = len(voucher_record)
        #total_balance = balance_total['total_credit']
        column_names = ["NO", "Description", "Debit"]
        return export_wraped_column_xls(' StudentPaymentReport', column_names, rows)
    except:
        return redirect('/donar/template_my_payments/')

def Register_Applicant_export(request):
    try:
        university_recs = UniversityDetails.objects.all()
        stud = []
        rows = []
        for obj in StudentDonorMapping.objects.filter(donor__user=request.user,applicant_id__year=get_current_year()):
            stud_id = StudentDetails.objects.get(id=obj.student.id)
            stud.append(StudentDetails.objects.get(id=obj.student.id))

        application_records = ApplicationDetails.objects.filter(student__in=stud,is_sponsored=True)
        for rec in application_records:
            rec_list  = []
            rec_list.append(rec.get_full_name())
            rec_list.append(rec.nationality)
            if rec.applicant_scholarship_rel.all():
                rec_list.append(rec.applicant_scholarship_rel.all()[0].university.university_name)
            else:
                rec_list.append("")
            if rec.applicant_scholarship_rel.all():
                rec_list.append(rec.applicant_scholarship_rel.all()[0].course_applied.degree_name)
            else:
                rec_list.append("")
            if rec.applicant_module_rel.all():
                rec_list.append(rec.applicant_module_rel.all()[0].program.program_name)
            else:
                rec_list.append("")
            rows.append(rec_list)

        column_names = ["Student Name", "Country", "University ", "Degree", "Program","Semester","GPA","CGPA","Payments"]

        return export_wraped_column_xls('RegisterApplicant', column_names, rows)
    except:
        return redirect('/donar/template_student_reports/')

