from django.db import models
from common.models import BaseModel
from masters.models import CountryDetails, AddressDetails, ModuleDetails
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
    country = models.ForeignKey('masters.CountryDetails', null=True, related_name='partner_country_rel',
                                on_delete=models.PROTECT)
    office_name = models.CharField(max_length=255, blank=True, null=True)
    person_one = models.CharField(max_length=100, blank=True, null=True)
    person_one_contact_number = models.CharField(max_length=16, blank=True, null=True)
    person_two = models.CharField(max_length=100, blank=True, null=True)
    person_two_contact_number = models.CharField(max_length=16, blank=True, null=True)
    office_contact_number = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address = models.ForeignKey('masters.AddressDetails', null=True, related_name='partner_address_rel',
                                on_delete=models.PROTECT)
    single_address = models.CharField(max_length=500, blank=True, null=True)
    photo = models.FileField(upload_to=content_file_name_partner, blank=True, null=True)
    user = models.ForeignKey('accounts.User', null=True, related_name='partner_user_rel', on_delete=models.PROTECT)

    class Meta:
        permissions = (
            ('can_view_applicant_details', 'can view applicant details'),
            ('can_view_approving_application', 'can view approving application'),
            ('can_view_progress_history', 'can view progress history'),
            ('can_view_psychometric_test_report', 'can view psychometric test report'),
            ('can_view_link_student_program', 'can view link student program'),
            ('can_view_academic_progress', 'can view academic progress'),
            ('can_view_attendance_report', 'can view attendance report'),
            ('can_view_accepted_students', 'can view accepted students'),
        )
        ordering = ('user__first_name',)

    def __str__(self):
        details = str(self.country.country_name) if self.country else '' + ' and ' + str(self.office_name) if self.office_name else ''
        return details


class StudentModuleMapping(BaseModel):
    module = models.ForeignKey('masters.DevelopmentProgram', null=True, related_name='student_module_link_rel',
                               on_delete=models.PROTECT)
    applicant_id = models.ForeignKey('student.ApplicationDetails', null=True, related_name='applicant_module_rel',
                                     on_delete=models.PROTECT)
    country = models.ForeignKey(CountryDetails, null=True, related_name='student_module_country_rel',
                                on_delete=models.PROTECT)
    degree = models.ForeignKey('masters.DegreeDetails', blank=True, null=True,
                               related_name='degree_module_rel',
                               on_delete=models.PROTECT)
    program = models.ForeignKey('masters.ProgramDetails', blank=True, null=True,
                                related_name='program_module_rel',
                                on_delete=models.PROTECT)

    def __str__(self):
        details = str(self.applicant_id.first_name) + ' and ' + str(self.module.module.module_name)
        return details

    def to_dict(self):
        res = {
            'id': self.id,
            'program': self.program.to_dict() if self.program else '',
        }
        return res
