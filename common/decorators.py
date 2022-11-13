from django.core.exceptions import PermissionDenied
from functools import wraps


def check_permissions(role):
    def _method_wrapper(func):
        @wraps(func)
        def inner_func(request, *args, **kwargs):
            if request.user.role.filter(name__in=[role]).exists():
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return inner_func
    return _method_wrapper
