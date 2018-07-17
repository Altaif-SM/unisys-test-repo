from django.db import models
from datetime import datetime
from common.models import BaseModel
import os
from accounts.models import User
from student.models import *
from student.models import StudentDetails
from donor.models import DonorDetails

def content_file_name_partner(instance, filename):
    dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.user.first_name, dirname, ext)
    return os.path.join('images', filename)


def content_file_name_donor(instance, filename):
    dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.user.first_name, dirname, ext)
    return os.path.join('reports', filename)


class CountryDetails(BaseModel):
    country_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('country_name',)

    def __str__(self):
        return self.country_name

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'country_name': self.country_name if self.country_name else '',
        }

        return res



class AddressDetails(BaseModel):
    residential_address = models.CharField(max_length=255, blank=True, null=True)
    sub_locality = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=80, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=80, blank=True, null=True)
    street = models.CharField(max_length=80, blank=True, null=True)
    country = models.ForeignKey(CountryDetails, null=True, related_name='address_country_rel', on_delete=models.PROTECT)

    class Meta:
        ordering = ('city',)

    def __str__(self):
        return self.city if self.city else ''

    def to_dict(self):
        res = {
            'id': self.id,
            'residential_address': self.residential_address,
            'sub_locality': self.sub_locality,
            'city': self.city,
            'post_code': self.post_code,
            'district': self.district,
            'state': self.state,
            'street': self.street,
            'country': self.country
        }
        return res


class YearDetails(BaseModel):
    year_name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    active_year = models.BooleanField(default=False)

    class Meta:
        ordering = ('year_name',)

    def __str__(self):
        return self.year_name


class ReligionDetails(BaseModel):
    religion_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('religion_name',)

    def __str__(self):
        return self.religion_name


class ScholarshipDetails(BaseModel):
    scholarship_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('scholarship_name',)

    def __str__(self):
        return self.scholarship_name

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'scholarship_name': self.scholarship_name if self.scholarship_name else '',
        }

        return res



class DegreeFormula(BaseModel):
    scholarship = models.ForeignKey(ScholarshipDetails, null=True, related_name='degree_scholarship_formula_relation',
                                    on_delete=models.PROTECT)
    cgpa_min = models.CharField(max_length=10, blank=True, null=True)
    cgpa_max = models.CharField(max_length=10, blank=True, null=True)
    grade_min = models.CharField(max_length=10, blank=True, null=True)
    grade_max = models.CharField(max_length=10, blank=True, null=True)
    repayment = models.CharField(max_length=10, blank=True, null=True)
    is_cgpa_or_grade = models.BooleanField(default=True)


class MasterAndPhdFormula(BaseModel):
    scholarship = models.ForeignKey(ScholarshipDetails, null=True, related_name='phd_scholarship_formula_relation',
                                    on_delete=models.PROTECT)
    result = models.CharField(max_length=10, blank=True, null=True)
    repayment = models.FloatField(max_length=10, blank=True, null=True)


class MasterAndCourseFormula(BaseModel):
    scholarship = models.ForeignKey(ScholarshipDetails, null=True, related_name='course_scholarship_formula_relation',
                                    on_delete=models.PROTECT)
    result_min = models.CharField(max_length=10, blank=True, null=True)
    result_max = models.CharField(max_length=10, blank=True, null=True)
    repayment = models.CharField(max_length=10, blank=True, null=True)


class StudentDonorMapping(BaseModel):
    student = models.ForeignKey(StudentDetails, null=True, related_name='student_donor_rel', on_delete=models.PROTECT)
    donor = models.ForeignKey(DonorDetails, null=True, related_name='donor_student_rel', on_delete=models.PROTECT)

    class Meta:
        ordering = ('student__user__first_name',)

    def __str__(self):
        details = str(self.student.user.first_name) + ' and ' + str(self.donor.user.first_name)
        return details


class UniversityDetails(BaseModel):
    country = models.ForeignKey(CountryDetails, null=True, related_name='university_country_rel',
                                on_delete=models.PROTECT)
    university_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey(AddressDetails, null=True, related_name='university_address_rel',
                                on_delete=models.PROTECT)

    class Meta:
        ordering = ('university_name',)

    def __str__(self):
        return self.university_name

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'university_name': self.university_name if self.university_name else '',
        }

        return res



class SemesterDetails(BaseModel):
    semester_name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ('semester_name',)

    def __str__(self):
        return self.semester_name

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'semester_name': self.semester_name if self.semester_name else '',
        }

        return res


class DegreeTypeDetails(BaseModel):
    degree_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('degree_name',)

    def __str__(self):
        return self.degree_name


class DegreeDetails(BaseModel):
    degree_name = models.CharField(max_length=255, blank=True, null=True)
    degree_type = models.ForeignKey(DegreeTypeDetails, null=True, related_name='degree_degree_type_rel',
                                    on_delete=models.PROTECT)

    class Meta:
        ordering = ('degree_name',)

    def __str__(self):
        return self.degree_name

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'degree_name': self.degree_name if self.degree_name else '',
        }

        return res



class ProgramDetails(BaseModel):
    program_name = models.CharField(max_length=255, blank=True, null=True)
    degree_type = models.ForeignKey(DegreeTypeDetails, null=True, related_name='program_degree_type_rel',
                                    on_delete=models.PROTECT)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='program_university_rel',
                                   on_delete=models.PROTECT)

    class Meta:
        ordering = ('program_name',)

    def __str__(self):
        return self.program_name


    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'program_name': self.program_name if self.program_name else '',
        }

        return res



class ModuleDetails(BaseModel):
    module_name = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(CountryDetails, null=True, related_name='module_country_rel', on_delete=models.PROTECT)


class DevelopmentProgram(BaseModel):
    year = models.ForeignKey(YearDetails, null=True, related_name='development_year_rel', on_delete=models.PROTECT)
    semester = models.ForeignKey(SemesterDetails, null=True, related_name='development_semester_rel',
                                 on_delete=models.PROTECT)
    module = models.ForeignKey(ModuleDetails, null=True, related_name='development_module_rel',
                               on_delete=models.PROTECT)
    code = models.CharField(max_length=100, blank=True, null=True)
    activity = models.CharField(max_length=2000, blank=True, null=True)
    outcome = models.CharField(max_length=2000, blank=True, null=True)
    duration_day = models.IntegerField(blank=True, null=True)
    duration_night = models.IntegerField(blank=True, null=True)
    method = models.CharField(max_length=255, blank=True, null=True)
    marks = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    remark = models.CharField(max_length=2000, blank=True, null=True)


class GuardianDetails(BaseModel):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=25)
    # photo = models.FileField(upload_to=content_file_name_student)
    is_active = models.BooleanField(default=True)
    nationality = models.ForeignKey(CountryDetails, null=True, related_name='guardian_nationality_rel',
                                    on_delete=models.PROTECT)
    religion = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=16, blank=True, null=True)
    address = models.ForeignKey(AddressDetails, null=True, related_name='guardian_address_rel',
                                on_delete=models.PROTECT)

    def get_all_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        if self.middle_name == None:
            self.middle_name = ''
        full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip()

    def to_dict(self):
        res = {
            'id': self.id,
            'first_name': self.first_name,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'contact_number': self.contact_number,
            'address': self.address,
            'get_all_name': self.get_all_name(),
        }
        return res


class GuardianStudentMapping(BaseModel):
    guardian = models.ForeignKey(GuardianDetails, null=True, related_name='gurd_std_mapping_rel',
                                 on_delete=models.PROTECT)
    student = models.ForeignKey(StudentDetails, null=True, related_name='std_gurd_mapping_rel',
                                on_delete=models.PROTECT)