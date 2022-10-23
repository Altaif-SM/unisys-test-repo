from django.contrib import admin
from tanseeq_app.models import (
    TanseeqPeriod,
    UniversityAttachment,
    TanseeqFaculty,
    TanseeqProgram,
    ConditionFilters,
    SecondarySchoolCetificate,
    ApplicationDetails,
    SecondaryCertificateInfo,
)

# Register your models here.
admin.site.register(TanseeqPeriod)
admin.site.register(UniversityAttachment)
admin.site.register(TanseeqFaculty)
admin.site.register(TanseeqProgram)
admin.site.register(ConditionFilters)
admin.site.register(SecondarySchoolCetificate)
admin.site.register(ApplicationDetails)
admin.site.register(SecondaryCertificateInfo)
