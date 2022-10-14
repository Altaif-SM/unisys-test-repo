from django.contrib import admin
from tanseeq_app.models import (
    TanseeqPeriod,
    UniversityAttachment,
    TanseeqFaculty,
    TanseeqProgram,
)

# Register your models here.
admin.site.register(TanseeqPeriod)
admin.site.register(UniversityAttachment)
admin.site.register(TanseeqFaculty)
admin.site.register(TanseeqProgram)
