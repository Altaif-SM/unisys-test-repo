from django import forms
from accounts.models import *
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate


class loginForm(forms.Form):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Email','autocomplete': 'off'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Password','autocomplete': 'off'}))

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class signUpForm(forms.ModelForm):
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'First Name','autocomplete': 'off'}), label='')
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Last Name','autocomplete': 'off'}), label='')
    email = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Username','autocomplete': 'off'}), label='')
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Password','autocomplete': 'off'}), label='')
    confirm_password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control form-control-solid placeholder-no-fix' , 'placeholder':'Confirm Password','autocomplete': 'off'}), label='')

    class Meta:
        model = User
        fields =['first_name','last_name','email','password']


    def clean(self):
        cleaned_data = super(signUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        try:
            User.objects.get(email__iexact=email)
            raise forms.ValidationError('email already exists')
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = User.objects.create(username=
            self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=make_password(self.cleaned_data['password']),
            # role=UserRole.objects.get(name=self.cleaned_data['role'])
        )
        return user


class ChangePasswordForm(forms.Form):

    current_password = forms.CharField(label=(u'Current Password'), widget=forms.PasswordInput(render_value=False))
    current_password.widget.attrs['placeholder'] = 'Current Password'
    current_password.widget.attrs['class'] = 'form-control'

    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    password.widget.attrs['placeholder'] = 'Password'
    password.widget.attrs['class'] = 'form-control'

    password1 = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))
    password1.widget.attrs['placeholder'] = 'Confirm Password'
    password1.widget.attrs['class'] = 'form-control'

    def clean(self):
        if self.cleaned_data.get('current_password') is None:
            raise forms.ValidationError("Current password is necessary")
        if self.cleaned_data.get('password') is None:
            raise forms.ValidationError("New password is necessary")
        if self.cleaned_data.get('password1') is None:
            raise forms.ValidationError("Confirm password is necessary")

        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError("The passwords did not match.")
        return self.cleaned_data