from django.db import models
from common.models import BaseModel
import os
from datetime import datetime
from masters.models import *
from accounts.models import *
import computed_property
from django.conf import settings


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


def content_aplicant_file_name_report(instance, filename):
    dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.applicant_id.first_name, dirname, ext)
    return os.path.join('reports', filename)


def year():
    now = datetime.now().year
    year_list = []

    for year in range(1960, now):
        year_list.append((year, year))

    year_list = tuple(year_list)
    return year_list


# YEAR_CHOICES = year()

class PassingYear(BaseModel):
    year = models.CharField(max_length=10)

    def __str__(self):
        return str(self.year)

    class Meta:
        ordering = ('-id',)


class AgentDetails(BaseModel):
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)

class StudentDetails(BaseModel):
    # student_name = computed_property.ComputedCharField(compute_from='student_full_name', null=True, max_length=250)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=25, null=True)
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
            ('can_view_scholarship_selection', 'can view scholarship selection'),
            ('can_view_my_application', 'can view my application'),
            ('can_view_student_psychometric_test', 'can view student psychometric test'),
            ('can_view_student_agreements', 'can view student agreements'),
            ('can_view_student_development_program', 'can view student development program certificate'),
            ('can_view_student_academic_progress', 'can view student academic progress'),
            ('can_view_student_application_progress_history', 'can view student application progress history'),
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
            'address': self.address.to_dict(),
            # 'get_all_name': self.get_all_name(),
        }
        return res

    def to_short_dict(self):
        res = {
            'id': self.id,
            'get_all_name': self.user.get_full_name() if self.user else "",
        }
        return res

    @property
    def student_full_name(self):
        return self.user.get_full_name() if self.user else ''


class ApplicationDetails(BaseModel):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)

    year = models.ForeignKey('masters.YearDetails', blank=True, null=True, related_name='applicant_year_rel',
                             on_delete=models.PROTECT)
    semester = models.ForeignKey('masters.SemesterDetails', blank=True, null=True,
                                 related_name='applicant_semester_rel', on_delete=models.PROTECT)

    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=25, blank=True, null=True, )
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
    passport_image = models.FileField(upload_to=content_file_name_image, blank=True, null=True)

    address = models.ForeignKey('masters.AddressDetails', blank=True, null=True, related_name='applicant_address_rel',
                                on_delete=models.PROTECT)
    permanent_address = models.ForeignKey('masters.AddressDetails', blank=True, null=True,
                                          related_name='applicant_permanent_address_rel', on_delete=models.PROTECT)
    telephone_hp = models.CharField(max_length=16, blank=True, null=True)
    telephone_home = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    image = models.FileField(upload_to=content_file_name_image)

    wife_name = models.CharField(max_length=255, blank=True, null=True)
    wife_income = models.CharField(max_length=10, blank=True, null=True)
    wife_pay_slip = models.FileField(upload_to=content_file_name_report)
    wife_nationality = models.CharField(max_length=50, blank=True, null=True)
    wife_home_address = models.CharField(max_length=255, blank=True, null=True)
    # wife_nationality = models.ForeignKey('masters.CountryDetails', null=True, related_name='wife_nationality_rel',on_delete=models.PROTECT)

    wife_occupation = models.CharField(max_length=255, blank=True, null=True)
    wife_telephone_home = models.CharField(max_length=16, blank=True, null=True)
    wife_dob = models.DateField(blank=True, null=True)
    wife_email = models.EmailField(max_length=255, blank=True, null=True)

    father_name = models.CharField(max_length=255, blank=True, null=True)
    father_income = models.CharField(max_length=10, blank=True, null=True)
    father_pay_slip = models.FileField(upload_to=content_file_name_report)
    father_nationality = models.CharField(max_length=50, blank=True, null=True)
    father_home_address = models.CharField(max_length=255, blank=True, null=True)

    # father_nationality = models.ForeignKey('masters.CountryDetails', blank=True, null=True, related_name='father_nationality_rel', on_delete=models.PROTECT)

    father_occupation = models.CharField(max_length=255, blank=True, null=True)
    father_telephone_home = models.CharField(max_length=16, blank=True, null=True)
    father_dob = models.DateField(blank=True, null=True)
    father_email = models.EmailField(max_length=255, blank=True, null=True)

    mother_name = models.CharField(max_length=255, blank=True, null=True)
    mother_income = models.CharField(max_length=10, blank=True, null=True)
    mother_pay_slip = models.FileField(upload_to=content_file_name_report)
    mother_nationality = models.CharField(max_length=50, blank=True, null=True)
    mother_home_address = models.CharField(max_length=255, blank=True, null=True)
    # mother_nationality = models.ForeignKey('masters.CountryDetails', null=True, related_name='mother_nationality_rel',on_delete=models.PROTECT)

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
    application_rejection = models.BooleanField(default=False)


    scholarship_fee = models.CharField(max_length=15, blank=True, null=True)

    interview_time = models.CharField(max_length=30, blank=True, null=True)
    interview_date = models.CharField(max_length=50, blank=True, null=True)
    interview_venue = models.CharField(max_length=500, blank=True, null=True)

    second_interview_time = models.CharField(max_length=30, blank=True, null=True)
    second_interview_date = models.CharField(max_length=50, blank=True, null=True)
    second_interview_venue = models.CharField(max_length=500, blank=True, null=True)

    personal_info_flag = models.BooleanField(default=True)

    is_sponsored = models.BooleanField(default=False)
    is_online_admission = models.BooleanField(default=False)

    # family_info_flag = models.BooleanField(default=False)
    # mother_sibling_info_flag = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_on',)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name if self.last_name else '')
        return full_name.strip()

    def get_full_name_with_father(self):

        full_name = '%s %s %s' % (self.first_name,self.middle_name if self.middle_name else '', self.last_name if self.last_name else '')
        return full_name.strip()

    def report_path(self):
        """
        Return the path plus the id, with a _ in between.
        """
        return str(settings.MEDIA_URL) + str('reports/') + str(self.first_name) + '_' + str(self.id) + '/'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name if self.last_name else '')

    def calculate_balance_amount(self):
        voucher_amount = 0.00
        for obj in self.rel_student_payment_receipt_voucher.all():
            if obj.voucher_type == "credit":
                voucher_amount += float(obj.voucher_amount)

        return float(self.scholarship_fee) - float(voucher_amount)

    def calculate_student_payment_balance_amount(self):
        voucher_amount = float(self.scholarship_fee)
        for obj in self.rel_student_payment_receipt_voucher.all():
            if obj.voucher_type == "debit":
                voucher_amount -= float(obj.voucher_amount)

        return float(voucher_amount)

    def calculate_student_repayment_balance(self):
        from masters.models import DegreeFormula
        # voucher_amount = float(self.scholarship_fee)
        repayment_percent = 0

        try:

            if self.applicant_scholarship_rel.get().degree.degree_type.degree_name == 'phd':
                if self.applicant_scholarship_rel.get().degree.degree_type.degree_formula_degree_type_relation.filter(
                        result=self.applicant_progress_rel.all()[0].result,
                        scholarship_id=self.applicant_scholarship_rel.all()[0].scholarship.id).exists():

                    repayment_percent = self.applicant_scholarship_rel.get().degree.degree_type.degree_formula_degree_type_relation.filter(
                        result=self.applicant_progress_rel.all()[0].result,
                        scholarship_id=self.applicant_scholarship_rel.all()[0].scholarship.id)[0].repayment


            elif self.applicant_scholarship_rel.get().degree.degree_type.degree_name == 'masters (course work)':
                if self.applicant_scholarship_rel.get().degree.degree_type.degree_formula_degree_type_relation.filter(
                        cgpa_min__lte=int(self.applicant_progress_rel.all()[0].cgpa_scored),
                        cgpa_max__gte=int(self.applicant_progress_rel.all()[0].cgpa_from),
                        scholarship_id=self.applicant_scholarship_rel.all()[0].scholarship.id).exists():
                    repayment_percent = self.applicant_scholarship_rel.get().degree.degree_type.degree_formula_degree_type_relation.filter(
                        cgpa_min__lte=int(self.applicant_progress_rel.all()[0].cgpa_scored),
                        cgpa_max__gte=int(self.applicant_progress_rel.all()[0].cgpa_from),
                        scholarship_id=self.applicant_scholarship_rel.all()[0].scholarship.id)[0].repayment

            else:
                if self.applicant_scholarship_rel.get().degree.degree_type.degree_formula_degree_type_relation.filter(
                        cgpa_min__lte=int(self.applicant_progress_rel.all()[0].cgpa_scored),
                        cgpa_max__gte=int(self.applicant_progress_rel.all()[0].cgpa_from),
                        scholarship_id=self.applicant_scholarship_rel.all()[0].scholarship.id).exists():

                    repayment_percent = self.applicant_scholarship_rel.get().degree.degree_type.degree_formula_degree_type_relation.filter(
                        cgpa_min__lte=int(self.applicant_progress_rel.all()[0].cgpa_scored),
                        cgpa_max__gte=int(self.applicant_progress_rel.all()[0].cgpa_from),
                        scholarship_id=self.applicant_scholarship_rel.all()[0].scholarship.id)[0].repayment
        except:
            pass

        if repayment_percent:
            voucher_amount = (
                    (int(self.scholarship_fee) * int(repayment_percent)) / float(100))
        else:
            voucher_amount = float(self.scholarship_fee)

        for obj in self.rel_student_payment_receipt_voucher.all():
            if obj.voucher_type == "credit":
                voucher_amount -= float(obj.voucher_amount)

        return float(voucher_amount)

    def calculate_student_repayment_amount(self):
        from masters.models import DegreeFormula, MasterAndPhdFormula, MasterAndCourseFormula

        repayment_percent = 0

        try:
            if self.applicant_scholarship_rel.get().degree.degree_type.degree_name == 'phd':
                # if self.applicant_scholarship_rel.get().degree.degree_type.degree_formula_degree_type_relation.filter(
                #         result=self.applicant_progress_rel.all()[0].result,
                #         scholarship_id=self.applicant_scholarship_rel.all()[0].scholarship.id).exists():
                #
                #     repayment_percent = self.applicant_scholarship_rel.get().degree.degree_type.degree_formula_degree_type_relation.filter(
                #         result=self.applicant_progress_rel.all()[0].result,
                #         scholarship_id=self.applicant_scholarship_rel.all()[0].scholarship.id)[0].repayment

                if self.applicant_progress_rel.all()[0].is_approved:
                    if (self.applicant_progress_rel.all()[0].result == 'Pass'):
                       return float(0.0)
                    elif (self.applicant_progress_rel.all()[0].result == 'Fail'):
                        repayment_percent = 100
                    else:
                        pass


            elif self.applicant_scholarship_rel.get().degree.degree_type.degree_name == 'masters (course work)':
                if self.applicant_scholarship_rel.get().degree.degree_type.degree_formula_degree_type_relation.filter(
                        cgpa_min__lte=int(self.applicant_progress_rel.all()[0].cgpa_scored),
                        cgpa_max__gte=int(self.applicant_progress_rel.all()[0].cgpa_from),
                        scholarship_id=self.applicant_scholarship_rel.all()[0].scholarship.id).exists():
                    repayment_percent = self.applicant_scholarship_rel.get().degree.degree_type.degree_formula_degree_type_relation.filter(
                        cgpa_min__lte=int(self.applicant_progress_rel.all()[0].cgpa_scored),
                        cgpa_max__gte=int(self.applicant_progress_rel.all()[0].cgpa_from),
                        scholarship_id=self.applicant_scholarship_rel.all()[0].scholarship.id)[0].repayment

            else:
                # if self.applicant_scholarship_rel.get().degree.degree_type.degree_formula_degree_type_relation.filter(
                #         cgpa_min__lte=int(self.applicant_progress_rel.all()[0].cgpa_scored),
                #         cgpa_max__gte=int(self.applicant_progress_rel.all()[0].cgpa_from),
                #         scholarship_id=self.applicant_scholarship_rel.all()[0].scholarship.id).exists():
                #     degree_name = self.applicant_scholarship_rel.get().degree.degree_type.degree_name
                #     DegreeFormula.objects.filter(cgpa_min__lte=int(self.applicant_progress_rel.all()[0].cgpa_scored), cgpa_max__gte=int(self.applicant_progress_rel.all()[0].cgpa_from,
                #                                  degree_type__degree_name=degree_name))


                    # repayment_percent = self.applicant_scholarship_rel.get().degree.degree_type.degree_formula_degree_type_relation.filter(
                    #     cgpa_min__lte=int(self.applicant_progress_rel.all()[0].cgpa_scored),
                    #     cgpa_max__gte=int(self.applicant_progress_rel.all()[0].cgpa_from),
                    #     scholarship_id=self.applicant_scholarship_rel.all()[0].scholarship.id)[0].repayment
                if self.applicant_progress_rel.all()[0].is_approved:
                    if (float(self.applicant_progress_rel.all()[0].cgpa_scored) <= float(2.99)):
                        repayment_percent = 50
                    elif (float(self.applicant_progress_rel.all()[0].cgpa_scored) <= float(3.29)):
                        repayment_percent = 30
                    elif (float(self.applicant_progress_rel.all()[0].cgpa_scored) <= float(3.49)):
                        repayment_percent = 10
                    elif (float(self.applicant_progress_rel.all()[0].cgpa_scored) <= float(4.00)):
                        return float(0.0)
                    else:
                        pass
        except:
            pass

        if repayment_percent:
            voucher_amount = ((int(self.scholarship_fee) * int(repayment_percent)) / float(100))
        else:
            voucher_amount = float(self.scholarship_fee)

        return float(voucher_amount)

    def to_dict(self):
        res = {
            'id': self.id,
            'first_name': self.first_name,
            'birth_date': self.birth_date.isoformat(),
            'gender': self.gender,
            'address': self.address.to_dict(),
            'get_all_name': self.get_full_name(),
        }
        return res

    def to_dict_student_application(self):
        res = {
            'id': self.student.id,
            'get_all_name': self.get_full_name(),
        }
        return res

    def to_application_dict(self):
        res = {
            'id': self.id,
            'country': self.address.country.to_dict() if self.address else '',
            'scholarship': self.applicant_scholarship_rel.all()[
                0].scholarship.to_dict() if self.applicant_scholarship_rel.all() else '',
            'university': self.applicant_scholarship_rel.all()[
                0].university.to_dict() if self.applicant_scholarship_rel.all() else '',
            'program': self.applicant_module_rel.all()[0].program.to_dict() if self.applicant_module_rel.all() else '',
            'donor': self.student.student_donor_rel.all()[
                0].donor.to_dict() if self.student.student_donor_rel.all() else '',
            'balance': self.calculate_balance_amount() if self.rel_student_payment_receipt_voucher.all() else 0,
            'scholarship_fee': self.scholarship_fee if self.scholarship_fee else 0,
            'voucher_number': self.rel_student_payment_receipt_voucher.all()[
                0].voucher_number if self.rel_student_payment_receipt_voucher.all() else '',
            # 'semester': self.applicant_progress_rel.all()[0].semester.to_dict() if self.applicant_progress_rel.all() else '',
            'degree': self.applicant_scholarship_rel.all()[
                0].degree.to_dict() if self.applicant_scholarship_rel.all() else '',
            'student': self.to_dict_student_application() if self.first_name else '',
            'repayment_balance': self.calculate_student_repayment_balance() if self.applicant_scholarship_rel.all() else self.scholarship_fee if self.scholarship_fee else 0,
            'repayment_amount': self.calculate_student_repayment_amount() if self.applicant_scholarship_rel.all() else self.scholarship_fee if self.scholarship_fee else 0,
            'application_progress': self.applicant_progress_rel.all()[
                0].to_dict() if self.applicant_progress_rel.all() else '',
        }
        return res

    def to_student_payment_application_dict(self):
        res = {
            'id': self.id,
            'country': self.address.country.to_dict() if self.address else '',
            'scholarship': self.applicant_scholarship_rel.all()[
                0].scholarship.to_dict() if self.applicant_scholarship_rel.all() else '',
            'university': self.applicant_scholarship_rel.all()[
                0].university.to_dict() if self.applicant_scholarship_rel.all() else '',
            'program': self.applicant_module_rel.all()[0].program.to_dict() if self.applicant_module_rel.all() else '',
            'donor': self.student.student_donor_rel.all()[
                0].donor.to_dict() if self.student.student_donor_rel.all() else '',
            'balance': self.calculate_student_payment_balance_amount() if self.rel_student_payment_receipt_voucher.all() else 0,
            'scholarship_fee': self.scholarship_fee if self.scholarship_fee else 0,
            'voucher_number': self.rel_student_payment_receipt_voucher.all()[
                0].voucher_number if self.rel_student_payment_receipt_voucher.all() else '',
            'semester': self.applicant_progress_rel.all()[
                0].semester.to_dict() if self.applicant_progress_rel.all() else '',
            'degree': self.applicant_scholarship_rel.all()[
                0].degree.to_dict() if self.applicant_scholarship_rel.all() else '',
            'student': self.to_dict_student_application() if self.first_name else '',
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
    sibling_age = models.CharField(max_length=5, blank=True, null=True)
    sibling_status = models.CharField(max_length=255, blank=True, null=True)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='sibling_applicant_rel',
                                     on_delete=models.PROTECT)


class AcademicQualificationDetails(BaseModel):
    level = models.CharField(max_length=255, blank=True, null=True)
    level_year = models.CharField(max_length=6, blank=True, null=True)
    level_result = models.CharField(max_length=255, blank=True, null=True)
    level_institution = models.CharField(max_length=255, blank=True, null=True)
    level_result_document = models.FileField(upload_to=content_file_name_report)
    degree = models.CharField(max_length=256, blank=True, null=True)
    other_degree = models.CharField(max_length=256, blank=True, null=True)
    major = models.CharField(max_length=256, blank=True, null=True)
    country = models.ForeignKey('masters.CountryDetails', null=True, related_name='academic_country_rel', on_delete=models.PROTECT)
    # o_level = models.CharField(max_length=255, blank=True, null=True)
    # o_level_year = models.CharField(max_length=6, blank=True, null=True)
    # o_level_result = models.CharField(max_length=255, blank=True, null=True)
    # o_level_institution = models.CharField(max_length=255, blank=True, null=True)
    # o_level_result_document = models.FileField(upload_to=content_file_name_report)
    #
    # high_school = models.CharField(max_length=255, blank=True, null=True)
    # high_school_year = models.CharField(max_length=10, blank=True, null=True)
    # high_school_result = models.CharField(max_length=255, blank=True, null=True)
    # high_school_institution = models.CharField(max_length=255, blank=True, null=True)
    # high_school_result_document = models.FileField(upload_to=content_file_name_report)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='academic_applicant_rel',
                                     on_delete=models.PROTECT)


class EnglishQualificationDetails(BaseModel):
    english_test = models.CharField(max_length=255, blank=True, null=True)
    english_test_year = models.CharField(max_length=10, blank=True, null=True)
    english_test_result = models.CharField(max_length=255, blank=True, null=True)
    english_test_result_document = models.FileField(upload_to=content_file_name_report)

    # english_test_two = models.CharField(max_length=255, blank=True, null=True)
    # english_test_two_year = models.CharField(max_length=10, blank=True, null=True)
    # english_test_two_result = models.CharField(max_length=255, blank=True, null=True)
    # english_test_two_result_document = models.FileField(upload_to=content_file_name_report)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='english_applicant_rel',
                                     on_delete=models.PROTECT)
    english_qualification = models.BooleanField(default=True)
    english_competency_test = models.ForeignKey('masters.EnglishCompetencyTestDetails', null=True, related_name='english_competency_test_rel',
                                     on_delete=models.PROTECT)


class CurriculumDetails(BaseModel):
    curriculum_name = models.CharField(max_length=255, blank=True, null=True)
    curriculum_year = models.CharField(max_length=10, blank=True, null=True)
    curriculum_result_document = models.FileField(upload_to=content_file_name_report, blank=True, null=True)
    academic_qualification = models.BooleanField(default=True)

    # curriculum_name_two = models.CharField(max_length=255, blank=True, null=True)
    # curriculum_year_two = models.CharField(max_length=10, blank=True, null=True)
    # curriculum_result_document_two = models.FileField(upload_to=content_file_name_report, blank=True, null=True)
    #
    # curriculum_name_three = models.CharField(max_length=255, blank=True, null=True)
    # curriculum_year_three = models.CharField(max_length=10, blank=True, null=True)
    # curriculum_result_document_three = models.FileField(upload_to=content_file_name_report, blank=True, null=True)

    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='curriculum_applicant_rel',
                                     on_delete=models.PROTECT)


class ExperienceDetails(BaseModel):
    work_experience = models.CharField(max_length=255, blank=True, null=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    work_experience_document = models.FileField(upload_to=content_file_name_report)
    experience_current = models.BooleanField(default=False)

    # work_experience_two = models.CharField(max_length=255, blank=True, null=True)
    # from_date_two = models.DateField(null=True, blank=True)
    # to_date_two = models.DateField(null=True, blank=True, )
    # experience_two_current = models.BooleanField(default=False)
    # work_experience_document_two = models.FileField(upload_to=content_file_name_report)

    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_experience_rel',
                                     on_delete=models.PROTECT)


class PostgraduateDetails(BaseModel):
    qualification_name = models.CharField(max_length=255, blank=True, null=True)
    license_certificate_no = models.CharField(max_length=255, blank=True, null=True)
    professional_body = models.CharField(max_length=255, blank=True, null=True)
    awarded_date = models.DateField(null=True, blank=True)
    agency_name_no = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey('masters.CountryDetails', null=True, related_name='academic_postgraduate_country_rel',
                                on_delete=models.PROTECT)
    expiration_date = models.DateField(null=True, blank=True)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_postgraduate_rel',
                                     on_delete=models.PROTECT)




class ScholarshipSelectionDetails(BaseModel):
    scholarship = models.ForeignKey('masters.ScholarshipDetails', null=True, related_name='scholarship_selection_rel',
                                    on_delete=models.PROTECT)
    degree = models.ForeignKey('masters.DegreeDetails', blank=True, null=True,
                               related_name='degree_scholarship_rel',
                               on_delete=models.PROTECT)

    course_applied = models.ForeignKey('masters.ProgramDetails', blank=True, null=True,
                                       related_name='course_scholarship_rel',
                                       on_delete=models.PROTECT)

    university = models.ForeignKey('masters.UniversityDetails', blank=True, null=True,
                                   related_name='university_scholarship_rel',
                                   on_delete=models.PROTECT)

    admission_letter_document = models.FileField(upload_to=content_aplicant_file_name_report)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_scholarship_rel',
                                     on_delete=models.PROTECT)

    scholarship_selection = models.BooleanField(default=True)

    def __str__(self):
        degree = self.degree.degree_name if self.degree else ''
        course_applied = self.course_applied.program_name if self.course_applied else ''
        scholarship_selection = self.scholarship.scholarship_name if self.scholarship else ''
        res = degree + ' - ' + course_applied + ' - ' + scholarship_selection
        return res


class ApplicantAboutDetails(BaseModel):
    about_yourself = models.CharField(max_length=600, blank=True, null=True)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_about_rel',
                                     on_delete=models.PROTECT)
    # my_application = models.BooleanField(default=True)


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
    date = models.DateField(null=True, blank=True)
    semester = models.ForeignKey('masters.SemesterDetails', null=True, related_name='applicant_progress_semester_rel',
                                 on_delete=models.PROTECT)
    gpa_scored = models.CharField(max_length=255, blank=True, null=True)
    gpa_from = models.CharField(max_length=255, blank=True, null=True)
    cgpa_scored = models.CharField(max_length=255, blank=True, null=True)
    cgpa_from = models.CharField(max_length=255, blank=True, null=True)
    transcript_document = models.FileField(upload_to=content_file_name_report)
    is_approved = models.BooleanField(default=False)
    result = models.CharField(max_length=255, blank=True, null=True)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_progress_rel',
                                     on_delete=models.PROTECT)

    def __str__(self):
        return self.semester.semester_name

    class Meta:
        ordering = ('-created_on',)

    def to_dict(self):
        res = {
            'id': self.id if self.id else '',
            'gpa_from': self.gpa_from if self.gpa_from else '',
            'cgpa_scored': self.cgpa_scored if self.cgpa_scored else '',
            'cgpa_from': self.cgpa_from if self.cgpa_from else '',
            'is_approved': self.is_approved if self.is_approved else '',
            'semester': self.semester.to_dict() if self.semester else '',
            'year': self.year.to_dict() if self.year else '',
        }
        return res


class ApplicantDevelopmentProgramDetails(BaseModel):
    module = models.ForeignKey('masters.DevelopmentProgram', null=True, related_name='development_program_module_rel',
                               on_delete=models.PROTECT)
    certificate_document = models.FileField(upload_to=content_file_name_report)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='development_program_applicant_rel',
                                     on_delete=models.PROTECT)


class StudentNotifications(BaseModel):
    is_read = models.BooleanField(default=False)
    message = models.CharField(max_length=500, blank=True, null=True)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_notification_rel',
                                     on_delete=models.PROTECT)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.applicant_id.first_name


class AdminNotifications(BaseModel):
    is_read = models.BooleanField(default=False)
    message = models.CharField(max_length=500, blank=True, null=True)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='admin_notification_rel',
                                     on_delete=models.PROTECT)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.applicant_id.first_name


class EmployementHistoryDetails(BaseModel):
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey('masters.CountryDetails', null=True, related_name='employement_history_country_rel',
                                on_delete=models.PROTECT)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    industry_type = models.CharField(max_length=255, blank=True, null=True)
    employed_years = models.CharField(max_length=255, blank=True, null=True)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='employement_history_rel',
                                     on_delete=models.PROTECT)


class ApplicantAttachementDetails(BaseModel):
    image = models.FileField(upload_to='photo/', null=True, blank=True)
    passport_image = models.FileField(upload_to='document/', null=True, blank=True)
    level_result_document = models.FileField(upload_to='document/', null=True, blank=True)
    transcript_document = models.FileField(upload_to='document/', null=True, blank=True)
    english_test_result_document = models.FileField(upload_to='document/', null=True, blank=True)
    recommendation_letter = models.FileField(upload_to='document/', null=True, blank=True)
    applicant_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_attachement_rel',
                                     on_delete=models.PROTECT)


class AdditionInformationDetails(BaseModel):
    ken_name = models.CharField(max_length=255, blank=True, null=True)
    ken_id = models.CharField(max_length=255, blank=True, null=True)
    ken_relationship = models.CharField(max_length=255, blank=True, null=True)
    ken_tel_no = models.CharField(max_length=255, blank=True, null=True)
    ken_email = models.CharField(max_length=255, blank=True, null=True)

    is_sponsored = models.BooleanField(default=False)
    sponsore_organisation = models.CharField(max_length=255, blank=True, null=True)
    sponsore_address = models.CharField(max_length=255, blank=True, null=True)
    sponsore_email = models.CharField(max_length=255, blank=True, null=True)
    sponsore_contact = models.CharField(max_length=255, blank=True, null=True)

    ref_by_student = models.ForeignKey(StudentDetails, blank=True, null=True, related_name='student_additional_info',
                                       on_delete=models.PROTECT)
    ref_by_agent = models.ForeignKey(AgentDetails, blank=True, null=True,
                                     related_name='agent_additional_info',
                                     on_delete=models.PROTECT)
    application_id = models.ForeignKey(ApplicationDetails, null=True, related_name='applicant_addition_info',
                                     on_delete=models.PROTECT)
