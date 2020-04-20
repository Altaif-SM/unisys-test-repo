from django.db.models.functions import Concat
from django_datatables_view.base_datatable_view import BaseDatatableView
from student.models import ApplicationDetails,ScholarshipSelectionDetails
from masters.models import UniversityDetails,CountryDetails,DegreeDetails
from django.db.models import Value as V, Q
from django.utils.html import escape
from common.utils import get_current_year



class FilterCompaniesList(BaseDatatableView):
    model = ApplicationDetails
    columns = ['id','first_name', 'nationality','address','application_id']
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
            if row.application_id:
                try:
                    return escape('{0}'.format(row.applicant_scholarship_rel.all()[0].university.university_name))
                except:
                    return ""
            else:
                return ""
        else:
            return super(FilterCompaniesList, self).render_column(row, column)



    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            q = Q(first_name__istartswith=search) | Q(last_name__istartswith=search) | Q(nationality__country_name__istartswith=search)| Q(address__country__country_name__istartswith=search)
            qs = qs.filter(q)

        return qs


