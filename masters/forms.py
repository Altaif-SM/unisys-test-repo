from django import forms
from masters.models import Subject, SubjectsComponent, ProgramDetails, StudyPlanDetails, Semester


class ProgramDetailsForm(forms.ModelForm):
    
    class Meta:
        model = ProgramDetails
        fields = (
            "university_type", "university", "faculty", "department", "program_name",
            "study_level", "study_type", "acceptance_avg", "capacity_avg", "program_overview",
            "program_objective", "program_vision", "program_mission", "status", "campus_details"
        )
        widgets = {
            'program_overview': forms.Textarea(attrs={'rows':'2'}),
            'program_objective': forms.Textarea(attrs={'rows':'2'}),
            'program_vision': forms.Textarea(attrs={'rows':'2'}),
            'program_mission': forms.Textarea(attrs={'rows':'2'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProgramDetailsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ["status"]:
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                })

class StudyPlanDetailsForm(forms.ModelForm):
    
    study_semester = forms.ChoiceField(choices=(), required=True)

    class Meta:
        model = StudyPlanDetails
        fields = (
            "is_credit", "program", "academic_year", "study_semester", "courses", "min_credit", "max_credit",
        )
       
    
    def __init__(self, *args, **kwargs):
        super(StudyPlanDetailsForm, self).__init__(*args, **kwargs)
        self.fields["is_credit"].label = "Credit Base"
        for field in self.fields:
            if field != "is_credit":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                })
        if self.data:
            for choice in self.data["study_semester"]:
                self.fields["study_semester"].choices.insert(0,(choice, choice))
        print(self.instance)
        if self.instance:
            study_semester_obj = self.instance.study_semester
            print("study_semester_obj",study_semester_obj)
            start_date = study_semester_obj.start_date
            end_date = study_semester_obj.end_date
            self.fields["study_semester"].choices= (
                   ( study_semester_obj.id, "{} {} - {}".format(study_semester_obj.semester, start_date, end_date)),
            )
            print(self.fields["study_semester"].choices)
    def clean_study_semester(self):
        study_semester_id = self.cleaned_data["study_semester"]
        try:
            semester = Semester.objects.get(id=study_semester_id)
        except:
            raise "Invalid Semester Choice."
        return semester


class SubjectForm(forms.ModelForm):
    
    class Meta:
        model = Subject
        fields = ("name", "program", "is_active",)
    
    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                })


class SubjectsComponentForm(forms.ModelForm):
    
    class Meta:
        model = SubjectsComponent
        fields = ("name", "subjects", "fee_per_credit", "is_active",)
    
    def __init__(self, *args, **kwargs):
        super(SubjectsComponentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != "is_active":
                self.fields[field].widget.attrs.update({
                    "class": "form-control",
                })
