from django import forms
from tanseeq_app.models import (
    AppliedPrograms
)


class ExaminerReviewForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ExaminerReviewForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
                "required": True
            })
        self.fields["review_status"].required = True
        self.fields["review_status"].choices = AppliedPrograms.EXAMINER_STATUS
        self.fields["review_status"].choices.insert(0, ("", "----"))

    class Meta:
        model = AppliedPrograms
        fields = ("review_status",)
