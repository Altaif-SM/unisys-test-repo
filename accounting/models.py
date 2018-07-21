from django.db import models
from common.models import BaseModel
from masters.models import SemesterDetails, StudentDonorMapping
from student.models import StudentDetails, ApplicationDetails
from donor.models import DonorDetails
from common.utils import create_voucher_number

# Create your models here.
class StudentPaymentReceiptVoucher(BaseModel):

    VOUCHER_NUMBER = 'voucher_number'
    APP_ID = 'application'
    SEMESTER = 'semester'
    VOUCHER_DATE = 'voucher_date'
    VOUCHER_AMOUNT = 'voucher_amount'
    VOUCHER_TOTAL = 'voucher_total'
    VOUCHER_DESC = 'voucher_description'
    VOUCHER_BEN = 'voucher_beneficiary'
    VOUCHER_TYPE = 'voucher_type'

    voucher_number = models.CharField(max_length=50, null=True)
    application = models.ForeignKey(ApplicationDetails, related_name="rel_student_payment_receipt_voucher", on_delete=models.PROTECT, null=True)
    voucher_date = models.DateField()
    voucher_amount = models.FloatField(max_length=50, null=True)
    voucher_total = models.FloatField(max_length=50, null=True)
    voucher_description = models.CharField(max_length=50, null=True)
    voucher_beneficiary = models.CharField(max_length=50, null=True)

    voucher_type = models.CharField(max_length=50, null=True)


    # debit = models.FloatField(max_length=50, null=True)
    # credit = models.FloatField(max_length=50, null=True)

    class Meta:
        permissions = (
            ('can_view_student_payment_voucher', 'can view student payment voucher'),
            ('can_view_student_receipt_voucher', 'can view student receipt voucher'),
            ('can_view_donor_payment_voucher', 'can view donor payment voucher'),
            ('can_view_donor_receipt_voucher', 'can view donor receipt voucher'),
        )

    def validate(self):
        self.voucher_amount >= self.application.scholarship_fee

    def __str__(self):
        return str(self.voucher_number)

    @staticmethod
    def get_instance(val_dict, voucher_id=None):

        if voucher_id:
            voucher = StudentPaymentReceiptVoucher.objects.get(id=StudentPaymentReceiptVoucher)
        else:
            voucher = StudentPaymentReceiptVoucher()

        if StudentPaymentReceiptVoucher.VOUCHER_NUMBER in val_dict and val_dict[StudentPaymentReceiptVoucher.VOUCHER_NUMBER]:
            voucher.voucher_number = val_dict[StudentPaymentReceiptVoucher.VOUCHER_NUMBER]

        if StudentPaymentReceiptVoucher.APP_ID in val_dict and val_dict[StudentPaymentReceiptVoucher.APP_ID]:
            voucher.application = ApplicationDetails.objects.get(id=val_dict[StudentPaymentReceiptVoucher.APP_ID])

        if StudentPaymentReceiptVoucher.VOUCHER_DATE in val_dict and val_dict[StudentPaymentReceiptVoucher.VOUCHER_DATE]:
            voucher.voucher_date = val_dict[StudentPaymentReceiptVoucher.VOUCHER_DATE]

        if StudentPaymentReceiptVoucher.VOUCHER_AMOUNT in val_dict and val_dict[StudentPaymentReceiptVoucher.VOUCHER_AMOUNT]:
            voucher.voucher_amount = float(val_dict[StudentPaymentReceiptVoucher.VOUCHER_AMOUNT])

        if StudentPaymentReceiptVoucher.VOUCHER_TOTAL in val_dict and val_dict[StudentPaymentReceiptVoucher.VOUCHER_TOTAL]:
            voucher.voucher_total = float(val_dict[StudentPaymentReceiptVoucher.VOUCHER_TOTAL])

        if StudentPaymentReceiptVoucher.VOUCHER_DESC in val_dict and val_dict[StudentPaymentReceiptVoucher.VOUCHER_DESC]:
            voucher.voucher_description= val_dict[StudentPaymentReceiptVoucher.VOUCHER_DESC]

        if StudentPaymentReceiptVoucher.VOUCHER_BEN in val_dict and val_dict[StudentPaymentReceiptVoucher.VOUCHER_BEN]:
            voucher.voucher_beneficiary = val_dict[StudentPaymentReceiptVoucher.VOUCHER_BEN]

        return voucher

    def to_dict(self):
        resp = {
            "id": self.id,
            StudentPaymentReceiptVoucher.VOUCHER_NUMBER: self.voucher_number,
            StudentPaymentReceiptVoucher.VOUCHER_DESC: self.voucher_description,
            StudentPaymentReceiptVoucher.VOUCHER_AMOUNT: self.voucher_amount,
            StudentPaymentReceiptVoucher.VOUCHER_TYPE: self.voucher_type,

            'country': self.application.address.country.to_dict() if self.application.address else '',
            'student': self.application.student.to_short_dict() if self.application.student else '',

            'scholarship': self.application.applicant_scholarship_rel.all()[0].scholarship.to_dict() if self.application.applicant_scholarship_rel.all() else '',
            'university': self.application.applicant_scholarship_rel.all()[0].university.to_dict() if self.application.applicant_scholarship_rel.all() else '',
            'program': self.application.applicant_module_rel.all()[0].program.to_dict() if self.application.applicant_module_rel.all() else '',
            'donor': self.application.student.student_donor_rel.all()[0].donor.to_dict() if self.application.student.student_donor_rel.all() else '',
            'voucher_number': self.voucher_number if self.voucher_number else '',
            'semester': self.application.applicant_progress_rel.all()[0].semester.to_dict() if self.application.applicant_progress_rel.all() else '',
            'degree': self.application.applicant_scholarship_rel.all()[0].course_applied.to_dict() if self.application.applicant_scholarship_rel.all() else '',

        }
        return resp

    def to_dict_short(self):
        resp = {
            "id": self.id,
            StudentPaymentReceiptVoucher.VOUCHER_NUMBER: self.voucher_number,
            "student": self.application.student.user.get_full_name() if self.application.student else ''
        }
        return resp


# class StudentReceiptVoucher(BaseModel):
#
#     RECEIPT_VOUCHER_NUMBER = 'receipt_voucher_number'
#     APP_ID = 'application'
#     SEMESTER = 'semester'
#     RECEIPT_VOUCHER_DATE = 'receipt_voucher_date'
#     RECEIPT_VOUCHER_AMOUNT = 'receipt_voucher_amount'
#     RECEIPT_VOUCHER_TOTAL = 'receipt_voucher_total'
#     RECEIPT_VOUCHER_DESC = 'receipt_voucher_description'
#     RECEIPT_VOUCHER_BEN = 'receipt_voucher_beneficiary'
#
#     receipt_voucher_number = models.CharField(max_length=50, null=True)
#     application = models.ForeignKey(ApplicationDetails, related_name="rel_student_receipt_voucher",
#                                     on_delete=models.PROTECT, null=True)
#     # student = models.ForeignKey(StudentDetails, related_name="rel_student_receipt_voucher", on_delete=models.PROTECT)
#     # semester = models.ForeignKey(SemesterDetails, related_name="rel_semester_receipt_voucher", on_delete=models.PROTECT)
#     receipt_voucher_date = models.DateField()
#     receipt_voucher_amount = models.FloatField(max_length=50, null=True)
#     receipt_voucher_total = models.FloatField(max_length=50, null=True)
#     receipt_voucher_description = models.CharField(max_length=50, null=True)
#     receipt_voucher_beneficiary = models.CharField(max_length=50, null=True)
#
#     class Meta:
#         permissions = (
#             ('can_view_student_receipt_voucher', 'can view student receipt voucher'),
#         )
#
#     def __str__(self):
#         return self.receipt_voucher_number
#
#     @staticmethod
#     def get_instance(val_dict, voucher_number=None):
#
#         if voucher_number:
#             voucher = StudentReceiptVoucher.objects.get(receipt_voucher_number=voucher_number)
#         else:
#             voucher = StudentReceiptVoucher()
#
#         if StudentReceiptVoucher.RECEIPT_VOUCHER_NUMBER in val_dict and val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_NUMBER]:
#             voucher.receipt_voucher_number = val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_NUMBER]
#
#         if StudentReceiptVoucher.APP_ID in val_dict and val_dict[StudentReceiptVoucher.APP_ID]:
#             voucher.application = ApplicationDetails.objects.get(id=val_dict[StudentReceiptVoucher.APP_ID])
#
#         if StudentReceiptVoucher.SEMESTER in val_dict and val_dict[StudentReceiptVoucher.SEMESTER]:
#             voucher.semester = SemesterDetails.objects.get(id=val_dict[StudentReceiptVoucher.SEMESTER])
#
#         if StudentReceiptVoucher.RECEIPT_VOUCHER_DATE in val_dict and val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_DATE]:
#             voucher.receipt_voucher_date = val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_DATE]
#
#         if StudentReceiptVoucher.RECEIPT_VOUCHER_AMOUNT in val_dict and val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_AMOUNT]:
#             voucher.receipt_voucher_amount = float(val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_AMOUNT])
#
#         if StudentReceiptVoucher.RECEIPT_VOUCHER_TOTAL in val_dict and val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_TOTAL]:
#             voucher.receipt_voucher_total = float(val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_TOTAL])
#
#         if StudentReceiptVoucher.RECEIPT_VOUCHER_DESC in val_dict and val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_DESC]:
#             voucher.receipt_voucher_description = val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_DESC]
#
#         if StudentReceiptVoucher.RECEIPT_VOUCHER_BEN in val_dict and val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_BEN]:
#             voucher.receipt_voucher_beneficiary = val_dict[StudentReceiptVoucher.RECEIPT_VOUCHER_BEN]
#
#         return voucher
#
# # class StudentReceiptVoucher(BaseModel):
# #     receipt_voucher_number = models.CharField(max_length=50, null=True)
# #     application = models.ForeignKey(ApplicationDetails, related_name="rel_donor_receipt_voucher",
# #                                     on_delete=models.PROTECT, null=True)
# #     student_donor = models.ForeignKey(StudentDonorMapping, related_name="rel_student_donor_receipt_voucher", on_delete=models.PROTECT, null=True)
# #     receipt_voucher_amount = models.FloatField(max_length=50, null=True)
# #     receipt_voucher_total = models.FloatField(max_length=50, null=True)
# #     receipt_voucher_description = models.CharField(max_length=50, null=True)
# #
# #     class Meta:
# #         permissions = (
# #             ('can_view_donor_payment_voucher', 'can view donor payment voucher'),
# #             ('can_view_donor_receipt_voucher', 'can view donor receipt voucher'),
# #         )
# #
# #     def __str__(self):
# #         return self.receipt_voucher_number
#
# class DonorReceiptVoucher(BaseModel):
#     receipt_voucher_number = models.CharField(max_length=50, null=True)
#     application = models.ForeignKey(ApplicationDetails, related_name="rel_donor_receipt_voucher",
#                                     on_delete=models.PROTECT, null=True)
#     donor_student = models.ForeignKey(StudentDonorMapping, related_name="rel_donor_student_receipt_voucher", on_delete=models.PROTECT, null=True)
#     receipt_voucher_amount = models.FloatField(max_length=50, null=True)
#     receipt_voucher_total = models.FloatField(max_length=50, null=True)
#     receipt_voucher_description = models.CharField(max_length=50, null=True)
#
#     class Meta:
#         permissions = (
#             ('can_view_donor_payment_voucher', 'can view donor payment voucher'),
#             ('can_view_donor_receipt_voucher', 'can view donor receipt voucher'),
#         )
#
#     def __str__(self):
#         return self.receipt_voucher_number