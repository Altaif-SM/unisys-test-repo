from django import forms
from accounts.models import *
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate


class loginForm(forms.Form):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Username','autocomplete': 'off'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Password','autocomplete': 'off'}))

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class signUpForm(forms.ModelForm):
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'First Name','autocomplete': 'off'}), label='')
    middle_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Middle Name','autocomplete': 'off'}), label='')
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Last Name','autocomplete': 'off'}), label='')
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Username','autocomplete': 'off'}), label='')
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Password','autocomplete': 'off'}), label='')
    confirm_password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Confirm Password','autocomplete': 'off'}), label='')

    class Meta:
        model = User
        fields =['first_name','middle_name','last_name','username','password']


    def clean(self):
        cleaned_data = super(signUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

    def clean_email(self):
        email = self.cleaned_data['username'].strip()
        try:
            User.objects.get(email__iexact=email)
            raise forms.ValidationError('email already exists')
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = User.objects.create(username=
            self.cleaned_data['username'],
            email=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            middle_name=self.cleaned_data['middle_name'],
            last_name=self.cleaned_data['last_name'],
            password=make_password(self.cleaned_data['password'])
        )
        return user

