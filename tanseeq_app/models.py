import uuid
from django.db import models
from common.models import BaseModel
from masters.models import UniversityDetails, YearDetails
from accounts.models import User
# Create your models here.


class TanseeqPeriod(BaseModel):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    university = models.ForeignKey(
        UniversityDetails, related_name="tanseeq_periord_university", on_delete=models.PROTECT
    )
    academic_year = models.ForeignKey(
        YearDetails, related_name="tanseeq_periord_academic_year", on_delete=models.PROTECT
    )
    from_date = models.DateField()
    to_date = models.DateField()
    is_active = models.BooleanField(default=True)


