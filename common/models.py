from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
