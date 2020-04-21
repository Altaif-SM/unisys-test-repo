from django.db.models.functions import Concat
from django_datatables_view.base_datatable_view import BaseDatatableView
from student.models import ApplicationDetails,ScholarshipSelectionDetails
from masters.models import UniversityDetails,CountryDetails,DegreeDetails
from django.db.models import Value as V, Q
from django.utils.html import escape
from common.utils import get_current_year


class FilterCompaniesList(BaseDatatableView):
    model = ApplicationDetails
    columns = ['id','first_name', 'nationality','address','application_id','year','semester','student']
    order_columns = []
    max_display_length = 100

    def get_initial_queryset(self):
        if self.request.user.is_super_admin():
            return ApplicationDetails.objects.filter(is_submitted=True, year=get_current_year(self.request))
        else:
            return ApplicationDetails.objects.filter(
                nationality=self.request.user.partner_user_rel.get().address.country, year=get_current_year(self.request),
                is_submitted=True)



    def render_column(self, row, column):
        if column == 'first_name':
            first_name = row.first_name if row.first_name else ""
            last_name = row.last_name if row.last_name else ""
            return escape('{0} {1}'.format(first_name, last_name))
        elif column == 'application_id':
            try:
                return escape('{0}'.format(row.applicant_scholarship_rel.all()[0].university.university_name))
            except:
                return ""
        elif column == 'year':
            try:
                return escape('{0}'.format(row.applicant_scholarship_rel.all()[0].degree.degree_name))
            except:
                return ""
        elif column == 'semester':
            try:
                return escape('{0}'.format(row.applicant_scholarship_rel.all()[0].course_applied.program_name))
            except:
                return ""
        elif column == 'student':
            try:
                return escape('{0}'.format(row.applicant_scholarship_rel.all()[0].scholarship.scholarship_name))
            except:
                return ""
        else:
            return super(FilterCompaniesList, self).render_column(row, column)


    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            q = Q(first_name__istartswith=search) | Q(last_name__istartswith=search) | Q(nationality__country_name__istartswith=search)| Q(address__country__country_name__istartswith=search)
            first_query = qs.filter(q)
            pks_list = list(ScholarshipSelectionDetails.objects.filter(Q(university__university_name__istartswith=search) | Q(degree__degree_name__istartswith=search) | Q(course_applied__program_name__istartswith=search)).values_list('applicant_id',flat=True))
            second_query = ApplicationDetails.objects.filter(pk__in=pks_list)
            qs = first_query | second_query
        return qs


