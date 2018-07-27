from django.contrib import admin
from accounts.models import User, UserRole
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'middle_name', 'last_name', 'email', 'role', 'is_active', 'is_staff', 'is_superuser', 'psyc_switch', 'agreements_switch', 'semester_switch', 'registration_switch', 'submission_switch')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')
    search_fields = ('username', 'first_name', 'last_name', 'email')
admin.site.register(User, CustomUserAdmin)

admin.site.register(UserRole)