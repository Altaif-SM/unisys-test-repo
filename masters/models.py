from django.db import models
from datetime import datetime
from common.models import BaseModel
import os
from accounts.models import User
from student.models import *
from student.models import StudentDetails, ApplicationDetails
from donor.models import DonorDetails
from masters.helpers import document_upload_path,university_logo_upload_path,tanseeq_guide_upload_path,registration_guide_upload_path,university_stamp_upload_path


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

class CitiDetails(BaseModel):
    city = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.city

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'city': self.city if self.city else '',
        }

        return res


class CountryDetails(BaseModel):
    country_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.ManyToManyField(CitiDetails, related_name='country_city')

    class Meta:
        ordering = ('id',)
        permissions = (
            ('can_view_country_details', 'Can View Country Details'),
        )

    def __str__(self):
        return self.country_name

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'country_name': self.country_name if self.country_name else '',
        }

        return res

class ArabCompetencyTestDetails(BaseModel):
    arab_competency_test = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ('id',)
        permissions = (
            ('can_view_arab_competency_test_details', 'Can View Arab Competency Test Details'),
        )

    def __str__(self):
        return self.arab_competency_test

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'arab_competency_test': self.arab_competency_test if self.arab_competency_test else '',
        }

        return res

class EnglishCompetencyTestDetails(BaseModel):
    english_competency_test = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ('id',)
        permissions = (
            ('can_view_english_competency_test_details', 'Can View English Competency Test Details'),
        )

    def __str__(self):
        return self.english_competency_test

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'english_competency_test': self.english_competency_test if self.english_competency_test else '',
        }

        return res

class UniversityTypeDetails(BaseModel):
    university_type = models.CharField(max_length=150, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('id',)
        permissions = (
            ('can_view_university_type_details', 'Can View University Type Details'),
        )


class TypeDetails(BaseModel):
    type = models.CharField(max_length=150, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('id',)
        permissions = (
            ('can_view_type_details', 'Can View Type Details'),
        )


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
    country = models.ForeignKey(CountryDetails, null=True, related_name='address_country_rel', on_delete=models.SET_NULL)
    nationality = models.ForeignKey(CountryDetails, null=True, related_name='nationality_country_rel', on_delete=models.SET_NULL)
    is_same = models.BooleanField(default=False)
    mobile = models.CharField(max_length=80, blank=True, null=True)
    whats_app = models.CharField(max_length=80, blank=True, null=True)
    country_code = models.CharField(max_length=80, blank=True, null=True)

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
    year_name = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    active_year = models.BooleanField(default=False)
    is_tanseeq_year = models.BooleanField(default=False)

    class Meta:
        ordering = ('year_name',)
        permissions = (
            ('can_view_year_details', 'Can view Year Details'),
        )

    def __str__(self):
        return self.year_name

    @classmethod
    def active_records(cls):
        return cls.objects.filter(is_tanseeq_year=True)

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'year_name': self.year_name if self.year_name else '',
        }

        return res


class ReligionDetails(BaseModel):
    religion_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ('religion_name',)

    def __str__(self):
        return self.religion_name


class DegreeTypeDetails(BaseModel):
    degree_name = models.CharField(max_length=100, blank=True, null=True)

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
                                    on_delete=models.SET_NULL)
    cgpa_min = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=10)
    cgpa_max = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=10)
    grade_min = models.CharField(max_length=10, blank=True, null=True)
    grade_max = models.CharField(max_length=10, blank=True, null=True)
    repayment = models.DecimalField(blank=True, null=True,decimal_places=2,max_digits=10)
    result = models.CharField(max_length=10, blank=True, null=True)
    is_cgpa_or_grade = models.BooleanField(default=True)

    degree_type = models.ForeignKey(DegreeTypeDetails, null=True, related_name='degree_formula_degree_type_relation',
                                    on_delete=models.SET_NULL)

    def __str__(self):
        cgpa_min = self.cgpa_min if self.cgpa_min else ''
        cgpa_max = self.cgpa_max if self.cgpa_max else ''
        scholarship = self.scholarship.scholarship_name if self.scholarship else ''
        repayment = self.repayment if self.repayment else ''
        res = 'scholarship = '+scholarship+',cgpa_min = '+str(cgpa_min)+', cgpa_max = '+str(cgpa_max) + ', repayment = '+str(repayment)
        return res


class MasterAndPhdFormula(BaseModel):
    scholarship = models.ForeignKey(ScholarshipDetails, null=True, related_name='phd_scholarship_formula_relation',
                                    on_delete=models.SET_NULL)
    result = models.CharField(max_length=10, blank=True, null=True)
    repayment = models.FloatField(max_length=10, blank=True, null=True)
    degree_type = models.ForeignKey(DegreeTypeDetails, null=True, related_name='master_phd_formula_degree_type_relation',
                                    on_delete=models.SET_NULL)

    def __str__(self):
        result = self.result if self.result else ''
        repayment = self.repayment if self.repayment else ''
        scholarship = self.scholarship.scholarship_name if self.scholarship else ''
        res = 'scholarship = '+scholarship+', result = '+result+', repayment = '+repayment
        return res


class MasterAndCourseFormula(BaseModel):
    scholarship = models.ForeignKey(ScholarshipDetails, null=True, related_name='course_scholarship_formula_relation',
                                    on_delete=models.SET_NULL)
    result_min = models.CharField(max_length=10, blank=True, null=True)
    result_max = models.CharField(max_length=10, blank=True, null=True)
    repayment = models.CharField(max_length=10, blank=True, null=True)
    degree_type = models.ForeignKey(DegreeTypeDetails, null=True,
                                    related_name='master_course_formula_degree_type_relation',
                                    on_delete=models.SET_NULL)

    def __str__(self):
        result_min = self.result_min if self.result_min else ''
        result_max = self.result_max if self.result_max else ''
        repayment = self.repayment if self.repayment else ''
        scholarship = self.scholarship.scholarship_name if self.scholarship else ''
        res = 'scholarship = '+scholarship+',result_min = '+result_min+', result_max = '+result_max + 'repayment = '+repayment
        return res


class StudentDonorMapping(BaseModel):
    student = models.ForeignKey(StudentDetails, null=True, related_name='student_donor_rel', on_delete=models.SET_NULL)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='donor_applicant_rel',
                                     on_delete=models.SET_NULL)
    donor = models.ForeignKey(DonorDetails, null=True, related_name='donor_student_rel', on_delete=models.SET_NULL)

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
    COLLEGE_TYPES = (
        ("Community College", "COMMUNITY COLLEGE"),
        ("College", "COLLEGE"),
    )
    college_type = models.CharField(choices=COLLEGE_TYPES, max_length=50,blank=True, null=True)
    university_name = models.CharField(max_length=150, blank=True, null=True)
    university_code = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    university_logo = models.ImageField(upload_to=university_logo_upload_path, max_length=256, blank=True, null=True)
    tanseeq_guide = models.FileField(upload_to=tanseeq_guide_upload_path, max_length=256, blank=True, null=True)
    registration_guide = models.FileField(upload_to=registration_guide_upload_path, max_length=256, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_details = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_registration = models.BooleanField(default=True)
    is_singup = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    is_partner_university = models.BooleanField(default=False)
    university_type = models.ForeignKey(UniversityTypeDetails, null=True, related_name='university_type_rel',
                                on_delete=models.SET_NULL)
    type = models.ForeignKey(TypeDetails, null=True, related_name='type_rel', on_delete=models.SET_NULL)
    file = models.FileField(upload_to=document_upload_path, max_length=256, blank=True, null=True)
    is_tanseeq_university = models.BooleanField(default=False)
    university_stamp = models.FileField(upload_to=university_stamp_upload_path, max_length=256, blank=True,
                                          null=True)
    class Meta:
        ordering = ('id',)
        permissions = (
            ('can_view_university_details', 'Can View University Details'),
        )

    def __str__(self):
        return self.university_name



    @classmethod
    def active_records(cls,):
        return cls.objects.filter(is_active=True, is_delete=False, is_tanseeq_university = True)

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'university_name': self.university_name if self.university_name else '',
        }

        return res

class StudyLevelDetails(BaseModel):
    study_level = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        permissions = (
            ('can_view_studyleveldetails', 'Can View Study Level Details'),
        )

    def __str__(self):
        return self.study_level

class Semester(models.Model):
    semester = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

class SemesterDetails(BaseModel):
    semester_name = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    study_level = models.ForeignKey(StudyLevelDetails, null=True, related_name='study_level_semester_rel',
                             on_delete=models.SET_NULL)
    year = models.ForeignKey(YearDetails, null=True, related_name='year_semester_rel',
                                on_delete=models.SET_NULL)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='university_semester_rel',
                             on_delete=models.SET_NULL)
    semester = models.ManyToManyField(Semester, blank=True)
    university_type = models.ForeignKey(UniversityTypeDetails, null=True, related_name='semester_university_type_rel',
                                        on_delete=models.SET_NULL)

    class Meta:
        permissions = (
            ('can_view_semester_details', 'Can View Semester Details'),
        )

    def __str__(self):
        return self.semester_name



class DegreeDetails(BaseModel):
    degree_name = models.CharField(max_length=255, blank=True, null=True)
    degree_type = models.ForeignKey(DegreeTypeDetails, null=True, related_name='degree_degree_type_rel',
                                    on_delete=models.SET_NULL)

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
    universities = models.ManyToManyField(UniversityDetails, related_name="study_mode_details_university_details")
    study_mode = models.CharField(max_length=150, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.study_mode

class StudyTypeDetails(BaseModel):
    study_type = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.study_type

    class Meta:
        ordering = ('-id',)

    permissions = (
        ('can_view_studytypedetails', 'Can View Study Type Details'),
    )


class Department(models.Model):
    department = models.CharField(max_length=100, blank=True, null=True)


class FacultyDetails(BaseModel):
    university = models.ForeignKey(UniversityDetails, null=True, related_name='university_faculty_rel',
                                on_delete=models.SET_NULL)
    faculty_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(upload_to='faculty_logo/', null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    department = models.ManyToManyField(Department, blank=True)
    university_type = models.ForeignKey(UniversityTypeDetails, null=True, related_name='faculty_university_type_rel',
                                        on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.faculty_name

    permissions = (
        ('can_view_faculty_details', 'Can View Faculty Details'),
    )

class CampusBranchesDetails(BaseModel):
    campus_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='campus_university_rel',
                                   on_delete=models.SET_NULL)
    country = models.ForeignKey(CountryDetails, null=True, related_name='campus_centers_country_rel',
                                on_delete=models.SET_NULL)
    university_type = models.ForeignKey(UniversityTypeDetails, null=True, related_name='campus_university_type_rel',
                                        on_delete=models.SET_NULL)


    class Meta:
        ordering = ('-id',)
        permissions = (
            ('can_view_campus_branches_details', 'Can View Campus Branches Details'),
        )

    def __str__(self):
        return self.campus_name

class ProgramCampusDetails(models.Model):
    campus = models.ForeignKey(CampusBranchesDetails, null=True, related_name='program_campus_rel',on_delete=models.SET_NULL)

class ProgramStudyModeDetails(models.Model):
    study_mode = models.CharField(max_length=100, blank=True, null=True)

class CourseDetails(models.Model):
    code = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    unit = models.CharField(max_length=150, blank=True, null=True)
    type = models.CharField(max_length=150, blank=True, null=True)


class ProgramFeeType(models.Model):
    fee_type = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(null=True, blank=True, default=0.0)


class ProgramDetails(BaseModel):
    program_name = models.CharField(max_length=100, blank=True, null=True)
    credit_hrs = models.CharField(max_length=50, blank=True, null=True)
    program_overview = models.TextField(blank=True, null=True)
    program_objective = models.TextField(blank=True, null=True)
    program_vision = models.TextField(blank=True, null=True)
    program_mission = models.TextField(blank=True, null=True)
    degree_type = models.ForeignKey(DegreeTypeDetails, null=True, related_name='program_degree_type_rel',
                                    on_delete=models.SET_NULL)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='program_university_rel',
                                   on_delete=models.SET_NULL)
    faculty = models.ForeignKey(FacultyDetails, null=True, related_name='program_faculty_rel',
                                   on_delete=models.SET_NULL)
    study_level = models.ForeignKey(StudyLevelDetails, null=True, related_name='program_study_level_rel',
                                   on_delete=models.SET_NULL)
    study_type = models.ForeignKey(StudyTypeDetails, null=True, related_name='program_study_type_rel',
                                   on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    campus = models.ManyToManyField(ProgramCampusDetails, blank=True)
    study_mode = models.ManyToManyField(ProgramStudyModeDetails, blank=True)
    department = models.ForeignKey(Department, null=True, related_name='program_department_rel',
                                    on_delete=models.SET_NULL)
    university_type = models.ForeignKey(UniversityTypeDetails, null=True, related_name='program_university_type_rel',
                                   on_delete=models.SET_NULL)
    acceptance_avg = models.CharField(max_length=150, blank=True, null=True)
    capacity_avg = models.CharField(max_length=150, blank=True, null=True)
    course = models.ManyToManyField(CourseDetails, blank=True)
    is_semester_based = models.BooleanField(default=True)

    class Meta:
        ordering = ('program_name',)
        permissions = (
            ('can_view_program_details', 'Can View Program Details'),
        )

    def __str__(self):
        return self.program_name

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'program_name': self.program_name if self.program_name else '',
        }

        return res

class StudyPlanDetails(BaseModel):
    program = models.ForeignKey(ProgramDetails, null=True, related_name='study_plan_program_rel',
                             on_delete=models.SET_NULL)
    semester = models.CharField(max_length=180, blank=True, null=True)
    study_semester = models.ForeignKey(Semester, null=True, related_name='study_plan_semester_rel',
                                on_delete=models.SET_NULL)
    course = models.ManyToManyField(CourseDetails, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    academic_year = models.ForeignKey(YearDetails, null=True, related_name='study_plan_academic_year_rel',
                             on_delete=models.SET_NULL)

class ProgramFeeDetails(BaseModel):
    university = models.ForeignKey(UniversityDetails, null=True, related_name='program_fee_university_rel',
                                   on_delete=models.SET_NULL)
    year = models.ForeignKey(YearDetails, null=True, related_name='program_fee_year_rel',
                                   on_delete=models.SET_NULL)
    program = models.ForeignKey(ProgramDetails, null=True, related_name='program_fee_rel',
                                   on_delete=models.SET_NULL)
    country = models.ForeignKey(CountryDetails, null=True, related_name='country_fee_rel',
                                on_delete=models.SET_NULL)
    total_amount = models.FloatField(null=True, blank=True, default=0.0)
    program_fee = models.ManyToManyField(ProgramFeeType, blank=True)
    university_type = models.ForeignKey(UniversityTypeDetails, null=True, related_name='program_fee_university_type_rel',
                                        on_delete=models.SET_NULL)

    class Meta:
        permissions = (
            ('can_view_program_fee_details', 'Can View Program Fee Details'),
        )


class ModuleDetails(BaseModel):
    module_name = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(CountryDetails, null=True, related_name='module_country_rel', on_delete=models.SET_NULL)


class DevelopmentProgram(BaseModel):
    year = models.ForeignKey(YearDetails, null=True, related_name='development_year_rel', on_delete=models.SET_NULL)
    semester = models.ForeignKey(SemesterDetails, null=True, related_name='development_semester_rel',
                                 on_delete=models.SET_NULL)
    module = models.ForeignKey(ModuleDetails, null=True, related_name='development_module_rel',
                               on_delete=models.SET_NULL)
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
                                on_delete=models.SET_NULL)

    user = models.ForeignKey('accounts.User', null=True, related_name='guardian_user_rel', on_delete=models.SET_NULL)

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
                                 on_delete=models.SET_NULL)
    student = models.ForeignKey(StudentDetails, null=True, related_name='std_gurd_mapping_rel',
                                on_delete=models.SET_NULL)


class EmailTemplates(BaseModel):
    template_for = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=500, blank=True, null=True)
    email_body = models.CharField(max_length=2000, blank=True, null=True)
    is_active = models.BooleanField(default=False)


class UploadTermCondition(BaseModel):
    term_condition = models.FileField(upload_to='term_condition/pdf', blank=True, null=True)



class LanguageDetails(BaseModel):
    short_code = models.CharField(max_length=10, blank=True, null=True)
    language_name = models.CharField(max_length=50, blank=True, null=True)
    language_direction = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-id',)
        permissions = (
            ('can_read_language_details', 'Can Read Language Details'),
        )

class CurrencyDetails(BaseModel):
    currency_number = models.CharField(max_length=11, blank=True, null=True)
    currency_code = models.CharField(max_length=10, blank=True, null=True)
    currency_name = models.CharField(max_length=50, blank=True, null=True)
    decimal_description = models.CharField(max_length=50, blank=True, null=True)
    record_status = models.BooleanField(default=False)
    length = models.CharField(max_length=50, blank=True, null=True)
    exchange_type = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        ordering = ('-id',)
        permissions = (
            ('can_read_currency_details', 'Can Read currency Details'),
        )


class ActivityDetails(BaseModel):
    activity_name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        permissions = (
            ('can_view_activity_details', 'Can View Activity Details'),
        )

    def __str__(self):
        return self.acivity_name


class StudentModeDetails(BaseModel):
    student_mode = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        permissions = (
            ('can_view_student_mode_details', 'Can View Student Mode Details'),
        )

    def __str__(self):
        return self.student_mode

class LearningCentersDetails(BaseModel):
    lc_name = models.CharField(max_length=100, blank=True, null=True)
    lc_address = models.CharField(max_length=255, blank=True, null=True)
    lc_email = models.CharField(max_length=50, blank=True, null=True)
    lc_tel = models.CharField(max_length=30, blank=True, null=True)
    country = models.ForeignKey(CountryDetails, null=True, related_name='learning_centers_country_rel',
                                    on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='learning_university_rel',
                                   on_delete=models.SET_NULL)
    university_type = models.ForeignKey(UniversityTypeDetails, null=True, related_name='learning_university_type_rel',
                                        on_delete=models.SET_NULL)
    class Meta:
        ordering = ('id',)
        permissions = (
            ('can_view_learning_centers_details', 'Can View Learning Centers Details'),
        )

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




class CalenderDetails(BaseModel):
    university = models.ForeignKey(UniversityDetails, null=True, related_name='calender_university_rel',on_delete=models.SET_NULL)
    year = models.ForeignKey(YearDetails, null=True, related_name='calender_year_rel',on_delete=models.SET_NULL)
    branch = models.ForeignKey(CampusBranchesDetails, null=True, related_name='calender_branch_rel',on_delete=models.SET_NULL)
    semester = models.ForeignKey(SemesterDetails, null=True, related_name='calender_semester_rel',on_delete=models.SET_NULL)
    activity = models.ForeignKey(ActivityDetails, null=True, related_name='calender_activity_rel',on_delete=models.SET_NULL)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField(default=True)
    university_type = models.ForeignKey(UniversityTypeDetails, null=True, related_name='calender_university_type_rel',
                                        on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)
        permissions = (
            ('can_view_calender_details', 'Can View Calender Details'),
        )



class DepartmentDetails(BaseModel):
    department_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='department_logo/', null=True, blank=True)
    status = models.BooleanField(default=True)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='university_depatment_rel',
                                   on_delete=models.SET_NULL)

    faculty = models.ForeignKey(FacultyDetails, null=True, related_name='faculty_department_rel',
                                   on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)


class DepartmentStaffMapping(BaseModel):
    department = models.ForeignKey(DepartmentDetails, null=True, related_name='department_staff_map', on_delete=models.SET_NULL)
    staff = models.ForeignKey(User, null=True, related_name='staff_department_mapp',
                                     on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)

class CampusStaffMapping(BaseModel):
    campus = models.ForeignKey(CampusBranchesDetails, null=True, related_name='campus_program_map', on_delete=models.SET_NULL)
    staff = models.ForeignKey(User, null=True, related_name='staff_campus_mapp',
                              on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)

class FacultyStaffMapping(BaseModel):
    faculty = models.ForeignKey(FacultyDetails, null=True, related_name='faculty_staff_map', on_delete=models.SET_NULL)
    staff = models.ForeignKey(User, null=True, related_name='staff_faculty_mapp',
                                     on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)

class UniversityStaffMapping(BaseModel):
    university = models.ForeignKey(UniversityDetails, null=True, related_name='university_staff_map', on_delete=models.SET_NULL)
    staff = models.ForeignKey(User, null=True, related_name='staff_university_mapp',
                                     on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)

class NotesDetails(models.Model):
    note = models.CharField(max_length=255, blank=True, null=True)

class DocumentDetails(BaseModel):
    document_name = models.CharField(max_length=150, blank=True, null=True)
    doc_required = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    notes = models.ManyToManyField(NotesDetails, blank=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.document_name


class GroupDetails(BaseModel):
    group_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.group_name



class PaymentDetails(BaseModel):
    university = models.ForeignKey(UniversityDetails, null=True, related_name='payment_university_rel',
                                   on_delete=models.SET_NULL)
    amount = models.FloatField(null=True, blank=True, default=0.0)
    currency = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=True)
    university_type = models.ForeignKey(UniversityTypeDetails, null=True,
                                        related_name='payment_fee_type_rel',
                                        on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)


class ApplicationFeeDetails(BaseModel):
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    currency_code = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    application_id = models.ForeignKey(ApplicationDetails, null=True, related_name='application_app_id',
                                       on_delete=models.SET_NULL)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='application_fee_rel',
                                   on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)


class ProgramRegistrationFeeDetails(BaseModel):
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    currency_code = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    application_id = models.ForeignKey(ApplicationDetails, null=True, related_name='program_registration_fee_id',
                                       on_delete=models.SET_NULL)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='program_registration_fee_rel',
                                   on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)



class SemesterFeeType(models.Model):
    fee_type = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(null=True, blank=True, default=0.0)

class SemesterBasedFeeDetails(BaseModel):
    study_plan = models.ForeignKey(StudyPlanDetails, null=True, related_name='study_plan_semester_rel',on_delete=models.SET_NULL)
    semester_fee = models.ManyToManyField(SemesterFeeType, blank=True)

class CourseFeeDetails(BaseModel):
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    currency_code = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    application_id = models.ForeignKey(ApplicationDetails, null=True, related_name='course_registration_fee_id',
                                       on_delete=models.SET_NULL)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='course_registration_fee_rel',
                                   on_delete=models.SET_NULL)
    study_plan = models.ForeignKey(StudyPlanDetails, null=True, related_name='course_study_plan_rel',
                                   on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)

class PrerequisiteCourseDetails(BaseModel):
    code = models.CharField(max_length=100, blank=True, null=True)
    course = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        ordering = ('-id',)
        permissions = (
            ('can_view_prerequisite_course_details', 'Can View Prerequisite Course Details'),
        )

    def __str__(self):
        return self.code

class CreditCourseDetails(models.Model):
    code = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    unit = models.CharField(max_length=150, blank=True, null=True)
    type = models.CharField(max_length=150, blank=True, null=True)
    is_prerequisite = models.BooleanField(default=False)
    course = models.ForeignKey(PrerequisiteCourseDetails, null=True, related_name='study_plan_course_program_rel',
                                on_delete=models.SET_NULL)

class CreditStudyPlanDetails(BaseModel):
    program = models.ForeignKey(ProgramDetails, null=True, related_name='study_plan_credit_program_rel',
                             on_delete=models.SET_NULL)
    min_credit = models.CharField(max_length=50, blank=True, null=True)
    max_credit = models.CharField(max_length=50, blank=True, null=True)
    credit_course = models.ManyToManyField(CreditCourseDetails, blank=True)
    academic_year = models.ForeignKey(YearDetails, null=True, related_name='study_credit_academic_year_rel',
                                      on_delete=models.SET_NULL)
    semester = models.ForeignKey(Semester, null=True, related_name='study_credit_semester_rel',
                                       on_delete=models.SET_NULL)
    credit_fee = models.FloatField(null=True, blank=True, default=0.0)


class StudentRegisteredCreditCourseDetails(BaseModel):
    application_id = models.ForeignKey(ApplicationDetails, null=True, related_name='student_credit_application_id',
                                       on_delete=models.SET_NULL)
    program = models.ForeignKey(ProgramDetails, null=True, related_name='student_credit_registered_course',
                             on_delete=models.SET_NULL)
    course = models.ForeignKey(CreditCourseDetails, null=True, related_name='student_credit_credit_course',
                                on_delete=models.SET_NULL)
    credit = models.ForeignKey(CreditStudyPlanDetails, null=True, related_name='student_credit_study_plan',
                               on_delete=models.SET_NULL)

class RegisteredPrerequisiteCourses(BaseModel):
    application_id = models.ForeignKey(ApplicationDetails, null=True, related_name='student_prerequisite_application_id',
                                       on_delete=models.SET_NULL)
    course = models.ForeignKey(CreditCourseDetails, null=True, related_name='student_prerequisite_course',
                                on_delete=models.SET_NULL)


class CreditFeeDetails(BaseModel):
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    currency_code = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    application_id = models.ForeignKey(ApplicationDetails, null=True, related_name='credit_application_id',
                                       on_delete=models.SET_NULL)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='credit_university_rel',
                                   on_delete=models.SET_NULL)
    credit = models.ForeignKey(CreditStudyPlanDetails, null=True, related_name='credit_plan_rel',
                                   on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)

class ResearchSubject(models.Model):
    code = models.CharField(max_length=150, blank=True, null=True)
    subject_name = models.CharField(max_length=150, blank=True, null=True)


class ResearchPlanDetails(BaseModel):
    program = models.ForeignKey(ProgramDetails, null=True, related_name='research_program_rel',
                             on_delete=models.SET_NULL)
    semester = models.ForeignKey(Semester, null=True, related_name='research_semester_rel',
                                on_delete=models.SET_NULL)
    subject = models.ManyToManyField(ResearchSubject, blank=True)
    year = models.ForeignKey(YearDetails, null=True, related_name='research_year_rel',
                             on_delete=models.SET_NULL)

class AgentIDDetails(BaseModel):
    agent_id = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(User, null=True, related_name='agent_user_rel', on_delete=models.SET_NULL)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    whats_app = models.CharField(max_length=15, blank=True, null=True)
    country = models.ForeignKey(CountryDetails, null=True, related_name='agent_country_rel',
                                on_delete=models.SET_NULL)
    nationality = models.ForeignKey(CountryDetails, null=True, related_name='agent_nationality_rel',
                                    on_delete=models.SET_NULL)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    address_line_1 = models.TextField(blank=True, null=True)
    address_line_2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    reject_comment = models.TextField(blank=True, null=True)
    is_submitted = models.BooleanField(default=False)
    application_status = models.CharField(max_length=50, default="PENDING", blank=True, null=True)



class ResearchFeeType(models.Model):
    fee_type = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(null=True, blank=True, default=0.0)

class ResearchBasedFeeDetails(BaseModel):
    research = models.ForeignKey(ResearchPlanDetails, null=True, related_name='research_fee_rel',on_delete=models.SET_NULL)
    research_fee = models.ManyToManyField(ResearchFeeType, blank=True)


class ResearchFeeDetails(BaseModel):
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    currency_code = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    application_id = models.ForeignKey(ApplicationDetails, null=True, related_name='research_student_application_id',
                                       on_delete=models.SET_NULL)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='research_student_university_rel',
                                   on_delete=models.SET_NULL)
    research = models.ForeignKey(ResearchPlanDetails, null=True, related_name='research_student_fee_rel',
                                   on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-id',)



class ReferralFeeDetails(BaseModel):
    amount = models.CharField(max_length=50, blank=True, null=True)
    university = models.ForeignKey(UniversityDetails, null=True, related_name='referral_fee_university_rel',
                             on_delete=models.SET_NULL)
    program = models.ForeignKey(ProgramDetails, null=True, related_name='referral_fee_program_rel',
                                on_delete=models.SET_NULL)

    class Meta:
        permissions = (
            ('can_view_referral_fee_details', 'Can view Referral Dee Details'),
        )
