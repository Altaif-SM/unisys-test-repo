from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from accounts.decoratars import user_login_required
from accounts.forms import loginForm, signUpForm
from accounts.service import *
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
    form = loginForm()

    if request.user.is_authenticated:
        return redirect('/accounts/home/')

    # return render(request, "template_login.html", {'form': form})
    return render(request, "template_login.html", {'form': form})

def user_signup(request):
    signup_form = signUpForm(request.POST)
    if request.method == 'POST':
        if signup_form.is_valid():
            signup_form.save()
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
