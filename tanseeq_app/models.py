import uuid
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

    study_mode = models.ForeignKey(StudyModeDetails, on_delete=models.PROTECT)
    faculty = models.ForeignKey(TanseeqFaculty, on_delete=models.PROTECT)
    program = models.ForeignKey(TanseeqProgram, on_delete=models.PROTECT)
    type_of_secondary = models.ForeignKey(SecondarySchoolCetificate, on_delete=models.PROTECT)
    year = models.IntegerField(
        _('year'), choices=YEAR_CHOICES, validators=[MinValueValidator(1984), max_value_current_year]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    average = models.FloatField(max_length=50)
    capacity = models.IntegerField(max_length=50)
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
