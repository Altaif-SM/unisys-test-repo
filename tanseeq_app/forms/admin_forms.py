from django import forms
from django.db.models import Q
from masters.models import UniversityDetails, StudyModeDetails, YearDetails
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
)
from accounts.models import User
from django.contrib.auth import password_validation


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

    class Meta:
        model = TanseeqProgram
        fields = ("university","faculty", "name", "code", "is_active",)

    def __init__(self, *args, **kwargs):
        super(TanseeqProgramForm, self).__init__(*args, **kwargs)
        self.fields['university'].queryset = UniversityDetails.objects.filter(is_tanseeq_university=True,
                                                                              is_active=True, is_delete=False)
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                    "required": "true",
                })


class ConditionFiltersForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ConditionFiltersForm, self).__init__(*args, **kwargs)
        self.fields['university'].queryset = UniversityDetails.objects.filter(is_tanseeq_university=True,
                                                                                is_active=True, is_delete=False)
        self.fields['academic_year'].queryset = YearDetails.objects.filter(is_tanseeq_year=True,)
        for field in self.fields:
            if field not in ["is_exam", "is_active"]:
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                    "required": "true",
                })

    class Meta:
        model = ConditionFilters
        fields = ("study_mode", "faculty", "program", "type_of_secondary", "academic_year",
            "start_date", "end_date", "average", "capacity", "fee", "is_exam", "is_active","university",
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


class TanseeqUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(render_value=True,),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(render_value=True,),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "role", "university", "faculty", "program", "is_active", "password1", "password2",)
                             
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Password Mismatch',
                code='password_mismatch',
            )
        return password2

    def __init__(self, *args, **kwargs):
        super(TanseeqUserForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = self.fields['role'].queryset.filter(is_tanseeq=True)
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                    "required": "true",
                })
        if self.instance.id:
            self.fields["password1"].required = False
            self.fields["password2"].required = False
    
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(~Q(id=self.instance.id), email=email).exists():
            raise forms.ValidationError(("A user with that email already exists."))
        return email

    def _post_clean(self):
        super(TanseeqUserForm, self)._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)