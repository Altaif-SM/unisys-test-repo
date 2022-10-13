import uuid
from django.db import models
from common.models import BaseModel
from masters.models import UniversityDetails, YearDetails
from accounts.models import User
from masters.helpers import university_logo_upload_path, tanseeq_guide_upload_path, registration_guide_upload_path
# Create your models here.

class TanseeqUniversityDetails(BaseModel):
    university_name = models.CharField(max_length=255, blank=True, null=True)
    university_code = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    university_logo = models.ImageField(upload_to=university_logo_upload_path, max_length=255, blank=True, null=True)
    tanseeq_guide = models.FileField(upload_to=tanseeq_guide_upload_path, max_length=255, blank=True, null=True)
    registration_guide = models.FileField(upload_to=registration_guide_upload_path, max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_details = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_registration = models.BooleanField(default=True)
    is_singup = models.BooleanField(default=True)
    university_type = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.university_name


class TanseeqPeriod(BaseModel):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    universities = models.ManyToManyField(TanseeqUniversityDetails, related_name="tansseq_period_univeristy")
    academic_year = models.ForeignKey(
        YearDetails, related_name="tanseeq_periord_academic_year", on_delete=models.PROTECT
    )
    from_date = models.DateField()
    to_date = models.DateField()
    is_active = models.BooleanField(default=True)


class SecondarySchoolCetificate(BaseModel):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    school_certificate = models.CharField(max_length=150, blank=True, null=True)


class UniversityAttachment(BaseModel):

    ATTACHMENT_TYPES = (
        ("pdf", "PDF"),
        ("jpeg", "JPEG"),
    )

    universities = models.ManyToManyField(UniversityDetails, related_name="univeristy_attachment_university_details")
    attachment_name = models.CharField(max_length=255)
    type_of_attachment = models.CharField(choices=ATTACHMENT_TYPES, max_length=50)
    is_required = models.BooleanField(default=True)

class TansseqCity(BaseModel):
    city = models.CharField(max_length=100, blank=True, null=True)

class TanseeqCountry(BaseModel):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    country_name = models.CharField(max_length=100, blank=True, null=True)
    cities = models.ManyToManyField(TansseqCity, related_name='tansseq_country_city' )