from dataclasses import fields
from datetime import datetime
from django import forms
from masters.models import UniversityDetails
from tanseeq_app.models import (
    TanseeqPeriod,
    SecondarySchoolCetificate,
    UniversityAttachment,
    StudyMode,
    TanseeqFaculty,
    TanseeqProgram,
)


class TanseeqPeriodForm(forms.ModelForm):

    class Meta:
        model = TanseeqPeriod
        fields = ('universities', 'academic_year', 'from_date', 'to_date', 'is_active',)

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


class StudyModeForm(forms.ModelForm):
    class Meta:
        model = StudyMode
        fields = ("universities", "study_mode", "code", "is_active",)

        def __init__(self, *args, **kwargs):
            super(StudyModeForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                if field != "is_active":
                    self.fields[field].widget.attrs.update({
                        "class": "form-control",
                        "required": "true",
                    })


class TanseeqFacultyForm(forms.ModelForm):
    class Meta:
        model = TanseeqFaculty
        fields = ("universities", "code", "name", "notes", "is_active",)

    def __init__(self, *args, **kwargs):
        super(TanseeqFacultyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                    "required": "true",
                })


class TanseeqProgramForm(forms.ModelForm):
    class Meta:
        model = TanseeqProgram
        fields = ("faculty", "name", "code", "is_active",)

    def __init__(self, *args, **kwargs):
        super(TanseeqProgramForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                    "required": "true",
                })
