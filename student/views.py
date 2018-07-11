from django.shortcuts import render
from masters.views import *

from django.http import HttpResponse
from django.contrib import messages


# Create your views here.

def applicant_personal_info(request):
    country_recs = CountryDetails.objects.all()
    religion_recs = ReligionDetails.objects.all()
    return render(request, 'applicant_personal_info.html',
                  {'country_recs': country_recs, 'religion_recs': religion_recs})


def applicant_family_info(request):
    country_recs = CountryDetails.objects.all()
    return render(request, 'applicant_family_info.html',
                  {'country_recs': country_recs})


def applicant_family_mother_sibling_info(request):
    country_recs = CountryDetails.objects.all()
    return render(request, 'applicant_family_mother_sibling_info.html',
                  {'country_recs': country_recs})


def applicant_academic_english_qualification(request):
    year_recs = YearDetails.objects.all()
    return render(request, 'applicant_academic_english_qualification.html',
                  {'year_recs': year_recs})


def applicant_curriculum_experience_info(request):
    year_recs = YearDetails.objects.all()
    return render(request, 'applicant_curriculum_experience_info.html',
                  {'year_recs': year_recs})


def applicant_scholarship_about_yourself_info(request):
    scholarship_recs = ScholarshipDetails.objects.all()
    return render(request, 'applicant_scholarship_about_yourself_info.html',
                  {'scholarship_recs': scholarship_recs})
