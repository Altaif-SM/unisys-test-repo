from django.db import models
from common.models import BaseModel
from masters.models import *
# Create your models here.
class CorporateDetails(BaseModel):
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_registration_no = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey('masters.CountryDetails', null=True, related_name='corporate_country_rel',
                                on_delete=models.SET_NULL)
    address = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    website_url = models.CharField(max_length=150, blank=True, null=True)
    agent_profile = models.ForeignKey('masters.AgentIDDetails', null=True, related_name='corporate_agent_rel',
                                on_delete=models.SET_NULL)

class AgentPaymentDetails(BaseModel):
    agent_profile = models.ForeignKey('masters.AgentIDDetails', null=True, related_name='payment_agent_rel',
                                      on_delete=models.SET_NULL)

class AgentAttachementDetails(BaseModel):
    image = models.FileField(upload_to='photo/', null=True, blank=True)
    passport_image = models.FileField(upload_to='document/', null=True, blank=True)
    company_registration = models.FileField(upload_to='document/', null=True, blank=True)
    license_certificate = models.FileField(upload_to='document/', null=True, blank=True)
    agent_profile = models.ForeignKey('masters.AgentIDDetails', null=True, related_name='attachement_agent_rel',
                                      on_delete=models.SET_NULL)

