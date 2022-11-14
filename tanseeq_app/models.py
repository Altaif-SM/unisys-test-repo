import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from common.models import BaseModel
from accounts.models import User
from masters.models import (
    UniversityDetails,
    YearDetails,
    StudyModeDetails
)
from tanseeq_app.helpers import profile_picture_upload_path, school_certificate_upload_path
# Create your models here.


class TanseeqPeriod(BaseModel):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    universities = models.ManyToManyField(UniversityDetails, related_name="tansseq_period_univeristy_details")
    academic_year = models.ForeignKey(
        YearDetails, related_name="tanseeq_periord_academic_year", on_delete=models.PROTECT
    )
    from_date = models.DateField()
    to_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}-{}".format(self.from_date, self.to_date)


class SecondarySchoolCetificate(BaseModel):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    school_certificate = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.school_certificate


class UniversityAttachment(BaseModel):

    ATTACHMENT_TYPES = (
        ("pdf", "PDF"),
        ("jpeg", "JPEG"),
    )

    universities = models.ManyToManyField(UniversityDetails, related_name="univeristy_attachment_university_details")
    attachment_name = models.CharField(max_length=255)
    type_of_attachment = models.CharField(choices=ATTACHMENT_TYPES, max_length=50)
    is_required = models.BooleanField(default=True)

    def __str__(self):
        return self.attachment_name


class TanseeqFaculty(BaseModel):
    universities = models.ManyToManyField(UniversityDetails, related_name="tanseeq_faculty_university_details")
    code = models.CharField(max_length=255) # auto generated
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        pass

    def __str__(self):
        return self.name


class TanseeqProgram(BaseModel):
    university = models.ForeignKey(UniversityDetails, related_name="tanseeq_program_tanseeq_program", null=True, on_delete=models.PROTECT)
    faculty = models.ForeignKey(TanseeqFaculty, related_name="tanseeq_program_tanseeq_faculty", on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        pass

    def __str__(self):
        return self.name


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class ConditionFilters(BaseModel):
    YEAR_CHOICES = [(r,r) for r in range(1984, datetime.date.today().year+1)]

    university = models.ForeignKey(UniversityDetails, on_delete=models.PROTECT, null=True)
    faculty = models.ForeignKey(TanseeqFaculty, on_delete=models.PROTECT)
    study_mode = models.ForeignKey(StudyModeDetails, on_delete=models.PROTECT)
    program = models.ForeignKey(TanseeqProgram, on_delete=models.PROTECT)
    type_of_secondary = models.ForeignKey(SecondarySchoolCetificate, on_delete=models.PROTECT)
    year = models.IntegerField(
        _('year'), choices=YEAR_CHOICES, blank=True, null=True, validators=[MinValueValidator(1984), max_value_current_year]
    )
    academic_year = models.ForeignKey(
        YearDetails, related_name="condition_filter_academic_year", on_delete=models.PROTECT, null=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    average = models.FloatField(max_length=50, validators=[MinValueValidator(0), MaxValueValidator(100)])
    capacity = models.IntegerField()
    fee = models.FloatField(max_length=50)
    is_exam = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Condition Filters"
        verbose_name_plural = "Condition Filters"


    # def __str__(self):
    #     return self.name


class TanseeqFee(BaseModel):
    universities = models.ManyToManyField(UniversityDetails, related_name="tanseeq_fee_university_details")
    faculty = models.ForeignKey(TanseeqFaculty, related_name="tanseeq_fee_faculty",
                                on_delete=models.PROTECT)
    fee = models.FloatField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)


class Course(BaseModel):
    course = models.CharField(max_length=100, blank=True, null=True)
    mark = models.FloatField(max_length=50, null=True)


class TanseeqCourses(BaseModel):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    course_name = models.CharField(max_length=100, blank=True, null=True)
    courses = models.ManyToManyField(Course, related_name='tansseq_course_details' )


class ApplicationDetails(BaseModel):
    GENDER_TYPE = (
        ("male", "MALE"),
        ("female", "FEMALE"),
    )
    APPLICATION_STATUS = (
        ("Submitted", "SUBMITTED"),
        ("Not Submitted", "NOT SUBMITTED"),
    )
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    gender_type = models.CharField(choices=GENDER_TYPE, max_length=50)
    application_status = models.CharField(choices=APPLICATION_STATUS, default='Not Submitted', max_length=50)
    birth_date = models.DateField()
    nationality = models.ForeignKey('masters.CountryDetails', null=True, related_name='student_nationality_details', on_delete=models.PROTECT)
    country = models.ForeignKey('masters.CountryDetails', null=True, related_name='student_country_details', on_delete=models.PROTECT)
    city = models.ForeignKey('masters.CitiDetails', null=True, related_name='student_city_details', on_delete=models.PROTECT)
    district = models.CharField(max_length=150, blank=True, null=True)
    contact_number = models.CharField(max_length=12, blank=True, null=True)
    user = models.ForeignKey(User, null=True, related_name='student_user_details', on_delete=models.PROTECT)
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    tanseeq_id = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT,null=True,)

    def save(self, *args, **kwargs):
        User.objects.filter(id=self.user_id).update(
        first_name = self.first_name,
        last_name = self.last_name
        )
        super(ApplicationDetails, self).save(args, kwargs)


class SecondaryCertificateInfo(BaseModel):
    YEAR_CHOICES = [(r, r) for r in range(1984, datetime.date.today().year + 1)]
    year = models.IntegerField(
        _('year'), choices=YEAR_CHOICES, validators=[MinValueValidator(1984), max_value_current_year], blank=True, null=True
    )
    academic_year = models.ForeignKey(
        YearDetails, related_name="secondary_certificate_academic_year", on_delete=models.PROTECT, null=True
    )
    secondary_certificate = models.ForeignKey(SecondarySchoolCetificate, null=True, related_name='student_secondary_certificate_details', on_delete=models.PROTECT)
    seat_number = models.CharField(max_length=50, blank=True, null=True)
    average = models.FloatField(max_length=50)
    school_name = models.CharField(max_length=150, blank=True, null=True)
    country = models.ForeignKey('masters.CountryDetails', null=True, related_name='student_secondary_country_details',
                                on_delete=models.PROTECT)
    city = models.ForeignKey('masters.CitiDetails', null=True, related_name='student_secondary_city_details',
                             on_delete=models.PROTECT)
    application = models.ForeignKey(ApplicationDetails, null=True, related_name='student_secondary_application_details',
                             on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT,null=True,)
    study_mode = models.ForeignKey(StudyModeDetails, on_delete=models.PROTECT, blank=True, null=True,)


class ApplicantAttachment(BaseModel):
    application = models.ForeignKey(ApplicationDetails, null=True, related_name='student_attachement_application',on_delete=models.PROTECT)
    photo = models.ImageField(upload_to=profile_picture_upload_path, max_length=256, blank=True, null=True)
    school_certificate = models.ImageField(upload_to=school_certificate_upload_path, max_length=256, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True,)


class AppliedPrograms(BaseModel):
    REVIEW_STATUS = (
        (0, "Not Acceptable"),
        (1, "Accepted")
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    program_details = models.ForeignKey(ConditionFilters, on_delete=models.PROTECT)
    bond_no = models.CharField(max_length=255, blank=True, null=True)
    is_denied = models.BooleanField(default=False)
    review_status = models.IntegerField(choices=REVIEW_STATUS, max_length=50, blank=True, null=True)
    review_note = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Applied Program"
        verbose_name_plural = "Applied Programs"

    def __str__(self):
        return "{} - {}".format(self.user.username, self.program_details.program.name)
