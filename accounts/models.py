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

class PersmissionDetails(models.Model):
    permission = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.permission

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
    SUPER_ADMIN = 'Super Admin'
    STUDENT = 'Student'
    DONOR = 'Donor'
    PARTNER = 'Partner'
    ACCOUNTANT = 'Accountant'
    PARENT = 'Parent'

    DEAN = 'Dean'
    DEPUTY_DEAN = 'Deputy Dean'
    HEAD = 'Head'
    REGISTRAR = 'Registrar'
    VICE_CHANCELLOR = 'Vice Chancellor'
    DEPUTT_VICE_CHANCELLOR = 'Deputy Vice Chancellor'
    HR = 'HR'

    ADMINISTRATOR = 'Administrator'
    ADMISSION_UNIT = 'Administrator'
    FACULTY = 'Faculty'


    first_name = models.CharField(max_length=256, blank=True, null=True)
    middle_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    role = models.ManyToManyField(UserRole, related_name='user_role', null=True)

    registration_switch = models.BooleanField(default=False)
    submission_switch = models.BooleanField(default=False)
    psyc_switch = models.BooleanField(default=False)
    agreements_switch = models.BooleanField(default=False)
    semester_switch = models.BooleanField(default=False)
    program_switch = models.BooleanField(default=False)
    address = models.ForeignKey('masters.AddressDetails', blank=True, null=True, related_name='user_address_rel',
                                on_delete=models.SET_NULL)
    permission = models.ManyToManyField(PersmissionDetails, blank=True)
    university = models.ForeignKey('masters.UniversityDetails', blank=True, null=True, related_name='user_university_rel',
                                on_delete=models.SET_NULL)
    faculty = models.ForeignKey('masters.FacultyDetails', blank=True, null=True,
                                   related_name='user_faculty_rel',
                                   on_delete=models.SET_NULL)

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
        return True if self.role.filter(name__in=[]).exists(self.SYSTEAM_ADMIN, self.ADMIN) else False

    def is_super_admin(self):
        return True if self.role.all().filter(name__in=[self.SUPER_ADMIN, self.ADMIN]).exists() else False

    def is_student(self):
        return True if self.role.all().filter(name__in=[self.STUDENT]).exists() else False

    def is_donor(self):
        return True if self.role.all().filter(name__in=[self.DONOR]).exists() else False

    def is_partner(self):
        return True if self.role.all().filter(name__in=[self.PARTNER]).exists() else False

    def is_parent(self):
        return True if self.role.all().filter(name__in=[self.PARENT]).exists() else False

    def is_accountant(self):
        return True if self.role.all().filter(name__in=[self.ACCOUNTANT]).exists() else False

    def accountant_type(self):
        return self.role.all()[0].name.title() if self.role.all().exists() else None

    def is_administrator(self):
        return True if self.role.all().filter(name__in=[self.ADMISSION_UNIT]).exists() else False

    def is_faculty(self):
        return True if self.role.all().filter(name__in=[self.FACULTY]).exists() else False

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
        json_dict['id'] = self.id if self.id else ''
        json_dict['email'] = self.email if self.email else ''
        json_dict['first_name'] = self.first_name if self.first_name else ''
        json_dict['last_name'] = self.last_name if self.last_name else ''

        return json_dict

    @property
    def get_application_id(self):
        try:
            return self.student_user_rel.get().student_applicant_rel.get(year__active_year=True).application_id
        except:
            return None

    @property
    def get_application(self):
        try:
            return self.student_user_rel.get().student_applicant_rel.get(year__active_year=True)
        except:
            return self.student_user_rel.get().student_applicant_rel.get()
            return None

    @property
    def get_student_application(self):
        form_vals = {}

        if self.role.all().filter(name__in=[self.STUDENT]).exists():
            try:
                applicaton_obj = self.student_user_rel.get().student_applicant_rel.get(year__active_year=True)
                form_vals['personal_info_flag'] = applicaton_obj.personal_info_flag
                form_vals['intake_flag'] = applicaton_obj.intake_flag

                if applicaton_obj.father_name == None or applicaton_obj.mother_name == None or applicaton_obj.father_income == None or applicaton_obj.father_occupation == None or applicaton_obj.mother_income == None or applicaton_obj.mother_occupation == None:
                    form_vals['family_flag'] = False

                elif not applicaton_obj.father_name == '' or not applicaton_obj.mother_name == '' or not applicaton_obj.father_income == '' or not applicaton_obj.father_occupation == '' or not applicaton_obj.mother_income == '' or not applicaton_obj.mother_occupation == '':
                    form_vals['family_flag'] = True

                else:
                    form_vals['family_flag'] = False
                if applicaton_obj.personal_info_flag:
                    pass
                form_vals[
                    'english_qualification'] = applicaton_obj.english_applicant_rel.filter()[0].english_qualification if applicaton_obj.english_applicant_rel.all() else False
                form_vals[
                    'scholarship_selection'] = True if applicaton_obj.applicant_addition_info.all() else False
                form_vals['attachment'] = True if applicaton_obj.applicant_attachement_rel.all() else False
                form_vals['declaration'] = True if applicaton_obj.is_submitted else False
                form_vals['my_application'] = applicaton_obj.is_submitted if applicaton_obj.is_submitted else False
                form_vals['psychometric_test'] = applicaton_obj.applicant_psychometric_test_rel.exists() if applicaton_obj.applicant_psychometric_test_rel.exists() else False
                form_vals['agreement'] = applicaton_obj.applicant_agreement_rel.exists() if applicaton_obj.applicant_agreement_rel.exists() else False

                return form_vals
            except:
                form_vals['personal_info_flag'] = False
                form_vals['intake_flag'] = False
                form_vals['english_qualification'] = False
                form_vals['scholarship_selection'] = False
                form_vals['attachment'] = False
                form_vals['declaration'] = False
                form_vals['my_application'] = False
                form_vals['psychometric_test'] = False
                form_vals['agreement'] = False
                form_vals['family_flag'] = False

                return form_vals
        else:

            # form_vals['personal_info_flag'] = False
            # form_vals['english_qualification'] = False
            # form_vals['scholarship_selection'] = False
            # form_vals['my_application'] = False

            return None

    @property
    def get_student_progress(self):
        form_vals = {}
        if self.role.all().filter(name__in=[self.STUDENT]).exists():
            try:
                applicaton_obj = self.student_user_rel.get().student_applicant_rel.get(year__active_year=True)
                form_vals['progress_counter'] = applicaton_obj.progress_counter
                return form_vals
            except:
                form_vals['progress_counter'] = 0
                return form_vals
        else:

            form_vals['progress_counter'] = 0
            return form_vals


    @property
    def notifications(self):
        payload = {'flag': False}
        try:
            if self.role.all().filter(name__in=[self.STUDENT]).exists():
                payload['notifications'] = self.student_user_rel.get().student_applicant_rel.get(year__active_year=True,
                                                                                                 is_submitted=True).applicant_notification_rel.all()
                payload['flag'] = True
                payload['active_count'] = self.student_user_rel.get().student_applicant_rel.get(year__active_year=True,
                                                                                                is_submitted=True).applicant_notification_rel.filter(
                    is_read=False).count()
                return payload
            elif self.role.all().filter(name__in=[self.SUPER_ADMIN, self.ADMIN]).exists():
                from common.utils import get_admin_notification
                payload['notifications'] = get_admin_notification()
                payload['flag'] = True
                payload['active_count'] = get_admin_notification().count()
                return payload
            # elif self.role.all().filter(name__in=[self.ADMINISTRATOR]).exists():
            #     from common.utils import get_university_admin_notification
            #     payload['notifications'] = get_university_admin_notification()
            #     payload['flag'] = True
            #     payload['active_count'] = get_university_admin_notification().count()
            #     return payload
            else:
                return payload

        except:
            return payload

    def year_list(self):
        from masters.models import YearDetails
        return YearDetails.objects.all()

    ADMIN_DASHBOARD = '/accounts/home/'
    STUDENT_DASHBOARD = '/student/student_home/'
    PARENT_DASHBOARD = '/accounts/home/'
    PARTNER_DASHBOARD = '/accounts/home/'
    DONOR_DASHBOARD = '/donor/template_donor_dashboard/'
    ACCOUNTANT_DASHBOARD = '/accounts/home/'
    ADMINISTRATOR_DASHBOARD = '/accounts/dashboard/'

    def get_dashboard_path(self):

        dashboard_path = User.ADMIN_DASHBOARD
        if self.role.get().name == User.ADMIN:
            dashboard_path = User.ADMIN_DASHBOARD
        elif self.role.get().name == User.STUDENT:
            dashboard_path = User.STUDENT_DASHBOARD
        elif self.role.get().name == User.PARTNER:
            dashboard_path = User.PARTNER_DASHBOARD
        elif self.role.get().name == User.PARENT:
            dashboard_path = User.PARENT_DASHBOARD
        elif self.role.get().name == User.DONOR:
            dashboard_path = User.DONOR_DASHBOARD
        elif self.role.get().name == User.ACCOUNTANT:
            dashboard_path = User.ACCOUNTANT_DASHBOARD
        elif self.role.get().name == User.ADMINISTRATOR:
            dashboard_path = User.ADMINISTRATOR_DASHBOARD
        elif self.role.get().name == User.FACULTY:
            dashboard_path = User.ADMINISTRATOR_DASHBOARD
        return dashboard_path
