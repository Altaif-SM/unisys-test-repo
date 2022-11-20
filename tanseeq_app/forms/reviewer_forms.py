from django import forms
from tanseeq_app.models import (
    AppliedPrograms
)


class ReviewerForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ReviewerForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
                "required": "true",
            })
        self.fields["review_status"].choices = AppliedPrograms.REVIEWER_STATUS

    class Meta:
        model = AppliedPrograms
        fields = ("review_status", "review_note",)

        widgets = {
            'review_note': forms.Textarea(attrs={'rows':'2'}),
        }
