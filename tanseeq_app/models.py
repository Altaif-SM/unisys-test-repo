import uuid
from django.db import models
from common.models import BaseModel
from masters.models import UniversityDetails, YearDetails
from accounts.models import User
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


class StudyMode(BaseModel):
    universities = models.ManyToManyField(UniversityDetails, related_name="study_mode_university_details")
    study_mode = models.CharField(max_length=150,blank=True, null=True)
    code = models.CharField(max_length=50,blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.study_mode


class TanseeqFaculty(BaseModel):
    universities = models.ManyToManyField(UniversityDetails, related_name="tanseeq_faculty_university_details")
    code = models.CharField(max_length=255)
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