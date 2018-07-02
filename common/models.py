from django.db import models

# Create your models here.
class BaseModel(models.Model):
    last_updated = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True