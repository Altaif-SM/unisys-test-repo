from django import forms
from tanseeq_app.models import (
    ApplicationDetails,
    SecondaryCertificateInfo,
    AppliedPrograms,
    ApplicantAttachment,
)


class ApplicationInfoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ApplicationInfoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                    "required": "true",
                })

    class Meta:
        model = ApplicationDetails
        fields = ("first_name","last_name","gender_type", "birth_date", "nationality", "country", "city",
            "contact_number", "address",
        )

        widgets = {
            'birth_date': forms.DateInput(attrs={'placeholder':'Select a date', 'type':'date'}),
            'address': forms.Textarea(attrs={'rows':'2'}),
        }


class SecondaryCertificationForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(SecondaryCertificationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                    "required": "true",
                })

    class Meta:
        model = SecondaryCertificateInfo
        fields = ("year", "secondary_certificate", "seat_number", "average", "school_name", "country", "city",)


class StudentStudyModeForm(forms.ModelForm):
    
    class Meta:
        model = SecondaryCertificateInfo
        fields = ("study_mode",)

    def __init__(self, *args, **kwargs):
        super(StudentStudyModeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
                "required": "true",
            })


class ApplyProgramForm(forms.ModelForm):

    class Meta:
        model = AppliedPrograms
        fields = ("user", "program_details",)


class ApplicantAttachementsForm(forms.ModelForm):

    class Meta:
        model = ApplicantAttachment
        fields = ('photo','school_certificate',)
