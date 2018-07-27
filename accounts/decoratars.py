from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from accounts.models import User
from django.contrib import messages

def user_login_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap

def admin_login_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_super_admin():
            return HttpResponseRedirect("/")
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap

def student_login_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_student():
            return HttpResponseRedirect("/")
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap

def parent_login_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_parent():
            return HttpResponseRedirect("/")
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap

def partner_login_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_partner():
            return HttpResponseRedirect("/")
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap

def donor_login_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_donor():
            return HttpResponseRedirect("/")
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap

def accountant_login_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_accountant():
            return HttpResponseRedirect("/")
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap


def psycho_test_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.psyc_switch:
            messages.warning(request, "You can't submit Psychometric Test now, Please contact Administrator for the same")
            return HttpResponseRedirect(request.user.get_dashboard_path())
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap

def submission_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.submission_switch:
            messages.warning(request, "Last Date of Application submission is over, Please contact Administrator for the same")
            return HttpResponseRedirect(request.user.get_dashboard_path())
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap

def registration_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.POST['role'] == "Student" and not User.objects.all()[0].registration_switch:
            messages.warning(request, "Registration closed for now, Please contact Administrator for the same")
            return HttpResponseRedirect("/")
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap

def semester_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.semester_switch:
            messages.warning(request, "You can't submit Academic Progress now, Please contact Administrator for the same")
            return HttpResponseRedirect(request.user.get_dashboard_path())
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap

def dev_program_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.program_switch:
            messages.warning(request, "You can't submit Development Program now, Please contact Administrator for the same")
            return HttpResponseRedirect(request.user.get_dashboard_path())
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap

def agreements_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.agreements_switch:
            messages.warning(request, "You can't submit Agreement now, Please contact Administrator for the same")
            return HttpResponseRedirect(request.user.get_dashboard_path())
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap