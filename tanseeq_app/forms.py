from datetime import datetime
from django import forms
from masters.models import UniversityDetails
from tanseeq_app.models import (
    TanseeqPeriod,
    SecondarySchoolCetificate,
    UniversityAttachment,
    TanseeqUniversityDetails,
)


class TanseeqPeriodForm(forms.ModelForm):

    class Meta:
        model = TanseeqPeriod
        fields = ('university', 'academic_year', 'from_date', 'to_date', 'is_active',)

    def clean(self):
        from_date = self.cleaned_data.get("from_date")
        to_date = self.cleaned_data.get("to_date")
        if from_date >= to_date:
            raise forms.ValidationError(
                'To Date must be greater than From Date.',
                code='incorrect_value',
            )


class UniversityDetailsForm(forms.ModelForm):

    class Meta:
        model = UniversityDetails
        fields = ('file',)


class SecondarySchoolCertificateForm(forms.ModelForm):

    class Meta:
        model = SecondarySchoolCetificate
        fields = ('school_certificate',)


class UniversityAttachmentForm(forms.ModelForm):
    class Meta:
        model = UniversityAttachment
        fields = ("universities", "attachment_name", "type_of_attachment", "is_required",)

    def __init__(self, *args, **kwargs):
        super(UniversityAttachmentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_required":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                    "required": "true",
                })

class UniversityForm(forms.ModelForm):
    class Meta:
        model = TanseeqUniversityDetails
        fields = ("university_name", "university_code", "email", "telephone", "website", "university_logo", "tanseeq_guide", "registration_guide", "address", "contact_details", "is_active", "is_registration", "is_singup", "university_type",)


