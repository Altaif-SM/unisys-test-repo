from django import forms
from masters.models import UniversityDetails, StudyModeDetails
from tanseeq_app.models import (
    TanseeqPeriod,
    SecondarySchoolCetificate,
    UniversityAttachment,
    TanseeqFaculty,
    TanseeqProgram,
    ConditionFilters,
    TanseeqFee,
    TanseeqCourses,
    Course,
    ApplicationDetails,
    SecondaryCertificateInfo,
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
        self.fields['universities'].queryset = UniversityDetails.objects.filter(is_tanseeq_university=True,
                                                                                is_active=True, is_delete=False)
        for field in self.fields:
            if field != "is_required":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                    "required": "true",
                })


class StudyModeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StudyModeForm, self).__init__(*args, **kwargs)
        self.fields['universities'].queryset = UniversityDetails.active_records()

    class Meta:
        model = StudyModeDetails
        fields = ("universities", "study_mode", "code", "is_active",)



class TanseeqFacultyForm(forms.ModelForm):

    class Meta:
        model = TanseeqFaculty
        fields = ("universities", "code", "name", "notes", "is_active",)

    def __init__(self, *args, **kwargs):
        super(TanseeqFacultyForm, self).__init__(*args, **kwargs)
        self.fields['universities'].queryset = UniversityDetails.active_records()
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                    "required": "true",
                })


class TanseeqProgramForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TanseeqProgramForm, self).__init__(*args, **kwargs)
        self.fields['universities'].queryset = UniversityDetails.objects.filter(is_tanseeq_university=True,is_active=True, is_delete=False)


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


class ConditionFiltersForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ConditionFiltersForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ["is_exam", "is_active"]:
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                    "required": "true",
                })

    class Meta:
        model = ConditionFilters
        fields = ("study_mode", "faculty", "program", "type_of_secondary", "year",
            "start_date", "end_date", "average", "capacity", "fee", "is_exam", "is_active"
        )

        widgets = {
            'start_date': forms.DateInput(attrs={'placeholder':'Select a date', 'type':'date'}),
            'end_date': forms.DateInput(attrs={'placeholder':'Select a date', 'type':'date'}),
        }

    def clean(self):
        from_date = self.cleaned_data.get("start_date")
        to_date = self.cleaned_data.get("end_date")
        if from_date >= to_date:
            raise forms.ValidationError(
                'End Date must be greater than Start Date.',
                code='incorrect_values',
            )


class TanseeqFeeForm(forms.ModelForm):

    class Meta:
        model = TanseeqFee
        fields = ("universities", "faculty", "fee", "is_active",)

    def __init__(self, *args, **kwargs):
        super(TanseeqFeeForm, self).__init__(*args, **kwargs)
        self.fields['universities'].queryset = UniversityDetails.objects.filter(is_tanseeq_university=True,
                                                                                is_active=True, is_delete=False)
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                    "required": "true",
                })


class TanseeqCourseForm(forms.ModelForm):

    class Meta:
        model = TanseeqCourses
        fields = ('course_name',)


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('course','mark',)
