from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from student.models import StudentDetails, ApplicationDetails
from masters.models import CountryDetails, ScholarshipDetails, StudentDonorMapping, DegreeDetails, SemesterDetails
from .models import StudentPaymentReceiptVoucher, DonorReceiptVoucher
import json
from common.utils import create_voucher_number
from django.db.models import Sum
from donor.models import DonorDetails
from django.db.models import Q
from common.utils import *
from datetime import datetime
from masters.models import DegreeFormula


# Create your views here.
def get_student_payment_voucher(request):
    # student_list = StudentDetails.objects.filter(student_applicant_rel__is_sponsored=True)

    query_student = request.GET.get('student') or None
    repayment_percent = 0

    myDate = datetime.now()

    # Give a format to the date
    formatedDate = myDate.strftime("%d-%m-%Y")

    student_list = ApplicationDetails.objects.filter(is_sponsored=True, year=get_current_year(request))

    voucher_record = StudentPaymentReceiptVoucher.objects.filter(voucher_type='debit',
                                                                 application__year=get_current_year(request))

    raw_dict = {}
    if query_student:
        application_rec = ApplicationDetails.objects.get(is_sponsored=True, student_id=query_student,
                                                         year=get_current_year(request))

        voucher_ids = voucher_record.filter(application_id=application_rec).values('id')
        voucher_record = voucher_record.filter(id__in=voucher_ids)

        total_amount = StudentPaymentReceiptVoucher.objects.filter(voucher_type="credit",
                                                                   application=application_rec).values(
            "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))

        total_debit_amount = StudentPaymentReceiptVoucher.objects.filter(voucher_type="debit",
                                                                         application=application_rec).values(
            "voucher_amount").aggregate(total_debit=Sum('voucher_amount'))

        raw_dict['total_amount'] = float(total_amount['total_credit']) if total_amount['total_credit'] else 0
        raw_dict['total_debit_amount'] = float(total_debit_amount['total_debit']) if total_debit_amount[
            'total_debit'] else 0
        raw_dict['application_rec'] = application_rec.to_student_payment_application_dict()
        raw_dict['voucher_rec'] = [obj.to_dict() for obj in voucher_record]

    return render(request, "template_student_payment_voucher.html",
                  {'student_list': student_list, 'voucher_record': voucher_record, 'formatedDate': formatedDate,
                   'raw_dict': raw_dict})


def get_student_receipt_voucher(request):
    query_student = request.GET.get('student') or None

    # student_list = StudentDetails.objects.filter(student_applicant_rel__is_sponsored=True)
    student_list = ApplicationDetails.objects.filter(is_sponsored=True, year=get_current_year(request))
    voucher_record = StudentPaymentReceiptVoucher.objects.filter(voucher_type='credit',
                                                                 application__year=get_current_year(request))

    raw_dict = {}
    if query_student:
        application_rec = ApplicationDetails.objects.get(is_sponsored=True, student_id=query_student,
                                                         year=get_current_year(request))

        voucher_ids = voucher_record.filter(application_id=application_rec).values('id')
        voucher_record = voucher_record.filter(id__in=voucher_ids)

        balance_total = StudentPaymentReceiptVoucher.objects.filter(voucher_type="credit",
                                                                    application=application_rec).values(
            "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))
        raw_dict['application_rec'] = application_rec.to_application_dict()
        raw_dict['outstanding_amount'] = (
                float(application_rec.scholarship_fee) - float(balance_total['total_credit'])) if \
            balance_total['total_credit'] else 0
        raw_dict['voucher_rec'] = [obj.to_dict() for obj in voucher_record]

    return render(request, "template_student_receipt_voucher.html",
                  {'student_list': student_list, 'voucher_record': voucher_record, 'raw_dict': raw_dict})


def get_student_payment_and_receipt_report(request):
    query_student = request.GET.get('student')
    raw_dict = {}
    if query_student:
        application_rec = ApplicationDetails.objects.get(student_id=query_student)
        voucher_record = StudentPaymentReceiptVoucher.objects.filter(application_id=application_rec.id,application__year=get_current_year(request))
        total_amount = StudentPaymentReceiptVoucher.objects.filter(voucher_type="credit", application=application_rec,application__year=get_current_year(request)).values("voucher_amount").aggregate(total_credit=Sum('voucher_amount'))
        total_debit_amount = StudentPaymentReceiptVoucher.objects.filter(voucher_type="debit",application=application_rec).values("voucher_amount").aggregate(total_debit=Sum('voucher_amount'))
        raw_dict['total_amount'] = float(total_amount['total_credit']) if total_amount['total_credit'] else 0
        raw_dict['total_debit_amount'] = float(total_debit_amount['total_debit']) if total_debit_amount['total_debit'] else 0
        raw_dict['application_rec'] = application_rec.to_student_payment_application_dict()
        raw_dict['voucher_rec'] = [obj.to_dict() for obj in voucher_record]

    # student_list = StudentDetails.objects.filter(student_applicant_rel__is_sponsored=True)
    student_list = ApplicationDetails.objects.filter(is_sponsored=True, year=get_current_year(request))
    return render(request, "template_student_payment_and_receipt_report.html", {'student_list': student_list,'raw_dict':raw_dict})


def get_student_report(request):
    query_country = request.GET.get("country") or None
    query_scholarship = request.GET.get("scholarship") or None
    query_voucher_beneficiary = request.GET.get("voucher_beneficiary") or None

    query_degree = request.GET.get("degree") or None
    query_semester = request.GET.get("semester") or None

    credit_total = 0
    balance_total = 0
    debit_total = 0
    voucher_rec_list = []

    stud_pay_voucher_list = StudentPaymentReceiptVoucher.objects.filter(application__year=get_current_year(request))

    if query_country:
        stud_pay_voucher_list = stud_pay_voucher_list.filter(application__address__country_id=query_country)
    if query_scholarship:
        stud_pay_voucher_list = stud_pay_voucher_list.filter(
            application__applicant_scholarship_rel__scholarship_id=query_scholarship)
    if query_voucher_beneficiary:
        stud_pay_voucher_list = stud_pay_voucher_list.filter(voucher_beneficiary=query_voucher_beneficiary)

    if query_degree:
        stud_pay_voucher_list = stud_pay_voucher_list.filter(
            application__applicant_scholarship_rel__degree_id=query_degree)

    if query_semester:
        ids_list = stud_pay_voucher_list.filter(application__applicant_progress_rel__semester_id=query_semester).values(
            "id").distinct()
        stud_pay_voucher_list = stud_pay_voucher_list.filter(id__in=ids_list)

    voucher_record = {}
    all_country_obj = type('', (object,), {"id": "", "country_name": "All"})()
    country = [all_country_obj]
    for co in CountryDetails.objects.all():
        country.append(co)

    all_scholarship_obj = type('', (object,), {"id": "", "scholarship_name": "All"})()
    scholarship = [all_scholarship_obj]
    for scho in ScholarshipDetails.objects.all():
        scholarship.append(scho)

    all_degree_obj = type('', (object,), {"id": "", "degree_name": "All"})()
    degree = [all_degree_obj]
    for scho in DegreeDetails.objects.all():
        degree.append(scho)

    all_semester_obj = type('', (object,), {"id": "", "semester_name": "All"})()
    semester = [all_semester_obj]
    for scho in SemesterDetails.objects.all():
        semester.append(scho)

    for obj in stud_pay_voucher_list:
        if obj.voucher_type == "debit":
            debit_total += float(obj.voucher_amount)

        if obj.voucher_type == "credit":
            credit_total += float(obj.voucher_amount)

        voucher_rec_list.append(obj)

    balance_total = StudentPaymentReceiptVoucher.objects.filter(application__year=get_current_year(request)).values(
        "application__scholarship_fee").distinct().aggregate(
        total_price=Sum('application__scholarship_fee'))

    if balance_total['total_price'] and stud_pay_voucher_list:
        voucher_record['debit_total'] = debit_total
        voucher_record['credit_total'] = credit_total
        # voucher_record['balance_total'] = (float(balance_total['total_price']) - debit_total)
        voucher_record['balance_total'] = (float(debit_total) - float(credit_total))
        voucher_record['voucher_record'] = voucher_rec_list

    return render(request, "template_student_report.html",
                  {'voucher_record': voucher_record, 'country_list': country, 'scholarship_list': scholarship,
                   'degree_list': degree, 'semester_list': semester,
                   'selected_country': CountryDetails.objects.filter(id=query_country),
                   'selected_degree': DegreeDetails.objects.filter(id=query_degree),
                   'selected_semester': SemesterDetails.objects.filter(id=query_semester),
                   'selected_scholarship': ScholarshipDetails.objects.filter(id=query_scholarship)})


def get_filtered_student_report(request):
    val_dict = request.POST

    country = val_dict['country']
    beneficiary = val_dict['beneficiary']
    scholarship_type = val_dict['scholarship_type']

    voucher_record = {}
    debit_total = 0
    credit_total = 0
    balance_total = 0
    voucher_rec_list = []
    for obj in StudentPaymentReceiptVoucher.objects.filter(application__address__country__country_name=country,
                                                           voucher_beneficiary=beneficiary,
                                                           application__year=get_current_year(request),
                                                           application__scholarship_selection_rel__scholarship__scholarship_name=scholarship_type):
        if obj.voucher_type == "debit":
            debit_total += float(obj.voucher_amount)

        if obj.voucher_type == "credit":
            credit_total += float(obj.voucher_amount)

        voucher_rec_list.append(obj)

    balance_total = StudentPaymentReceiptVoucher.objects.filter(application__year=get_current_year(request)).values(
        "application__scholarship_fee").distinct().aggregate(
        total_price=Sum('application__scholarship_fee'))

    voucher_record['debit_total'] = debit_total
    voucher_record['credit_total'] = credit_total
    voucher_record['balance_total'] = float(balance_total['total_price']) - credit_total
    voucher_record['voucher_record'] = voucher_rec_list

    return render(request, "template_student_report.html", {'voucher_record': voucher_record})


def get_approval_and_paid_total(request):
    debit_total = 0
    outstanding_total = 0

    query_country = request.GET.get("country") or None
    query_scholarship = request.GET.get("scholarship") or None
    query_student = request.GET.get("student") or None

    all_country_obj = type('', (object,), {"id": "", "country_name": "All"})()
    country = [all_country_obj]
    for co in CountryDetails.objects.all():
        country.append(co)

    all_scholarship_obj = type('', (object,), {"id": "", "scholarship_name": "All"})()
    scholarship = [all_scholarship_obj]
    for scho in ScholarshipDetails.objects.all():
        scholarship.append(scho)

    all_student_obj = type('', (object,), {"id": "", "get_full_name": "All"})()
    students = [all_student_obj]
    for stud in ApplicationDetails.objects.filter(is_sponsored=True, year=get_current_year(request)):
        students.append(stud)

    student_list = StudentDetails.objects.all().distinct()

    if query_student:
        student_list = student_list.filter(id=query_student)

    if query_scholarship:
        student_list = student_list.filter(
            student_applicant_rel__applicant_scholarship_rel__scholarship_id=query_scholarship)

    if query_country:
        student_list = student_list.filter(address__country_id=query_country)

    student_list_rec = []

    for obj in student_list:

        raw_dict = {}
        raw_dict_one = {}
        approval_amount = 0
        credit_total = 0
        outstanding_amount = 0
        application_list = []
        for application_obj in obj.student_applicant_rel.filter(is_sponsored=True):
            if application_obj.rel_student_payment_receipt_voucher.all():
                approval_amount = application_obj.scholarship_fee

                raw_dict['application_list'] = application_obj
                for voucher_obj in application_obj.rel_student_payment_receipt_voucher.all():

                    raw_dict['voucher_list'] = voucher_obj
                    if voucher_obj.voucher_type == "debit":
                        credit_total += float(voucher_obj.voucher_amount)

                outstanding_amount = float(approval_amount) - float(credit_total)

                raw_dict['approval_amount'] = float(approval_amount)
                raw_dict['credit_total'] = float(credit_total)
                raw_dict['outstanding_amount'] = float(outstanding_amount)
                student_list_rec.append(raw_dict)

        debit_total += float(credit_total)
        outstanding_total += float(outstanding_amount)

    return render(request, "template_approval_and_paid_total.html",
                  {'voucher_record': student_list_rec, 'debit_total': debit_total,
                   'outstanding_total': outstanding_total, 'country_list': country, 'scholarship_list': scholarship,
                   'selected_country': CountryDetails.objects.filter(id=query_country),
                   'selected_scholarship': ScholarshipDetails.objects.filter(id=query_scholarship),
                   'student_list': students,
                   'selected_student': ApplicationDetails.objects.filter(student_id=query_student)})


def get_donor_receipt_voucher(request):
    donor_list = DonorDetails.objects.all()

    query_student = request.GET.get('student')
    donor = request.GET.get('donor')
    student_list = []

    if donor:
        student_list = StudentDonorMapping.objects.filter(donor_id=donor,
                                                          student__student_applicant_rel__is_sponsored=True)

    raw_dict = {}
    if query_student:
        application_rec = ApplicationDetails.objects.get(student_id=query_student)
        voucher_record = DonorReceiptVoucher.objects.filter(application_id=application_rec.id)
        total_amount = DonorReceiptVoucher.objects.filter(voucher_type="debit", application=application_rec).values(
            "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))

        balance_total = DonorReceiptVoucher.objects.filter(voucher_type="debit", application=application_rec).values(
            "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))
        raw_dict['application_rec'] = application_rec.to_application_dict() if application_rec else ''
        raw_dict['outstanding_amount'] = (float(application_rec.scholarship_fee) - float(
            balance_total['total_credit'])) if application_rec.scholarship_fee and balance_total['total_credit'] else 0
        raw_dict['total_amount'] = float(total_amount['total_credit']) if total_amount['total_credit'] else 0
        raw_dict['voucher_rec'] = [obj.to_dict() for obj in voucher_record] if voucher_record else ''

    return render(request, "template_donor_receipt_voucher.html",
                  {'donor_list': donor_list, 'raw_dict': raw_dict, 'student_list': student_list})


from django.forms.models import model_to_dict


def get_donors_student_list(request):
    student_list = StudentDonorMapping.objects.filter(donor=request.POST['donor'],
                                                      student__student_applicant_rel__is_sponsored=True)

    return HttpResponse(json.dumps([obj.to_dict() for obj in student_list]), content_type='application/json')


def get_donor_report(request):
    donor_list = DonorDetails.objects.all()

    debit_total = 0
    outstanding_total = 0
    query_donor = request.GET.get('donor') or None
    student_main_list = []

    if query_donor:

        selected_donor = DonorDetails.objects.get(id=query_donor)
        student_ids = StudentDonorMapping.objects.filter(donor_id=query_donor).values('student')

        student_list = StudentDetails.objects.filter(id__in=student_ids).distinct()
        student_list_rec = []

        raw_dict_one = {}

        for obj in student_list:

            raw_dict = {}

            approval_amount = 0
            credit_total = 0
            outstanding_amount = 0
            application_list = []
            for application_obj in obj.student_applicant_rel.filter(is_sponsored=True):
                approval_amount = application_obj.scholarship_fee

                for voucher_obj in application_obj.rel_donor_receipt_voucher.all():

                    raw_dict['voucher_rec'] = voucher_obj.to_dict_short()
                    if voucher_obj.voucher_type == "debit":
                        credit_total += float(voucher_obj.voucher_amount)

                outstanding_amount = float(approval_amount) - float(credit_total)

                if application_obj.rel_donor_receipt_voucher.all():
                    raw_dict['approval_amount'] = float(approval_amount) if approval_amount else 0
                    raw_dict['credit_total'] = float(credit_total) if credit_total else 0
                    raw_dict['outstanding_amount'] = float(outstanding_amount) if outstanding_amount else 0
                    student_list_rec.append(raw_dict)

            debit_total += float(credit_total) if credit_total else 0
            outstanding_total += float(outstanding_amount) if outstanding_amount else 0

        raw_dict = {}
        raw_dict['voucher_records'] = student_list_rec
        raw_dict['total_credit_amount'] = debit_total
        raw_dict['total_outstanding_amount'] = outstanding_total
        raw_dict['selected_donor'] = selected_donor

        student_main_list.append(raw_dict)

    return render(request, "template_donor_report.html",
                  {'donor_list': donor_list, 'student_main_list': student_main_list})


def get_voucher_data_by_donor(request):
    debit_total = 0
    outstanding_total = 0

    student_ids = StudentDonorMapping.objects.filter(donor_id=request.POST['donor']).values('student')

    student_list = StudentDetails.objects.filter(id__in=student_ids).distinct()
    student_list_rec = []

    raw_dict_one = {}
    student_main_list = []
    for obj in student_list:

        raw_dict = {}

        approval_amount = 0
        credit_total = 0
        outstanding_amount = 0
        application_list = []
        for application_obj in obj.student_applicant_rel.filter(is_sponsored=True):
            approval_amount = application_obj.scholarship_fee

            for voucher_obj in application_obj.rel_donor_receipt_voucher.all():

                raw_dict['voucher_rec'] = voucher_obj.to_dict_short()
                if voucher_obj.voucher_type == "debit":
                    credit_total += float(voucher_obj.voucher_amount)

            outstanding_amount = float(approval_amount) - float(credit_total)

            if application_obj.rel_donor_receipt_voucher.all():
                raw_dict['approval_amount'] = float(approval_amount) if approval_amount else 0
                raw_dict['credit_total'] = float(credit_total) if credit_total else 0
                raw_dict['outstanding_amount'] = float(outstanding_amount) if outstanding_amount else 0
                student_list_rec.append(raw_dict)

        debit_total += float(credit_total) if credit_total else 0
        outstanding_total += float(outstanding_amount) if outstanding_amount else 0

    raw_dict = {}
    raw_dict['voucher_records'] = student_list_rec
    raw_dict['total_credit_amount'] = debit_total
    raw_dict['total_outstanding_amount'] = outstanding_total

    student_main_list.append(raw_dict)

    return HttpResponse(json.dumps(raw_dict), content_type='application/json')


def get_payment_voucher_data_by_student(request):
    application_rec = ApplicationDetails.objects.get(student_id=request.POST['student'])
    voucher_record = StudentPaymentReceiptVoucher.objects.filter(application_id=application_rec.id,
                                                                 application__year=get_current_year(request))
    total_amount = StudentPaymentReceiptVoucher.objects.filter(voucher_type="credit",
                                                               application=application_rec,
                                                               application__year=get_current_year(request)).values(
        "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))

    total_debit_amount = StudentPaymentReceiptVoucher.objects.filter(voucher_type="debit",
                                                                     application=application_rec).values(
        "voucher_amount").aggregate(total_debit=Sum('voucher_amount'))

    raw_dict = {}
    raw_dict['total_amount'] = float(total_amount['total_credit']) if total_amount['total_credit'] else 0
    raw_dict['total_debit_amount'] = float(total_debit_amount['total_debit']) if total_debit_amount[
        'total_debit'] else 0
    raw_dict['application_rec'] = application_rec.to_student_payment_application_dict()
    raw_dict['voucher_rec'] = [obj.to_dict() for obj in voucher_record]

    return HttpResponse(json.dumps(raw_dict), content_type='application/json')


def get_receipt_voucher_data_by_student(request):
    application_rec = ApplicationDetails.objects.get(student_id=request.POST['student'])
    voucher_record = StudentPaymentReceiptVoucher.objects.filter(application_id=application_rec.id)

    raw_dict = {}
    balance_total = StudentPaymentReceiptVoucher.objects.filter(voucher_type="credit",
                                                                application=application_rec).values(
        "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))
    raw_dict['application_rec'] = application_rec.to_application_dict()
    raw_dict['outstanding_amount'] = (float(application_rec.scholarship_fee) - float(balance_total['total_credit'])) if \
        balance_total['total_credit'] else 0
    raw_dict['voucher_rec'] = [obj.to_dict() for obj in voucher_record]
    return HttpResponse(json.dumps(raw_dict), content_type='application/json')


def save_payment_voucher_data_by_student(request):
    if request.method == 'POST':
        val_dict = request.POST
        voucher = StudentPaymentReceiptVoucher.get_instance(val_dict, None)
        voucher.voucher_type = "debit"
        voucher.save()
        voucher_number = create_voucher_number("SPV", voucher)
        voucher.voucher_number = voucher_number
        voucher.voucher_total = voucher.application.calculate_student_payment_balance_amount()
        voucher.save()

        if str(request.POST['btn_type']) == 'save_and_send':
            params = {
                'voucher_type': 'Student Payment Voucher Report',
                'voucher': voucher,
                'request': request
            }
            # return render_to_pdf('report_voucher.html', params)
            if voucher.application.email:
                subject, from_email, to = 'Student Payment Voucher', settings.EMAIL_HOST_USER, voucher.application.email
                text_content = 'Please Find Attachment'

                file = render_to_file('report_voucher.html', params)
                thread = Thread(target=send_email, args=(file, subject, text_content, from_email, to))
                thread.start()

        if str(request.POST['btn_type']) == 'save_and_print':
            params = {
                'voucher_type': 'Student Payment Voucher Report',
                'voucher': voucher,
                'request': request
            }
            return render_to_pdf('report_voucher.html', params)

    return redirect("/accounting/get_student_payment_voucher/")


def update_student_payment_voucher(request):
    if request.method == "POST":
        val_dict = request.POST
        try:
            voucher = StudentPaymentReceiptVoucher.objects.get(id=val_dict['voucher_id'])
            voucher.voucher_amount = float(val_dict['voucher_amount'])
            voucher.save()
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')
        return HttpResponse(json.dumps({'success': "Record updated successfully."}), content_type='application/json')


def delete_student_payment_voucher(request):
    if request.method == "POST":
        val_dict = request.POST
        try:
            StudentPaymentReceiptVoucher.objects.get(id=val_dict['voucher_id']).delete()
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')

        return HttpResponse(json.dumps({'success': "Record deleted successfully."}), content_type='application/json')


def save_student_receipt_voucher(request):
    if request.method == 'POST':
        val_dict = request.POST
        receipt_voucher = StudentPaymentReceiptVoucher.get_instance(val_dict, None)
        receipt_voucher.voucher_type = "credit"
        # receipt_voucher = StudentReceiptVoucher.get_instance(val_dict, val_dict["receipt_voucher_number"])
        receipt_voucher.save()
        voucher_number = create_voucher_number("SRV", receipt_voucher)
        receipt_voucher.voucher_number = voucher_number
        receipt_voucher.voucher_total = receipt_voucher.application.calculate_balance_amount()
        receipt_voucher.save()

        if str(request.POST['btn_type']) == 'save_and_send':
            params = {
                'voucher_type': 'Student Receipt Voucher Report',
                'voucher': receipt_voucher,
                'request': request
            }
            # return render_to_pdf('report_voucher.html', params)

            if receipt_voucher.application.email:
                subject, from_email, to = 'Student Receipt Voucher', settings.EMAIL_HOST_USER, receipt_voucher.application.email
                text_content = 'Please Find Attachment'

                file = render_to_file('report_voucher.html', params)
                thread = Thread(target=send_email, args=(file, subject, text_content, from_email, to))
                thread.start()

        if str(request.POST['btn_type']) == 'save_and_print':
            params = {
                'voucher_type': 'Student Receipt Voucher Report',
                'voucher': receipt_voucher,
                'request': request
            }
            return render_to_pdf('report_voucher.html', params)

        return redirect("/accounting/get_student_receipt_voucher/")


def get_donor_recipt_for_org_payment(request):
    application_rec = ApplicationDetails.objects.get(student_id=request.POST['student'])
    voucher_record = DonorReceiptVoucher.objects.filter(application_id=application_rec.id)
    total_amount = DonorReceiptVoucher.objects.filter(voucher_type="debit", application=application_rec).values(
        "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))

    raw_dict = {}
    balance_total = DonorReceiptVoucher.objects.filter(voucher_type="debit", application=application_rec).values(
        "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))
    raw_dict['application_rec'] = application_rec.to_application_dict() if application_rec else ''
    raw_dict['outstanding_amount'] = (float(application_rec.scholarship_fee) - float(
        balance_total['total_credit'])) if application_rec.scholarship_fee and balance_total['total_credit'] else 0
    raw_dict['total_amount'] = float(total_amount['total_credit']) if total_amount['total_credit'] else 0
    raw_dict['voucher_rec'] = [obj.to_dict() for obj in voucher_record] if voucher_record else ''

    return HttpResponse(json.dumps(raw_dict), content_type='application/json')


def save_donor_recipt_for_org_payment(request):
    if request.method == 'POST':
        val_dict = request.POST
        donor_voucher = DonorReceiptVoucher.get_instance(val_dict, None)
        donor_voucher.voucher_type = "debit"
        donor_voucher.donor_student = StudentDonorMapping.objects.get(student_id=val_dict['student'],
                                                                      donor_id=val_dict['donor'])
        donor_voucher.save()
        voucher_number = create_voucher_number("DRV", donor_voucher)
        donor_voucher.voucher_number = voucher_number
        donor_voucher.voucher_total = donor_voucher.application.calculate_student_payment_balance_amount()
        donor_voucher.save()

        if str(request.POST['btn_type']) == 'save_and_send':
            params = {
                'voucher_type': 'Donor Receipt Voucher Report',
                'voucher': donor_voucher,
                'request': request
            }
            # return render_to_pdf('report_voucher.html', params)

            if donor_voucher.donor_student.donor.email:
                subject, from_email, to = 'Donor Receipt Voucher', settings.EMAIL_HOST_USER, donor_voucher.donor_student.donor.email
                text_content = 'Please Find Attachment'

                file = render_to_file('report_voucher.html', params)
                thread = Thread(target=send_email, args=(file, subject, text_content, from_email, to))
                thread.start()

        if str(request.POST['btn_type']) == 'save_and_print':
            params = {
                'voucher_type': 'Donor Receipt Voucher Report',
                'voucher': donor_voucher,
                'request': request
            }
            return render_to_pdf('report_voucher.html', params)

        return redirect("/accounting/get_donor_receipt_voucher/")


def export_student_recipt_voucher(request):
    try:
        val_dict = request.POST
        student_id = val_dict['student_id']
        application_rec = ApplicationDetails.objects.filter(student_id=student_id, is_sponsored=True,
                                                            year=get_current_year(request))
        voucher_record = StudentPaymentReceiptVoucher.objects.filter(application__in=application_rec)
        balance_total = StudentPaymentReceiptVoucher.objects.filter(voucher_type="credit",
                                                                    application__in=application_rec).values(
            "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))
        rows = []
        count = 0
        for app_rec in application_rec:
            for rec in app_rec.rel_student_payment_receipt_voucher.all():
                rec_list = []
                if app_rec.rel_student_payment_receipt_voucher.all()[count].voucher_type == "credit":
                    if app_rec.rel_student_payment_receipt_voucher.all():
                        rec_list.append(app_rec.rel_student_payment_receipt_voucher.all()[count].voucher_number)
                    else:
                        rec_list.append("")

                    if rec.voucher_date:
                        rec_list.append(rec.voucher_date)
                    else:
                        rec_list.append("")

                    rec_list.append(app_rec.get_full_name())

                    if app_rec.applicant_progress_rel.all():
                        rec_list.append(app_rec.applicant_progress_rel.all()[0].semester.semester_name)
                    else:
                        rec_list.append("")

                    rec_list.append(app_rec.address.country.country_name)

                    if app_rec.applicant_scholarship_rel.all():
                        rec_list.append(app_rec.applicant_scholarship_rel.all()[0].university.university_name)
                    else:
                        rec_list.append("")

                    if app_rec.applicant_scholarship_rel.all():
                        rec_list.append(app_rec.applicant_scholarship_rel.all()[0].scholarship.scholarship_name)
                    else:
                        rec_list.append("")

                    if app_rec.applicant_scholarship_rel.all():
                        rec_list.append(app_rec.applicant_scholarship_rel.all()[0].course_applied.program_name)

                    else:
                        rec_list.append("")

                    if app_rec.student.student_donor_rel.all():
                        rec_list.append(app_rec.student.student_donor_rel.all()[0].donor.user.get_full_name())
                    else:
                        rec_list.append("")

                    if app_rec.rel_student_payment_receipt_voucher.all():
                        rec_list.append(app_rec.rel_student_payment_receipt_voucher.all()[count].voucher_amount)

                    count = count + 1
                    rows.append(rec_list)
                else:
                    count = count + 1
                    pass
        column_names = ["No", "Voucher Date", "Student Name", "Semester", "Country", "University", "Scholarship",
                        "Program", "Donor", "Amount"]
        return export_wraped_column_xls('StudentReceiptVoucher', column_names, rows)
    except:
        return redirect("/accounting/get_student_receipt_voucher/")


def export_student_payment_voucher(request):
    try:
        val_dict = request.POST
        student_id = val_dict['student_id']
        application_rec = ApplicationDetails.objects.filter(student_id=student_id, is_sponsored=True,
                                                            year=get_current_year(request))
        voucher_record = StudentPaymentReceiptVoucher.objects.filter(application__in=application_rec)
        balance_total = StudentPaymentReceiptVoucher.objects.filter(voucher_type="debit",
                                                                    application__in=application_rec).values(
            "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))

        rows = []
        count = 0
        for app_rec in application_rec:
            for rec in app_rec.rel_student_payment_receipt_voucher.all():
                rec_list = []
                if app_rec.rel_student_payment_receipt_voucher.all()[count].voucher_type == "debit":
                    if app_rec.rel_student_payment_receipt_voucher.all():
                        rec_list.append(app_rec.rel_student_payment_receipt_voucher.all()[count].voucher_number)
                    else:
                        rec_list.append("")
                    if rec.voucher_date:
                        rec_list.append(rec.voucher_date)
                    else:
                        rec_list.append("")

                    rec_list.append(app_rec.get_full_name())
                    if app_rec.applicant_progress_rel.all():
                        rec_list.append(app_rec.applicant_progress_rel.all()[0].semester.semester_name)
                    else:
                        rec_list.append("")

                    rec_list.append(app_rec.address.country.country_name)

                    if app_rec.applicant_scholarship_rel.all():
                        rec_list.append(app_rec.applicant_scholarship_rel.all()[0].university.university_name)
                    else:
                        rec_list.append("")

                    if app_rec.applicant_scholarship_rel.all():
                        rec_list.append(app_rec.applicant_scholarship_rel.all()[0].scholarship.scholarship_name)
                    else:
                        rec_list.append("")

                    if app_rec.applicant_scholarship_rel.all():
                        rec_list.append(app_rec.applicant_scholarship_rel.all()[0].course_applied.program_name)

                    else:
                        rec_list.append("")

                    if app_rec.student.student_donor_rel.all():
                        rec_list.append(app_rec.student.student_donor_rel.all()[0].donor.user.get_full_name())
                    else:
                        rec_list.append("")

                    if app_rec.rel_student_payment_receipt_voucher.all():
                        rec_list.append(app_rec.rel_student_payment_receipt_voucher.all()[count].voucher_amount)

                    count = count + 1
                    rows.append(rec_list)
                else:
                    count = count + 1
                    pass
        column_names = ["No", "Voucher Date", "Student Name", "Semester", "Country", "University", "Scholarship",
                        "Program", "Donor", "Amount"]
        return export_wraped_column_xls('StudentPaymentVoucher', column_names, rows)
    except:
        return redirect("/accounting/get_student_payment_voucher/")


def export_donor_receipt_report(request):
    try:
        debit_total = 0
        outstanding_total = 0
        val_dict = request.POST
        donar_id = val_dict['donar_id']
        student_ids = StudentDonorMapping.objects.filter(donor_id=donar_id).values('student')
        student_list = StudentDetails.objects.filter(id__in=student_ids).distinct()
        rows = []
        for obj in student_list:
            rec_list = []
            approval_amount = 0
            credit_total = 0
            outstanding_amount = 0

            for application_obj in obj.student_applicant_rel.filter(is_sponsored=True):

                approval_amount = application_obj.scholarship_fee

                for voucher_obj in application_obj.rel_donor_receipt_voucher.all():
                    # if voucher_obj!="":
                    #   rec_list.append(voucher_obj.voucher_number)

                    if voucher_obj.voucher_type == "debit":
                        credit_total += float(voucher_obj.voucher_amount)

                outstanding_amount = float(approval_amount) - float(credit_total)

                if application_obj.rel_donor_receipt_voucher.all():
                    rec_list.append(voucher_obj.voucher_number)
                    rec_list.append(voucher_obj.application.get_full_name())
                    if voucher_obj.application.applicant_progress_rel.all():
                        rec_list.append(voucher_obj.application.applicant_progress_rel.all()[0].semester.semester_name)
                    else:
                        rec_list.append("")

                    if application_obj != "":
                        rec_list.append(application_obj.scholarship_fee)

                    rec_list.append(float(credit_total))

                    rec_list.append(float(outstanding_amount))

                    rows.append(rec_list)

        column_names = ["No", "Student Name", "Semester", "Scholorship Fee", "Credit", "Outstanding", ]
        return export_wraped_column_xls('DonorReceiptReport', column_names, rows)
    except:
        return redirect("/accounting/get_donor_report/")


# def export_student_recipt_voucher(request):
#         val_dict = request.POST
#         student_id = val_dict['student_id']
#         application_rec = ApplicationDetails.objects.filter(student_id=student_id, is_sponsored=True)
#         voucher_record = StudentPaymentReceiptVoucher.objects.filter(application__in=application_rec)
#         balance_total = StudentPaymentReceiptVoucher.objects.filter(voucher_type="credit",application__in=application_rec).values("voucher_amount").aggregate(total_credit=Sum('voucher_amount'))
#         rows = []
#         count =0
#         for app_rec in application_rec:
#            for rec in app_rec.rel_student_payment_receipt_voucher.all():
#                 rec_list = []
#                 if app_rec.rel_student_payment_receipt_voucher.all()[count].voucher_type=="credit":
#                     if app_rec.rel_student_payment_receipt_voucher.all():
#                         rec_list.append(app_rec.rel_student_payment_receipt_voucher.all()[count].voucher_number)
#                     else:
#                         rec_list.append("")
#                     rec_list.append(app_rec.get_full_name())
#                     rec_list.append(app_rec.address.country.country_name)
#
#                     if app_rec.applicant_scholarship_rel.all() != '':
#                         rec_list.append(app_rec.applicant_scholarship_rel.all()[0].university.university_name)
#                     else:
#                         rec_list.append("")
#
#                     if app_rec.applicant_scholarship_rel.all():
#                         rec_list.append(app_rec.applicant_scholarship_rel.all()[0].scholarship.scholarship_name)
#                     else:
#                         rec_list.append("")
#
#                     if app_rec.applicant_module_rel.all():
#                         rec_list.append(app_rec.applicant_module_rel.all()[0].program.program_name)
#
#                     else:
#                         rec_list.append("")
#
#                     if app_rec.student.student_donor_rel.all():
#                         rec_list.append(app_rec.student.student_donor_rel.all()[0].donor.user.get_full_name())
#                     else:
#                         rec_list.append("")
#
#                     if app_rec.rel_student_payment_receipt_voucher.all():
#                         rec_list.append(app_rec.rel_student_payment_receipt_voucher.all()[count].voucher_amount)
#
#                     count = count + 1
#                     rows.append(rec_list)
#                 else:
#                      count = count + 1
#                      pass
#         column_names = ["No", "Student Name", "Country", "University", "Scholarship", "Program", "Donor", "Amount"]
#         return export_wraped_column_xls('StudentReceiptVoucher', column_names, rows)
#

# def export_student_payment_voucher(request):
#     val_dict = request.POST
#     student_id = val_dict['student_id']
#     application_rec = ApplicationDetails.objects.filter(student_id=student_id, is_sponsored=True)
#     voucher_record = StudentPaymentReceiptVoucher.objects.filter(application__in=application_rec)
#     balance_total = StudentPaymentReceiptVoucher.objects.filter(voucher_type="debit",application__in=application_rec).values("voucher_amount").aggregate(total_credit=Sum('voucher_amount'))
#
#     rows = []
#     count = 0
#     for app_rec in application_rec:
#         for rec in app_rec.rel_student_payment_receipt_voucher.all():
#             rec_list = []
#             if app_rec.rel_student_payment_receipt_voucher.all()[count].voucher_type == "debit":
#                 if app_rec.rel_student_payment_receipt_voucher.all():
#                     rec_list.append(app_rec.rel_student_payment_receipt_voucher.all()[count].voucher_number)
#                 else:
#                     rec_list.append("")
#                 rec_list.append(app_rec.get_full_name())
#                 rec_list.append(app_rec.address.country.country_name)
#
#                 if app_rec.applicant_scholarship_rel.all() != '':
#                     rec_list.append(app_rec.applicant_scholarship_rel.all()[0].university.university_name)
#                 else:
#                     rec_list.append("")
#
#                 if app_rec.applicant_scholarship_rel.all():
#                     rec_list.append(app_rec.applicant_scholarship_rel.all()[0].scholarship.scholarship_name)
#                 else:
#                     rec_list.append("")
#
#                 if app_rec.applicant_module_rel.all():
#                     rec_list.append(app_rec.applicant_module_rel.all()[0].program.program_name)
#
#                 else:
#                     rec_list.append("")
#
#                 if app_rec.student.student_donor_rel.all():
#                     rec_list.append(app_rec.student.student_donor_rel.all()[0].donor.user.get_full_name())
#                 else:
#                     rec_list.append("")
#
#                 if app_rec.rel_student_payment_receipt_voucher.all():
#                     rec_list.append(app_rec.rel_student_payment_receipt_voucher.all()[count].voucher_amount)
#
#                 count = count + 1
#                 rows.append(rec_list)
#             else:
#                 count = count + 1
#                 pass
#     column_names = ["No", "Student Name", "Country", "University", "Scholarship", "Program", "Donor", "Amount"]
#     return export_wraped_column_xls('StudentReceiptVoucher', column_names, rows)

# def export_donor_receipt_report(request):
#     val_dict = request.POST
#     donar_id = val_dict['donar_id']
#     student_ids = StudentDonorMapping.objects.filter(donor_id=donar_id).values('student')
#     student_list = StudentDetails.objects.filter(id__in=student_ids).distinct()
#     rows = []
#     for obj in student_list:
#         rec_list = []
#         approval_amount = 0
#         credit_total = 0
#         outstanding_amount = 0
#         for application_obj in obj.student_applicant_rel.filter(is_sponsored=True):
#             approval_amount = application_obj.scholarship_fee
#             for voucher_obj in application_obj.rel_donor_receipt_voucher.all():
#                 if voucher_obj!="":
#                     rec_list.append(voucher_obj.voucher_number)
#                 if voucher_obj.voucher_type == "debit":
#                     credit_total += float(voucher_obj.voucher_amount)
#             outstanding_amount = float(approval_amount) - float(credit_total)
#             if application_obj.rel_donor_receipt_voucher.all():
#                 rec_list.append(obj.student_full_name)
#                 if application_obj!="":
#                     rec_list.append(application_obj.scholarship_fee)
#                 rec_list.append(float(credit_total))
#                 rec_list.append(float(outstanding_amount))
#                 rows.append(rec_list)
#
#     column_names = ["No", "Student Name", "Scholorship Fee", "Credit", "Outstanding",]
#     return export_wraped_column_xls('DonorReceiptReport', column_names, rows)

def export_student_receipt_payment_report(request):
    try:
        val_dict = request.POST
        debit_total = 0
        outstanding_total = 0
        query_country = val_dict['query_country']
        query_scholarship = val_dict['query_scholarship']
        query_student = val_dict['query_student']

        # query_country = request.GET.get("country") or None
        # query_scholarship = request.GET.get("scholarship") or None
        # query_student = request.GET.get("student") or None

        all_country_obj = type('', (object,), {"id": "", "country_name": "All"})()
        country = [all_country_obj]
        for co in CountryDetails.objects.all():
            country.append(co)

        all_scholarship_obj = type('', (object,), {"id": "", "scholarship_name": "All"})()
        scholarship = [all_scholarship_obj]
        for scho in ScholarshipDetails.objects.all():
            scholarship.append(scho)

        all_student_obj = type('', (object,), {"id": "", "get_full_name": "All"})()
        students = [all_student_obj]
        for stud in ApplicationDetails.objects.filter(is_sponsored=True, year=get_current_year(request)):
            students.append(stud)

        student_list = StudentDetails.objects.all().distinct()

        if query_student:
            student_list = student_list.filter(id=query_student)

        if query_scholarship:
            student_list = student_list.filter(
                student_applicant_rel__applicant_scholarship_rel__scholarship_id=query_scholarship)

        if query_country:
            student_list = student_list.filter(address__country_id=query_country)

        rec_len = len(student_list)
        rows = []
        for obj in student_list:
            rec_list = []
            approval_amount = 0
            credit_total = 0
            outstanding_amount = 0
            for application_obj in obj.student_applicant_rel.filter(is_sponsored=True):
                rec_list.append(application_obj.get_full_name())
                if application_obj.applicant_scholarship_rel.all():
                    rec_list.append(application_obj.applicant_scholarship_rel.all()[0].course_applied.program_name)
                else:
                    rec_list.append("")
                if application_obj.applicant_progress_rel.all():
                    rec_list.append(application_obj.applicant_progress_rel.all()[0].semester.semester_name)
                else:
                    rec_list.append("")
                if application_obj.rel_student_payment_receipt_voucher.all():
                    approval_amount = application_obj.scholarship_fee
                    for voucher_obj in application_obj.rel_student_payment_receipt_voucher.all():
                        if voucher_obj.voucher_type == "debit":
                            credit_total += float(voucher_obj.voucher_amount)

                    outstanding_amount = float(approval_amount) - float(credit_total)

                    rec_list.append(float(approval_amount))

                    rec_list.append(float(credit_total))

                    rec_list.append(float(outstanding_amount))

                    rows.append(rec_list)

            debit_total += float(credit_total)
            outstanding_total += float(outstanding_amount)

        column_names = ["Student", "Program", "Semester", "Approval Amount", "Debit", "Outstanding"]
        return export_student_payment_wraped_column_xls('StudentReceipt&Payment', column_names, rows, rec_len,
                                                        debit_total, outstanding_total)
    except:
        return redirect("/accounting/get_approval_and_paid_total/")


def student_receipt_payment_report_export(request):
    try:
        val_dict = request.POST
        query_country = val_dict['query_country']
        query_scholarship = val_dict['query_scholarship']
        credit_total = 0
        balance_total = 0
        debit_total = 0
        temp_list = []
        stud_pay_voucher_list = StudentPaymentReceiptVoucher.objects.filter(application__year=get_current_year(request))
        if query_country:
            stud_pay_voucher_list = stud_pay_voucher_list.filter(application__address__country_id=query_country)
        if query_scholarship:
            stud_pay_voucher_list = stud_pay_voucher_list.filter(
                application__applicant_scholarship_rel__scholarship_id=query_scholarship)

        rows = []
        voucher_record = {}

        all_country_obj = type('', (object,), {"id": "", "country_name": "All"})()
        country = [all_country_obj]

        for co in CountryDetails.objects.all():
            country.append(co)

        all_scholarship_obj = type('', (object,), {"id": "", "scholarship_name": "All"})()
        scholarship = [all_scholarship_obj]

        for scho in ScholarshipDetails.objects.all():
            scholarship.append(scho)

        rec_len = len(stud_pay_voucher_list)

        for obj in stud_pay_voucher_list:
            rec_list = []
            rec_list.append(obj.voucher_number)
            rec_list.append(obj.voucher_date)
            rec_list.append(obj.application.get_full_name())
            if obj.application.applicant_progress_rel.all():
                rec_list.append(obj.application.applicant_progress_rel.all()[0].semester.semester_name)
            else:
                rec_list.append("")

            if obj.voucher_type == "debit":
                debit_total += float(obj.voucher_amount)
                credit_value = 0
                if debit_total != "":
                    debit_value = float(obj.voucher_amount)
                    rec_list.append(debit_value)

            if obj.voucher_type == "credit":
                rec_list.append("")
                credit_value = float(obj.voucher_amount)
                credit_total += float(obj.voucher_amount)
                debit_value = 0
                if credit_total != "":
                    rec_list.append(credit_value)

            if obj.voucher_type != "credit":
                rec_list.append("")

            balance_value = (float(debit_value) - float(credit_value))

            rec_list.append(balance_value)
            rows.append(rec_list)
        balance_total = StudentPaymentReceiptVoucher.objects.filter(application__year=get_current_year(request)).values(
            "application__scholarship_fee").distinct().aggregate(total_price=Sum('application__scholarship_fee'))

        if balance_total and stud_pay_voucher_list:
            debit_total = debit_total
            credit_total = credit_total
            balance_total = (float(debit_total) - float(credit_total))
            temp_list.append("Total")
            temp_list.append(debit_total)
            temp_list.append(credit_total)
            temp_list.append(balance_total)

        column_names = ["NO", "Voucher Date", "Student", "Semester", "Debit", "Credit", "Balance"]

        return export_last_row_wraped_column_xls('StudentReceipt&Payment', column_names, rows, rec_len, temp_list)
    except:
        return redirect("/accounting/get_student_report/")


def export_payment_receipt_report(request):
    try:
        val_dict = request.POST
        student_id = val_dict['student_id']
        rows = []
        application_rec = ApplicationDetails.objects.filter(student_id=student_id, year=get_current_year(request))
        voucher_record = StudentPaymentReceiptVoucher.objects.filter(application__in=application_rec)
        total_amount = StudentPaymentReceiptVoucher.objects.filter(voucher_type="credit",
                                                                   application__in=application_rec).values(
            "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))
        raw_dict = {}
        for rec in voucher_record:
            rec_list = []
            rec_list.append(rec.voucher_number)
            rec_list.append(rec.voucher_description)
            if rec.voucher_type == "debit":
                debit_value = float(rec.voucher_amount)
                if debit_value != "":
                    debit_value = float(rec.voucher_amount)
                    rec_list.append(debit_value)

            if rec.voucher_type == "credit":
                rec_list.append("")
                credit_value = float(rec.voucher_amount)
                if credit_value != "":
                    rec_list.append(credit_value)

            if rec.voucher_type != "credit":
                rec_list.append("")

            rows.append(rec_list)

        column_names = ["NO", "Description", "Debit", "Credit"]
        return export_wraped_column_xls('StudentPayment&Receipt', column_names, rows)
    except:
        return redirect("/accounting/get_student_payment_and_receipt_report/")


from django.http import HttpResponse
from django.views.generic import View
from common.utils import render_to_pdf, render_to_file  # created in step 4
from threading import Thread, activeCount
from django.core.mail import EmailMultiAlternatives


def send_email(file: list, subject, text_content, from_email, to):
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # attachment = open('/home/redbytes/scholarship_mgmt_system/scholarship_mgmt/store/' + file[0], 'rb')
    path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "store/") + file[0]
    attachment = open(os.path.join(os.path.abspath(os.path.dirname("__file__")), "store/") + file[0], 'rb')
    msg.attach(file[0], attachment.read(), 'application/pdf')
    msg.send()

    if os.path.exists(path):
        os.remove(path)


def get_report(request):
    payment_voucher = StudentPaymentReceiptVoucher.objects.filter(application__year=get_current_year(request))
    # today = datetime.date.today()
    params = {
        'payment_voucher': payment_voucher,
        'request': request
    }
    # return render_to_pdf('report_voucher.html', params)
    subject, from_email, to = 'Student Payment Voucher', 'redbytes.test@gmail.com', 'vaibhav734@gmail.com'
    text_content = 'Please FInd Attachment'

    file = render_to_file('report_voucher.html', params)
    thread = Thread(target=send_email, args=(file, subject, text_content, from_email, to))
    thread.start()
    return HttpResponse("Processed")


def save_and_send_payment_voucher_data_by_student(request):
    if request.method == 'POST':
        val_dict = request.POST
        voucher = StudentPaymentReceiptVoucher.get_instance(val_dict, None)
        voucher.voucher_type = "debit"
        voucher.save()
        voucher_number = create_voucher_number("SPV", voucher)
        voucher.voucher_number = voucher_number
        voucher.voucher_total = voucher.application.calculate_student_payment_balance_amount()
        voucher.save()

        params = {
            'voucher': voucher,
            'request': request
        }
        # return render_to_pdf('report_voucher.html', params)
        subject, from_email, to = 'Student Payment Voucher', 'redbytes.test@gmail.com', 'vaibhav734@gmail.com'
        text_content = 'Please FInd Attachment'

        file = render_to_file('report_voucher.html', params)
        thread = Thread(target=send_email, args=(file, subject, text_content, from_email, to))
        thread.start()

        return redirect("/accounting/get_student_payment_voucher/")


def update_donar_receipt_voucher(request):
    if request.method == "POST":
        val_dict = request.POST
        try:
            voucher = DonorReceiptVoucher.objects.get(id=val_dict['donar_id'])
            voucher.voucher_amount = float(val_dict['donar_amount'])
            voucher.save()
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')
        return HttpResponse(json.dumps({'success': "Record updated successfully."}), content_type='application/json')


def delete_donar_receipt_voucher(request):
    if request.method == "POST":
        val_dict = request.POST
        try:
            DonorReceiptVoucher.objects.get(id=val_dict['voucher_id']).delete()
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')

        return HttpResponse(json.dumps({'success': "Record deleted successfully."}), content_type='application/json')
