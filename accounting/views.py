from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from student.models import StudentDetails, ApplicationDetails
from masters.models import CountryDetails, ScholarshipDetails, StudentDonorMapping
from .models import StudentPaymentReceiptVoucher
import json
from common.utils import create_voucher_number
from django.db.models import Sum
from donor.models import DonorDetails

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

    country = CountryDetails.objects.all()
    scholarship = ScholarshipDetails.objects.all()

    voucher_record = {}
    debit_total = 0
    credit_total = 0
    balance_total = 0
    voucher_rec_list = []
    for obj in StudentPaymentReceiptVoucher.objects.all():
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

    return render(request, "template_student_report.html",{'voucher_record': voucher_record, 'country_list': country, 'scholarship_list': scholarship})

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

    student_list = StudentDetails.objects.all().distinct()
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


    return render(request, "template_approval_and_paid_total.html",{'voucher_record': student_list_rec, 'debit_total': debit_total, 'outstanding_total': outstanding_total})

def get_donor_receipt_voucher(request):

    donor_list = DonorDetails.objects.all()

    return render(request, "template_donor_receipt_voucher.html",{'donor_list': donor_list})

from django.forms.models import model_to_dict
def get_donors_student_list(request):

    student_list = StudentDonorMapping.objects.filter(donor=request.POST['donor'])

    return HttpResponse(json.dumps([ obj.to_dict() for obj in student_list]), content_type='application/json')

def get_donor_report(request):
    return render(request, "template_donor_report.html")

def get_payment_voucher_data_by_student(request):

    application_rec = ApplicationDetails.objects.get(student_id=request.POST['student'])

    voucher_record = StudentPaymentReceiptVoucher.objects.filter(application_id=application_rec.id)

    raw_dict = {}

    raw_dict['application_rec'] = application_rec.to_student_payment_application_dict()

    raw_dict['voucher_rec'] = [ obj.to_dict() for obj in voucher_record]

    return HttpResponse(json.dumps(raw_dict), content_type='application/json')


def get_receipt_voucher_data_by_student(request):

    application_rec = ApplicationDetails.objects.get(student_id=request.POST['student'])

    voucher_record = StudentPaymentReceiptVoucher.objects.filter(application_id=application_rec.id)

    raw_dict = {}

    balance_total = StudentPaymentReceiptVoucher.objects.filter(voucher_type="credit", application=application_rec).values("voucher_amount").aggregate(total_credit=Sum('voucher_amount'))

    raw_dict['application_rec'] = application_rec.to_application_dict()

    raw_dict['outstanding_amount'] = float(application_rec.scholarship_fee) - float(balance_total['total_credit'])

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
        voucher_number.voucher_total = voucher_number.application.calculate_student_payment_balance_amount()
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