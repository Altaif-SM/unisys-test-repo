from django.db import models
from common.models import BaseModel
from masters.models import SemesterDetails, DonorDetails
from student.models import StudentDetails

# Create your models here.
class StudentPaymentVoucher(BaseModel):

    PAYMENT_VOUCHER_NUMBER = 'payment_voucher_number'
    STUDENT = 'student'
    SEMESTAR = 'semester'
    PAYMENT_VOUCHER_DATE = 'payment_voucher_date'
    PAYMENT_VOUCHER_AMOUNT = 'payment_voucher_amount'
    PAYMENT_VOUCHER_TOTAL = 'payment_voucher_total'
    PAYMENT_VOUCHER_DESC = 'payment_voucher_description'
    PAYMENT_VOUCHER_BEN = 'payment_voucher_beneficiary'

    payment_voucher_number = models.CharField(max_length=50, null=True)
    student = models.ForeignKey(StudentDetails, related_name="rel_student_payment_voucher", on_delete=models.PROTECT)
    semester = models.ForeignKey(SemesterDetails, related_name="rel_semester_payment_voucher", on_delete=models.PROTECT, null=True)
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

    @staticmethod
    def get_instance(val_dict, voucher_id=None):

        if voucher_id:
            voucher = StudentPaymentVoucher.objects.get(id=StudentPaymentVoucher)
        else:
            voucher = StudentPaymentVoucher()

        if StudentPaymentVoucher.PAYMENT_VOUCHER_NUMBER in val_dict and val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_NUMBER]:
            voucher.payment_voucher_number = val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_NUMBER]

        if StudentPaymentVoucher.STUDENT in val_dict and val_dict[StudentPaymentVoucher.STUDENT]:
            voucher.student = StudentDetails.objects.get(id=val_dict[StudentPaymentVoucher.STUDENT])

        if StudentPaymentVoucher.SEMESTAR in val_dict and val_dict[StudentPaymentVoucher.SEMESTAR]:
            voucher.semester = SemesterDetails.objects.get(id=val_dict[StudentPaymentVoucher.SEMESTAR])

        if StudentPaymentVoucher.PAYMENT_VOUCHER_DATE in val_dict and val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_DATE]:
            voucher.payment_voucher_date = val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_DATE]

        if StudentPaymentVoucher.PAYMENT_VOUCHER_AMOUNT in val_dict and val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_AMOUNT]:
            voucher.payment_voucher_amount = float(val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_AMOUNT])

        if StudentPaymentVoucher.PAYMENT_VOUCHER_TOTAL in val_dict and val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_TOTAL]:
            voucher.payment_voucher_total = float(val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_TOTAL])

        if StudentPaymentVoucher.PAYMENT_VOUCHER_DESC in val_dict and val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_DESC]:
            voucher.payment_voucher_description= val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_DESC]

        if StudentPaymentVoucher.PAYMENT_VOUCHER_BEN in val_dict and val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_BEN]:
            voucher.payment_voucher_beneficiary = val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_BEN]

        return voucher


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