from django.core.exceptions import PermissionDenied
from functools import wraps
from accounts.models import User


def check_permissions(role):
    def _method_wrapper(func):
        @wraps(func)
        def inner_func(request, *args, **kwargs):
            if request.user.role.filter(name__in=[User.TANSEEQ_ADMIN, User.TANSEEQ_APPLICATION_ENTRY]):
                try:
                    del request.session['form_data']
                except:
                    pass
            is_admin = request.user.role.filter(name__in=[User.TANSEEQ_ADMIN, User.TANSEEQ_UNIVERSITY_ADMIN])
            if is_admin or request.user.tanseeq_role.name == role:
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied

        return inner_func
    return _method_wrapper
