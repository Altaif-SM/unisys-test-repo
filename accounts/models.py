from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from common.models import BaseModel
from django.db.models import Q


# Create your models here.
class UserRole(BaseModel):
    name = models.CharField(max_length=50)
    role_permission = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ID = 'id'
    USERNAME = 'username'
    PASSWORD = 'password'
    FIRST_NAME = 'first_name'
    MIDDLE_NAME = 'middle_name'
    LAST_NAME = 'last_name'
    EMAIL = 'email'
    IS_ACTIVE = 'is_active'
    ROLE = 'role'

    SYSTEAM_ADMIN = 'System Admin'  # Group.objects.filter(Q(name__istartswith='System Admin') | Q(name__istartswith='system admin') | Q(name='System Admin'))[0]
    ADMIN = 'Admin'

    first_name = models.CharField(max_length=256, blank=True, null=True)
    middle_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    role = models.ManyToManyField(UserRole, related_name='user_role', null=True)

    class Meta:
        permissions = (
            ('can_view_year_master', 'can view year master'),
        )

    @staticmethod
    def get_instance(user_detail_form, user=None, generate_password=False):

        if user:
            user = User.objects.get(id=user.id)
        else:
            user = User()
            user.username = user_detail_form.cleaned_data[User.EMAIL]

        if user_detail_form.cleaned_data[User.EMAIL]:
            user.email = user_detail_form.cleaned_data[User.EMAIL]

        if user_detail_form.cleaned_data[User.FIRST_NAME]:
            user.first_name = user_detail_form.cleaned_data[User.FIRST_NAME]

        if user_detail_form.cleaned_data[User.MIDDLE_NAME]:
            user.middle_name = user_detail_form.cleaned_data[User.MIDDLE_NAME]
        else:
            user.middle_name = ''

        if user_detail_form.cleaned_data[User.LAST_NAME]:
            user.last_name = user_detail_form.cleaned_data[User.LAST_NAME]
        else:
            user.last_name = ''

        if generate_password:
            user.password = user_detail_form.cleaned_data[User.PASSWORD]

        return user

    @staticmethod
    def get_dict_instance(user_detail_form, user=None, generate_password=False):

        if user:
            user = User.objects.get(id=user.id)
        else:
            user = User()
            user.username = user_detail_form[User.EMAIL]

        if User.EMAIL in user_detail_form and user_detail_form[User.EMAIL]:
            user.email = user_detail_form[User.EMAIL]

        if User.FIRST_NAME in user_detail_form and user_detail_form[User.FIRST_NAME]:
            user.first_name = user_detail_form[User.FIRST_NAME]

        if User.LAST_NAME in user_detail_form and user_detail_form[User.LAST_NAME]:
            user.last_name = user_detail_form[User.LAST_NAME]
        else:
            user.last_name = ''

        if generate_password:
            user.password = user_detail_form[User.PASSWORD]

        return user

    def is_system_admin(self):
        return True if self.role.all().filter(name__in=[self.SYSTEAM_ADMIN, self.ADMIN]).exists() else False

    # def is_student(self):
    #     return True if self.role.all().filter(name__in=[self.SYSTEAM_ADMIN, self.ADMIN]).exists() else False

    @property
    def get_user_permissions(self):

        role_list = self.role.all()
        perms = []

        for role_name in role_list:
            role_rec = UserRole.objects.get(name=role_name)
            user_group_perms = Permission.objects.filter(group__name=role_rec.name)
            user_role_perms = UserRole.objects.get(name=role_rec.name)

            group_include_perms = Permission.objects.all().filter(Q(id__in=user_group_perms))
            role_include_perms = user_role_perms.role_permission.all()

            for obj in role_include_perms:
                perms.append(obj.content_type.app_label + '.' + obj.codename)

            for obj in group_include_perms:
                perms.append(obj.content_type.app_label + '.' + obj.codename)
        return perms

    def to_dict(self):
        json_dict = {}
        json_dict['id'] = self.id
        json_dict['email'] = self.email
        json_dict['first_name'] = self.first_name
        json_dict['last_name'] = self.last_name

        return json_dict

    @property
    def get_application_id(self):
        try:
            return self.student_user_rel.get().student_applicant_rel.get(year__active_year=True).application_id
        except:
            return ''

    @property
    def get_application(self):
        try:
            return self.student_user_rel.get().student_applicant_rel.get(year__active_year=True)
        except:
            return ''
