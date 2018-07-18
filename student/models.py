from django.db import models
from common.models import BaseModel
import os
from datetime import datetime
from masters.models import *
from accounts.models import *


def content_file_name_image(instance, filename):
    dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.first_name, dirname, ext)
    return os.path.join('images', filename)


def content_student_file_name_image(instance, filename):
    dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.user.first_name, dirname, ext)
    return os.path.join('images', filename)


def content_file_name_report(instance, filename):
    dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.first_name, dirname, ext)
    return os.path.join('reports', filename)


class StudentDetails(BaseModel):
    birth_date = models.DateField()
    gender = models.CharField(max_length=25)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    photo = models.FileField(upload_to=content_student_file_name_image)
    is_active = models.BooleanField(default=True)
    nationality = models.ForeignKey('masters.CountryDetails', null=True, related_name='student_nationality_rel',
                                    on_delete=models.PROTECT)
    religion = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=16, blank=True, null=True)
    address = models.ForeignKey('masters.AddressDetails', blank=True, null=True, related_name='student_address_rel',
                                on_delete=models.PROTECT)
    user = models.ForeignKey(User, null=True, related_name='student_user_rel', on_delete=models.PROTECT)

    class Meta:
        permissions = (
            ('can_view_student_personal_info', 'can view student personal info'),
            ('can_view_student_family_info', 'can view student family info'),
            ('can_view_student_academic_qualification', 'can view student academic qualification'),
            ('can_view_student_psychometric_test', 'can view student psychometric test'),
        )

    def __str__(self):
        return self.user.first_name

    def to_dict(self):
        res = {
            'id': self.id,
            # 'first_name': self.first_name,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'contact_number': self.contact_number,
            'address': self.address,
            # 'get_all_name': self.get_all_name(),
        }
        return res


class ApplicationDetails(BaseModel):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    year = models.ForeignKey('masters.YearDetails', blank=True, null=True,
                             related_name='applicant_year_rel',
                             on_delete=models.PROTECT)

    birth_date = models.DateField()
    gender = models.CharField(max_length=25)
    nationality = models.ForeignKey('masters.CountryDetails', blank=True, null=True,
                                    related_name='applicant_nationality_rel',
                                    on_delete=models.PROTECT)
    religion = models.ForeignKey('masters.ReligionDetails', blank=True, null=True,
                                 related_name='applicant_religion_rel',
                                 on_delete=models.PROTECT)

    id_number = models.CharField(max_length=100, blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_issue_country = models.ForeignKey('masters.CountryDetails', blank=True, null=True,
                                               related_name='passport_issue_country_rel',
                                               on_delete=models.PROTECT)

    address = models.ForeignKey('masters.AddressDetails', blank=True, null=True, related_name='applicant_address_rel',
                                on_delete=models.PROTECT)
    telephone_hp = models.CharField(max_length=16, blank=True, null=True)
    telephone_home = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    image = models.FileField(upload_to=content_file_name_image)

    wife_name = models.CharField(max_length=255, blank=True, null=True)
    wife_income = models.IntegerField(blank=True, null=True)
    wife_pay_slip = models.FileField(upload_to=content_file_name_report)
    wife_nationality = models.ForeignKey('masters.CountryDetails', null=True, related_name='wife_nationality_rel',
                                         on_delete=models.PROTECT)
    wife_occupation = models.CharField(max_length=255, blank=True, null=True)
    wife_telephone_home = models.CharField(max_length=16, blank=True, null=True)
    wife_dob = models.DateField(blank=True, null=True)
    wife_email = models.EmailField(max_length=255, blank=True, null=True)

    father_name = models.CharField(max_length=255, blank=True, null=True)
    father_income = models.IntegerField(blank=True, null=True)
    father_pay_slip = models.FileField(upload_to=content_file_name_report)
    father_nationality = models.ForeignKey('masters.CountryDetails', blank=True, null=True,
                                           related_name='father_nationality_rel',
                                           on_delete=models.PROTECT)
    father_occupation = models.CharField(max_length=255, blank=True, null=True)
    father_telephone_home = models.CharField(max_length=16, blank=True, null=True)
    father_dob = models.DateField(blank=True, null=True)
    father_email = models.EmailField(max_length=255, blank=True, null=True)

    mother_name = models.CharField(max_length=255, blank=True, null=True)
    mother_income = models.IntegerField(blank=True, null=True)
    mother_pay_slip = models.FileField(upload_to=content_file_name_report)
    mother_nationality = models.ForeignKey('masters.CountryDetails', null=True, related_name='mother_nationality_rel',
                                           on_delete=models.PROTECT)
    mother_occupation = models.CharField(max_length=255, blank=True, null=True)
    mother_telephone_home = models.CharField(max_length=16, blank=True, null=True)
    mother_dob = models.DateField(blank=True, null=True)
    mother_email = models.EmailField(max_length=255, blank=True, null=True)

    is_submitted = models.BooleanField(default=False)
    application_id = models.CharField(max_length=100, blank=True, null=True)
    student = models.ForeignKey(StudentDetails, blank=True, null=True, related_name='student_applicant_rel',
                                on_delete=models.PROTECT)

    first_interview = models.BooleanField(default=False)
    first_interview_attend = models.BooleanField(default=False)
    first_interview_approval = models.BooleanField(default=False)
    psychometric_test = models.BooleanField(default=False)
    second_interview_attend = models.BooleanField(default=False)
    second_interview_approval = models.BooleanField(default=False)
    admin_approval = models.BooleanField(default=False)
    is_sponsored = models.BooleanField(default=False)

    scholarship_fee = models.CharField(max_length=15, blank=True, null=True)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def to_dict(self):
        res = {
            'id': self.id,
            'first_name': self.first_name,
            'birth_date': self.birth_date.isoformat(),
            'gender': self.gender,
            'address': self.address.to_dict(),
            'get_all_name': self.student.user.get_all_name(),
        }
        return res

    def to_application_dict(self):
        res = {
            'id': self.id,
            'country': self.address.country.to_dict() if self.address else '',
            'scholarship': self.applicant_scholarship_rel.all()[0].scholarship.to_dict() if self.applicant_scholarship_rel.all() else '',
            'university': self.applicant_scholarship_rel.all()[0].university.to_dict() if self.applicant_scholarship_rel.all() else '',
            'program':    self.applicant_module_rel.all()[0].program.to_dict() if self.applicant_module_rel.all() else '',
            'donor': self.student.student_donor_rel.all()[0].donor.to_dict() if self.student.student_donor_rel.all() else '',
            'balance': 0,
            'scholarship_fee': self.scholarship_fee if self.scholarship_fee else 0,
            'semester': self.applicant_progress_rel.all()[0].semester.to_dict() if self.applicant_progress_rel.all() else '',
            'degree': self.applicant_scholarship_rel.all()[0].course_applied.to_dict() if self.applicant_scholarship_rel.all() else '',
        }
        return res


class ApplicationHistoryDetails(BaseModel):
    status = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=1000, blank=True, null=True)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_history_rel',
                                     on_delete=models.PROTECT)

    class Meta:
        ordering = ('-id',)

class SiblingDetails(BaseModel):
    sibling_name = models.CharField(max_length=255, blank=True, null=True)
    sibling_age = models.IntegerField(blank=True, null=True)
    sibling_status = models.CharField(max_length=255, blank=True, null=True)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='sibling_applicant_rel',
                                     on_delete=models.PROTECT)


class AcademicQualificationDetails(BaseModel):
    a_level = models.CharField(max_length=255, blank=True, null=True)
    a_level_year = models.ForeignKey('masters.YearDetails', null=True, blank=True, related_name='a_level_year_rel',
                                     on_delete=models.PROTECT)
    a_level_result = models.CharField(max_length=255, blank=True, null=True)
    a_level_result_document = models.FileField(upload_to=content_file_name_report)

    o_level = models.CharField(max_length=255, blank=True, null=True)
    o_level_year = models.ForeignKey('masters.YearDetails', null=True, blank=True, related_name='o_level_year_rel',
                                     on_delete=models.PROTECT)
    o_level_result = models.CharField(max_length=255, blank=True, null=True)
    o_level_result_document = models.FileField(upload_to=content_file_name_report)

    high_school = models.CharField(max_length=255, blank=True, null=True)
    high_school_year = models.ForeignKey('masters.YearDetails', null=True, blank=True,
                                         related_name='high_school_year_rel',
                                         on_delete=models.PROTECT)
    high_school_result = models.CharField(max_length=255, blank=True, null=True)
    high_school_result_document = models.FileField(upload_to=content_file_name_report)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='academic_applicant_rel',
                                     on_delete=models.PROTECT)


class EnglishQualificationDetails(BaseModel):
    english_test_one = models.CharField(max_length=255, blank=True, null=True)
    english_test_one_year = models.ForeignKey('masters.YearDetails', null=True, blank=True,
                                              related_name='english_test_one_rel',
                                              on_delete=models.PROTECT)
    english_test_one_result = models.CharField(max_length=255, blank=True, null=True)
    english_test_one_result_document = models.FileField(upload_to=content_file_name_report)

    english_test_two = models.CharField(max_length=255, blank=True, null=True)
    english_test_two_year = models.ForeignKey('masters.YearDetails', null=True, blank=True,
                                              related_name='english_test_two_rel',
                                              on_delete=models.PROTECT)
    english_test_two_result = models.CharField(max_length=255, blank=True, null=True)
    english_test_two_result_document = models.FileField(upload_to=content_file_name_report)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='english_applicant_rel',
                                     on_delete=models.PROTECT)


class CurriculumDetails(BaseModel):
    curriculum_name_one = models.CharField(max_length=255, blank=True, null=True)
    curriculum_year_one = models.ForeignKey('masters.YearDetails', null=True, blank=True,
                                            related_name='curriculum_year_one_rel',
                                            on_delete=models.PROTECT)
    curriculum_result_document_one = models.FileField(upload_to=content_file_name_report, blank=True, null=True)

    curriculum_name_two = models.CharField(max_length=255, blank=True, null=True)
    curriculum_year_two = models.ForeignKey('masters.YearDetails', null=True, blank=True,
                                            related_name='curriculum_year_two_rel',
                                            on_delete=models.PROTECT)
    curriculum_result_document_two = models.FileField(upload_to=content_file_name_report, blank=True, null=True)

    curriculum_name_three = models.CharField(max_length=255, blank=True, null=True)
    curriculum_year_three = models.ForeignKey('masters.YearDetails', null=True, blank=True,
                                              related_name='curriculum_year_three_rel',
                                              on_delete=models.PROTECT)
    curriculum_result_document_three = models.FileField(upload_to=content_file_name_report, blank=True, null=True)

    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='curriculum_applicant_rel',
                                     on_delete=models.PROTECT)


class ExperienceDetails(BaseModel):
    work_experience_one = models.CharField(max_length=255, blank=True, null=True)
    from_date_one = models.DateField(null=True, blank=True, )
    to_date_one = models.DateField(null=True, blank=True, )
    work_experience_document_one = models.FileField(upload_to=content_file_name_report)

    work_experience_two = models.CharField(max_length=255, blank=True, null=True)
    from_date_two = models.DateField(null=True, blank=True, )
    to_date_two = models.DateField(null=True, blank=True, )
    work_experience_document_two = models.FileField(upload_to=content_file_name_report)

    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_experience_rel',
                                     on_delete=models.PROTECT)


class ScholarshipSelectionDetails(BaseModel):
    scholarship = models.ForeignKey('masters.ScholarshipDetails', null=True, related_name='scholarship_selection_rel',
                                    on_delete=models.PROTECT)
    course_applied = models.ForeignKey('masters.DegreeDetails', blank=True, null=True,
                                       related_name='degree_scholarship_rel',
                                       on_delete=models.PROTECT)

    # course_applied = models.CharField(max_length=255, blank=True, null=True)
    # university = models.CharField(max_length=255, blank=True, null=True)

    university = models.ForeignKey('masters.UniversityDetails', blank=True, null=True,
                                   related_name='university_scholarship_rel',
                                   on_delete=models.PROTECT)

    admission_letter_document = models.FileField(upload_to=content_file_name_report)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_scholarship_rel',
                                     on_delete=models.PROTECT)


class ApplicantAboutDetails(BaseModel):
    about_yourself = models.CharField(max_length=255, blank=True, null=True)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_about_rel',
                                     on_delete=models.PROTECT)


class ApplicantPsychometricTestDetails(BaseModel):
    # application_id = models.CharField(max_length=255, blank=True, null=True)
    result = models.CharField(max_length=255, blank=True, null=True)
    test_result_document = models.FileField(upload_to=content_file_name_report)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_psychometric_test_rel',
                                     on_delete=models.PROTECT)


class ApplicantAgreementDetails(BaseModel):
    four_parties_agreement_document = models.FileField(upload_to=content_file_name_report)
    education_loan_agreement_document = models.FileField(upload_to=content_file_name_report)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_agreement_rel',
                                     on_delete=models.PROTECT)


class ApplicantAcademicProgressDetails(BaseModel):
    year = models.ForeignKey('masters.YearDetails', null=True, related_name='applicant_progress_year_rel',
                             on_delete=models.PROTECT)
    date = models.DateField()
    semester = models.ForeignKey('masters.SemesterDetails', null=True, related_name='applicant_progress_semester_rel',
                                 on_delete=models.PROTECT)
    gpa_scored = models.CharField(max_length=255, blank=True, null=True)
    gpa_from = models.CharField(max_length=255, blank=True, null=True)
    cgpa_scored = models.CharField(max_length=255, blank=True, null=True)
    cgpa_from = models.CharField(max_length=255, blank=True, null=True)
    transcript_document = models.FileField(upload_to=content_file_name_report)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_progress_rel',
                                     on_delete=models.PROTECT)


class ApplicantDevelopmentProgramDetails(BaseModel):
    module = models.ForeignKey('masters.ModuleDetails', null=True, related_name='development_program_module_rel',
                               on_delete=models.PROTECT)
    certificate_document = models.FileField(upload_to=content_file_name_report)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='development_program_applicant_rel',
                                     on_delete=models.PROTECT)
