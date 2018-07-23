from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from student.models import StudentDetails, ApplicationDetails
from masters.models import CountryDetails, ScholarshipDetails, StudentDonorMapping
from .models import StudentPaymentReceiptVoucher, DonorReceiptVoucher
import json
from common.utils import create_voucher_number
from django.db.models import Sum
from donor.models import DonorDetails
from django.db.models import Q

# Create your views here.
def get_student_payment_voucher(request):
    student_list = StudentDetails.objects.all()
    voucher_record = StudentPaymentReceiptVoucher.objects.all()
    return render(request, "template_student_payment_voucher.html",{'student_list': student_list, 'voucher_record': voucher_record})

def get_student_receipt_voucher(request):
    student_list = StudentDetails.objects.all()
    voucher_record = StudentPaymentReceiptVoucher.objects.all()
    return render(request, "template_student_receipt_voucher.html",{'student_list': student_list, 'voucher_record': voucher_record})

def get_student_payment_and_receipt_report(request):
    student_list = StudentDetails.objects.all()
    return render(request, "template_student_payment_and_receipt_report.html",{'student_list': student_list})

def get_student_report(request):

    query_country = request.GET.get("country") or None
    query_scholarship = request.GET.get("scholarship") or None

    credit_total = 0
    balance_total = 0
    voucher_rec_list = []


    stud_pay_voucher_list = StudentPaymentReceiptVoucher.objects.all()

    if query_country:
        stud_pay_voucher_list = stud_pay_voucher_list.filter(application__address__country_id=query_country)
    if query_scholarship:
        stud_pay_voucher_list = stud_pay_voucher_list.filter(application__applicant_scholarship_rel__scholarship_id=query_scholarship)

    voucher_record = {}
    all_country_obj = type('', (object,), {"id": "", "country_name": "All"})()
    country = [all_country_obj]
    for co in CountryDetails.objects.all():
        country.append(co)

    all_scholarship_obj = type('', (object,), {"id": "", "scholarship_name": "All"})()
    scholarship = [all_scholarship_obj]
    for scho in ScholarshipDetails.objects.all():
        scholarship.append(scho)


    for obj in stud_pay_voucher_list:
        if obj.voucher_type == "debit":
            debit_total += float(obj.voucher_amount)

        if obj.voucher_type == "credit":
            credit_total += float(obj.voucher_amount)

        debit_total = 0
        voucher_rec_list.append(obj)

    balance_total = StudentPaymentReceiptVoucher.objects.values("application__scholarship_fee").distinct().aggregate(total_price=Sum('application__scholarship_fee'))

    if balance_total['total_price'] and stud_pay_voucher_list:
        voucher_record['debit_total'] = debit_total
        voucher_record['credit_total'] = credit_total
        voucher_record['balance_total'] = (float(balance_total['total_price']) - credit_total)
        voucher_record['voucher_record'] = voucher_rec_list

    return render(request, "template_student_report.html",{'voucher_record': voucher_record, 'country_list': country, 'scholarship_list': scholarship, 'selected_country':CountryDetails.objects.filter(id=query_country), 'selected_scholarship': ScholarshipDetails.objects.filter(id=query_scholarship)})

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
    for obj in StudentPaymentReceiptVoucher.objects.filter(application__address__country__country_name=country, voucher_beneficiary=beneficiary, application__scholarship_selection_rel__scholarship__scholarship_name=scholarship_type):
        if obj.voucher_type == "debit":
            debit_total += float(obj.voucher_amount)

        if obj.voucher_type == "credit":
            credit_total += float(obj.voucher_amount)

        voucher_rec_list.append(obj)

    balance_total = StudentPaymentReceiptVoucher.objects.values("application__scholarship_fee").distinct().aggregate(total_price=Sum('application__scholarship_fee'))

    voucher_record['debit_total'] = debit_total
    voucher_record['credit_total'] = credit_total
    voucher_record['balance_total'] = float(balance_total['total_price']) - credit_total
    voucher_record['voucher_record'] = voucher_rec_list

    return render(request, "template_student_report.html",{'voucher_record': voucher_record})

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

    all_student_obj = type('', (object,), {"id": "", "country_name": "All"})()
    students = [all_student_obj]
    for stud in StudentDetails.objects.all():
        students.append(stud)

    all_scholarship_obj = type('', (object,), {"id": "", "scholarship_name": "All"})()
    scholarship = [all_scholarship_obj]
    for scho in ScholarshipDetails.objects.all():
        scholarship.append(scho)



    student_list = StudentDetails.objects.all().distinct()

    if query_student:
        student_list = student_list.filter(id=query_student)

    if query_scholarship:
        student_list = student_list.filter(id=query_scholarship)

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
        for application_obj in obj.student_applicant_rel.all():
            if application_obj.rel_student_payment_receipt_voucher.all():
                approval_amount = application_obj.scholarship_fee

                raw_dict['application_list'] = application_obj
                for voucher_obj in application_obj.rel_student_payment_receipt_voucher.all():

                    raw_dict['voucher_list'] = voucher_obj
                    if voucher_obj.voucher_type == "credit":
                        credit_total += float(voucher_obj.voucher_amount)

                outstanding_amount = float(approval_amount) - float(credit_total)

                raw_dict['approval_amount'] = float(approval_amount)
                raw_dict['credit_total'] = float(credit_total)
                raw_dict['outstanding_amount'] = float(outstanding_amount)
                student_list_rec.append(raw_dict)

        debit_total += float(credit_total)
        outstanding_total += float(outstanding_amount)

    return render(request, "template_approval_and_paid_total.html",{'voucher_record': student_list_rec, 'debit_total': debit_total, 'outstanding_total': outstanding_total, 'country_list': country, 'scholarship_list': scholarship, 'selected_country':CountryDetails.objects.filter(id=query_country), 'selected_scholarship': ScholarshipDetails.objects.filter(id=query_scholarship),'student_list': students, 'selected_student': StudentDetails.objects.filter(id=query_student)})

def get_donor_receipt_voucher(request):

    donor_list = DonorDetails.objects.all()

    return render(request, "template_donor_receipt_voucher.html",{'donor_list': donor_list})

from django.forms.models import model_to_dict
def get_donors_student_list(request):

    student_list = StudentDonorMapping.objects.filter(donor=request.POST['donor'])

    return HttpResponse(json.dumps([ obj.to_dict() for obj in student_list]), content_type='application/json')

def get_donor_report(request):
    donor_list = DonorDetails.objects.all()
    return render(request, "template_donor_report.html",{'donor_list': donor_list})

def get_voucher_data_by_donor(request):
    debit_total = 0
    outstanding_total = 0

    student_ids = StudentDonorMapping.objects.filter(donor_id=request.POST['donor']).values('student')

    student_list = StudentDetails.objects.filter(id__in=student_ids).distinct()
    student_list_rec = []

    for obj in student_list:

        raw_dict = {}
        raw_dict_one = {}
        approval_amount = 0
        credit_total = 0
        outstanding_amount = 0
        application_list = []
        for application_obj in obj.student_applicant_rel.all():
            approval_amount = application_obj.scholarship_fee

            for voucher_obj in application_obj.rel_donor_receipt_voucher.all():

                raw_dict['voucher_rec'] = voucher_obj.to_dict_short()
                if voucher_obj.voucher_type == "debit":
                    credit_total += float(voucher_obj.voucher_amount)

            outstanding_amount = float(approval_amount) - float(credit_total)

            if application_obj.rel_donor_receipt_voucher.all():
                raw_dict['approval_amount'] = float(approval_amount)
                raw_dict['credit_total'] = float(credit_total)
                raw_dict['outstanding_amount'] = float(outstanding_amount)
                student_list_rec.append(raw_dict)

        debit_total += float(credit_total)
        outstanding_total += float(outstanding_amount)

    return HttpResponse(json.dumps(student_list_rec), content_type='application/json')

def get_payment_voucher_data_by_student(request):

    application_rec = ApplicationDetails.objects.get(student_id=request.POST['student'])
    voucher_record = StudentPaymentReceiptVoucher.objects.filter(application_id=application_rec.id)
    total_amount = StudentPaymentReceiptVoucher.objects.filter(voucher_type="credit",application=application_rec).values(
        "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))

    raw_dict = {}
    raw_dict['total_amount'] = float(total_amount['total_credit']) if total_amount['total_credit'] else 0
    raw_dict['application_rec'] = application_rec.to_student_payment_application_dict()
    raw_dict['voucher_rec'] = [ obj.to_dict() for obj in voucher_record]

    return HttpResponse(json.dumps(raw_dict), content_type='application/json')


def get_receipt_voucher_data_by_student(request):

    application_rec = ApplicationDetails.objects.get(student_id=request.POST['student'])
    voucher_record = StudentPaymentReceiptVoucher.objects.filter(application_id=application_rec.id)

    raw_dict = {}
    balance_total = StudentPaymentReceiptVoucher.objects.filter(voucher_type="credit", application=application_rec).values("voucher_amount").aggregate(total_credit=Sum('voucher_amount'))
    raw_dict['application_rec'] = application_rec.to_application_dict()
    raw_dict['outstanding_amount'] = (float(application_rec.scholarship_fee) - float(balance_total['total_credit'])) if balance_total['total_credit'] else 0
    raw_dict['voucher_rec'] = [ obj.to_dict() for obj in voucher_record]
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
        return redirect("/accounting/get_student_payment_voucher/")

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
        return redirect("/accounting/get_student_receipt_voucher/")



def get_donor_recipt_for_org_payment(request):

    application_rec = ApplicationDetails.objects.get(student_id=request.POST['student'])
    voucher_record = DonorReceiptVoucher.objects.filter(application_id=application_rec.id)
    total_amount = DonorReceiptVoucher.objects.filter(voucher_type="debit",application=application_rec).values(
        "voucher_amount").aggregate(total_credit=Sum('voucher_amount'))

    raw_dict = {}
    balance_total = DonorReceiptVoucher.objects.filter(voucher_type="debit", application=application_rec).values("voucher_amount").aggregate(total_credit=Sum('voucher_amount'))
    raw_dict['application_rec'] = application_rec.to_application_dict() if application_rec else ''
    raw_dict['outstanding_amount'] = ( float(application_rec.scholarship_fee) - float(balance_total['total_credit']) ) if application_rec.scholarship_fee and balance_total['total_credit'] else 0
    raw_dict['total_amount'] = float(total_amount['total_credit']) if total_amount['total_credit'] else 0
    raw_dict['voucher_rec'] = [ obj.to_dict() for obj in voucher_record] if voucher_record else ''

    return HttpResponse(json.dumps(raw_dict), content_type='application/json')

def save_donor_recipt_for_org_payment(request):
    if request.method == 'POST':
        val_dict = request.POST
        donor_voucher = DonorReceiptVoucher.get_instance(val_dict, None)
        donor_voucher.voucher_type = "debit"
        donor_voucher.save()
        voucher_number = create_voucher_number("DRV", donor_voucher)
        donor_voucher.voucher_number = voucher_number
        donor_voucher.voucher_total = donor_voucher.application.calculate_student_payment_balance_amount()
        donor_voucher.save()
        return redirect("/accounting/get_donor_receipt_voucher/")