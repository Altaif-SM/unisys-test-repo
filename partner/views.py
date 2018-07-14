from django.shortcuts import render
from masters.models import *
from student.models import *


# Create your views here.

def template_registered_application(request):
    applicant_recs = ApplicationDetails.objects.filter(address__country=request.user.partner_user_rel.get().country,
                                                       is_submitted=True)
    country_recs = CountryDetails.objects.all()
    university_recs = UniversityDetails.objects.filter(country=request.user.partner_user_rel.get().country)
    degree_recs = DegreeDetails.objects.all()
    return render(request, 'template_registered_application.html',
                  {'applicant_recs': applicant_recs, 'country_recs': country_recs, 'university_recs': university_recs,
                   'degree_recs': degree_recs})
