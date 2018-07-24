from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from accounts.decoratars import user_login_required
from accounts.forms import loginForm, signUpForm
from accounts.service import *
from accounts.models import UserRole
from student.models import StudentDetails
from masters.models import AddressDetails, CountryDetails
from partner.models import PartnerDetails
from donor.models import DonorDetails

from accounts.service import UserService
# Create your views here.

def index(request):
    return render(request, "index.html")

@user_login_required
def home(request):
    if request.user.is_authenticated:
        user = request.user

        # if user.is_superuser:
        return render(request, "template_admin_dashboard.html", {'user': user})



def template_signup(request):
    form = signUpForm()
    return render(request, 'signup.html', {'form': form})

def template_signin(request):
    country_list = CountryDetails.objects.all()
    form = loginForm()

    if request.user.is_authenticated:
        return redirect('/accounts/home/')

    # return render(request, "template_login.html", {'form': form})
    return render(request, "template_login.html", {'form': form, 'country_list': country_list})

@transaction.atomic
def user_signup(request):
    signup_form = signUpForm(request.POST)
    if request.method == 'POST':
        if signup_form.is_valid():
            try:
                user = signup_form.save()
                user.role.add(UserRole.objects.get(name=signup_form.cleaned_data['role']))
                if str(signup_form.cleaned_data['role']) not in  ["Accountant", "Parent"]:
                    country = CountryDetails.objects.get(country_name=request.POST['country'])
                    address = AddressDetails.objects.create(country=country)
                    if signup_form.cleaned_data['role'] == "Student":
                        StudentDetails.objects.create(user=user,address=address)
                    if signup_form.cleaned_data['role'] == "Partner":
                        PartnerDetails.objects.create(user=user,address=address)
                    if signup_form.cleaned_data['role'] == "Donor":
                        DonorDetails.objects.create(user=user,address=address)

            except Exception as e:
                messages.success(request, str(e))
            return redirect('/')
        else:
            print(signup_form.errors)
            for error_msg in signup_form.errors:
                # form = signUpForm()
                for msg in signup_form.errors[error_msg]:
                    messages.success(request, msg)
        return render(request, 'signup.html', {'form': signup_form})

# @csrf_exempt
def user_signin(request):
    form_data=request.POST
    if request.POST:
        form = loginForm(request.POST or None)
        request.session['form_data'] = form_data
    else:
        form=loginForm(request.session.get('form_data'))

    if form.is_valid():
        user = form.login(request)

        if user:
            login(request, user)

            if user.is_student():
                return redirect('/student/student_home/')

            if user.is_donor():
                return redirect('/donor/template_donor_dashboard/')

            return redirect('/accounts/home/')
        else:
            messages.success(request, "Enter Valid User Name and Password.")
            return redirect('/')

@user_login_required
def user_signout(request):
    logout(request)
    return redirect('/')



def template_manage_user(request):
    country_list = CountryDetails.objects.all()
    user_recs = User.objects.filter().exclude(role__name='Admin')
    return render(request, 'template_manage_user.html',
                  {'country_list': country_list, 'user_recs': user_recs})