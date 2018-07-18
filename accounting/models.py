from django.db import models
from common.models import BaseModel
from masters.models import SemesterDetails, StudentDonorMapping
from student.models import StudentDetails, ApplicationDetails
from donor.models import DonorDetails
from common.utils import create_voucher_number

# Create your models here.
class StudentPaymentVoucher(BaseModel):

    PAYMENT_VOUCHER_NUMBER = 'payment_voucher_number'
    APP_ID = 'application'
    SEMESTER = 'semester'
    PAYMENT_VOUCHER_DATE = 'payment_voucher_date'
    PAYMENT_VOUCHER_AMOUNT = 'payment_voucher_amount'
    PAYMENT_VOUCHER_TOTAL = 'payment_voucher_total'
    PAYMENT_VOUCHER_DESC = 'payment_voucher_description'
    PAYMENT_VOUCHER_BEN = 'payment_voucher_beneficiary'

    payment_voucher_number = models.CharField(max_length=50, null=True)
    application = models.ForeignKey(ApplicationDetails, related_name="rel_student_payment_voucher", on_delete=models.PROTECT, null=True)
    # student = models.ForeignKey(StudentDetails, related_name="rel_student_payment_voucher", on_delete=models.PROTECT)
    # semester = models.ForeignKey(SemesterDetails, related_name="rel_semester_payment_voucher", on_delete=models.PROTECT, null=True)
    payment_voucher_date = models.DateField()
    payment_voucher_amount = models.FloatField(max_length=50, null=True)
    payment_voucher_total = models.FloatField(max_length=50, null=True)
    payment_voucher_description = models.CharField(max_length=50, null=True)
    payment_voucher_beneficiary = models.CharField(max_length=50, null=True)

    class Meta:
        permissions = (
            ('can_view_student_payment_voucher', 'can view student payment voucher'),
        )

    def validate(self):
        self.payment_voucher_amount >= self.application.scholarship_fee

    def __str__(self):
        return str(self.payment_voucher_number)

    @staticmethod
    def get_instance(val_dict, voucher_id=None):

        if voucher_id:
            voucher = StudentPaymentVoucher.objects.get(id=StudentPaymentVoucher)
        else:
            voucher = StudentPaymentVoucher()
            voucher.payment_voucher_number = create_voucher_number(ApplicationDetails.objects.get(id=val_dict[StudentPaymentVoucher.APP_ID]))

        if StudentPaymentVoucher.PAYMENT_VOUCHER_NUMBER in val_dict and val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_NUMBER]:
            voucher.payment_voucher_number = val_dict[StudentPaymentVoucher.PAYMENT_VOUCHER_NUMBER]

        if StudentPaymentVoucher.APP_ID in val_dict and val_dict[StudentPaymentVoucher.APP_ID]:
            voucher.application = ApplicationDetails.objects.get(id=val_dict[StudentPaymentVoucher.APP_ID])

        if StudentPaymentVoucher.SEMESTER in val_dict and val_dict[StudentPaymentVoucher.SEMESTER]:
            voucher.semester = SemesterDetails.objects.get(id=val_dict[StudentPaymentVoucher.SEMESTER])

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

    RECEIPT_VOUCHER_NUMBER = 'receipt_voucher_number'
    APP_ID = 'application'
    SEMESTER = 'semester'
    RECEIPT_VOUCHER_DATE = 'receipt_voucher_date'
    RECEIPT_VOUCHER_AMOUNT = 'receipt_voucher_amount'
    RECEIPT_VOUCHER_TOTAL = 'receipt_voucher_total'
    RECEIPT_VOUCHER_DESC = 'receipt_voucher_description'
    RECEIPT_VOUCHER_BEN = 'receipt_voucher_beneficiary'

    receipt_voucher_number = models.CharField(max_length=50, null=True)
    application = models.ForeignKey(ApplicationDetails, related_name="rel_student_receipt_voucher",
                                    on_delete=models.PROTECT, null=True)
    # student = models.ForeignKey(StudentDetails, related_name="rel_student_receipt_voucher", on_delete=models.PROTECT)
    # semester = models.ForeignKey(SemesterDetails, related_name="rel_semester_receipt_voucher", on_delete=models.PROTECT)
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

    @staticmethod
    def get_instance(val_dict, voucher_id=None):

        if voucher_id:
            voucher = StudentReceiptVoucher.objects.get(id=StudentReceiptVoucher)
        else:
            voucher = StudentReceiptVoucher()

        if StudentReceiptVoucher.RECEIPT_VOUCHER_NUMBER in val_dict and val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_NUMBER]:
            voucher.receipt_voucher_number = val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_NUMBER]

        if StudentReceiptVoucher.APP_ID in val_dict and val_dict[StudentReceiptVoucher.APP_ID]:
            voucher.application = ApplicationDetails.objects.get(id=val_dict[StudentReceiptVoucher.APP_ID])

        if StudentReceiptVoucher.SEMESTER in val_dict and val_dict[StudentReceiptVoucher.SEMESTER]:
            voucher.semester = SemesterDetails.objects.get(id=val_dict[StudentReceiptVoucher.SEMESTER])

        if StudentReceiptVoucher.RECEIPT_VOUCHER_DATE in val_dict and val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_DATE]:
            voucher.receipt_voucher_date = val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_DATE]

        if StudentReceiptVoucher.RECEIPT_VOUCHER_AMOUNT in val_dict and val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_AMOUNT]:
            voucher.receipt_voucher_amount = float(val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_AMOUNT])

        if StudentReceiptVoucher.RECEIPT_VOUCHER_TOTAL in val_dict and val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_TOTAL]:
            voucher.receipt_voucher_total = float(val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_TOTAL])

        if StudentReceiptVoucher.RECEIPT_VOUCHER_DESC in val_dict and val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_DESC]:
            voucher.receipt_voucher_description = val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_DESC]

        if StudentReceiptVoucher.RECEIPT_VOUCHER_BEN in val_dict and val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_BEN]:
            voucher.receipt_voucher_beneficiary = val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_BEN]

        return voucher

class DonorReceiptVoucher(BaseModel):
    receipt_voucher_number = models.CharField(max_length=50, null=True)
    application = models.ForeignKey(ApplicationDetails, related_name="rel_donor_receipt_voucher",
                                    on_delete=models.PROTECT, null=True)
    donor_student = models.ForeignKey(StudentDonorMapping, related_name="rel_donor_student_receipt_voucher", on_delete=models.PROTECT, null=True)
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