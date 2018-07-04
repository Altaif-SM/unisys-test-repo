from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
import json
from masters.models import *
from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages


def template_year_master(request):
    year_recs = YearDetails.objects.all()
    return render(request, 'template_year_master.html', {'year_recs': year_recs})


def template_scholarship_master(request):
    data = [{'id': 1, 'first_name': 'abc', 'last_name': 'Yes', 'phone_number': 9898989898},
            {'id': 2, 'first_name': 'xyz', 'last_name': 'No', 'phone_number': 8888888888},
            {'id': 3, 'first_name': 'pqrs', 'last_name': 'No', 'phone_number': 7777777777},
            {'id': 4, 'first_name': 'lmnop', 'last_name': 'No', 'phone_number': 6666666666}]
    return render(request, 'template_scholarship_master.html', {'data': data, 'data_length': len(data)})


def template_degree_formula_master(request):
    data = [{'id': 1, 'first_name': 'abc', 'last_name': 'Yes', 'phone_number': 9898989898},
            {'id': 2, 'first_name': 'xyz', 'last_name': 'No', 'phone_number': 8888888888},
            {'id': 3, 'first_name': 'pqrs', 'last_name': 'No', 'phone_number': 7777777777},
            {'id': 4, 'first_name': 'lmnop', 'last_name': 'No', 'phone_number': 6666666666}]
    return render(request, 'template_degree_formula_master.html', {'data': data, 'data_length': len(data)})


def get_table_data(request):
    # data = {'id': 1, 'column_name': 'abc', 'value': 'ABCD'}

    return HttpResponse(json.dumps(data), content_type="application/json")


def save_year(request):
    year_name = request.POST.get('year_name')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    try:
        YearDetails.objects.create(year_name=year_name.lower(), start_date=start_date, end_date=end_date)
        messages.success(request, "Record saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_year_master/')


def update_year(request):
    year_id = request.POST.get('year_id')
    year_name = request.POST.get('year_name')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    try:
        YearDetails.objects.filter(id=year_id).update(year_name=year_name.lower(),start_date=start_date,end_date=end_date)
        messages.success(request, "Record updated.")
        return HttpResponse(json.dumps({'success': 'Record updated.'}),content_type="application/json")

        # messages.success(request, "Record updated.")
    except:
        messages.warning(request, "Record not updated.")
    return HttpResponse(json.dumps({'error': 'Record not updated.'}), content_type="application/json")


def delete_year(request):
    year_id = request.POST.get('year_id')

    try:
        YearDetails.objects.filter(id=year_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}),content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")