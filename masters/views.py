from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
import json
from masters.models import *
from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages


# *********------------ Year Master ----------***************

def template_year_master(request):
    year_recs = YearDetails.objects.all()
    return render(request, 'template_year_master.html', {'year_recs': year_recs})


def save_year(request):
    year_name = request.POST.get('year_name')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    try:
        if not YearDetails.objects.filter(year_name=year_name.lower()).exists():
            YearDetails.objects.create(year_name=year_name.lower(), start_date=start_date, end_date=end_date)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Year name already exists. Record not saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_year_master/')


def update_year(request):
    year_id = request.POST.get('year_id')
    year_name = request.POST.get('year_name')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    try:
        if not YearDetails.objects.filter(year_name=year_name.lower()).exists():
            YearDetails.objects.filter(id=year_id).update(year_name=year_name.lower(), start_date=start_date,
                                                          end_date=end_date)
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request, "Year name already exists. Record not updated.")
        return HttpResponse(json.dumps({'success': 'Year name already exists. Record not updated.'}),
                            content_type="application/json")

    except:
        messages.warning(request, "Record not updated.")
    return HttpResponse(json.dumps({'error': 'Record not updated.'}), content_type="application/json")


def delete_year(request):
    year_id = request.POST.get('year_id')

    try:
        YearDetails.objects.filter(id=year_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


# *********------------ Scholarship Master ----------***************

def template_scholarship_master(request):
    scholarship_recs = ScholarshipDetails.objects.all()
    return render(request, 'template_scholarship_master.html', {'scholarship_recs': scholarship_recs})


def save_scholarship(request):
    scholarship_name = request.POST.get('scholarship_name')
    try:
        if not ScholarshipDetails.objects.filter(scholarship_name=scholarship_name.lower()).exists():
            ScholarshipDetails.objects.create(scholarship_name=scholarship_name.lower())
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Scholarship name already exists. Record not saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_scholarship_master/')


def update_scholarship(request):
    scholarship_id = request.POST.get('scholarship_id')
    scholarship_name = request.POST.get('scholarship_name')
    try:
        if not ScholarshipDetails.objects.filter(scholarship_name=scholarship_name.lower()).exists():
            ScholarshipDetails.objects.filter(id=scholarship_id).update(scholarship_name=scholarship_name.lower())
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")

    except:
        messages.warning(request, "Scholarship name already exists. Record not updated.")
    return HttpResponse(json.dumps({'error': 'Scholarship name already exists. Record not updated.'}),
                        content_type="application/json")


def delete_scholarship(request):
    scholarship_id = request.POST.get('scholarship_id')

    try:
        ScholarshipDetails.objects.filter(id=scholarship_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


# *********------------ Country Master ----------***************

def template_country_master(request):
    country_recs = CountryDetails.objects.all()
    return render(request, 'template_country_master.html', {'country_recs': country_recs})


def save_country(request):
    country_name = request.POST.get('country_name')
    try:
        if not CountryDetails.objects.filter(country_name=country_name.lower()).exists():
            CountryDetails.objects.create(country_name=country_name.lower())
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Country name already exists. Record not saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_country_master/')


def update_country(request):
    country_id = request.POST.get('country_id')
    country_name = request.POST.get('country_name')
    try:
        if not CountryDetails.objects.filter(country_name=country_name.lower()).exists():
            CountryDetails.objects.filter(id=country_id).update(country_name=country_name.lower())
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request, "Country name already exists. Record not updated.")
            return HttpResponse(json.dumps({'success': '"Country name already exists. Record not updated.'}),
                                content_type="application/json")

    except:
        messages.warning(request, "Record not updated.")
    return HttpResponse(json.dumps({'error': 'Record not updated.'}), content_type="application/json")


def delete_country(request):
    country_id = request.POST.get('country_id')

    try:
        CountryDetails.objects.filter(id=country_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


# *********------------ University Master ----------***************

def template_university_master(request):
    university_recs = UniversityDetails.objects.all()
    country_recs = CountryDetails.objects.all()
    return render(request, 'template_university_master.html',
                  {'university_recs': university_recs, 'country_recs': country_recs})


def save_university(request):
    university_name = request.POST.get('university_name')
    try:
        if not UniversityDetails.objects.filter(university_name=university_name.lower()).exists():
            UniversityDetails.objects.create(university_name=university_name.lower())
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "University name already exists. Record not saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_university_master/')


def update_university(request):
    university_id = request.POST.get('university_id')
    university_name = request.POST.get('university_name')
    try:
        if not UniversityDetails.objects.filter(university_name=university_name.lower()).exists():
            UniversityDetails.objects.filter(id=university_id).update(university_name=university_name.lower())
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request, "University name already exists. Record not updated.")
            return HttpResponse(json.dumps({'success': "University name already exists. Record not updated."}),
                                content_type="application/json")

    except:
        messages.warning(request, "University name already exists. Record not updated.")
    return HttpResponse(json.dumps({'error': 'University name already exists. Record not updated.'}),
                        content_type="application/json")


def delete_university(request):
    university_id = request.POST.get('university_id')

    try:
        UniversityDetails.objects.filter(id=university_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


def template_degree_formula_master(request):
    data = [{'id': 1, 'first_name': 'abc', 'last_name': 'Yes', 'phone_number': 9898989898},
            {'id': 2, 'first_name': 'xyz', 'last_name': 'No', 'phone_number': 8888888888},
            {'id': 3, 'first_name': 'pqrs', 'last_name': 'No', 'phone_number': 7777777777},
            {'id': 4, 'first_name': 'lmnop', 'last_name': 'No', 'phone_number': 6666666666}]
    return render(request, 'template_degree_formula_master.html', {'data': data, 'data_length': len(data)})


def get_table_data(request):
    # data = {'id': 1, 'column_name': 'abc', 'value': 'ABCD'}

    return HttpResponse(json.dumps(data), content_type="application/json")
