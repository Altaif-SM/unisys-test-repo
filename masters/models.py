from django.db import models
from datetime import datetime
from common.models import BaseModel
import os
from accounts.models import User
from student.models import *
from student.models import StudentDetails, ApplicationDetails
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

class EnglishCompetencyTestDetails(BaseModel):
    english_competency_test = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.english_competency_test

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'english_competency_test': self.english_competency_test if self.english_competency_test else '',
        }

        return res



class AllCountries(BaseModel):
    country_name = models.CharField(max_length=100, blank=True, null=True)
    country_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ('country_name',)

    def __str__(self):
        return self.country_name


class AddressDetails(BaseModel):
    residential_address = models.CharField(max_length=255, blank=True, null=True)
    sub_locality = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=80, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=80, blank=True, null=True)
    street = models.CharField(max_length=80, blank=True, null=True)
    country = models.ForeignKey(CountryDetails, null=True, related_name='address_country_rel', on_delete=models.PROTECT)
    is_same = models.BooleanField(default=False)
    mobile = models.CharField(max_length=80, blank=True, null=True)
    whats_app = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        ordering = ('country',)

    def __str__(self):
        city = self.city if self.city else ''
        country = self.country.country_name if self.country else ''

        return str(city) + str(country)

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
            'country': self.country.to_dict(),
        }
        return res


class YearDetails(BaseModel):
    year_name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    active_year = models.BooleanField(default=False)
    #base_date = models.BooleanField(default=False)

    class Meta:
        ordering = ('year_name',)

    def __str__(self):
        return self.year_name

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'year_name': self.year_name if self.year_name else '',
        }

        return res


class ReligionDetails(BaseModel):
    religion_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('religion_name',)

    def __str__(self):
        return self.religion_name


class DegreeTypeDetails(BaseModel):
    degree_name = models.CharField(max_length=255, blank=True, null=True)

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
    cgpa_min = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=10)
    cgpa_max = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=10)
    grade_min = models.CharField(max_length=10, blank=True, null=True)
    grade_max = models.CharField(max_length=10, blank=True, null=True)
    repayment = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=10)
    result = models.CharField(max_length=10, blank=True, null=True)
    is_cgpa_or_grade = models.BooleanField(default=True)

    degree_type = models.ForeignKey(DegreeTypeDetails, null=True, related_name='degree_formula_degree_type_relation',
                                    on_delete=models.PROTECT)

    def __str__(self):
        cgpa_min = self.cgpa_min if self.cgpa_min else ''
        cgpa_max = self.cgpa_max if self.cgpa_max else ''
        scholarship = self.scholarship.scholarship_name if self.scholarship else ''
        repayment = self.repayment if self.repayment else ''
        res = 'scholarship = '+scholarship+',cgpa_min = '+str(cgpa_min)+', cgpa_max = '+str(cgpa_max) + ', repayment = '+str(repayment)
        return res


class MasterAndPhdFormula(BaseModel):
    scholarship = models.ForeignKey(ScholarshipDetails, null=True, related_name='phd_scholarship_formula_relation',
                                    on_delete=models.PROTECT)
    result = models.CharField(max_length=10, blank=True, null=True)
    repayment = models.FloatField(max_length=10, blank=True, null=True)
    degree_type = models.ForeignKey(DegreeTypeDetails, null=True, related_name='master_phd_formula_degree_type_relation',
                                    on_delete=models.PROTECT)

    def __str__(self):
        result = self.result if self.result else ''
        repayment = self.repayment if self.repayment else ''
        scholarship = self.scholarship.scholarship_name if self.scholarship else ''
        res = 'scholarship = '+scholarship+', result = '+result+', repayment = '+repayment
        return res


class MasterAndCourseFormula(BaseModel):
    scholarship = models.ForeignKey(ScholarshipDetails, null=True, related_name='course_scholarship_formula_relation',
                                    on_delete=models.PROTECT)
    result_min = models.CharField(max_length=10, blank=True, null=True)
    result_max = models.CharField(max_length=10, blank=True, null=True)
    repayment = models.CharField(max_length=10, blank=True, null=True)
    degree_type = models.ForeignKey(DegreeTypeDetails, null=True,
                                    related_name='master_course_formula_degree_type_relation',
                                    on_delete=models.PROTECT)

    def __str__(self):
        result_min = self.result_min if self.result_min else ''
        result_max = self.result_max if self.result_max else ''
        repayment = self.repayment if self.repayment else ''
        scholarship = self.scholarship.scholarship_name if self.scholarship else ''
        res = 'scholarship = '+scholarship+',result_min = '+result_min+', result_max = '+result_max + 'repayment = '+repayment
        return res


class StudentDonorMapping(BaseModel):
    student = models.ForeignKey(StudentDetails, null=True, related_name='student_donor_rel', on_delete=models.PROTECT)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='donor_applicant_rel',
                                     on_delete=models.PROTECT)
    donor = models.ForeignKey(DonorDetails, null=True, related_name='donor_student_rel', on_delete=models.PROTECT)

    class Meta:
        ordering = ('student__user__first_name',)

    def __str__(self):
        details = str(self.student.user.first_name) + ' and ' + str(self.donor.user.first_name)
        return details

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'student': self.student.student_applicant_rel.all()[
                0].to_dict_student_application() if self.student else '',
            'donor': self.donor.to_dict() if self.donor else '',
        }

        return res


class UniversityDetails(BaseModel):
    country = models.ForeignKey(CountryDetails, null=True, related_name='university_country_rel',
                                on_delete=models.PROTECT)
    university_id = models.CharField(max_length=255, blank=True, null=True)
    university_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey(AddressDetails, null=True, related_name='university_address_rel',
                                on_delete=models.PROTECT)
    university_logo = models.ImageField(upload_to='university_logo/', null=True, blank=True)
    university_address = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)


    class Meta:
        ordering = ('-id',)

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

    # class Meta:
    #     ordering = ('semester_name',)

    def __str__(self):
        return self.semester_name

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'semester_name': self.semester_name if self.semester_name else '',
        }

        return res



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
            'degree_type': self.degree_type.to_dict() if self.degree_type else '',
        }

        return res


class StudyModeDetails(BaseModel):
    study_mode = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.study_mode

class StudyTypeDetails(BaseModel):
    study_type = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.study_type



class StudyLevelDetails(BaseModel):
    study_level = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.study_level

class FacultyDetails(BaseModel):
    university = models.ForeignKey(UniversityDetails, null=True, related_name='university_faculty_rel',
                                on_delete=models.PROTECT)
    faculty_id = models.CharField(max_length=255, blank=True, null=True)
    faculty_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='faculty_logo/', null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('-id',)

class ProgramDetails(BaseModel):
    program_name = models.CharField(max_length=255, blank=True, null=True)
    program_overview = models.TextField(blank=True, null=True)
    program_objective = models.TextField(blank=True, null=True)
    program_vision = models.TextField(blank=True, null=True)
    program_mission = models.TextField(blank=True, null=True)
    program_id = models.CharField(max_length=255, blank=True, null=True)
    degree_type = models.ForeignKey(DegreeTypeDetails, null=True, related_name='program_degree_type_rel',
                                    on_delete=models.PROTECT)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='program_university_rel',
                                   on_delete=models.PROTECT)
    faculty = models.ForeignKey(FacultyDetails, null=True, related_name='program_faculty_rel',
                                   on_delete=models.PROTECT)
    study_mode = models.ForeignKey(StudyModeDetails, null=True, related_name='program_study_mode_rel',
                                on_delete=models.PROTECT)
    study_level = models.ForeignKey(StudyLevelDetails, null=True, related_name='program_study_level_rel',
                                   on_delete=models.PROTECT)
    study_type = models.ForeignKey(StudyTypeDetails, null=True, related_name='program_study_type_rel',
                                   on_delete=models.PROTECT)
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
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
    name = models.CharField(max_length=255, blank=True, null=True)
    activity = models.CharField(max_length=2000, blank=True, null=True)
    outcome = models.CharField(max_length=2000, blank=True, null=True)
    duration_day = models.IntegerField(blank=True, null=True)
    duration_night = models.IntegerField(blank=True, null=True)
    method = models.CharField(max_length=255, blank=True, null=True)
    marks = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    remark = models.CharField(max_length=2000, blank=True, null=True)

class SoftSkillDevelopmentProgram(BaseModel):
    program_name = models.CharField(max_length=255, blank=True, null=True)
    objectives = models.CharField(max_length=2000, blank=True, null=True)
    delivery_method = models.CharField(max_length=100, blank=True, null=True)
    delivery_location = models.CharField(max_length=256, blank=True, null=True)
    organizer = models.CharField(max_length=256, blank=True, null=True)
    delivery_date = models.DateField(null=True)
    completion_deadline = models.DateField(null=True)
    rsvp_method = models.CharField(max_length=2000, blank=True, null=True)
    remarks = models.CharField(max_length=2000, blank=True, null=True)


class GuardianDetails(BaseModel):
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=25, null=True)
    # photo = models.FileField(upload_to=content_file_name_student)
    is_active = models.BooleanField(default=True)
    religion = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=16, blank=True, null=True)
    address = models.ForeignKey(AddressDetails, null=True, related_name='guardian_address_rel',
                                on_delete=models.PROTECT)

    user = models.ForeignKey('accounts.User', null=True, related_name='guardian_user_rel', on_delete=models.PROTECT)

    class Meta:
        ordering = ('user__first_name',)

        permissions = (
            ('can_view_student_academic_reports', 'can view student academic reports'),
            ('can_view_application_progress_history', 'can view application progress history'),
        )

    def to_dict(self):
        res = {
            'id': self.id,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'contact_number': self.contact_number,
            'address': self.address,
        }
        return res


class GuardianStudentMapping(BaseModel):
    guardian = models.ForeignKey(GuardianDetails, null=True, related_name='gurd_std_mapping_rel',
                                 on_delete=models.PROTECT)
    student = models.ForeignKey(StudentDetails, null=True, related_name='std_gurd_mapping_rel',
                                on_delete=models.PROTECT)


class EmailTemplates(BaseModel):
    template_for = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=500, blank=True, null=True)
    email_body = models.CharField(max_length=2000, blank=True, null=True)
    is_active = models.BooleanField(default=False)


class UploadTermCondition(BaseModel):
    term_condition = models.FileField(upload_to='term_condition/pdf', blank=True, null=True)



class LanguageDetails(BaseModel):
    short_code = models.CharField(max_length=255, blank=True, null=True)
    language_name = models.CharField(max_length=255, blank=True, null=True)
    language_direction = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False)
    class Meta:
        ordering = ('-id',)

class CurrencyDetails(BaseModel):
    currency_number = models.CharField(max_length=255, blank=True, null=True)
    currency_code = models.CharField(max_length=255, blank=True, null=True)
    currency_name = models.CharField(max_length=255, blank=True, null=True)
    decimal_description = models.CharField(max_length=255, blank=True, null=True)
    record_status = models.BooleanField(default=False)
    length = models.CharField(max_length=255, blank=True, null=True)
    exchange_type = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        ordering = ('-id',)


class ActivityDetails(BaseModel):
    activity_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.acivity_name


class StudentModeDetails(BaseModel):
    student_mode = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.student_mode

class LearningCentersDetails(BaseModel):
    lc_name = models.CharField(max_length=255, blank=True, null=True)
    lc_address = models.CharField(max_length=255, blank=True, null=True)
    lc_email = models.CharField(max_length=255, blank=True, null=True)
    lc_tel = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(CountryDetails, null=True, related_name='learning_centers_country_rel',
                                    on_delete=models.PROTECT)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.lc_name


class UniversitPartnerDetails(BaseModel):
    university_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    university_address = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.university_name