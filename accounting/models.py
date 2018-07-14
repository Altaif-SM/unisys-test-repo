from django.db import models
from common.models import BaseModel
from masters.models import SemesterDetails, DonorDetails
from student.models import StudentDetails

# Create your models here.
class StudentPaymentVoucher(BaseModel):
    payment_voucher_number = models.CharField(max_length=50, null=True)
    student = models.ForeignKey(StudentDetails, related_name="rel_student_payment_voucher", on_delete=models.PROTECT)
    semester = models.ForeignKey(SemesterDetails, related_name="rel_semester_payment_voucher", on_delete=models.PROTECT)
    payment_voucher_date = models.DateField()
    payment_voucher_amount = models.FloatField(max_length=50, null=True)
    payment_voucher_total = models.FloatField(max_length=50, null=True)
    payment_voucher_description = models.CharField(max_length=50, null=True)
    payment_voucher_beneficiary = models.CharField(max_length=50, null=True)

    class Meta:
        permissions = (
            ('can_view_student_payment_voucher', 'can view student payment voucher'),
        )

    def __str__(self):
        return self.payment_voucher_number

class StudentReceiptVoucher(BaseModel):
    receipt_voucher_number = models.CharField(max_length=50, null=True)
    student = models.ForeignKey(StudentDetails, related_name="rel_student_receipt_voucher", on_delete=models.PROTECT)
    semester = models.ForeignKey(SemesterDetails, related_name="rel_semester_receipt_voucher", on_delete=models.PROTECT)
    receipt_voucher_date = models.DateField()
    receipt_voucher_amount = models.FloatField(max_length=50, null=True)
    receipt_voucher_total = models.FloatField(max_length=50, null=True)
    receipt_voucher_description = models.CharField(max_length=50, null=True)
    receipt_voucher_beneficiary = models.CharField(max_length=50, null=True)

    class Meta:
        permissions = (
            ('can_view_student_receipt_voucher', 'can view student receipt voucher'),
        )

    def __str__(self):
        return self.receipt_voucher_number

class DonorReceiptVoucher(BaseModel):
    receipt_voucher_number = models.CharField(max_length=50, null=True)
    student = models.ForeignKey(StudentDetails, related_name="rel_student_donor_receipt_voucher", on_delete=models.PROTECT)
    donor = models.ForeignKey(DonorDetails, related_name="rel_donor_student_receipt_voucher", on_delete=models.PROTECT)
    receipt_voucher_amount = models.FloatField(max_length=50, null=True)
    receipt_voucher_total = models.FloatField(max_length=50, null=True)
    receipt_voucher_description = models.CharField(max_length=50, null=True)

    class Meta:
        permissions = (
            ('can_view_donor_payment_voucher', 'can view donor payment voucher'),
            ('can_view_donor_receipt_voucher', 'can view donor receipt voucher'),
        )

    def __str__(self):
        return self.receipt_voucher_number