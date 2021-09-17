from django.db import models
from common.models import BaseModel
from masters.models import *

# Create your models here.
class OrderDetails(BaseModel):
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    currency_code = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('accounts.User', null=True, related_name='order_user_rel', on_delete=models.PROTECT)
    application_id = models.ForeignKey(ApplicationDetails, null=True, related_name='order_application_rel',
                                       on_delete=models.PROTECT)
    class Meta:
        ordering = ('-id',)