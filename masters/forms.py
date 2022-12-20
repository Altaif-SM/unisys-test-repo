from django import forms
from masters.models import Subject, SubjectsComponent


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
