from django.db import models
from common.models import BaseModel
from masters.models import CountryDetails, AddressDetails
from accounts.models import User
from datetime import datetime
import os
# Create your models here.


def content_file_name_partner(instance, filename):
    dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.user.first_name, dirname, ext)
    return os.path.join('images', filename)


class PartnerDetails(BaseModel):
    country = models.ForeignKey('masters.CountryDetails', null=True, related_name='partner_country_rel', on_delete=models.PROTECT)
    office_name = models.CharField(max_length=255, blank=True, null=True)
    person_one = models.CharField(max_length=100, blank=True, null=True)
    person_one_contact_number = models.CharField(max_length=16, blank=True, null=True)
    person_two = models.CharField(max_length=100, blank=True, null=True)
    person_two_contact_number = models.CharField(max_length=16, blank=True, null=True)
    office_contact_number = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address = models.ForeignKey('masters.AddressDetails', null=True, related_name='partner_address_rel', on_delete=models.PROTECT)
    single_address = models.CharField(max_length=500, blank=True, null=True)
    photo = models.FileField(upload_to=content_file_name_partner, blank=True, null=True)
    user = models.ForeignKey('accounts.User', null=True, related_name='partner_user_rel', on_delete=models.PROTECT)

    class Meta:
        permissions = (
            ('can_view_applicant_details', 'can view applicant details'),
            ('can_view_approving_application', 'can view approving application'),
            ('can_view_progress_history', 'can view progress history'),
            ('can_view_psychometric_test_report', 'can view psychometric test report'),
        )
        ordering = ('user__first_name',)

    def __str__(self):
        details = str(self.country.country_name) + ' and ' + str(self.office_name)
        return details
