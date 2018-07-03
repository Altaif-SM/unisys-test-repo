from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden

def user_login_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__
    return wrap