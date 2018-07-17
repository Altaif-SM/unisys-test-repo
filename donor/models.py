from django.db import models
from common.models import BaseModel


# Create your models here.
class DonorDetails(BaseModel):
    organisation = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey('masters.CountryDetails', null=True, related_name='donor_country_rel',
                                on_delete=models.PROTECT)
    person = models.CharField(max_length=255, blank=True, null=True)
    person_contact_number = models.CharField(max_length=16, blank=True, null=True)
    single_donor_address = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey('masters.AddressDetails', null=True, related_name='donor_address_rel',
                                on_delete=models.PROTECT)
    email = models.EmailField(max_length=255, blank=True, null=True)
    reg_document = models.FileField(upload_to='masters.content_file_name_donor')
    due_amount = models.IntegerField(blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    bank_account_number = models.CharField(max_length=100, blank=True, null=True)
    bank_swift_code = models.CharField(max_length=50, blank=True, null=True)
    bank_address = models.ForeignKey('masters.AddressDetails', null=True, related_name='donor_bank_address_rel',
                                     on_delete=models.PROTECT)
    donor_bank_address = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('accounts.User', null=True, related_name='donor_user_rel', on_delete=models.PROTECT)

    class Meta:
        ordering = ('user__first_name',)

        permissions = (
            ('can_view_scholarship', 'can view scholarship'),
            ('can_view_student_selection', 'can view student selection'),
            ('can_view_reports', 'can view reports'),
            ('can_view_student_reports', 'can view student reports'),
            ('can_view_app_progress_history', 'can view app progress history'),
            ('can_view_payments_reports', 'can view payments reports'),
            ('can_view_my_payments', 'can view my payments'),
            ('can_view_student_receipts', 'can view student receipts'),
        )

    def __str__(self):
        return self.user.first_name

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'user': self.user.to_dict() if self.user else '',
        }

        return res
