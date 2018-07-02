from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
import json

# Create your views here.
def template_year_master(request):
    data =  [{'id': 1, 'first_name': 'abc', 'last_name': 'ABCD','phone_number':9898989898},
            {'id': 2, 'first_name': 'xyz', 'last_name': 'ABCD','phone_number':8888888888},
            {'id': 3, 'first_name': 'pqrs', 'last_name': 'ABCD','phone_number':7777777777},
            {'id': 4, 'first_name': 'lmnop', 'last_name': 'ABCD','phone_number':6666666666}]
    return render(request, 'template_year_master.html',{'data':data, 'data_length':len(data)})


def get_table_data(request):


    # data = {'id': 1, 'column_name': 'abc', 'value': 'ABCD'}

    return HttpResponse(json.dumps(data), content_type="application/json")

def save_year(request):
    print(request.POST)
    pass