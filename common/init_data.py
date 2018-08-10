from django.conf import settings
import os
from masters.models import AllCountries
from student.models import PassingYear
from datetime import datetime
import json
import pycountry

"""
>>> from common.init_data import load_initial_data
>>> load_initial_data()
"""

def import_years():
    now = int(datetime.now().year)

    for year in range(1960, now+1):
        PassingYear.objects.create(year=year)

def import_world_all_countries():
    for country in pycountry.countries:
        AllCountries.objects.create(country_name=country.name)


def load_initial_data():
    import_years()
    import_world_all_countries()
