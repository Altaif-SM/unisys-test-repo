from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from student.models import StudentDetails, ApplicationDetails
from .models import StudentPaymentVoucher
import json

# Create your views here.
def get_student_payment_voucher(request):
    student_list = StudentDetails.objects.all()
    voucher_record = StudentPaymentVoucher.objects.all()
    return render(request, "template_student_payment_voucher.html",{'student_list': student_list, 'voucher_record': voucher_record})

def get_student_receipt_voucher(request):
    return render(request, "template_student_receipt_voucher.html")

def get_student_payment_and_receipt_report(request):
    return render(request, "template_student_payment_and_receipt_report.html")

def get_student_report(request):
    return render(request, "template_student_report.html")

def get_approval_and_paid_total(request):
    return render(request, "template_approval_and_paid_total.html")

def get_donor_receipt_voucher(request):
    return render(request, "template_donor_receipt_voucher.html")

def get_donor_report(request):
    return render(request, "template_donor_report.html")

def get_payment_voucher_data_by_student(request):

    application_rec = ApplicationDetails.objects.get(student_id=request.POST['student'])

    return HttpResponse(json.dumps(application_rec.to_application_dict()), content_type='application/json')

def save_payment_voucher_data_by_student(request):
    if request.method == 'POST':
        val_dict = request.POST
        voucher = StudentPaymentVoucher.get_instance(val_dict, None)
        voucher.save()
        return redirect("/accounting/get_student_payment_voucher/")