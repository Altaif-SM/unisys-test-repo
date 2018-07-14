from django.shortcuts import render
from student.models import StudentDetails

# Create your views here.
def get_student_payment_voucher(request):
    student_list = StudentDetails.objects.all()
    return render(request, "template_student_payment_voucher.html",{'student_list': student_list})

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