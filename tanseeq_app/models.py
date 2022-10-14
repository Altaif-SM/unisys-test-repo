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

