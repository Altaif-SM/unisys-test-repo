from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
import json
from masters.models import *
from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.db.models import Q
import base64
from django.conf import settings
from common.utils import *
from partner.models import *
from datetime import date
import datetime
from django.http import HttpResponse, JsonResponse
from datetime import datetime




# *********------------ Year Master ----------***************

def template_year_master(request):
    year_recs = YearDetails.objects.all()
    return render(request, 'template_year_master.html', {'year_recs': year_recs})


def save_year(request):
    year_name = request.POST.get('year_name')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    end_dt = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date()
    start_dt = datetime.datetime.strptime(str(start_date), "%Y-%m-%d").date()

    try:
        if  YearDetails.objects.filter(year_name=year_name.lower()).exists():
            messages.warning(request, "Year name already exists. Record not saved.")

        elif  YearDetails.objects.all().filter((Q(start_date__lte=start_dt) & Q(end_date__gte=end_dt)) | Q(start_date__range=(start_dt, end_dt)) | Q(end_date__range=(start_dt, end_dt))):
                messages.success(request, "Academic year already Exists")

        else:

            # today = date.today()
            #
            # if (start_dt <= today) and (end_dt > today):
            #     YearDetails.objects.filter().update(active_year = False)
            #     YearDetails.objects.filter().update(base_date = False)
            #     YearDetails.objects.create(year_name=year_name.lower(), start_date=start_date, end_date=end_date,active_year = True,base_date = True)
            # else:
            #     YearDetails.objects.create(year_name=year_name.lower(), start_date=start_date, end_date=end_date)

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
    end_dt = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date()
    start_dt = datetime.datetime.strptime(str(start_date), "%Y-%m-%d").date()
    try:
        if YearDetails.objects.filter(~Q(id=year_id), year_name=year_name.lower()).exists():
            messages.success(request, "Year name already exists. Record not updated..")

        # elif YearDetails.objects.filter(~Q(id=year_id)).filter((Q(start_date__lte=start_date) & Q(end_date__gte=end_date)) | Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date))):
        #     messages.success(request, "Academic year already Exists")
        else:
            # today = date.today()
            # if (start_dt <= today) and (end_dt > today):
            #     YearDetails.objects.filter().update(active_year=False)
            #     YearDetails.objects.filter().update(base_date=False)
            #     YearDetails.objects.filter(id=year_id).update(year_name=year_name.lower(), start_date=start_date,end_date=end_date,active_year = True,base_date = True)
            # else:
            #     YearDetails.objects.filter(id=year_id).update(year_name=year_name.lower(), start_date=start_date,
            #                                                   end_date=end_date,active_year = False)
            YearDetails.objects.filter(id=year_id).update(year_name=year_name.lower(), start_date=start_date,
                                                              end_date=end_date)
            messages.success(request, "Record saved.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
        return HttpResponse(json.dumps({'success': 'Year name already exists. Record not saved.'}),
                            content_type="application/json")

    except:
        messages.warning(request, "Record not saved.")
    return HttpResponse(json.dumps({'error': 'Record not updated.'}), content_type="application/json")


def delete_years(request):
    year_id = request.POST.get('year_id')

    try:
        YearDetails.objects.filter(id=year_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


def change_session_year(request):
    year_id = request.POST.get('selected_year')

    try:
        # YearDetails.objects.get(id=year_id)
        request.session['selected_year'] = YearDetails.objects.get(id=year_id).id
    except:
        request.session['selected_year'] = ''

    return HttpResponse(json.dumps({}), content_type="application/json")


# *********------------ Scholarship Master ----------***************

def template_scholarship_master(request):
    scholarship_recs = ScholarshipDetails.objects.all()
    return render(request, 'template_scholarship_master.html', {'scholarship_recs': scholarship_recs})


def save_scholarship(request):
    scholarship_name = request.POST.get('scholarship_name')
    try:
        if not ScholarshipDetails.objects.filter(scholarship_name=scholarship_name).exists():
            ScholarshipDetails.objects.create(scholarship_name=scholarship_name)
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
        if not ScholarshipDetails.objects.filter(~Q(id=scholarship_id),
                                                 scholarship_name=scholarship_name).exists():
            ScholarshipDetails.objects.filter(id=scholarship_id).update(scholarship_name=scholarship_name)
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
    except Exception as e:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


# *********------------ Country Master ----------***************

def country_settings(request):
    country_recs = CountryDetails.objects.all()
    return render(request, 'template_country_master.html', {'country_recs': country_recs})


def save_country(request):
    country_name = request.POST.get('country_name')
    try:
        if not CountryDetails.objects.filter(country_name=country_name.lower()).exists():
            CountryDetails.objects.create(country_name=country_name.lower())
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Country name already exists.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/country_settings/')


def update_country(request):
    country_id = request.POST.get('country_id')
    country_name = request.POST.get('country_name')
    try:
        if not CountryDetails.objects.filter(~Q(id=country_id), country_name=country_name.lower()).exists():
            CountryDetails.objects.filter(id=country_id).update(country_name=country_name.lower())
            messages.success(request, "Record saved.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
        else:
            messages.warning(request, "Country name already exists.")
            return HttpResponse(json.dumps({'success': '"Country name already exists.'}),
                                content_type="application/json")
    except:
        messages.warning(request, "Record not saved.")
    return HttpResponse(json.dumps({'error': 'Record not updated.'}), content_type="application/json")


def delete_country(request):
    country_delete_id = request.POST.get('country_delete_id')
    try:
        CountryDetails.objects.filter(id=country_delete_id).delete()
        messages.success(request, "Record deleted.")
    except:
        messages.warning(request, "Record not deleted.")
    return redirect('/masters/country_settings/')


# *********------------ University Master ----------***************

def template_university_master(request):
    university_recs = UniversityDetails.objects.all()
    country_recs = CountryDetails.objects.all()
    return render(request, 'template_university_master.html',
                  {'university_recs': university_recs, 'country_recs': country_recs})


def save_university(request):
    university_name = request.POST.get('university_name')
    country_id = request.POST.get('country')
    try:
        if not UniversityDetails.objects.filter(university_name=university_name.lower(),
                                                country_id=country_id).exists():
            UniversityDetails.objects.create(university_name=university_name.lower(), country_id=country_id)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "University and Country relation already exists. Record not saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_university_master/')


def update_university(request):
    university_id = request.POST.get('university_id')
    university_name = request.POST.get('university_name')
    country_id = request.POST.get('country_id')
    try:
        if not UniversityDetails.objects.filter(~Q(id=university_id), university_name=university_name.lower(),
                                                country_id=country_id).exists():
            UniversityDetails.objects.filter(id=university_id).update(university_name=university_name.lower(),
                                                                      country_id=country_id)
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request, "University and Country relation already exists. Record not updated.")
            return HttpResponse(
                json.dumps({'success': "University and Country relation already exists. Record not updated."}),
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


# *********------------ Semester Master ----------***************

def template_semester_master(request):
    semester_recs = SemesterDetails.objects.all()
    return render(request, 'template_semester_master.html', {'semester_recs': semester_recs})


def save_semester(request):
    semester_name = request.POST.get('semester_name')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    try:
        if not SemesterDetails.objects.filter(semester_name=semester_name.lower()).exists():
            SemesterDetails.objects.create(semester_name=semester_name.lower(), start_date=start_date,
                                           end_date=end_date)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Semester name already exists. Record not saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_semester_master/')


def update_semester(request):
    semester_id = request.POST.get('semester_id')
    semester_name = request.POST.get('semester_name')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    try:
        if not SemesterDetails.objects.filter(~Q(id=semester_id), semester_name=semester_name.lower()).exists():
            SemesterDetails.objects.filter(id=semester_id).update(semester_name=semester_name.lower(),
                                                                  start_date=start_date, end_date=end_date)
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")

    except:
        messages.warning(request, "Semester name already exists. Record not updated.")
    return HttpResponse(json.dumps({'error': 'Semester name already exists. Record not updated.'}),
                        content_type="application/json")


def delete_semesters(request):
    semester_id = request.POST.get('semester_id')

    try:
        SemesterDetails.objects.filter(id=semester_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


# *********------------ Degree Master ----------***************

def template_degree_master(request):
    degree_recs = DegreeDetails.objects.all()
    degree_type_recs = DegreeTypeDetails.objects.all()
    return render(request, 'template_degree_master.html',
                  {'degree_recs': degree_recs, 'degree_type_recs': degree_type_recs})


def save_degree(request):
    degree_name = request.POST.get('degree_name')
    degree_type_id = request.POST.get('degree_type')
    try:
        if not DegreeDetails.objects.filter(degree_name=degree_name.lower(), degree_type_id=degree_type_id).exists():
            DegreeDetails.objects.create(degree_name=degree_name.lower(), degree_type_id=degree_type_id)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Degree and degree type relation already exists. Record not saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_degree_master/')


def update_degree(request):
    degree_id = request.POST.get('degree_id')
    degree_name = request.POST.get('degree_name')
    degree_type_id = request.POST.get('degree_type_id')
    try:
        if not DegreeDetails.objects.filter(~Q(id=degree_id), degree_name=degree_name.lower(),
                                            degree_type_id=degree_type_id).exists():
            DegreeDetails.objects.filter(id=degree_id).update(degree_name=degree_name.lower(),
                                                              degree_type_id=degree_type_id)
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request, "Degree and degree type relation already exists. Record not updated.")
            return HttpResponse(
                json.dumps({'success': "Degree and degree type relation already exists. Record not updated."}),
                content_type="application/json")

    except:
        messages.warning(request, "Degree name already exists. Record not updated.")
    return HttpResponse(json.dumps({'error': 'Degree name already exists. Record not updated.'}),
                        content_type="application/json")


def delete_degree(request):
    degree_id = request.POST.get('degree_id')

    try:
        DegreeDetails.objects.filter(id=degree_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


# *********------------ Program Master ----------***************

def template_program_master(request):
    program_recs = ProgramDetails.objects.all()
    degree_type_recs = DegreeTypeDetails.objects.all()
    university_recs = UniversityDetails.objects.all()
    return render(request, 'template_program_master.html',
                  {'program_recs': program_recs, 'degree_type_recs': degree_type_recs,
                   'university_recs': university_recs})


def save_program(request):
    program_name = request.POST.get('program_name')
    degree_type_id = request.POST.getlist('degree_type')
    university = request.POST.getlist('university')
    try:
        for degree in degree_type_id:
            if degree :
                for rec in university:
                    if rec :
                        data = ProgramDetails.objects.filter(program_name=program_name.lower(), degree_type_id=degree,university_id=rec)
                        if data:
                            pass
                        else:
                            ProgramDetails.objects.create(program_name=program_name.lower(), degree_type_id=degree,university_id=rec)

        messages.success(request, "Record saved.")

    except Exception as e:
        messages.warning(request, "Record not saved." +str(e))

    return redirect('/masters/template_program_master/')


def update_program(request):
    program_id = request.POST.get('program_id')
    program_name = request.POST.get('program_name')
    degree_type_id = request.POST.get('degree_type_id')
    university = request.POST.get('university_id')
    try:
        if not ProgramDetails.objects.filter(~Q(id=program_id), program_name=program_name.lower(),
                                             degree_type_id=degree_type_id,
                                             university_id=university).exists():
            ProgramDetails.objects.filter(id=program_id).update(program_name=program_name.lower(),
                                                                degree_type_id=degree_type_id,
                                                                university_id=university)
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request, "Program, degree type and university relation already exists. Record not saved.")
            return HttpResponse(
                json.dumps(
                    {'success': "Program, degree type and university relation already exists. Record not saved."}),
                content_type="application/json")

    except:
        messages.warning(request, "Record not updated.")
    return HttpResponse(json.dumps({'error': 'Record not updated.'}),
                        content_type="application/json")


def delete_programs(request):
    program_id = request.POST.get('program_id')

    try:
        ProgramDetails.objects.filter(id=program_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


# *********------------ Module Master ----------***************

def template_module_master(request):
    module_recs = ModuleDetails.objects.all()
    country_recs = CountryDetails.objects.all()
    return render(request, 'template_module_master.html',
                  {'module_recs': module_recs, 'country_recs': country_recs})


def save_module(request):
    module_name = request.POST.get('module_name')
    country_id = request.POST.get('country')
    try:
        if not ModuleDetails.objects.filter(module_name=module_name.lower(),
                                            country_id=country_id).exists():
            ModuleDetails.objects.create(module_name=module_name.lower(), country_id=country_id)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Module and Country relation already exists. Record not saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_module_master/')


def update_module(request):
    module_id = request.POST.get('module_id')
    module_name = request.POST.get('module_name')
    country_id = request.POST.get('country_id')
    try:
        if not ModuleDetails.objects.filter(~Q(id=module_id), module_name=module_name.lower(),
                                            country_id=country_id).exists():
            ModuleDetails.objects.filter(id=module_id).update(module_name=module_name.lower(),
                                                              country_id=country_id)
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request, "Module and Country relation already exists. Record not updated.")
            return HttpResponse(
                json.dumps({'success': "Module and Country relation already exists. Record not updated."}),
                content_type="application/json")

    except:
        messages.warning(request, "Module name already exists. Record not updated.")
    return HttpResponse(json.dumps({'error': 'Module name already exists. Record not updated.'}),
                        content_type="application/json")


def delete_module(request):
    module_id = request.POST.get('module_id')

    try:
        ModuleDetails.objects.filter(id=module_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


# *********------------ Master and PhD Master ----------***************

# def template_master_and_phd_master(request):
#     master_and_phd_recs = MasterAndPhdFormula.objects.all()
#     scholarship_recs = ScholarshipDetails.objects.all()
#     return render(request, 'template_master_and_phd_master.html',
#                   {'master_and_phd_recs': master_and_phd_recs, 'scholarship_recs': scholarship_recs})


def template_master_and_phd_master(request):
    try:
        master_and_phd_recs = DegreeFormula.objects.filter(degree_type__degree_name__in=['phd','master'])
        scholarship_recs = ScholarshipDetails.objects.all()
        # degree_type_rec = ''
        degree_type_rec = []

        if DegreeTypeDetails.objects.filter(degree_name='phd').exists():
            degree_type = DegreeTypeDetails.objects.get(degree_name='phd')
            degree_type_rec.append(degree_type)
        if DegreeTypeDetails.objects.filter(degree_name='master').exists():
            degree_master = DegreeTypeDetails.objects.get(degree_name='master')
            degree_type_rec.append(degree_master)

        return render(request, 'template_master_and_phd_master.html',
                      {'master_and_phd_recs': master_and_phd_recs, 'scholarship_recs': scholarship_recs,
                       'degree_type_rec': degree_type_rec})
    except Exception as e:
        messages.warning(request, "Record not saved." + str(e))
    return redirect('/masters/template_master_and_phd_master/')


def save_master_and_phd(request):
    scholarship_id = request.POST.get('scholarship')
    result = request.POST.get('result')
    repayment = request.POST.get('repayment')
    degree_type = request.POST.get('degree_type')
    try:
        if not DegreeFormula.objects.filter(scholarship_id=scholarship_id.lower(),
                                            result=result.lower(), degree_type_id=degree_type).exists():
            DegreeFormula.objects.create(scholarship_id=scholarship_id,
                                         result=result.lower(), repayment=repayment, degree_type_id=degree_type)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Formula already exists for this master. Record not saved.")
    except Exception as e:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_master_and_phd_master/')


# def save_master_and_phd(request):
#     scholarship_id = request.POST.get('scholarship')
#     result = request.POST.get('result')
#     repayment = request.POST.get('repayment')
#     try:
#         if not MasterAndPhdFormula.objects.filter(scholarship_id=scholarship_id.lower(),
#                                                   result=result.lower()).exists():
#             MasterAndPhdFormula.objects.create(scholarship_id=scholarship_id,
#                                                result=result.lower(), repayment=repayment)
#             messages.success(request, "Record saved.")
#         else:
#             messages.warning(request, "Formula already exists for this master. Record not saved.")
#     except:
#         messages.warning(request, "Record not saved.")
#     return redirect('/masters/template_master_and_phd_master/')


def update_master_and_phd(request):
    master_and_phd_id = request.POST.get('master_and_phd_id')
    scholarship_id = request.POST.get('scholarship_id')
    result = request.POST.get('result')
    repayment = request.POST.get('repayment')
    degree_type_id = request.POST.get('degree_type')
    try:
        if not DegreeFormula.objects.filter(~Q(id=master_and_phd_id), scholarship_id=scholarship_id,
                                                  result=result.lower()).exists():
            DegreeFormula.objects.filter(id=master_and_phd_id).update(scholarship_id=scholarship_id.lower(),
                                                                            result=result.lower(),
                                                                            repayment=repayment.lower(),degree_type_id=degree_type_id)
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request, "Formula already exists for this master. Record not saved.")
            return HttpResponse(
                json.dumps({'success': "Formula already exists for this master. Record not saved."}),
                content_type="application/json")

    except:
        messages.warning(request, "Record not updated.")
    return HttpResponse(json.dumps({'error': 'Record not updated.'}),
                        content_type="application/json")


def delete_master_and_phd(request):
    master_and_phd_id = request.POST.get('master_and_phd_id')

    try:
        DegreeFormula.objects.filter(id=master_and_phd_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


def formula_type_master(request):
   # degree_type = DegreeTypeDetails.objects.all()
    try:
        degree_type = DegreeTypeDetails.objects.all().exclude(degree_name__in=['master', 'masters (course work)', 'phd'])
        if request.POST:
            degree_type = request.POST.get('degree_type')

            degree_type_name = DegreeTypeDetails.objects.get(id=degree_type).degree_name

            if degree_type_name == 'masters (course work)':
                return redirect('/masters/template_master_course_work_master/')

            elif degree_type_name == 'phd':
                return redirect('/masters/template_master_and_phd_master/')

            else:
                degree_recs = DegreeFormula.objects.filter(degree_type=degree_type)
                scholarship_recs = ScholarshipDetails.objects.all()
                degree_type_recs = DegreeTypeDetails.objects.get(id=degree_type)

                return render(request, 'template_degree_formula_master.html',
                              {'scholarship_recs': scholarship_recs,
                               'degree_type_recs': degree_type_recs,'degree_recs':degree_recs})
    except:
        messages.warning(request, 'Some error occoured.')

    return render(request, 'template_formula_type_master.html',
                  {'degree_type_recs': degree_type})


# *********------------ Master and course work Master ----------***************

# def template_master_course_work_master(request):
#     course_work_recs = MasterAndCourseFormula.objects.all()
#     scholarship_recs = ScholarshipDetails.objects.all()
#     return render(request, 'template_course_work_master.html',
#                   {'course_work_recs': course_work_recs, 'scholarship_recs': scholarship_recs})


def template_master_course_work_master(request):
    course_work_recs = DegreeFormula.objects.filter(degree_type__degree_name='masters (course work)')
    scholarship_recs = ScholarshipDetails.objects.all()

    degree_type_rec = ''

    if DegreeTypeDetails.objects.filter(degree_name='masters (course work)').exists():
        degree_type_rec = DegreeTypeDetails.objects.get(degree_name='masters (course work)')

    return render(request, 'template_course_work_master.html',
                  {'course_work_recs': course_work_recs, 'scholarship_recs': scholarship_recs,
                   'degree_type_rec': degree_type_rec})


def save_master_course_work(request):
    scholarship_id = request.POST.get('scholarship')
    result_min = request.POST.get('result_min')
    result_max = request.POST.get('result_max')
    repayment = request.POST.get('repayment')
    degree_type = request.POST.get('degree_type')

    try:
        if not DegreeFormula.objects.filter(scholarship_id=scholarship_id.lower(),
                                            cgpa_max=result_max.lower(),
                                            cgpa_min=result_min.lower(), degree_type_id=degree_type).exists():

            DegreeFormula.objects.create(scholarship_id=scholarship_id, cgpa_max=result_max,
                                         cgpa_min=result_min, repayment=repayment, degree_type_id=degree_type)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Formula already exists for this master. Record not saved.")
    except Exception as e:
        messages.warning(request, "Record not saved."+str(e))
    return redirect('/masters/template_master_course_work_master/')


# def save_master_course_work(request):
#     scholarship_id = request.POST.get('scholarship')
#     result_min = request.POST.get('result_min')
#     result_max = request.POST.get('result_max')
#     repayment = request.POST.get('repayment')
#     try:
#         if not MasterAndCourseFormula.objects.filter(scholarship_id=scholarship_id.lower(),
#                                                      result_max=result_max.lower(),
#                                                      result_min=result_min.lower()).exists():
#             MasterAndCourseFormula.objects.create(scholarship_id=scholarship_id, result_max=result_max.lower(),
#                                                   result_min=result_min.lower(), repayment=repayment)
#             messages.success(request, "Record saved.")
#         else:
#             messages.warning(request, "Formula already exists for this master. Record not saved.")
#     except:
#         messages.warning(request, "Record not saved.")
#     return redirect('/masters/template_master_course_work_master/')


def update_master_course_work(request):
    course_work_id = request.POST.get('course_work_id')
    scholarship_id = request.POST.get('scholarship_id')
    result_min = request.POST.get('result_min')
    result_max = request.POST.get('result_max')
    repayment = request.POST.get('repayment')
    try:
        if not DegreeFormula.objects.filter(~Q(id=course_work_id), scholarship_id=scholarship_id.lower(),
                                            cgpa_max=result_max.lower(),
                                            cgpa_min=result_min.lower()).exists():

            DegreeFormula.objects.filter(id=course_work_id).update(scholarship_id=scholarship_id.lower(),
                                                                            cgpa_max=result_max.lower(),
                                                                            cgpa_min=result_min.lower(),
                                                                            repayment=repayment.lower())
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request, "Formula already exists for this master. Record not saved.")
            return HttpResponse(
                json.dumps({'success': "Formula already exists for this master. Record not saved."}),
                content_type="application/json")

    except:
        messages.warning(request, "Record not updated.")
    return HttpResponse(json.dumps({'error': 'Record not updated.'}),
                        content_type="application/json")


def delete_master_course_work(request):
    course_work_id = request.POST.get('course_work_id')

    try:
        MasterAndCourseFormula.objects.filter(id=course_work_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


# *********------------ Degree formula Master ----------***************

# def template_degree_formula_master(request):
#     degree_recs = DegreeFormula.objects.all()
#     scholarship_recs = ScholarshipDetails.objects.all()
#     degree_type_recs = DegreeTypeDetails.objects.filter(degree_name='degree')
#
#     if degree_type_recs:
#         degree_type_recs = degree_type_recs[0]
#     return render(request, 'template_degree_formula_master.html',
#                   {'degree_recs': degree_recs, 'scholarship_recs': scholarship_recs,
#                    'degree_type_recs': degree_type_recs})

def template_degree_formula_master(request):
    degree_recs = DegreeFormula.objects.all()
    scholarship_recs = ScholarshipDetails.objects.all()
    degree_type_recs = DegreeTypeDetails.objects.filter(degree_name='degree')

    if degree_type_recs:
        degree_type_recs = degree_type_recs[0]
    return render(request, 'template_degree_formula_master.html',
                  {'degree_recs': degree_recs, 'scholarship_recs': scholarship_recs,
                   'degree_type_recs': degree_type_recs})


def save_degree_formula_master(request):
    scholarship_id = request.POST.get('scholarship')
    degree_type = request.POST.get('degree_type')
    cgpa_min = request.POST.get('cgpa_min')
    cgpa_max = request.POST.get('cgpa_max')

    grade_min = request.POST.get('grade_min')
    grade_max = request.POST.get('grade_max')
    repayment = request.POST.get('repayment')
    try:
        if not DegreeFormula.objects.filter(Q(cgpa_max=cgpa_max,
                                              cgpa_min=cgpa_min) or Q(grade_max=grade_max,
                                                                      grade_min=grade_min),
                                            scholarship_id=scholarship_id.lower()).exists():

            DegreeFormula.objects.create(scholarship_id=scholarship_id, cgpa_max=cgpa_max, degree_type_id=degree_type,
                                         cgpa_min=cgpa_min, grade_max=grade_max,
                                         grade_min=grade_min, repayment=repayment)

            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Formula already exists for this master. Record not saved.")
    except Exception as e:
        messages.warning(request, "Record not saved."+str(e))

    degree_recs = DegreeFormula.objects.filter(degree_type=degree_type)
    scholarship_recs = ScholarshipDetails.objects.all()
    degree_type_recs = DegreeTypeDetails.objects.get(id=degree_type)

    return render(request, 'template_degree_formula_master.html',
                  {'scholarship_recs': scholarship_recs,
                   'degree_type_recs': degree_type_recs, 'degree_recs': degree_recs})
    # return redirect('/masters/template_degree_formula_master/')


def update_degree_formula_master(request):
    degree_id = request.POST.get('degree_id')
    scholarship_id = request.POST.get('scholarship_id')
    cgpa_min = request.POST.get('cgpa_min')
    cgpa_max = request.POST.get('cgpa_max')

    grade_min = request.POST.get('grade_min')
    grade_max = request.POST.get('grade_max')
    repayment = request.POST.get('repayment')
    try:
        if not DegreeFormula.objects.filter(~Q(id=degree_id), Q(cgpa_max=cgpa_max,
                                                                cgpa_min=cgpa_min) or Q(grade_max=grade_max,
                                                                                        grade_min=grade_min),
                                            scholarship_id=scholarship_id.lower()).exists():

            DegreeFormula.objects.filter(id=degree_id).update(scholarship_id=scholarship_id, cgpa_max=cgpa_max,
                                                              cgpa_min=cgpa_min, grade_max=grade_max,
                                                              grade_min=grade_min, repayment=repayment)
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request, "Formula already exists for this master. Record not saved.")
            return HttpResponse(
                json.dumps({'success': "Formula already exists for this master. Record not saved."}),
                content_type="application/json")

    except:
        messages.warning(request, "Record not updated.")
    return HttpResponse(json.dumps({'error': 'Record not updated.'}),
                        content_type="application/json")


def delete_degree_formula_master(request):
    degree_id = request.POST.get('degree_id')

    try:
        DegreeFormula.objects.filter(id=degree_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


# *********------------ Development Program Master ----------***************

def template_development_program_master(request):
    year_recs = YearDetails.objects.all()
    semester_recs = SemesterDetails.objects.all()
    module_recs = ModuleDetails.objects.all()
    # development_program_recs = DevelopmentProgram.objects.all()
    development_program_recs = SoftSkillDevelopmentProgram.objects.all()
    return render(request, 'template_development_program_master.html',
                  {'year_recs': year_recs, 'semester_recs': semester_recs, 'module_recs': module_recs,
                   'development_program_recs': development_program_recs})


# def save_development_program_master(request):
#     year_name = request.POST.get('year_name')
#     semester_name = request.POST.get('semester_name')
#     module_name = request.POST.get('module_name')
#     code_name = request.POST.get('code_name')
#     name = request.POST.get('name')
#
#     activities = request.POST.get('activities')
#     outcomes = request.POST.get('outcomes')
#
#     day_duration = request.POST.get('day_duration')
#     night_duration = request.POST.get('night_duration')
#     method_name = request.POST.get('method_name')
#
#     mark_name = request.POST.get('mark_name')
#     date_name = request.POST.get('date_name')
#     remark_name = request.POST.get('remark_name')
#     try:
#         if not DevelopmentProgram.objects.filter(year_id=year_name, semester_id=semester_name, name=name,
#                                                  module_id=module_name).exists():
#             DevelopmentProgram.objects.create(year_id=year_name, semester_id=semester_name, module_id=module_name,
#                                               code=code_name, date=date_name, marks=mark_name, name=name,
#                                               method=method_name, duration_night=night_duration,
#                                               duration_day=day_duration, outcome=outcomes, activity=activities,
#                                               remark=remark_name)
#             messages.success(request, "Record saved.")
#         else:
#             messages.warning(request,
#                              "Development program is already exist for this Year, semester and module. Record not saved.")
#     except:
#         messages.warning(request, "Record not saved.")
#     return redirect('/masters/template_development_program_master/')


def save_development_program_master(request):
    program_name = request.POST.get('program_name')
    objectives = request.POST.get('objectives')
    delivery_method = request.POST.get('delivery_method')
    delivery_location = request.POST.get('delivery_location')
    organizer = request.POST.get('organizer')

    delivery_date = request.POST.get('delivery_date')
    completion_deadline = request.POST.get('completion_deadline')

    rsvp_method = request.POST.get('rsvp_method')
    remarks = request.POST.get('remarks')
    try:
        SoftSkillDevelopmentProgram.objects.create(program_name=program_name, objectives=objectives, delivery_method=delivery_method,
                                          delivery_location=delivery_location, organizer=organizer, delivery_date=delivery_date, completion_deadline=completion_deadline,

                                          rsvp_method=rsvp_method, remarks=remarks)
        messages.success(request, "Record saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_development_program_master/')


# def update_development_program_master(request):
#     development_program_id = request.POST.get('development_program_id')
#
#     year_name = request.POST.get('year_name')
#     name = request.POST.get('name')
#     semester_name = request.POST.get('semester_name')
#     module_name = request.POST.get('module_name')
#     code_name = request.POST.get('code_name')
#
#     activities = request.POST.get('activities')
#     outcomes = request.POST.get('outcomes')
#
#     day_duration = request.POST.get('day_duration')
#     night_duration = request.POST.get('night_duration')
#     method_name = request.POST.get('method_name')
#
#     mark_name = request.POST.get('mark_name')
#     date_name = request.POST.get('date_name')
#     remark_name = request.POST.get('remark_name')
#     try:
#         if not DevelopmentProgram.objects.filter(~Q(id=development_program_id), year_id=year_name,
#                                                  semester_id=semester_name,
#                                                  module_id=module_name).exists():
#
#             DevelopmentProgram.objects.filter(id=development_program_id).update(year_id=year_name,
#                                                                                 semester_id=semester_name,
#                                                                                 module_id=module_name, name=name,
#                                                                                 code=code_name, date=date_name,
#                                                                                 marks=mark_name,
#                                                                                 method=method_name,
#                                                                                 duration_night=night_duration,
#                                                                                 duration_day=day_duration,
#                                                                                 outcome=outcomes,
#                                                                                 activity=activities,
#                                                                                 remark=remark_name)
#             messages.success(request, "Record updated.")
#             return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
#         else:
#             messages.warning(request,
#                              "Development program is already exist for this Year, semester and module. Record not saved.")
#             return HttpResponse(
#                 json.dumps({
#                     'success': "Development program is already exist for this Year, semester and module. Record not saved."}),
#                 content_type="application/json")
#
#     except:
#         messages.warning(request, "Record not updated.")
#     return HttpResponse(json.dumps({'error': 'Record not updated.'}),
#                         content_type="application/json")
def update_development_program_master(request):
    development_program_id = request.POST.get('development_program_id')
    program_name = request.POST.get('program_name')
    objectives = request.POST.get('objectives')
    delivery_method = request.POST.get('delivery_method')
    delivery_location = request.POST.get('delivery_location')
    organizer = request.POST.get('organizer')
    delivery_date = request.POST.get('delivery_date')
    completion_deadline = request.POST.get('completion_deadline')
    rsvp_method = request.POST.get('rsvp_method')
    remarks = request.POST.get('remarks')
    try:
        SoftSkillDevelopmentProgram.objects.filter(id=development_program_id).update(program_name=program_name,
                                                                                     objectives=objectives,
                                                                                     delivery_method=delivery_method, delivery_location=delivery_location,
                                                                                     organizer=organizer, delivery_date=delivery_date,
                                                                                     completion_deadline=completion_deadline,
                                                                                     rsvp_method=rsvp_method,
                                                                                     remarks=remarks)
        messages.success(request, "Record updated.")
        return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")

    except:
        messages.warning(request, "Record not updated.")
    return HttpResponse(json.dumps({'error': 'Record not updated.'}),
                        content_type="application/json")


def delete_development_program_master(request):
    development_program_id = request.POST.get('development_program_id')

    try:
        SoftSkillDevelopmentProgram.objects.filter(id=development_program_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


# *********------------ Manage Partner Master ----------***************

def template_manage_partner_master(request):
    country_recs = CountryDetails.objects.all()
    partner_recs = PartnerDetails.objects.all()

    user_recs = User.objects.filter(role__name__in=['Partner'])

    query_query = request.GET.get("user") or None
    partner_rec = {}
    selected_user = {}
    if query_query:
        selected_user = User.objects.get(id=query_query)
        partner_rec = PartnerDetails.objects.get(user_id=query_query)

    # user_recs = User.objects.all()#.role.all().filter(name__in=[self.DONOR])
    # user_recs = User.objects.filter(role__name__in=['Partner'])
    return render(request, 'template_partner_master.html',
                  {'country_recs': country_recs, 'partner_recs': partner_recs, 'user_recs': user_recs,
                   'partner_rec': partner_rec, 'selected_user': selected_user})


def save_manage_partner_master(request):
    country = request.POST.get('country')
    office_name = request.POST.get('office_name')
    person_one = request.POST.get('person_one')
    person_one_contact = request.POST.get('person_one_contact')

    person_two = request.POST.get('person_two')
    person_two_contact = request.POST.get('person_two_contact')
    office_contact = request.POST.get('office_contact')

    email = request.POST.get('email')
    user = request.POST.get('user')
    address = request.POST.get('address')
    photo = request.POST.get('photo')
    pic = request.POST.get('pic')

    partner_details_id = request.POST.get('partner_details_id')

    try:
        country = CountryDetails.objects.get(id=country)
        parent_obj = PartnerDetails.objects.filter(id=partner_details_id).update(country_id=country,
                                                                                 office_name=office_name,
                                                                                 person_one=person_one,
                                                                                 person_one_contact_number=person_one_contact,
                                                                                 person_two=person_two,
                                                                                 person_two_contact_number=person_two_contact,
                                                                                 office_contact_number=office_contact,
                                                                                 email=email, single_address=address)

        address = AddressDetails.objects.filter(id=PartnerDetails.objects.get(id=partner_details_id).address.id).update(
            country=country)
        try:
            if pic:
                partner_obj = PartnerDetails.objects.get(id=partner_details_id)
                dirname = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
                filename = "%s_%s.%s" % (str(partner_obj.id), dirname, 'png')
                raw_file_path_and_name = os.path.join('images/' + filename)
                data = str(pic)
                temp_data = data.split('base64,')[1]
                raw_data = base64.b64decode(temp_data)
                f = open(settings.MEDIA_ROOT + raw_file_path_and_name, 'wb')
                f.write(raw_data)
                f.close()
                partner_obj.photo = raw_file_path_and_name
                partner_obj.save()
        except Exception as e:
            messages.warning(request, "Form have some error" + str(e))

        messages.success(request, "Record Updated.")

        # if not PartnerDetails.objects.filter(country_id=country, office_name=office_name).exists():
        #     parent_obj = PartnerDetails.objects.create(country_id=country, office_name=office_name,
        #                                                person_one=person_one,
        #                                                person_one_contact_number=person_one_contact,
        #                                                person_two=person_two,
        #                                                person_two_contact_number=person_two_contact,
        #                                                office_contact_number=office_contact,
        #                                                email=email, single_address=address, user_id=user)
        #
        #     try:
        #         if pic:
        #             dirname = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        #             filename = "%s_%s.%s" % (str(parent_obj.id), dirname, 'png')
        #             raw_file_path_and_name = os.path.join('images/' + filename)
        #             data = str(pic)
        #             temp_data = data.split('base64,')[1]
        #             raw_data = base64.b64decode(temp_data)
        #             f = open(settings.MEDIA_ROOT + raw_file_path_and_name, 'wb')
        #             f.write(raw_data)
        #             f.close()
        #             parent_obj.photo = raw_file_path_and_name
        #             parent_obj.save()
        #     except Exception as e:
        #         messages.warning(request, "Form have some error" + str(e))
        #         return redirect('/masters/template_manage_partner_master/')
        #     messages.success(request, "Record saved.")
        # else:
        #     messages.warning(request, "Partner and country is already exist. Record not saved.")
    except Exception as e:
        messages.warning(request, "Record not saved." + str(e))
    return redirect('/masters/template_manage_partner_master/')


def update_manage_partner_master(request):
    partner_id = request.POST.get('partner_id')

    country = request.POST.get('country_name')
    office_name = request.POST.get('office_name')
    person_one = request.POST.get('person_one')
    person_one_contact = request.POST.get('person_one_contact')

    office_contact = request.POST.get('office_contact')

    email = request.POST.get('email')
    address = request.POST.get('address')
    try:
        if not PartnerDetails.objects.filter(~Q(id=partner_id), country_id=country, office_name=office_name).exists():

            PartnerDetails.objects.filter(id=partner_id).update(country_id=country, person_one=person_one,
                                                                person_one_contact_number=person_one_contact,
                                                                office_contact_number=office_contact,
                                                                email=email, single_address=address,
                                                                office_name=office_name)
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request,
                             "Partner and country is already exist. Record not updated.")
            return HttpResponse(
                json.dumps({
                    'success': "Partner and country is already exist. Record not updated."}),
                content_type="application/json")

    except:
        messages.warning(request, "Record not updated.")
    return HttpResponse(json.dumps({'error': 'Record not updated.'}),
                        content_type="application/json")


def delete_manage_partner_master(request):
    partner_id = request.POST.get('partner_id')

    try:
        PartnerDetails.objects.filter(id=partner_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


def export_partner_list(request):
    try:
        partner_recs = PartnerDetails.objects.all().values_list('address__country__country_name', 'office_name',
                                                                'person_one', 'person_one_contact_number',
                                                                'office_contact_number', 'email', 'single_address')
        column = ['Country', 'Office Name', 'Person One', 'Person One Contact', 'Office Contact', 'Email', 'Address']
        return export_wraped_column_xls('Parent_Details', column, partner_recs)
    except Exception as e:
        messages.warning(request, "Record not exported." + str(e))
    return redirect('/masters/template_manage_partner_master/')


# *********------------ Manage Donor Master ----------***************

def template_manage_donor_master(request):
    country_recs = CountryDetails.objects.all()
    donor_recs = DonorDetails.objects.all()
    user_recs = User.objects.filter(role__name="Donor")

    query_query = request.GET.get("user") or None
    donor_rec = {}
    selected_user = {}
    if query_query:
        selected_user = User.objects.get(id=query_query)
        donor_rec = DonorDetails.objects.get(user_id=query_query)

    return render(request, 'template_donor_master.html',
                  {'country_recs': country_recs, 'donor_recs': donor_recs, 'user_recs': user_recs,
                   'donor_rec': donor_rec, 'selected_user': selected_user})


def save_manage_donor_master(request):
    organisation = request.POST.get('organisation')
    country = request.POST.get('country')
    person = request.POST.get('person')
    person_contact = request.POST.get('person_contact')

    donor_address = request.POST.get('donor_address')
    email = request.POST.get('email')
    reg_document = request.POST.get('reg_document')
    due_amount = request.POST.get('due_amount')

    bank_account_number = request.POST.get('bank_account_number')
    bank_name = request.POST.get('bank_name')
    bank_swift_code = request.POST.get('bank_swift_code')
    donor_bank_address = request.POST.get('donor_bank_address')
    abc_document = request.FILES.get('reg_document')

    donor_details_id = request.POST.get('donor_details_id')

    try:

        # if not DonorDetails.objects.filter(id=donor_details_id).exists():
        #     donor_obj = DonorDetails.objects.create(country_id=country, organisation=organisation, person=person,
        #                                             person_contact_number=person_contact,
        #                                             single_donor_address=donor_address,
        #                                             due_amount=due_amount, bank_account_number=bank_account_number,
        #                                             bank_name=bank_name, bank_swift_code=bank_swift_code, email=email,
        #                                             donor_bank_address=donor_bank_address)
        #
        #     if abc_document:
        #         file_url = str(abc_document)
        #
        #         handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + file_url), abc_document)
        #         donor_obj.reg_document = file_url
        #         donor_obj.save()
        #     messages.success(request, "Record saved.")
        # else:

        country = CountryDetails.objects.get(id=country)
        donor_obj = DonorDetails.objects.filter(id=donor_details_id).update(country_id=country,
                                                                            organisation=organisation, person=person,
                                                                            person_contact_number=person_contact,
                                                                            single_donor_address=donor_address,
                                                                            due_amount=due_amount,
                                                                            bank_account_number=bank_account_number,
                                                                            bank_name=bank_name,
                                                                            bank_swift_code=bank_swift_code,
                                                                            email=email,
                                                                            donor_bank_address=donor_bank_address)

        address = AddressDetails.objects.filter(id=DonorDetails.objects.get(id=donor_details_id).address.id).update(
            country=country)
        if abc_document:
            donor_obj = DonorDetails.objects.get(id=donor_details_id)
            file_url = str(abc_document)

            handle_uploaded_file(settings.MEDIA_ROOT + os.path.join('reports/' + file_url), abc_document)
            donor_obj.reg_document = file_url
            donor_obj.save()
        messages.success(request, "Record Updated.")

    except Exception as e:
        messages.warning(request, "Record not saved." + str(e))
    return redirect('/masters/template_manage_donor_master/')


def update_manage_donor_master(request):
    donor_id = request.POST.get('donor_id')

    organisation = request.POST.get('organisation')
    country = request.POST.get('country')
    person = request.POST.get('person')
    person_contact = request.POST.get('person_contact_number')

    donor_address = request.POST.get('address')
    email = request.POST.get('email')

    try:
        if not DonorDetails.objects.filter(~Q(id=donor_id), country_id=country, organisation=organisation).exists():

            DonorDetails.objects.filter(id=donor_id).update(country_id=country, organisation=organisation,
                                                            person=person, person_contact_number=person_contact,
                                                            single_donor_address=donor_address,
                                                            email=email)
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
        else:
            messages.warning(request,
                             "Organisation and country is already exist. Record not updated.")
            return HttpResponse(
                json.dumps({
                    'success': "Organisation and country is already exist. Record not updated."}),
                content_type="application/json")

    except:
        messages.warning(request, "Record not updated.")
    return HttpResponse(json.dumps({'error': 'Record not updated.'}),
                        content_type="application/json")


def delete_manage_donor_master(request):
    donor_id = request.POST.get('donor_id')

    try:
        DonorDetails.objects.filter(id=donor_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


def create_email_template(request):
    return render(request, 'create_email_template.html')


def email_templates_list(request):
    template_recs = EmailTemplates.objects.all()

    return render(request, 'email_templates_list.html', {'template_recs': template_recs})


def email_templates_view(request, rec_id):
    template_recs = EmailTemplates.objects.get(id=rec_id)

    return render(request, 'create_email_template.html', {'template_recs': template_recs})


def save_email_template(request):
    template_for = request.POST.get('template_for')
    subject = request.POST.get('subject')
    email_body = request.POST.get('email_body')
    active = request.POST.get('active')
    update = request.POST.get('update')

    try:
        if template_for:
            if update:
                EmailTemplates.objects.filter(id=update).update(template_for=template_for, subject=subject,
                                                                email_body=email_body)
                create_email = EmailTemplates.objects.get(id=update)
            else:
                create_email = EmailTemplates.objects.create(template_for=template_for, subject=subject,
                                                             email_body=email_body)

            if active:
                EmailTemplates.objects.filter(template_for=template_for).update(is_active=False)
                create_email.is_active = True
                create_email.save()
    except Exception as e:
        messages.warning(request, "Template not saved." + str(e))
    return redirect('/masters/email_templates_list/')


# def development_program_pdf(request):
#     pdf_recs = [['Development Program: ','AAAAA bbbbbbbbbbb dddddddddddddddd eeeeeeeeeeeee qqqqqqqqqqqqq eeeeeeeeeeeeee ffffffffffffffffffffff \n eeeeeeeeeeeeeeeeeee weeeeeeeeee'],['Name:','Javed Alam', 'Class','10']]
#     return export_pdf1('test_pdf',pdf_recs)


from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def development_program_pdf(request):
    return export_pdf1()
    # doc = SimpleDocTemplate("/tmp/somefilename.pdf")
    # styles = getSampleStyleSheet()
    # Story = [Spacer(1,2*inch)]
    # style = styles["Normal"]
    # bogustext = ('Development Program: Test')
    # p = Paragraph(bogustext, style)
    # Story.append(p)
    #
    # bogustext = ('Test Work: Open')
    # p = Paragraph(bogustext, style)
    # Story.append(p)
    #
    # bogustext = ('Class: 10')
    # p = Paragraph(bogustext, style)
    # Story.append(p)
    #
    # bogustext = ('Role: Admin')
    # p = Paragraph(bogustext, style)
    # Story.append(p)
    #
    # Story.append(Spacer(1,0.2*inch))
    # doc.build(Story)
    #
    # fs = FileSystemStorage("/tmp")
    # with fs.open("somefilename.pdf") as pdf:
    #     response = HttpResponse(pdf, content_type='application/pdf')
    #     response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    #     return response
    #
    # return response

    return render(request, 'development_program_pdf_template.html')


import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
import datetime
from xhtml2pdf import pisa
from threading import Thread, activeCount


# from io import StringIO

def generate_PDF(request):
    program_list = DevelopmentProgram.objects.all()[0:4]

    #####---- PDF Generation code  ---------------######33

    # template = get_template('development_program_pdf_template.html')

    # file = open('test.pdf', "w+b")
    # for rec in program_list:

    # program_rec = DevelopmentProgram.objects.get(id=rec)

    # Context = ({'x':16,'program_list':program_list})
    # html = template.render(Context)
    #
    # # pisa.pisaDocument(StringIO.StringIO(html), dest=file)
    #
    #
    # pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
    #
    # file.seek(0)
    # pdf = file.read()
    # # arr.append(pdf)
    # file.close()

    ###--------------********************

    # params = {'x':16,'program_list':program_list,'request':request}
    #
    # subject, from_email, to = 'Scholarship Module Details', settings.EMAIL_HOST_USER, 'javedalam113@gmail.com'
    # text_content = 'Following module has been assigned to you. Please Find The Attachment'
    #
    # from accounting.views import send_email
    # file = render_to_file('development_program_pdf_template.html', params)
    # thread = Thread(target=send_email, args=(file, subject, text_content, from_email, to))
    # thread.start()

    return redirect('/masters/template_manage_partner_master/')


def get_table_data(request):
    data = {'id': 1, 'column_name': 'abc', 'value': 'ABCD'}

    return HttpResponse(json.dumps(data), content_type="application/json")


def template_partner_details(request, partner_id=None):
    if partner_id:
        partner_rec = PartnerDetails.objects.get(id=partner_id)
        return render(request, "template_partner_details.html", {'partner_rec': partner_rec})


def partner_all_details_pdf(request, partner_id):
    try:
        year_recs = YearDetails.objects.all()
        curriculum_obj = ''
        experience_obj = ''
        x = 14
        if partner_id:
            partner_rec = PartnerDetails.objects.get(id=partner_id)
        template = get_template('template_partner_details_pdf.html')
        Context = ({'partner_rec': partner_rec, 'x': x})
        html = template.render(Context)

        file = open('test.pdf', "w+b")
        pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                    encoding='utf-8')

        file.seek(0)
        pdf = file.read()
        file.close()
        return HttpResponse(pdf, 'application/pdf')
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/masters/template_partner_details/' + str(partner_id))


def template_partner_details(request, partner_id=None):
    try:
        if partner_id:
            partner_rec = PartnerDetails.objects.get(id=partner_id)
            return render(request, "template_partner_details.html", {'partner_rec': partner_rec})
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/masters/template_manage_partner_master/')


def partner_all_details_pdf(request, partner_id):
    try:
        year_recs = YearDetails.objects.all()
        curriculum_obj = ''
        experience_obj = ''
        logo_path = settings.MEDIA_ROOT + 'logo.png'
        x = 14
        if partner_id:
            partner_rec = PartnerDetails.objects.get(id=partner_id)
        template = get_template('template_partner_details_pdf.html')
        Context = ({'partner_rec': partner_rec, 'x': x, 'logo_path': logo_path})
        html = template.render(Context)

        file = open('test.pdf', "w+b")
        pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                    encoding='utf-8')
        file.seek(0)
        pdf = file.read()
        file.close()
        return HttpResponse(pdf, 'application/pdf')
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/masters/template_partner_details/' + str(partner_id))


def template_donar_details(request, donor_id=None):
    try:
        if donor_id:
            donor_rec = DonorDetails.objects.get(id=donor_id)
            return render(request, "template_donor_details.html", {'donor_rec': donor_rec})
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/masters/template_manage_donor_master/')


def donar_all_details_pdf(request, donor_id):
    try:
        year_recs = YearDetails.objects.all()
        curriculum_obj = ''
        experience_obj = ''
        logo_path = settings.MEDIA_ROOT + 'logo.png'
        x = 14
        if donor_id:
            donar_rec = DonorDetails.objects.get(id=donor_id)
        template = get_template('template_donar_details_PDF.html')
        Context = ({'donar_rec': donar_rec, 'x': x, 'logo_path': logo_path})
        html = template.render(Context)
        file = open('test.pdf', "w+b")
        pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
        file.seek(0)
        pdf = file.read()
        file.close()
        return HttpResponse(pdf, 'application/pdf')
    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/masters/template_donar_details/' + str(donor_id))

# *********------------ Terms and Condition Master ----------***************

def terms_condition_master(request):
    try:
        terms_rec = UploadTermCondition.objects.filter()[0]
    except IndexError:
        terms_rec = None
    return render(request, 'terms_and_condition.html', {'terms_rec': terms_rec})


def save_terms_condition(request):
    term_file = request.FILES.get('terms_condition',None)
    try:
        upload_recs = UploadTermCondition.objects.filter()
        if upload_recs:
            rec = UploadTermCondition.objects.filter()[0]
            rec.term_condition = term_file
            rec.save()
            messages.success(request, "Record updated.")
        else:
            UploadTermCondition.objects.create(term_condition=term_file)
            messages.success(request, "Record saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/terms_condition_master/')


def university_details(request):
    try:
        university_details = UniversityDetails.objects.get(is_active = True)
    except IndexError:
        university_details = None
    return render(request, 'university_details.html', {'university_details': university_details})

def save_university_details(request):
    university_logo = request.FILES.get('university_logo',None)
    university_name = request.POST.get('university_name')
    university_address = request.POST.get('university_address')
    try:
        university_obj = UniversityDetails.objects.filter(is_active = True)
        if university_obj:
            university_obj = university_obj[0]
            if university_logo:
                university_obj.university_logo = university_logo
            university_obj.university_name = university_name
            university_obj.university_address = university_address
            university_obj.save()
            messages.success(request, "Record updated.")
        else:
            UniversityDetails.objects.create(university_logo=university_logo,university_name = university_name,university_address = university_address,is_active = True)
            messages.success(request, "Record saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/university_details/')


def language_settings(request):
    language_recs = LanguageDetails.objects.all()
    return render(request, 'template_language_settings.html', {'language_recs': language_recs})

def add_language(request):
    if request.method == 'POST':
        short_code = request.POST.get('short_code')
        language_name = request.POST.get('language_name')
        language_direction = request.POST.get('language_direction')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            language_dict = {
                'short_code':short_code,
                'language_name':language_name,
                'language_direction':language_direction,
                'status':status,
            }
            if LanguageDetails.objects.filter(short_code=short_code).exists():
                messages.warning(request, "Short code already exists.")
                return render(request, 'add_language.html', {'language_dict': language_dict})
            elif LanguageDetails.objects.filter(language_name=language_name).exists():
                messages.warning(request, "Language name already exists.")
                return render(request, 'add_language.html', {'language_dict': language_dict})
            LanguageDetails.objects.create(short_code=short_code, language_name=language_name,
                                             language_direction=language_direction, status=status)
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/language_settings/')
    language_dict = {
        'short_code': '',
        'language_name': '',
        'language_direction': '',
        'status': True,
    }
    return render(request, 'add_language.html',{'language_dict':language_dict})


def edit_language(request, language_id=None):
    language_obj = LanguageDetails.objects.get(id=language_id)
    if request.method == 'POST':
        short_code = request.POST.get('short_code')
        language_name = request.POST.get('language_name')
        language_direction = request.POST.get('language_direction')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            language_obj = {
                'id':language_id,
                'short_code': short_code,
                'language_name': language_name,
                'language_direction': language_direction,
                'status': status,
            }
            if LanguageDetails.objects.filter(~Q(id=language_id), short_code=short_code).exists():
                messages.warning(request, "Short code already exists.")
                return render(request, "edit_language.html", {'language_obj': language_obj})
            elif LanguageDetails.objects.filter(~Q(id=language_id), language_name=language_name).exists():
                messages.warning(request, "Language name already exists.")
                return render(request, "edit_language.html", {'language_obj': language_obj})
            LanguageDetails.objects.filter(id = language_id).update(short_code = short_code,language_name = language_name,language_direction = language_direction,status = status)
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/language_settings/')
    language_obj = {
        'id': language_id,
        'short_code': language_obj.short_code,
        'language_name': language_obj.language_name,
        'language_direction': language_obj.language_direction,
        'status': language_obj.status,
    }
    return render(request, "edit_language.html", {'language_obj': language_obj})


def delete_language(request):
    if request.method == 'POST':
        language_delete_id = request.POST.get('language_delete_id')
        try:
            LanguageDetails.objects.filter(id=language_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/language_settings/')


def currency_settings(request):
    currency_recs = CurrencyDetails.objects.all()
    return render(request, 'template_currency_settings.html', {'currency_recs': currency_recs})

def add_currency(request):
    if request.method == 'POST':
        currency_number = request.POST.get('currency_number')
        currency_code = request.POST.get('currency_code')
        currency_name = request.POST.get('currency_name')
        decimal_description = request.POST.get('decimal_description')
        record_status = request.POST.get('record_status')
        length = request.POST.get('length')
        exchange_type = request.POST.get('exchange_type')

        if record_status == 'on':
            record_status = True
        else:
            record_status = False
        try:
            currency_dict = {
                'currency_number':currency_number,
                'currency_code':currency_code,
                'currency_name':currency_name,
                'decimal_description':decimal_description,
                'record_status':record_status,
                'length':length,
                'exchange_type':exchange_type,
            }
            if CurrencyDetails.objects.filter(currency_name=currency_name).exists():
                messages.warning(request, "Currency Name already exists.")
                return render(request, 'add_currency.html', {'currency_dict': currency_dict})
            elif CurrencyDetails.objects.filter(currency_code=currency_code).exists():
                messages.warning(request, "Currency Code already exists.")
                return render(request, 'add_currency.html', {'currency_dict': currency_dict})

            CurrencyDetails.objects.create(currency_number=currency_number, currency_name=currency_name, currency_code = currency_code,
                                             decimal_description=decimal_description, record_status=record_status,length = length,exchange_type = exchange_type)
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/currency_settings/')
    currency_dict = {
        'currency_number': '',
        'currency_code': '',
        'currency_name': '',
        'decimal_description': '',
        'record_status': True,
        'length': '',
        'exchange_type': '',
    }
    return render(request, 'add_currency.html',{'currency_dict':currency_dict})


def edit_currency(request, currency_id=None):
    currency_obj = CurrencyDetails.objects.get(id=currency_id)
    if request.method == 'POST':
        currency_number = request.POST.get('currency_number')
        currency_code = request.POST.get('currency_code')
        currency_name = request.POST.get('currency_name')
        decimal_description = request.POST.get('decimal_description')
        record_status = request.POST.get('record_status')
        length = request.POST.get('length')
        exchange_type = request.POST.get('exchange_type')
        if record_status == 'on':
            record_status = True
        else:
            record_status = False
        try:
            currency_obj = {
                'id':currency_id,
                'currency_number': currency_number,
                'currency_code': currency_code,
                'currency_name': currency_name,
                'decimal_description': decimal_description,
                'record_status': record_status,
                'length': length,
                'exchange_type': exchange_type,
            }
            if CurrencyDetails.objects.filter(~Q(id=currency_id), currency_name=currency_name.strip()).exists():
                messages.warning(request, "Currency Name already exists.")
                return render(request, "edit_currency.html", {'currency_obj': currency_obj})
            if CurrencyDetails.objects.filter(~Q(id=currency_id), currency_code=currency_code.strip()).exists():
                messages.warning(request, "Currency Code already exists.")
                return render(request, "edit_currency.html", {'currency_obj': currency_obj})
            CurrencyDetails.objects.filter(id = currency_id).update(currency_number=currency_number, currency_code = currency_code,currency_name=currency_name,
                                             decimal_description=decimal_description, record_status=record_status,length = length,exchange_type = exchange_type)
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/currency_settings/')
    currency_obj = {
        'id': currency_id,
        'currency_number': currency_obj.currency_number,
        'currency_code': currency_obj.currency_code,
        'currency_name': currency_obj.currency_name,
        'decimal_description': currency_obj.decimal_description,
        'record_status': currency_obj.record_status,
        'length': currency_obj.length,
        'exchange_type': currency_obj.exchange_type,
    }
    return render(request, "edit_currency.html", {'currency_obj': currency_obj})

def delete_currency(request):
    if request.method == 'POST':
        currency_delete_id = request.POST.get('currency_delete_id')
        try:
            CurrencyDetails.objects.filter(id=currency_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/currency_settings/')


def university_settings(request):
    university_recs = UniversityDetails.objects.filter(is_delete = False)
    return render(request, 'university_settings.html', {'university_recs': university_recs})


def add_university(request):
    if request.method == 'POST':
        university_logo = request.FILES.get('university_logo', None)
        university_type = request.POST.get('university_type')
        type = request.POST.get('type')
        university_name = request.POST.get('university_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        website = request.POST.get('website')
        university_address = request.POST.get('university_address')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            university_obj = UniversityDetails.objects.create(
                                             university_name=university_name, email=email,telephone = telephone,website = website,
                                             address = university_address,is_active = status,university_type_id = university_type,type_id = type)
            if university_logo:
                university_obj.university_logo = university_logo
                university_obj.save()
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/university_settings/')
    university_type_recs = UniversityTypeDetails.objects.filter(status = True)
    type_recs = TypeDetails.objects.filter(status = True)
    return render(request, 'add_university.html',{'university_type_recs':university_type_recs,'type_recs':type_recs})

def edit_university(request, university_id=None):
    university_obj = UniversityDetails.objects.get(id=university_id)
    if request.method == 'POST':
        university_logo = request.FILES.get('university_logo', None)
        university_type = request.POST.get('university_type')
        type = request.POST.get('type')
        university_name = request.POST.get('university_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        website = request.POST.get('website')
        university_address = request.POST.get('university_address')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            university_obj.university_type_id = university_type
            university_obj.type_id = type
            university_obj.university_name = university_name
            university_obj.email = email
            university_obj.telephone = telephone
            university_obj.website = website
            university_obj.address = university_address
            university_obj.is_active = status
            if university_logo:
                university_obj.university_logo = university_logo
            university_obj.save()
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/university_settings/')
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    type_recs = TypeDetails.objects.filter(status=True)
    return render(request, "edit_university.html", {'university_obj': university_obj,'type_recs':type_recs,'university_type_recs':university_type_recs})

def delete_university(request):
    if request.method == 'POST':
        university_delete_id = request.POST.get('university_delete_id')
        try:
            UniversityDetails.objects.filter(id=university_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/university_settings/')

def faculty_settings(request):
    faculty_recs = FacultyDetails.objects.filter()
    return render(request, 'faculty_settings.html', {'faculty_recs': faculty_recs})

def add_faculty(request):
    university_recs = UniversityDetails.objects.filter(is_delete=False,is_active=True,is_partner_university = False).order_by('-id')
    if request.method == 'POST':
        logo = request.FILES.get('logo', None)
        university = request.POST.get('university')
        university_type = request.POST.get('university_type')
        # faculty_id = request.POST.get('faculty_id')
        faculty_name = request.POST.get('faculty_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        website = request.POST.get('website')
        address = request.POST.get('address')
        status = request.POST.get('status')
        department_count = request.POST.get('department_count')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            faculty_obj = FacultyDetails.objects.create(university_id=university,
                                             faculty_name=faculty_name, email=email,telephone = telephone,website = website,
                                             address = address,status = status,university_type_id = university_type)

            faculty_obj.department.clear()
            for x in range(int(department_count)):
                try:
                    x = x + 1
                    department_obj = Department.objects.create(
                        department=request.POST.get('department_' + str(x)))
                    faculty_obj.department.add(department_obj)
                except:
                    pass
            if logo:
                faculty_obj.logo = logo
                faculty_obj.save()
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/faculty_settings/')
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    return render(request, 'add_faculty.html',{'university_recs':university_recs,'university_type_recs':university_type_recs})

def edit_faculty(request, faculty_id=None):
    faculty_obj = FacultyDetails.objects.get(id=faculty_id)
    department_total_count = faculty_obj.department.all().count()
    university_recs = ''
    if faculty_obj.university_type:
    # if faculty_obj.university.is_partner_university == False:
    #     university_recs = UniversityDetails.objects.filter(is_delete = False,is_active = True,is_partner_university = False).order_by('-id')
    # else:
        university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                           university_type_id=faculty_obj.university_type.id).order_by('-id')
    if request.method == 'POST':
        logo = request.FILES.get('logo', None)
        university = request.POST.get('university')
        university_type = request.POST.get('university_type')
        faculty_name = request.POST.get('faculty_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        website = request.POST.get('website')
        address = request.POST.get('address')
        status = request.POST.get('status')
        department_count = request.POST.get('department_count')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            faculty_obj.university_type_id = university_type
            faculty_obj.university_id = university
            faculty_obj.faculty_name = faculty_name
            faculty_obj.email = email
            faculty_obj.telephone = telephone
            faculty_obj.website = website
            faculty_obj.address = address
            faculty_obj.status = status

            faculty_obj.department.clear()
            for x in range(int(department_count)):
                try:
                    x = x + 1
                    department_obj = Department.objects.create(
                        department=request.POST.get('department_' + str(x)))
                    faculty_obj.department.add(department_obj)
                except:
                    pass

            if logo:
                faculty_obj.logo = logo
            faculty_obj.save()
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/faculty_settings/')
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    return render(request, "edit_faculty.html", {'faculty_obj': faculty_obj,'university_recs':university_recs,'department_total_count':department_total_count,'university_type_recs':university_type_recs})

def delete_faculty(request):
    if request.method == 'POST':
        faculty_delete_id = request.POST.get('faculty_delete_id')
        try:
            FacultyDetails.objects.filter(id=faculty_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/faculty_settings/')



def study_mode_settings(request):
    study_mode_recs = StudyModeDetails.objects.filter().order_by('-id')
    return render(request, 'study_mode.html',
                  {'study_mode_recs': study_mode_recs})

def add_study_mode(request):
    study_mode = request.POST.get('study_mode')
    try:
        if not StudyModeDetails.objects.filter(study_mode=study_mode).exists():
            StudyModeDetails.objects.create(study_mode=study_mode)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Study mode already exists.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/study_mode_settings/')

def edit_study_mode(request):
    study_mode_id = request.POST.get('study_mode_id')
    study_mode = request.POST.get('study_mode')
    try:
        if not StudyModeDetails.objects.filter(~Q(id=study_mode_id), study_mode=study_mode).exists():
            StudyModeDetails.objects.filter(id=study_mode_id).update(study_mode=study_mode)
            messages.success(request, "Record saved.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
        else:
            messages.warning(request, "Study mode already exists.")
            return HttpResponse(
                json.dumps({'success': "Study mode already exists."}),
                content_type="application/json")
    except:
        messages.warning(request, "Record not updated.")
        return HttpResponse(json.dumps({'error': 'Record not updated.'}), content_type="application/json")


def delete_study_mode(request):
    if request.method == 'POST':
        study_mode_delete_id = request.POST.get('study_mode_delete_id')
        try:
            StudyModeDetails.objects.filter(id=study_mode_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/study_mode_settings/')


def study_level_settings(request):
    study_level_recs = StudyLevelDetails.objects.filter().order_by('-id')
    return render(request, 'study_level.html',
                  {'study_level_recs': study_level_recs})

def add_study_level(request):
    study_level = request.POST.get('study_level')
    try:
        if not StudyLevelDetails.objects.filter(study_level=study_level).exists():
            StudyLevelDetails.objects.create(study_level=study_level)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Study level already exists.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/study_level_settings/')

def edit_study_level(request):
    study_level_id = request.POST.get('study_level_id')
    study_level = request.POST.get('study_level')
    try:
        if not StudyLevelDetails.objects.filter(~Q(id=study_level_id), study_level=study_level).exists():
            StudyLevelDetails.objects.filter(id=study_level_id).update(study_level=study_level)
            messages.success(request, "Record saved.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
        else:
            messages.warning(request, "Study mode already exists.")
            return HttpResponse(
                json.dumps({'success': "Study mode already exists."}),
                content_type="application/json")
    except:
        messages.warning(request, "Record not updated.")
        return HttpResponse(json.dumps({'error': 'Record not updated.'}), content_type="application/json")

def delete_study_level(request):
    if request.method == 'POST':
        study_level_delete_id = request.POST.get('study_level_delete_id')
        try:
            StudyLevelDetails.objects.filter(id=study_level_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/study_level_settings/')



def study_type_settings(request):
    study_type_recs = StudyTypeDetails.objects.all()
    return render(request, 'study_type.html',
                  {'study_type_recs': study_type_recs})

def add_study_type(request):
    study_type = request.POST.get('study_type')
    try:
        if not StudyTypeDetails.objects.filter(study_type=study_type).exists():
            StudyTypeDetails.objects.create(study_type=study_type)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Study type already exists.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/study_type_settings/')

def edit_study_type(request):
    study_type_id = request.POST.get('study_type_id')
    study_type = request.POST.get('study_type')
    try:
        if not StudyTypeDetails.objects.filter(~Q(id=study_type_id), study_type=study_type).exists():
            StudyTypeDetails.objects.filter(id=study_type_id).update(study_type=study_type)
            messages.success(request, "Record saved.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
        else:
            messages.warning(request, "Study type already exists.")
            return HttpResponse(
                json.dumps({'success': "Study type already exists."}),
                content_type="application/json")
    except:
        messages.warning(request, "Record not updated.")
        return HttpResponse(json.dumps({'error': 'Record not updated.'}), content_type="application/json")

def delete_study_type(request):
    if request.method == 'POST':
        study_type_delete_id = request.POST.get('study_type_delete_id')
        try:
            StudyTypeDetails.objects.filter(id=study_type_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/study_type_settings/')

def program_fee_settings(request):
    program_fee_recs = ProgramFeeDetails.objects.filter().order_by('-id')
    return render(request, 'program_fee_settings.html', {'program_fee_recs': program_fee_recs})

def add_program_fee(request):
    if request.method == 'POST':
        university = request.POST.get('university')
        university_type = request.POST.get('university_type')
        year = request.POST.get('year')
        program = request.POST.get('program')
        country = request.POST.get('country')
        discount = request.POST.get('discount')
        total_amount = request.POST.get('total_amount')
        program_fee_count = request.POST.get('program_fee_count')

        if ProgramFeeDetails.objects.filter(university_id=university,program_id=program).exists():
            messages.warning(request, "Program Fee already exists.")
            return redirect('/masters/program_fee_settings/')
        try:
            program_fee_obj = ProgramFeeDetails.objects.create(university_id=university,country_id = country,
                                                                                   year_id=year,
                                                                                   program_id=program,total_amount = total_amount,university_type_id = university_type)
            program_fee_obj.program_fee.clear()
            for x in range(int(program_fee_count)):
                try:
                    x = x + 1
                    program_fee_type_obj = ProgramFeeType.objects.create(fee_type=request.POST.get('fee_type_' + str(x)),
                                                                      amount=request.POST.get('amount_' + str(x))
                                                                      )
                    program_fee_obj.program_fee.add(program_fee_type_obj)
                except:
                    pass
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/program_fee_settings/')
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,is_partner_university = False).order_by('-id')
    year_recs = YearDetails.objects.all()
    program_recs = ProgramDetails.objects.filter(is_delete=False).order_by('-id')
    country_recs = CountryDetails.objects.all()
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    return render(request, 'add_program_fee.html',{
        'university_recs':university_recs,
        'year_recs':year_recs,
        'program_recs':program_recs,
        'country_recs':country_recs,
        'university_type_recs':university_type_recs,
                                                   })

def edit_program_fee(request, program_id=None):
    program_fee_obj = ProgramFeeDetails.objects.get(id=program_id)
    if request.method == 'POST':
        university_type = request.POST.get('university_type')
        university = request.POST.get('university')
        year = request.POST.get('year')
        program = request.POST.get('program')
        country = request.POST.get('country')
        discount = request.POST.get('discount')
        total_amount = request.POST.get('total_amount')
        program_fee_count = request.POST.get('program_fee_count')
        if ProgramFeeDetails.objects.filter(~Q(id=program_id), university_id=university,program_id = program).exists():
            messages.warning(request, "Program Fee already exists.")
            return redirect('/masters/program_fee_settings/')

        try:
            program_fee_obj.university_type_id = university_type
            program_fee_obj.university_id = university
            program_fee_obj.country_id = country
            program_fee_obj.year_id = year
            program_fee_obj.program_id = program
            program_fee_obj.total_amount = total_amount
            program_fee_obj.save()

            program_fee_obj.program_fee.clear()
            for x in range(int(program_fee_count)):
                try:
                    x = x + 1
                    program_fee_type_obj = ProgramFeeType.objects.create(
                        fee_type=request.POST.get('fee_type_' + str(x)),
                        amount=request.POST.get('amount_' + str(x))
                        )
                    program_fee_obj.program_fee.add(program_fee_type_obj)
                except:
                    pass
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/program_fee_settings/')
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                           university_type_id=program_fee_obj.university_type.id).order_by('-id')
    year_recs = YearDetails.objects.all()
    program_recs = ProgramDetails.objects.filter(is_delete=False).order_by('-id')
    country_recs = CountryDetails.objects.all()
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    return render(request, 'edit_program_fee.html', {
        'university_recs': university_recs,
        'year_recs': year_recs,
        'program_recs': program_recs,
        'country_recs': country_recs,
        'program_fee_obj': program_fee_obj,
        'program_fee_count': program_fee_obj.program_fee.count(),
        'university_type_recs': university_type_recs,
    })

def program_settings(request):
    program_recs = ProgramDetails.objects.filter(is_delete=False).order_by('-id')
    return render(request, 'program_settings.html', {'program_recs': program_recs})

def add_program(request):
    if request.method == 'POST':
        university = request.POST.get('university')
        faculty = request.POST.get('faculty')
        program_name = request.POST.get('program_name')
        # program_fee = request.POST.get('program_fee')
        # credit_hrs = request.POST.get('credit_hrs')
        study_type = request.POST.get('study_type')
        study_level = request.POST.get('study_level')
        program_overview = request.POST.get('program_overview')
        program_objective = request.POST.get('program_objective')
        program_vision = request.POST.get('program_vision')
        program_mission = request.POST.get('program_mission')
        status = request.POST.get('status')
        study_mode_recs = request.POST.getlist('study_mode[]')
        campus_recs = request.POST.getlist('campus')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            program_obj = ProgramDetails.objects.create(faculty_id=faculty,university_id=university,
                                             program_name=program_name,program_overview = program_overview,program_objective = program_objective,
                                             program_vision = program_vision,program_mission = program_mission,status = status,study_type_id = study_type,study_level_id = study_level,
                                                        )

            program_obj.study_mode.clear()
            for study_mode in study_mode_recs:
                program_study_mode_obj = ProgramStudyModeDetails.objects.create(study_mode=study_mode)
                program_obj.study_mode.add(program_study_mode_obj)

            program_obj.campus.clear()
            for campus_id in campus_recs:
                program_campus_obj = ProgramCampusDetails.objects.create(campus_id=campus_id)
                program_obj.campus.add(program_campus_obj)

            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/program_settings/')
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,is_partner_university = False).order_by('-id')
    study_mode_recs = StudyModeDetails.objects.filter().order_by('-id')
    study_level_recs = StudyLevelDetails.objects.filter().order_by('-id')
    study_type_recs = StudyTypeDetails.objects.filter().order_by('-id')
    faculty_recs = FacultyDetails.objects.filter(status=True).order_by('-id')
    campus_recs = CampusBranchesDetails.objects.filter().order_by('-id')
    study_mode_list = ['Online', 'On Campus']

    return render(request, 'add_program.html',{'university_recs':university_recs,'faculty_recs':faculty_recs,'study_level_recs':study_level_recs,'study_mode_recs':study_mode_recs,'study_type_recs':study_type_recs,'campus_recs':campus_recs,'study_mode_list':study_mode_list})

def add_program(request):
    if request.method == 'POST':
        university_type = request.POST.get('university_type')
        acceptance_avg = request.POST.get('acceptance_avg')
        capacity_avg = request.POST.get('capacity_avg')
        university = request.POST.get('university')
        faculty = request.POST.get('faculty')
        program_type = request.POST.get('program_type')
        department = request.POST.get('department',None)
        program_name = request.POST.get('program_name')
        # program_fee = request.POST.get('program_fee')
        # credit_hrs = request.POST.get('credit_hrs')
        study_type = request.POST.get('study_type')
        study_level = request.POST.get('study_level')
        program_overview = request.POST.get('program_overview')
        program_objective = request.POST.get('program_objective')
        program_vision = request.POST.get('program_vision')
        program_mission = request.POST.get('program_mission')
        status = request.POST.get('status')
        study_mode_recs = request.POST.getlist('study_mode[]')
        campus_recs = request.POST.getlist('campus')
        course_count = request.POST.get('course_count')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            program_obj = ProgramDetails.objects.create(faculty_id=faculty,university_id=university,department_id = department,
                                             program_name=program_name,program_overview = program_overview,program_objective = program_objective,
                                             program_vision = program_vision,program_mission = program_mission,status = status,study_type_id = study_type,study_level_id = study_level,
                                                        university_type_id = university_type,acceptance_avg = acceptance_avg,capacity_avg = capacity_avg)

            program_obj.study_mode.clear()
            for study_mode in study_mode_recs:
                program_study_mode_obj = ProgramStudyModeDetails.objects.create(study_mode=study_mode)
                program_obj.study_mode.add(program_study_mode_obj)

            program_obj.campus.clear()
            for campus_id in campus_recs:
                program_campus_obj = ProgramCampusDetails.objects.create(campus_id=campus_id)
                program_obj.campus.add(program_campus_obj)



            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/program_settings/')
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,is_partner_university = False).order_by('-id')
    study_mode_recs = StudyModeDetails.objects.filter().order_by('-id')
    study_level_recs = StudyLevelDetails.objects.filter().order_by('-id')
    study_type_recs = StudyTypeDetails.objects.all()
    faculty_recs = FacultyDetails.objects.filter(status=True).order_by('-id')
    campus_recs = CampusBranchesDetails.objects.filter().order_by('-id')
    study_mode_list = ['Online', 'On Campus']
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    passing_year_recs = PassingYear.objects.filter().order_by('-year')
    return render(request, 'add_program.html',{'university_recs':university_recs,'faculty_recs':faculty_recs,'study_level_recs':study_level_recs,'study_mode_recs':study_mode_recs,'study_type_recs':study_type_recs,'campus_recs':campus_recs,'study_mode_list':study_mode_list,'university_type_recs':university_type_recs,'passing_year_recs':passing_year_recs})


def edit_program(request, program_id=None,type = None):
    program_obj = ProgramDetails.objects.get(id=program_id)
    if request.method == 'POST':
        university = request.POST.get('university')
        university_type = request.POST.get('university_type')
        acceptance_avg = request.POST.get('acceptance_avg')
        capacity_avg = request.POST.get('capacity_avg')
        faculty = request.POST.get('faculty')
        program_type = request.POST.get('program_type')
        department = request.POST.get('department',None)
        # program_id = request.POST.get('program_id')
        program_name = request.POST.get('program_name')
        study_type = request.POST.get('study_type')
        study_level = request.POST.get('study_level')
        # study_mode = request.POST.get('study_mode')
        program_overview = request.POST.get('program_overview')
        program_objective = request.POST.get('program_objective')
        program_vision = request.POST.get('program_vision')
        program_mission = request.POST.get('program_mission')
        # campus = request.POST.get('campus')
        status = request.POST.get('status')
        study_mode_recs = request.POST.getlist('study_mode[]')
        campus_recs = request.POST.getlist('campus')
        # program_fee = request.POST.get('program_fee')
        # credit_hrs = request.POST.get('credit_hrs')
        course_count = request.POST.get('course_count')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            program_obj.university_type_id = university_type
            program_obj.acceptance_avg = acceptance_avg
            program_obj.capacity_avg = capacity_avg
            program_obj.university_id = university
            program_obj.faculty_id = faculty
            program_obj.department_id = department
            # program_obj.campus_id = campus
            # program_obj.program_id = program_id
            program_obj.program_name = program_name
            program_obj.study_type_id = study_type
            program_obj.study_level_id = study_level
            # program_obj.study_mode_id = study_mode
            program_obj.program_overview = program_overview
            program_obj.program_objective = program_objective
            program_obj.program_vision = program_vision
            program_obj.program_mission = program_mission
            program_obj.status = status
            # program_obj.program_fee = program_fee
            # program_obj.credit_hrs = credit_hrs
            program_obj.save()

            program_obj.study_mode.clear()
            for study_mode in study_mode_recs:
                program_study_mode_obj = ProgramStudyModeDetails.objects.create(study_mode=study_mode)
                program_obj.study_mode.add(program_study_mode_obj)

            program_obj.campus.clear()
            for campus_id in campus_recs:
                program_campus_obj = ProgramCampusDetails.objects.create(campus_id=campus_id)
                program_obj.campus.add(program_campus_obj)

            # program_obj.course.clear()
            # for count in range(int(course_count)):
            #     try:
            #         count = count + 1
            #         if (request.POST['code_' + str(count)] is not '') or (request.POST['title_' + str(count)] is not '') or (request.POST['unit_' + str(count)] is not '') or (request.POST['type_' + str(count)] is not ''):
            #             course_obj = CourseDetails.objects.create(code=request.POST['code_' + str(count)],
            #                                                   title=request.POST['title_' + str(count)],
            #                                                   unit=request.POST['unit_' + str(count)],
            #                                                   type=request.POST['type_' + str(count)])
            #             program_obj.course.add(course_obj)
            #     except Exception as e:
            #         pass

            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/program_settings/')

    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                           university_type_id=program_obj.university_type.id).order_by('-id')
    study_mode_recs = StudyModeDetails.objects.filter().order_by('-id')
    study_level_recs = StudyLevelDetails.objects.filter().order_by('-id')
    study_type_recs = StudyTypeDetails.objects.all()
    faculty_recs = FacultyDetails.objects.filter(status=True).order_by('-id')
    if program_obj.university:
        faculty_recs = FacultyDetails.objects.filter(university_id = program_obj.university.id)
    campus_recs = CampusBranchesDetails.objects.filter().order_by('-id')
    study_mode_list = ['Online', 'On Campus']
    selected_study_mode_list = program_obj.study_mode.values_list('study_mode',flat = True)
    selected_campus_list = list(program_obj.campus.values_list('campus_id',flat = True))
    department_recs = program_obj.faculty.department.all()
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    course_count = program_obj.course.all().count()
    course_obj = program_obj.course.all()
    passing_year_recs = PassingYear.objects.filter().order_by('-year')
    year_recs = YearDetails.objects.all()

    year_list = []
    semester_recs = SemesterDetails.objects.filter(university_id=program_obj.university.id)
    if semester_recs:
        for rec in semester_recs:
            raw_dict = {}
            raw_dict['id'] = rec.year.id
            raw_dict['year'] = rec.year.year_name
            year_list.append(raw_dict)

    prerequisite_course_recs = PrerequisiteCourseDetails.objects.all()

    return render(request, "edit_program.html", {'program_obj': program_obj,'university_recs':university_recs,'course_count':course_count,'course_obj':course_obj,
                                                 'study_mode_recs':study_mode_recs,'study_level_recs':study_level_recs,'study_type_recs':study_type_recs,'faculty_recs':faculty_recs,'campus_recs':campus_recs,'study_mode_list':study_mode_list,'selected_study_mode_list':selected_study_mode_list,'selected_campus_list':selected_campus_list,'department_recs':department_recs,
                                                 'university_type_recs':university_type_recs,'passing_year_recs':passing_year_recs,'year_recs':year_recs,
                                                 'year_list':year_list,
                                                 'prerequisite_course_recs':prerequisite_course_recs})


def delete_program(request):
    if request.method == 'POST':
        program_delete_id = request.POST.get('program_delete_id')
        try:
            ProgramDetails.objects.filter(id=program_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/program_settings/')


def year_settings(request):
    year_recs = YearDetails.objects.all()
    return render(request, 'year_settings.html', {'year_recs': year_recs})

def add_year(request):
    year_name = request.POST.get('year_name')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    end_dt = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date()
    start_dt = datetime.datetime.strptime(str(start_date), "%Y-%m-%d").date()

    try:
        if YearDetails.objects.filter(year_name=year_name).exists():
            messages.warning(request, "Year name already exists.")

        # elif YearDetails.objects.all().filter(
        #         (Q(start_date__lte=start_dt) & Q(end_date__gte=end_dt)) | Q(start_date__range=(start_dt, end_dt)) | Q(
        #                 end_date__range=(start_dt, end_dt))):
        #     messages.success(request, "Academic year already Exists")

        else:

            # today = date.today()
            #
            # if (start_dt <= today) and (end_dt > today):
            #     YearDetails.objects.filter().update(active_year = False)
            #     YearDetails.objects.filter().update(base_date = False)
            #     YearDetails.objects.create(year_name=year_name.lower(), start_date=start_date, end_date=end_date,active_year = True,base_date = True)
            # else:
            #     YearDetails.objects.create(year_name=year_name.lower(), start_date=start_date, end_date=end_date)

            YearDetails.objects.create(year_name=year_name, start_date=start_date, end_date=end_date)
            messages.success(request, "Record saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/year_settings/')


def delete_year(request):
    if request.method == 'POST':
        year_delete_id = request.POST.get('year_delete_id')
        try:
            YearDetails.objects.filter(id=year_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/year_settings/')

def semester_settings(request):
    semester_recs = SemesterDetails.objects.all()
    return render(request, 'semester_settings.html', {'semester_recs': semester_recs})


def add_semester(request):
    if request.method == 'POST':
        university_type = request.POST.get('university_type')
        university = request.POST.get('university')
        year = request.POST.get('year')
        study_level = request.POST.get('study_level')
        semester_count = request.POST.get('semester_count')
        try:
            semester_obj = SemesterDetails.objects.create(university_id = university,year_id = year,study_level_id = study_level,university_type_id = university_type)
            semester_obj.semester.clear()
            for x in range(int(semester_count)):
                try:
                    x = x + 1
                    semester = Semester.objects.create(
                        semester=request.POST.get('semester_' + str(x)),
                        start_date=request.POST.get('start_date_' + str(x)),
                        end_date=request.POST.get('end_date_' + str(x))
                    )
                    semester_obj.semester.add(semester)
                except:
                    pass
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/semester_settings/')
    else:
        university_type_recs = UniversityTypeDetails.objects.filter(status=True)
        university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                           is_partner_university=False).order_by('-id')
        year_recs = YearDetails.objects.all()
        study_level_recs  = StudyLevelDetails.objects.filter().order_by('-id')
        context = {
            'university_recs':university_recs,
            'year_recs':year_recs,
            'study_level_recs':study_level_recs,
            'university_type_recs':university_type_recs
        }
        return render(request, 'add_semester.html',context)


def edit_semester(request, semester_id=None):
    semester_obj = SemesterDetails.objects.get(id=semester_id)
    semester_total_count = semester_obj.semester.all().count()
    if request.method == 'POST':
        university_type = request.POST.get('university_type')
        university = request.POST.get('university')
        year = request.POST.get('year')
        study_level = request.POST.get('study_level')
        semester_count = request.POST.get('semester_count')
        try:
            semester_obj.university_type_id = university_type
            semester_obj.university_id = university
            semester_obj.year_id = year
            semester_obj.study_level_id = study_level
            semester_obj.university_id = university
            semester_obj.save()
            semester_obj.semester.clear()
            for x in range(int(semester_count)):
                try:
                    x = x + 1
                    semester = Semester.objects.create(
                        semester=request.POST.get('semester_' + str(x)),
                        start_date=request.POST.get('start_date_' + str(x)),
                        end_date=request.POST.get('end_date_' + str(x))
                    )
                    semester_obj.semester.add(semester)
                except:
                    pass
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Semester name already exists. Record not updated.")
        return redirect('/masters/semester_settings/')
    # if semester_obj.university:
    #     if semester_obj.university.is_partner_university == False:
    #         university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,is_partner_university = False).order_by('-id')
    #     else:
    #         university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
    #                                                            is_partner_university=True).order_by('-id')
    # else:
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                           university_type_id=semester_obj.university_type.id).order_by('-id')
    year_recs = YearDetails.objects.all()
    study_level_recs = StudyLevelDetails.objects.filter().order_by('-id')
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)

    context = {
        'semester_obj': semester_obj,
        'university_recs': university_recs,
        'year_recs': year_recs,
        'semester_total_count': semester_total_count,
        'study_level_recs': study_level_recs,
        'university_type_recs': university_type_recs,
    }
    return render(request, "edit_semester.html",context)

def delete_semester(request):
    if request.method == 'POST':
        semester_delete_id = request.POST.get('semester_delete_id')
        try:
            SemesterDetails.objects.filter(id=semester_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/semester_settings/')

def activity_settings(request):
    activity_recs = ActivityDetails.objects.all()
    return render(request, 'activity_settings.html', {'activity_recs': activity_recs})

def add_activity(request):
    activity_name = request.POST.get('activity_name')
    description = request.POST.get('description')
    try:
        if not ActivityDetails.objects.filter(activity_name=activity_name).exists():
            ActivityDetails.objects.create(activity_name=activity_name,description = description)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Activity name already exists.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/activity_settings/')


def update_activity(request):
    activity_id = request.POST.get('activity_id')
    activity_name = request.POST.get('activity_name')
    description = request.POST.get('description')
    try:
        if not ActivityDetails.objects.filter(~Q(id=activity_id), activity_name=activity_name).exists():
            ActivityDetails.objects.filter(id=activity_id).update(activity_name=activity_name,
                                                                  description=description)
            messages.success(request, "Record saved.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
        else:
            messages.warning(request, "Activity name already exists.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/activity_settings/')


def delete_activity(request):
    if request.method == 'POST':
        activity_delete_id = request.POST.get('activity_delete_id')
        try:
            ActivityDetails.objects.filter(id=activity_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/activity_settings/')


def student_mode_settings(request):
    student_mode_recs = StudentModeDetails.objects.all()
    return render(request, 'student_mode.html', {'student_mode_recs': student_mode_recs})

def add_student_mode(request):
    student_mode = request.POST.get('student_mode')
    description = request.POST.get('description')
    try:
        if not StudentModeDetails.objects.filter(student_mode=student_mode).exists():
            StudentModeDetails.objects.create(student_mode=student_mode,description = description)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Student mode already exists.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/student_mode_settings/')


def update_student_mode(request):
    student_mode_id = request.POST.get('student_mode_id')
    student_mode = request.POST.get('student_mode')
    description = request.POST.get('description')
    try:
        if not StudentModeDetails.objects.filter(~Q(id=student_mode_id), student_mode=student_mode).exists():
            StudentModeDetails.objects.filter(id=student_mode_id).update(student_mode=student_mode,
                                                                  description=description)
            messages.success(request, "Record saved.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
        else:
            messages.warning(request, "Student mode already exists.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/student_mode_settings/')


def delete_student_mode(request):
    if request.method == 'POST':
        student_mode_delete_id = request.POST.get('student_mode_delete_id')
        try:
            StudentModeDetails.objects.filter(id=student_mode_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/student_mode_settings/')

def learning_centers_settings(request):
    learning_centers_recs = LearningCentersDetails.objects.all()
    return render(request, 'learning_centers_settings.html', {'learning_centers_recs': learning_centers_recs})

def add_learning_centers(request):
    if request.method == 'POST':
        university_type = request.POST.get('university_type')
        university = request.POST.get('university')
        country = request.POST.get('country')
        lc_name = request.POST.get('lc_name')
        lc_address = request.POST.get('lc_address')
        lc_email = request.POST.get('lc_email')
        lc_tel = request.POST.get('lc_tel')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            LearningCentersDetails.objects.create(country_id=country,lc_name=lc_name,university_id = university,
                                             lc_address=lc_address, lc_email=lc_email,lc_tel = lc_tel,status = status,university_type_id = university_type)
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/learning_centers_settings/')
    country_recs = CountryDetails.objects.all()
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                       is_partner_university=False).order_by('-id')
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    return render(request, 'add_learning_centers.html',{'country_recs':country_recs,'university_recs':university_recs,'university_type_recs':university_type_recs})

def edit_learning_centers(request, learning_center_id=None):
    learning_center_obj = LearningCentersDetails.objects.get(id=learning_center_id)
    if request.method == 'POST':
        university_type = request.POST.get('university_type')
        university = request.POST.get('university')
        country = request.POST.get('country')
        lc_name = request.POST.get('lc_name')
        lc_address = request.POST.get('lc_address')
        lc_email = request.POST.get('lc_email')
        lc_tel = request.POST.get('lc_tel')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            learning_center_obj.university_type_id = university_type
            learning_center_obj.university_id = university
            learning_center_obj.country_id = country
            learning_center_obj.lc_name = lc_name
            learning_center_obj.lc_address = lc_address
            learning_center_obj.lc_email = lc_email
            learning_center_obj.lc_tel = lc_tel
            learning_center_obj.status = status
            learning_center_obj.save()
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/learning_centers_settings/')
    country_recs = CountryDetails.objects.all()
    # if learning_center_obj.university:
    #     if learning_center_obj.university.is_partner_university == False:
    #         university_recs = UniversityDetails.objects.filter(is_delete = False,is_active = True,is_partner_university = False).order_by('-id')
    #     else:
    #         university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
    #                                                        is_partner_university=True).order_by('-id')
    # else:
    university_recs = ''
    if learning_center_obj.university_type:
        university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                           university_type_id=learning_center_obj.university_type.id).order_by('-id')
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    return render(request, "edit_learning_centers.html", {'learning_center_obj': learning_center_obj,'country_recs':country_recs,'university_recs':university_recs,'university_type_recs':university_type_recs})

def delete_learning_centers(request):
    if request.method == 'POST':
        learning_centers_delete_id = request.POST.get('learning_centers_delete_id')
        try:
            LearningCentersDetails.objects.filter(id=learning_centers_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/learning_centers_settings/')


def university_partner_settings(request):
    university_partner_recs = UniversityDetails.objects.filter(is_partner_university = True,is_delete=False)
    return render(request, 'university_partner_settings.html', {'university_partner_recs': university_partner_recs})


def add_university_partner(request):
    if request.method == 'POST':
        university_logo = request.FILES.get('university_logo', None)
        university_name = request.POST.get('university_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        website = request.POST.get('website')
        university_address = request.POST.get('university_address')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            UniversityDetails.objects.create(is_partner_university = True,university_logo = university_logo,
                                             university_name=university_name, email=email,telephone = telephone,website = website,
                                             address = university_address,is_active = status)
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/university_partner_settings/')
    return render(request, 'add_university_partner.html')


def edit_university_partner(request, university_id=None):
    university_obj = UniversityDetails.objects.get(id=university_id)
    if request.method == 'POST':
        university_logo = request.FILES.get('university_logo', None)
        university_name = request.POST.get('university_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        website = request.POST.get('website')
        university_address = request.POST.get('university_address')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            university_obj.university_name = university_name
            university_obj.email = email
            university_obj.telephone = telephone
            university_obj.website = website
            university_obj.address = university_address
            university_obj.is_active = status
            if university_logo:
                university_obj.university_logo = university_logo
            university_obj.save()
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/university_partner_settings/')
    return render(request, "edit_university_partner.html", {'university_obj': university_obj})


def delete_university_partner(request):
    if request.method == 'POST':
        university_delete_id = request.POST.get('university_delete_id')
        try:
            UniversitPartnerDetails.objects.filter(id=university_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/university_partner_settings/')

def campus_settings(request):
    campus_recs = CampusBranchesDetails.objects.all()
    return render(request, 'campus_settings.html', {'campus_recs': campus_recs})


def add_campus(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        university = request.POST.get('university')
        university_type = request.POST.get('university_type')
        campus_name = request.POST.get('campus_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        website = request.POST.get('website')
        address = request.POST.get('address')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            CampusBranchesDetails.objects.create(
                                             campus_name=campus_name, email=email,telephone = telephone,website = website,
                                             address = address,is_active = status,country_id = country,university_id=university,university_type_id = university_type)
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/campus_settings/')
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,is_partner_university = False).order_by('-id')
    country_recs = CountryDetails.objects.all()
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    return render(request, 'add_campus.html',{'university_recs':university_recs,'country_recs':country_recs,'university_type_recs':university_type_recs})


def edit_campus(request, campus_id=None):
    campus_obj = CampusBranchesDetails.objects.get(id=campus_id)
    if request.method == 'POST':
        country = request.POST.get('country')
        university_type = request.POST.get('university_type')
        university = request.POST.get('university')
        campus_name = request.POST.get('campus_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        website = request.POST.get('website')
        address = request.POST.get('address')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            campus_obj.university_type_id = university_type
            campus_obj.country_id = country
            campus_obj.university_id = university
            campus_obj.campus_name = campus_name
            campus_obj.email = email
            campus_obj.telephone = telephone
            campus_obj.website = website
            campus_obj.address = address
            campus_obj.is_active = status
            campus_obj.save()
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/campus_settings/')
    # if campus_obj.university.is_partner_university == False:
    #     university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,is_partner_university = False).order_by('-id')
    # else:
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                           university_type_id=campus_obj.university_type.id).order_by('-id')
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    country_recs = CountryDetails.objects.all()
    return render(request, "edit_campus.html", {'campus_obj': campus_obj,'university_recs':university_recs,'country_recs':country_recs,'university_type_recs':university_type_recs})

def delete_campus(request):
    if request.method == 'POST':
        campus_delete_id = request.POST.get('campus_delete_id')
        try:
            CampusBranchesDetails.objects.filter(id=campus_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/campus_settings/')


def calendar_settings(request):
    calender_recs = CalenderDetails.objects.all()
    return render(request, 'calendar_settings.html', {'calender_recs': calender_recs})


def add_calendar(request):
    if request.method == 'POST':
        university = request.POST.get('university')
        university_type = request.POST.get('university_type')
        year = request.POST.get('year')
        branch = request.POST.get('branch')
        semester = request.POST.get('semester')
        activity = request.POST.get('activity')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')
        end_dt = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date()
        start_dt = datetime.datetime.strptime(str(start_date), "%Y-%m-%d").date()
        if status == 'on':
            status = True
        else:
            status = False
        try:
            CalenderDetails.objects.create(university_id=university, year_id=year,branch_id = branch,
                                             activity_id = activity,start_date = start_dt,end_date = end_dt,status=status,university_type_id = university_type)
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/calendar_settings/')
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,is_partner_university=False).order_by('-id')
    year_recs = YearDetails.objects.all()
    branch_recs = CampusBranchesDetails.objects.all()
    semester_recs = SemesterDetails.objects.all()
    activity_recs = ActivityDetails.objects.all()
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    return render(request, 'add_calender.html',{'university_recs':university_recs,'year_recs':year_recs,'branch_recs':branch_recs,'semester_recs':semester_recs,'activity_recs':activity_recs,'university_type_recs':university_type_recs})


def edit_calender(request, calender_id=None):
    calender_obj = CalenderDetails.objects.get(id=calender_id)
    if request.method == 'POST':
        university = request.POST.get('university')
        university_type = request.POST.get('university_type')
        year = request.POST.get('year')
        branch = request.POST.get('branch')
        semester = request.POST.get('semester')
        activity = request.POST.get('activity')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')
        start_dt = datetime.datetime.strptime(str(start_date), "%Y-%m-%d").date()
        end_dt = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").date()
        if status == 'on':
            status = True
        else:
            status = False
        try:
            calender_obj.university_type_id = university_type
            calender_obj.university_id = university
            calender_obj.year_id = year
            calender_obj.branch_id = branch
            calender_obj.activity_id = activity
            calender_obj.start_date = start_dt
            calender_obj.end_date = end_dt
            calender_obj.status = status
            calender_obj.save()
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/calendar_settings/')
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                           university_type_id=calender_obj.university_type.id).order_by('-id')
    year_recs = YearDetails.objects.all()
    branch_recs = CampusBranchesDetails.objects.all()
    semester_recs = SemesterDetails.objects.all()
    activity_recs = ActivityDetails.objects.all()
    university_type_recs = UniversityTypeDetails.objects.filter(status=True)
    return render(request, 'edit_calender.html',
                  {'university_recs': university_recs, 'year_recs': year_recs, 'branch_recs': branch_recs,
                   'semester_recs': semester_recs, 'activity_recs': activity_recs,'calender_obj':calender_obj,'university_type_recs':university_type_recs})

def delete_calender(request):
    if request.method == 'POST':
        calender_delete_id = request.POST.get('calender_delete_id')
        try:
            CalenderDetails.objects.filter(id=calender_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/calendar_settings/')


def department_settings(request):
    department_recs = DepartmentDetails.objects.all()
    return render(request, 'department_settings.html', {'department_recs': department_recs})

def add_department(request):
    if request.method == 'POST':
        logo = request.FILES.get('logo', None)
        department_name = request.POST.get('department_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        website = request.POST.get('website')
        university = request.POST.get('university')
        faculty = request.POST.get('faculty')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            department_obj = DepartmentDetails.objects.create(department_name=department_name,
                                             email=email,telephone = telephone,website = website,
                                             university_id = university,faculty_id = faculty,status = status)
            if department_obj:
                department_obj.logo = logo
                department_obj.save()
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/department_settings/')
    university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,is_partner_university = False).order_by('-id')
    faculty_recs = FacultyDetails.objects.filter(status=True).order_by('-id')
    return render(request, 'add_department.html',{'university_recs':university_recs,'faculty_recs':faculty_recs})


def edit_department(request, department_id=None):
    department_obj = DepartmentDetails.objects.get(id=department_id)
    if request.method == 'POST':
        logo = request.FILES.get('logo', None)
        department_name = request.POST.get('department_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        website = request.POST.get('website')
        university = request.POST.get('university')
        faculty = request.POST.get('faculty')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            department_obj.department_name = department_name
            department_obj.email = email
            department_obj.telephone = telephone
            department_obj.website = website
            department_obj.university_id = university
            department_obj.faculty_id = faculty
            department_obj.status = status
            if logo:
                department_obj.logo = logo
            department_obj.save()
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/department_settings/')
    if department_obj.university.is_partner_university == False:
        university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,is_partner_university=False).order_by('-id')
    else:
        university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                           is_partner_university=True).order_by('-id')
    faculty_recs = FacultyDetails.objects.filter(status=True).order_by('-id')
    return render(request, "edit_department.html", {'university_recs': university_recs,'faculty_recs':faculty_recs,'department_obj':department_obj})

def delete_department(request):
    if request.method == 'POST':
        department_delete_id = request.POST.get('department_delete_id')
        try:
            DepartmentDetails.objects.filter(id=department_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/department_settings/')


def link_department_staff(request):
    if request.method == 'POST':
        department = request.POST.get('department')
        staff = request.POST.get('staff')
        if not DepartmentStaffMapping.objects.filter(department_id = department,staff_id = staff):
            DepartmentStaffMapping.objects.create(department_id=department, staff_id=staff)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Already department and user exists.")
        return redirect('/masters/link_department_staff/')
    role_name_list = ['Admin', 'Student', 'Donor', 'Partner', 'Parent', 'System Admin']
    user_recs = User.objects.filter().exclude(role__name__in=role_name_list)
    department_recs = DepartmentDetails.objects.all()
    department_staff_recs = DepartmentStaffMapping.objects.all()
    return render(request, 'link_department_to_staff.html', {'department_staff_recs': department_staff_recs,'user_recs':user_recs,'department_recs':department_recs})



def delete_department_staff(request):
    if request.method == 'POST':
        mapping_delete_id = request.POST.get('mapping_delete_id')
        try:
            DepartmentStaffMapping.objects.filter(id=mapping_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/link_department_staff/')

def document_settings(request):
    documents_recs = DocumentDetails.objects.filter().exclude(document_name='Research Proposal')
    return render(request, 'document_settings.html', {'documents_recs': documents_recs})

def add_document(request):
    document_name = request.POST.get('document_name')
    try:
        if not DocumentDetails.objects.filter(document_name=document_name).exists():
            DocumentDetails.objects.create(document_name=document_name)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Document name already exists.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/document_settings/')


def update_documet(request):
    document_id = request.POST.get('document_id')
    document_name = request.POST.get('document_name')
    try:
        if not DocumentDetails.objects.filter(~Q(id=document_id), document_name=document_name).exists():
            DocumentDetails.objects.filter(id=document_id).update(document_name=document_name,
                                                                  )
            messages.success(request, "Record saved.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
        else:
            messages.warning(request, "Document name already exists.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/document_settings/')


def delete_document(request):
    if request.method == 'POST':
        document_delete_id = request.POST.get('document_delete_id')
        try:
            DocumentDetails.objects.filter(id=document_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/document_settings/')

def link_campus_staff(request):
    if request.method == 'POST':
        campus = request.POST.get('campus')
        staff = request.POST.get('staff')
        if not CampusStaffMapping.objects.filter(campus_id = campus,staff_id = staff):
            CampusStaffMapping.objects.create(campus_id=campus, staff_id=staff)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Already campus and user exists.")
        return redirect('/masters/link_campus_staff/')
    campus_recs = CampusBranchesDetails.objects.all()
    program_recs = ProgramDetails.objects.filter(is_delete=False).order_by('-id')
    role_name_list = ['Admin', 'Student', 'Donor', 'Partner', 'Parent', 'System Admin']
    user_recs = User.objects.filter().exclude(role__name__in=role_name_list)
    campus_staff_recs = CampusStaffMapping.objects.all()
    return render(request, 'link_campus_to_program.html', {'campus_recs': campus_recs,'program_recs':program_recs,'user_recs':user_recs,'campus_staff_recs':campus_staff_recs})


def delete_campus_staff(request):
    if request.method == 'POST':
        mapping_delete_id = request.POST.get('mapping_delete_id')
        try:
            CampusStaffMapping.objects.filter(id=mapping_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/link_campus_staff/')


def link_faculty_staff(request):
    if request.method == 'POST':
        faculty = request.POST.get('faculty')
        staff = request.POST.get('staff')
        if not FacultyStaffMapping.objects.filter(faculty_id = faculty,staff_id = staff):
            FacultyStaffMapping.objects.create(faculty_id=faculty, staff_id=staff)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Already faculty and user exists.")
        return redirect('/masters/link_faculty_staff/')
    role_name_list = ['Admin', 'Student', 'Donor', 'Partner', 'Parent', 'System Admin']
    user_recs = User.objects.filter().exclude(role__name__in=role_name_list)
    faculty_recs = FacultyDetails.objects.all()
    faculty_user_recs = FacultyStaffMapping.objects.all()
    return render(request, 'link_faculty_to_user.html', {'faculty_user_recs': faculty_user_recs,'user_recs':user_recs,'faculty_recs':faculty_recs})

def delete_faculty_user(request):
    if request.method == 'POST':
        mapping_delete_id = request.POST.get('mapping_delete_id')
        try:
            FacultyStaffMapping.objects.filter(id=mapping_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/link_faculty_staff/')


def link_university_staff(request):
    if request.method == 'POST':
        university_type = request.POST.get('university_type')
        if university_type == 'Main':
            university = request.POST.get('university')
        else:
            university = request.POST.get('university_partner_id')
        staff = request.POST.get('staff')
        if not UniversityStaffMapping.objects.filter(university_id = university,staff_id = staff):
            UniversityStaffMapping.objects.create(university_id=university, staff_id=staff)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Already university and user exists.")
        return redirect('/masters/link_university_staff/')
    role_name_list = ['Admin', 'Student', 'Donor', 'Partner', 'Parent', 'System Admin']
    user_recs = User.objects.filter().exclude(role__name__in=role_name_list)
    university_staff_recs = UniversityStaffMapping.objects.all()
    university_recs = UniversityDetails.objects.filter(is_delete=False,is_partner_university=False).order_by('-id')
    university_partner_recs = UniversityDetails.objects.filter(is_delete=False,is_partner_university=True).order_by('-id')
    return render(request, 'link_university_staff.html', {'university_staff_recs': university_staff_recs,'user_recs':user_recs,'university_recs':university_recs,'university_partner_recs':university_partner_recs})


def delete_university_user(request):
    if request.method == 'POST':
        mapping_delete_id = request.POST.get('mapping_delete_id')
        try:
            UniversityStaffMapping.objects.filter(id=mapping_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/link_university_staff/')


def group_settings(request):
    group_recs = GroupDetails.objects.all()
    return render(request, 'group_settings.html', {'group_recs': group_recs})


def add_group(request):
    group_name = request.POST.get('group_name')
    description = request.POST.get('description')
    try:
        if not GroupDetails.objects.filter(group_name=group_name).exists():
            GroupDetails.objects.create(group_name=group_name,description = description)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Group name already exists.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/group_settings/')

def update_group(request):
    group_id = request.POST.get('group_id')
    group_name = request.POST.get('group_name')
    description = request.POST.get('description')
    try:
        if not GroupDetails.objects.filter(~Q(id=group_id), group_name=group_name).exists():
            GroupDetails.objects.filter(id=group_id).update(group_name=group_name,
                                                                  description=description)
            messages.success(request, "Record saved.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
        else:
            messages.warning(request, "Group name already exists.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/group_settings/')

def delete_group(request):
    if request.method == 'POST':
        group_delete_id = request.POST.get('group_delete_id')
        try:
            GroupDetails.objects.filter(id=group_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/group_settings/')


def payment_settings(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        payment = request.POST.get('payment')
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        if payment == 'Yes':
            payment = True
        else:
            payment = False
        if payment_id:
            PaymentDetails.objects.filter(id=payment_id).update(amount = amount,currency = currency,is_payment = payment)
        else:
            PaymentDetails.objects.create(amount=amount, currency=currency,is_payment = payment)
        messages.success(request, "Record saved.")
        return redirect('/masters/payment_settings/')
    try:
        payment_obj = PaymentDetails.objects.get()
    except:
        payment_obj = None
    return render(request, 'payment_settings.html',{'payment_obj':payment_obj})

import requests
import json
def api_test(request):
    url = 'http://159.65.159.193:18000/api/user/v2/account/registration/'
    body = {
        "email": "it.support1@ust.edu",
        "name": "Ezz",
        "username": "Ezz551",
        "password": "Ezz@123",
        "level_of_education": "",
        "gender": "",
        "year_of_birth": "",
        "mailing_address": "",
        "goals": "",
        "country": "IN",
        "honor_code": "true",
        "terms_of_service": "true"
    }
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(body), headers=headers)
    print(r.content)


def get_departments_from_faculty(request):
    finalDict = []
    faculty_id = request.POST.get('faculty_id', None)
    faculty_recs = FacultyDetails.objects.filter(id = faculty_id)
    for rec in faculty_recs:
        for dep in rec.department.all():
            raw_dict = {}
            raw_dict['department']=dep.department
            raw_dict['id']=dep.id
            finalDict.append(raw_dict)
    return JsonResponse(finalDict, safe=False)

def get_departments_from_faculty_2(request):
    finalDict = []
    faculty_id = request.POST.get('faculty_id', None)
    faculty_recs = FacultyDetails.objects.filter(id = faculty_id)
    for rec in faculty_recs:
        for dep in rec.department.all():
            raw_dict = {}
            raw_dict['department']=dep.department
            raw_dict['id']=dep.id
            finalDict.append(raw_dict)
    return JsonResponse(finalDict, safe=False)

def get_departments_from_faculty_3(request):
    finalDict = []
    faculty_id = request.POST.get('faculty_id', None)
    faculty_recs = FacultyDetails.objects.filter(id = faculty_id)
    for rec in faculty_recs:
        for dep in rec.department.all():
            raw_dict = {}
            raw_dict['department']=dep.department
            raw_dict['id']=dep.id
            finalDict.append(raw_dict)
    return JsonResponse(finalDict, safe=False)

def get_programs_from_filter(request):
    final_list = []
    program_list = []
    study_mode = request.POST.get('study_mode', None)
    university = request.POST.get('university', None)
    study_level = request.POST.get('study_level', None)
    faculty = request.POST.get('faculty', None)
    department = request.POST.get('department', None)
    program_recs = ProgramDetails.objects.filter(is_delete=False)

    if university:
        program_recs = program_recs.filter(university_id = university)

    if study_level:
        program_recs = program_recs.filter(study_level_id = study_level)

    if faculty:
        program_recs = program_recs.filter(faculty_id = faculty)

    if department:
        program_recs = program_recs.filter(department_id = department)

    if study_mode:
        for rec in program_recs:
            for mode in rec.study_mode.filter(study_mode = study_mode):
                program_list.append(rec)

    if program_list:
        for rec in program_recs:
            raw_dict = {}
            raw_dict['id'] = rec.id
            raw_dict['program'] = rec.program_name
            final_list.append(raw_dict)
    return JsonResponse(final_list, safe=False)


def get_programs_from_faculty(request):
    final_list = []
    program_list = []
    study_mode = request.POST.get('study_mode', None)
    university = request.POST.get('university', None)
    study_level = request.POST.get('study_level', None)
    faculty = request.POST.get('faculty', None)
    department = request.POST.get('department', None)
    acceptance_avg = request.POST.get('acceptance_avg', None)

    program_recs = ProgramDetails.objects.filter(is_delete=False)

    if university:
        program_recs = program_recs.filter(university_id = university)

    if study_level:
        program_recs = program_recs.filter(study_type_id = study_level)

    if faculty:
        program_recs = program_recs.filter(faculty_id = faculty)

    if department:
        program_recs = program_recs.filter(department_id = department)

    # if study_mode:
    #     for rec in program_recs:
    #         for mode in rec.study_mode.filter(study_mode = study_mode):
    #             program_list.append(rec)

    # if program_list:
    for rec in program_recs:
        try:
            if int(acceptance_avg) >= int(rec.acceptance_avg):
                raw_dict = {}
                raw_dict['id'] = rec.id
                raw_dict['program'] = rec.program_name
                final_list.append(raw_dict)
        except:
            pass
    return JsonResponse(final_list, safe=False)

def get_programs_from_faculty_2(request):
    final_list = []
    program_list = []
    study_mode = request.POST.get('study_mode', None)
    university = request.POST.get('university', None)
    study_level = request.POST.get('study_level', None)
    faculty = request.POST.get('faculty', None)
    department = request.POST.get('department', None)
    acceptance_avg = request.POST.get('acceptance_avg', None)

    program_recs = ProgramDetails.objects.filter(is_delete=False)

    if university:
        program_recs = program_recs.filter(university_id = university)

    if study_level:
        program_recs = program_recs.filter(study_type_id = study_level)

    if faculty:
        program_recs = program_recs.filter(faculty_id = faculty)

    if department:
        program_recs = program_recs.filter(department_id = department)

    # if study_mode:
    #     for rec in program_recs:
    #         for mode in rec.study_mode.filter(study_mode = study_mode):
    #             program_list.append(rec)

    # if program_list:
    for rec in program_recs:
        if int(acceptance_avg) >= int(rec.acceptance_avg):
            raw_dict = {}
            raw_dict['id'] = rec.id
            raw_dict['program'] = rec.program_name
            final_list.append(raw_dict)
    return JsonResponse(final_list, safe=False)


def get_programs_from_faculty_3(request):
    final_list = []
    program_list = []
    study_mode = request.POST.get('study_mode', None)
    university = request.POST.get('university', None)
    study_level = request.POST.get('study_level', None)
    faculty = request.POST.get('faculty', None)
    department = request.POST.get('department', None)
    acceptance_avg = request.POST.get('acceptance_avg', None)

    program_recs = ProgramDetails.objects.filter(is_delete=False)

    if university:
        program_recs = program_recs.filter(university_id = university)

    if study_level:
        program_recs = program_recs.filter(study_type_id = study_level)

    if faculty:
        program_recs = program_recs.filter(faculty_id = faculty)

    if department:
        program_recs = program_recs.filter(department_id = department)

    # if study_mode:
    #     for rec in program_recs:
    #         for mode in rec.study_mode.filter(study_mode = study_mode):
    #             program_list.append(rec)

    # if program_list:
    for rec in program_recs:
        if int(acceptance_avg) >= int(rec.acceptance_avg):
            raw_dict = {}
            raw_dict['id'] = rec.id
            raw_dict['program'] = rec.program_name
            final_list.append(raw_dict)
    return JsonResponse(final_list, safe=False)


def get_faculty_from_university(request):
    faculty_list = []
    university_id = request.POST.get('university_id', None)
    faculty_recs = FacultyDetails.objects.filter(university_id = university_id)
    for faculty_obj in faculty_recs:
        raw_dict = {}
        raw_dict['id']=faculty_obj.id
        raw_dict['faculty_name']=faculty_obj.faculty_name
        faculty_list.append(raw_dict)
    return JsonResponse(faculty_list, safe=False)

def edit_document(request, doc_id=None):
    doc_obj = DocumentDetails.objects.get(id=doc_id)
    notes_total_count = doc_obj.notes.all().count()
    if request.method == 'POST':
        document_name = request.POST.get('document_name')
        doc_required = request.POST.get('doc_required')
        note_count = request.POST.get('note_count')
        # description = request.POST.get('description')
        try:
            doc_obj.document_name = document_name
            doc_obj.doc_required = doc_required
            # doc_obj.description = description
            doc_obj.save()
            doc_obj.notes.clear()
            for x in range(int(note_count)):
                try:
                    x = x + 1
                    note_obj = NotesDetails.objects.create(
                        note=request.POST.get('department_' + str(x)))
                    doc_obj.notes.add(note_obj)
                except:
                    pass

            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/document_settings/')
    return render(request, "edit_document.html", {'doc_obj': doc_obj,'notes_total_count':notes_total_count})

def arabic_lang_proficiency_settings(request):
    arabic_recs = ArabCompetencyTestDetails.objects.all()
    return render(request, 'arabic_lang_proficiency.html',
                  {'arabic_recs': arabic_recs})


def add_arabic_lang_proficiency(request):
    arab_competency_test = request.POST.get('arab_competency_test')
    try:
        if not ArabCompetencyTestDetails.objects.filter(arab_competency_test=arab_competency_test).exists():
            ArabCompetencyTestDetails.objects.create(arab_competency_test=arab_competency_test)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Arabic Competency Test already exists.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/arabic_lang_proficiency_settings/')

def edit_arabic_lang_proficiency(request):
    arab_competency_test_id = request.POST.get('arab_competency_test_id')
    arab_competency_test = request.POST.get('arab_competency_test')
    try:
        if not ArabCompetencyTestDetails.objects.filter(~Q(id=arab_competency_test_id), arab_competency_test=arab_competency_test).exists():
            ArabCompetencyTestDetails.objects.filter(id=arab_competency_test_id).update(arab_competency_test=arab_competency_test)
            messages.success(request, "Record saved.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
        else:
            messages.warning(request, "Arabic Competency Test already exists.")
            return HttpResponse(
                json.dumps({'success': "Arabic Competency Test already exists."}),
                content_type="application/json")
    except:
        messages.warning(request, "Record not updated.")
        return HttpResponse(json.dumps({'error': 'Record not updated.'}), content_type="application/json")

def delete_arabic_lang_proficiency(request):
    if request.method == 'POST':
        arab_competency_test_delete__id = request.POST.get('arab_competency_test_delete_id')
        try:
            ArabCompetencyTestDetails.objects.filter(id=arab_competency_test_delete__id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/arabic_lang_proficiency_settings/')


def english_lang_proficiency_settings(request):
    english_recs = EnglishCompetencyTestDetails.objects.all()
    return render(request, 'english_lang_proficiency.html',
                  {'english_recs': english_recs})

def add_english_lang_proficiency(request):
    english_competency_test = request.POST.get('english_competency_test')
    try:
        if not EnglishCompetencyTestDetails.objects.filter(english_competency_test=english_competency_test).exists():
            EnglishCompetencyTestDetails.objects.create(english_competency_test=english_competency_test)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "English Competency Test already exists.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/english_lang_proficiency_settings/')

def edit_english_lang_proficiency(request):
    english_competency_test_id = request.POST.get('english_competency_test_id')
    english_competency_test = request.POST.get('english_competency_test')
    try:
        if not EnglishCompetencyTestDetails.objects.filter(~Q(id=english_competency_test_id), english_competency_test=english_competency_test).exists():
            EnglishCompetencyTestDetails.objects.filter(id=english_competency_test_id).update(english_competency_test=english_competency_test)
            messages.success(request, "Record saved.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
        else:
            messages.warning(request, "English Competency Test already exists.")
            return HttpResponse(
                json.dumps({'success': "English Competency Test already exists."}),
                content_type="application/json")
    except:
        messages.warning(request, "Record not updated.")
        return HttpResponse(json.dumps({'error': 'Record not updated.'}), content_type="application/json")

def delete_english_lang_proficiency(request):
    if request.method == 'POST':
        english_competency_test_delete_id = request.POST.get('english_competency_test_delete_id')
        try:
            EnglishCompetencyTestDetails.objects.filter(id=english_competency_test_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/english_lang_proficiency_settings/')


def get_year_from_university(request):
    semester_list = []
    year_ids = []
    university = request.POST.get('university', None)
    year_recs = SemesterDetails.objects.all()
    if university:
        year_recs = year_recs.filter(university_id = university)
    if year_recs:
        for rec in year_recs:
            if not  rec.year.id in year_ids:
                raw_dict = {}
                raw_dict['id'] = rec.year.id
                raw_dict['year'] = rec.year.year_name
                year_ids.append(rec.year.id)
                semester_list.append(raw_dict)
    return JsonResponse(semester_list, safe=False)

def get_intake_semester_from_year(request):
    semester_list = []
    year = request.POST.get('year', None)
    program_level = request.POST.get('program_level', None)
    university = request.POST.get('university', None)
    semester_recs = SemesterDetails.objects.all()
    if year:
        semester_recs = semester_recs.filter(year_id = year)
    if program_level:
        semester_recs = semester_recs.filter(study_level_id = program_level)
    if university:
        semester_recs = semester_recs.filter(university_id = university)
    if semester_recs:
        for rec in semester_recs:
            for sem in rec.semester.all():
                raw_dict = {}
                raw_dict['id'] = sem.id
                raw_dict['semester'] = str(sem.semester + ' ' + (str(sem.start_date) + ' - ' + str(sem.end_date)))
                semester_list.append(raw_dict)
    return JsonResponse(semester_list, safe=False)

def get_semester_already_exists(request):
    semester_id = request.POST.get('semester_id', None)
    university = request.POST.get('university', None)
    year = request.POST.get('year', None)
    study_level = request.POST.get('study_level', None)
    semester_exists = False
    if semester_id:
        if SemesterDetails.objects.filter(university_id=university,year_id = year,study_level = study_level).exclude(
                id=semester_id).exists():
            semester_exists = True
        else:
            semester_exists = False
        return JsonResponse(semester_exists, safe=False)
    else:
        if SemesterDetails.objects.filter(university_id=university,year_id = year,study_level = study_level).exists():
            semester_exists = True
        else:
            semester_exists = False
        return JsonResponse(semester_exists, safe=False)


def get_faculty_from_study_mode(request):
    final_list = []
    program_list = []
    faculty_ids = []
    study_mode = request.POST.get('study_mode', None)
    study_level = request.POST.get('study_level', None)
    university = request.POST.get('university', None)
    program_recs = ProgramDetails.objects.filter(is_delete=False)
    if study_level:
        program_recs = program_recs.filter(study_level_id=study_level)
    if study_mode:
        for rec in program_recs:
            for mode in rec.study_mode.filter(study_mode=study_mode):
                program_list.append(rec)
    if program_list:
        for rec in program_list:
            if not rec.faculty.id in faculty_ids:
                raw_dict = {}
                if university:
                    if int(university) == rec.university.id:
                        raw_dict['id'] = rec.faculty.id
                        raw_dict['faculty'] = rec.faculty.faculty_name
                        faculty_ids.append(rec.faculty.id)
                        final_list.append(raw_dict)
                else:
                    raw_dict['id'] = rec.faculty.id
                    raw_dict['faculty'] = rec.faculty.faculty_name
                    faculty_ids.append(rec.faculty.id)
                    final_list.append(raw_dict)
    return JsonResponse(final_list, safe=False)




def get_faculty_from_study_mode_2(request):
    final_list = []
    program_list = []
    faculty_ids = []
    study_mode_2 = request.POST.get('study_mode_2', None)
    study_level_2 = request.POST.get('study_level_2', None)
    university = request.POST.get('university', None)
    program_recs = ProgramDetails.objects.filter(is_delete=False)
    if study_level_2:
        program_recs = program_recs.filter(study_level_id=study_level_2)
    if study_mode_2:
        for rec in program_recs:
            for mode in rec.study_mode.filter(study_mode=study_mode_2):
                program_list.append(rec)
    if program_list:
        for rec in program_list:
            if not rec.faculty.id in faculty_ids:
                raw_dict = {}
                if university:
                    if int(university) == rec.university.id:
                        raw_dict['id'] = rec.faculty.id
                        raw_dict['faculty'] = rec.faculty.faculty_name
                        faculty_ids.append(rec.faculty.id)
                        final_list.append(raw_dict)
                else:
                    raw_dict['id'] = rec.faculty.id
                    raw_dict['faculty'] = rec.faculty.faculty_name
                    faculty_ids.append(rec.faculty.id)
                    final_list.append(raw_dict)
    return JsonResponse(final_list, safe=False)

def get_faculty_from_study_mode_3(request):
    final_list = []
    program_list = []
    faculty_ids = []
    study_mode = request.POST.get('study_mode', None)
    study_level = request.POST.get('study_level', None)
    university = request.POST.get('university', None)
    program_recs = ProgramDetails.objects.filter(is_delete=False)
    if study_level:
        program_recs = program_recs.filter(study_level_id=study_level)
    if study_mode:
        for rec in program_recs:
            for mode in rec.study_mode.filter(study_mode=study_mode):
                program_list.append(rec)
    if program_list:
        for rec in program_list:
            if not rec.faculty.id in faculty_ids:
                raw_dict = {}
                if university:
                    if int(university) == rec.university.id:
                        raw_dict['id'] = rec.faculty.id
                        raw_dict['faculty'] = rec.faculty.faculty_name
                        faculty_ids.append(rec.faculty.id)
                        final_list.append(raw_dict)
                else:
                    raw_dict['id'] = rec.faculty.id
                    raw_dict['faculty'] = rec.faculty.faculty_name
                    faculty_ids.append(rec.faculty.id)
                    final_list.append(raw_dict)
    return JsonResponse(final_list, safe=False)

def get_faculty_from_study_level(request):
    final_list = []
    program_list = []
    faculty_ids = []
    study_mode = request.POST.get('study_mode', None)
    study_level = request.POST.get('study_level', None)
    university = request.POST.get('university', None)
    program_recs = ProgramDetails.objects.filter(is_delete=False)
    if university:
        program_recs = program_recs.filter(university_id=university)
    if study_level:
        program_recs = program_recs.filter(study_level_id=study_level)
    if study_mode:
        program_recs = program_recs.filter(study_type_id=study_mode)
    if program_recs:
        for rec in program_recs:
            if not rec.faculty.id in faculty_ids:
                raw_dict = {}
                raw_dict['id'] = rec.faculty.id
                raw_dict['faculty'] = rec.faculty.faculty_name
                faculty_ids.append(rec.faculty.id)
                final_list.append(raw_dict)
    # if study_mode:
    #     for rec in program_recs:
    #         for mode in rec.study_mode.filter(study_mode=study_mode):
    #             program_list.append(rec)

    # if program_list:
    #     for rec in program_list:
    #         if not rec.faculty.id in faculty_ids:
    #             raw_dict = {}
    #             if university:
    #                 if int(university) == rec.university.id:
    #                     raw_dict['id'] = rec.faculty.id
    #                     raw_dict['faculty'] = rec.faculty.faculty_name
    #                     faculty_ids.append(rec.faculty.id)
    #                     final_list.append(raw_dict)
    #             else:
    #                 raw_dict['id'] = rec.faculty.id
    #                 raw_dict['faculty'] = rec.faculty.faculty_name
    #                 faculty_ids.append(rec.faculty.id)
    #                 final_list.append(raw_dict)
    return JsonResponse(final_list, safe=False)


def get_faculty_from_study_level_2(request):
    final_list = []
    program_list = []
    faculty_ids = []
    study_mode = request.POST.get('study_mode_2', None)
    study_level = request.POST.get('study_level_2', None)
    university = request.POST.get('university', None)
    program_recs = ProgramDetails.objects.filter(is_delete=False)
    if university:
        program_recs = program_recs.filter(university_id=university)
    if study_level:
        program_recs = program_recs.filter(study_level_id=study_level)
    if study_mode:
        program_recs = program_recs.filter(study_type_id=study_mode)
    if program_recs:
        for rec in program_recs:
            if not rec.faculty.id in faculty_ids:
                raw_dict = {}
                raw_dict['id'] = rec.faculty.id
                raw_dict['faculty'] = rec.faculty.faculty_name
                faculty_ids.append(rec.faculty.id)
                final_list.append(raw_dict)
    return JsonResponse(final_list, safe=False)

    # final_list = []
    # program_list = []
    # faculty_ids = []
    # study_mode_2 = request.POST.get('study_mode_2', None)
    # study_level_2 = request.POST.get('study_level_2', None)
    # university = request.POST.get('university', None)
    # program_recs = ProgramDetails.objects.filter(is_delete=False)
    # if study_level_2:
    #     program_recs = program_recs.filter(study_level_id=study_level_2)
    # if study_mode_2:
    #     for rec in program_recs:
    #         for mode in rec.study_mode.filter(study_mode=study_mode_2):
    #             program_list.append(rec)
    # if program_list:
    #     for rec in program_list:
    #         if not rec.faculty.id in faculty_ids:
    #             raw_dict = {}
    #             if university:
    #                 if int(university) == rec.university.id:
    #                     raw_dict['id'] = rec.faculty.id
    #                     raw_dict['faculty'] = rec.faculty.faculty_name
    #                     faculty_ids.append(rec.faculty.id)
    #                     final_list.append(raw_dict)
    #             else:
    #                 raw_dict['id'] = rec.faculty.id
    #                 raw_dict['faculty'] = rec.faculty.faculty_name
    #                 faculty_ids.append(rec.faculty.id)
    #                 final_list.append(raw_dict)
    # return JsonResponse(final_list, safe=False)



def get_faculty_from_study_level_3(request):
    final_list = []
    program_list = []
    faculty_ids = []
    study_mode = request.POST.get('study_mode', None)
    study_level = request.POST.get('study_level', None)
    university = request.POST.get('university', None)
    program_recs = ProgramDetails.objects.filter(is_delete=False)
    if university:
        program_recs = program_recs.filter(university_id=university)
    if study_level:
        program_recs = program_recs.filter(study_level_id=study_level)
    if study_mode:
        program_recs = program_recs.filter(study_type_id=study_mode)
    if program_recs:
        for rec in program_recs:
            if not rec.faculty.id in faculty_ids:
                raw_dict = {}
                raw_dict['id'] = rec.faculty.id
                raw_dict['faculty'] = rec.faculty.faculty_name
                faculty_ids.append(rec.faculty.id)
                final_list.append(raw_dict)
    return JsonResponse(final_list, safe=False)
    # final_list = []
    # program_list = []
    # faculty_ids = []
    # study_mode = request.POST.get('study_mode', None)
    # study_level = request.POST.get('study_level', None)
    # university = request.POST.get('university', None)
    # program_recs = ProgramDetails.objects.filter(is_delete=False)
    # if study_level:
    #     program_recs = program_recs.filter(study_level_id=study_level)
    # if study_mode:
    #     for rec in program_recs:
    #         for mode in rec.study_mode.filter(study_mode=study_mode):
    #             program_list.append(rec)
    # if program_list:
    #     for rec in program_list:
    #         if not rec.faculty.id in faculty_ids:
    #             raw_dict = {}
    #             if university:
    #                 if int(university) == rec.university.id:
    #                     raw_dict['id'] = rec.faculty.id
    #                     raw_dict['faculty'] = rec.faculty.faculty_name
    #                     faculty_ids.append(rec.faculty.id)
    #                     final_list.append(raw_dict)
    #             else:
    #                 raw_dict['id'] = rec.faculty.id
    #                 raw_dict['faculty'] = rec.faculty.faculty_name
    #                 faculty_ids.append(rec.faculty.id)
    #                 final_list.append(raw_dict)
    # return JsonResponse(final_list, safe=False)


def get_program_mode_from_selected_program(request):
    program_mode_list = []
    program_id = request.POST.get('program_id', None)
    if program_id:
        program_mode_recs = ProgramDetails.objects.filter(id = program_id)
    if program_mode_recs:
        for rec in program_mode_recs:
            raw_dict = {}
            raw_dict['id'] = rec.study_type.id
            raw_dict['program_mode'] = rec.study_type.study_type
            program_mode_list.append(raw_dict)
    return JsonResponse(program_mode_list, safe=False)


def get_program_mode_from_selected_program_2(request):
    program_mode_list = []
    program_id = request.POST.get('program_id', None)
    if program_id:
        program_mode_recs = ProgramDetails.objects.filter(id = program_id)
    if program_mode_recs:
        for rec in program_mode_recs:
            raw_dict = {}
            raw_dict['id'] = rec.study_type.id
            raw_dict['program_mode'] = rec.study_type.study_type
            program_mode_list.append(raw_dict)
    return JsonResponse(program_mode_list, safe=False)



def get_program_mode_from_selected_program_3(request):
    program_mode_list = []
    program_id = request.POST.get('program_id', None)
    if program_id:
        program_mode_recs = ProgramDetails.objects.filter(id = program_id)
    if program_mode_recs:
        for rec in program_mode_recs:
            raw_dict = {}
            raw_dict['id'] = rec.study_type.id
            raw_dict['program_mode'] = rec.study_type.study_type
            program_mode_list.append(raw_dict)
    return JsonResponse(program_mode_list, safe=False)


def get_country_from_semester_year(request):
    country_list = []
    duplicate_country_ids = []
    university = request.POST.get('university', None)
    learning_centers_recs = LearningCentersDetails.objects.all()
    if university:
        learning_centers_recs = learning_centers_recs.filter(university_id = university)
        for rec in learning_centers_recs:
            if rec.country.id not in duplicate_country_ids:
                raw_dict = {}
                raw_dict['id'] = rec.country.id
                raw_dict['country'] = rec.country.country_name.capitalize()
                duplicate_country_ids.append(rec.country.id)
                country_list.append(raw_dict)
    return JsonResponse(country_list, safe=False)

def application_fee(request):
    application_fee_recs = PaymentDetails.objects.all()
    return render(request, 'application_fee_settings.html', {'application_fee_recs': application_fee_recs})

def add_application_fee(request):
    university_recs = UniversityDetails.objects.filter(is_delete=False,is_active=True,is_partner_university = False).order_by('-id')
    if request.method == 'POST':
        university = request.POST.get('university')
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            if not PaymentDetails.objects.filter(university_id=university).exists():
                PaymentDetails.objects.create(university_id=university,
                                             amount=amount, currency=currency,status = status)
                messages.success(request, "Record saved.")
            else:
                messages.warning(request, "University already exists.")

        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/application_fee/')
    return render(request, 'add_application_fee.html',{'university_recs':university_recs})

def edit_application_fee(request, fee_id=None):
    application_fee_obj = PaymentDetails.objects.get(id=fee_id)
    if request.method == 'POST':
        university = request.POST.get('university')
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            if not PaymentDetails.objects.filter(university_id=university).exclude(id = fee_id).exists():
                application_fee_obj.university_id = university
                application_fee_obj.amount = amount
                application_fee_obj.status = status
                application_fee_obj.currency = currency
                application_fee_obj.save()
                messages.success(request, "Record saved.")
            else:
                messages.warning(request, "University already exists.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/application_fee/')
    if application_fee_obj.university.is_partner_university == False:
        university_recs = UniversityDetails.objects.filter(is_delete = False,is_active = True,is_partner_university = False).order_by('-id')
    else:
        university_recs = UniversityDetails.objects.filter(is_delete=False, is_active=True,
                                                           is_partner_university=True).order_by('-id')
    return render(request, "edit_application_fee.html", {'university_recs':university_recs,'application_fee_obj':application_fee_obj})

def delete_application_fee(request):
    if request.method == 'POST':
        fee_delete_id = request.POST.get('fee_delete_id')
        try:
            PaymentDetails.objects.filter(id=fee_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/application_fee/')

def load_country(request):
    with open(settings.BASE_DIR + '/raw/countries.json') as f:
        data = json.load(f)
        count = 1
        for rec in data:
            CountryDetails.objects.create(country_name=rec['name'])
            print(count)
            count = count + 1


def delete_program_fee(request):
    if request.method == 'POST':
        program_delete_id = request.POST.get('program_delete_id')
        try:
            ProgramFeeDetails.objects.filter(id=program_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/program_fee_settings/')


def get_year_from_study_level(request):
    year_list = []
    program_level = request.POST.get('program_level', None)
    university = request.POST.get('university', None)
    semester_recs = SemesterDetails.objects.all()
    if program_level:
        semester_recs = semester_recs.filter(study_level_id = program_level)
    if university:
        semester_recs = semester_recs.filter(university_id = university)
    if semester_recs:
        for rec in semester_recs:
            raw_dict = {}
            raw_dict['id'] = rec.year.id
            raw_dict['year'] = rec.year.year_name
            year_list.append(raw_dict)
    return JsonResponse(year_list, safe=False)


def university_type_settings(request):
    university_type_recs = UniversityTypeDetails.objects.filter()
    return render(request, 'university_type_settings.html', {'university_type_recs': university_type_recs})


def add_university_type(request):
    if request.method == 'POST':
        university_type = request.POST.get('university_type')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            if not UniversityTypeDetails.objects.filter(university_type=university_type).exists():
                UniversityTypeDetails.objects.create(university_type=university_type,status = status)
            else:
                messages.warning(request, "University Type already exists.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/university_type_settings/')
    return render(request, 'add_university_type.html')

def edit_university_type(request, university_type_id=None):
    university_type_obj = UniversityTypeDetails.objects.get(id=university_type_id)
    if request.method == 'POST':
        university_type = request.POST.get('university_type')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            if not UniversityTypeDetails.objects.filter(university_type=university_type).exclude(id=university_type_id).exists():
                university_type_obj.university_type = university_type
                university_type_obj.status = status
                university_type_obj.save()
                messages.success(request, "Record saved.")
            else:
                messages.warning(request, "University Type already exists.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/university_type_settings/')
    return render(request, "edit_university_type.html", {'university_type_obj': university_type_obj})

def delete_university_type(request):
    if request.method == 'POST':
        university_type_delete_id = request.POST.get('university_type_delete_id')
        try:
            UniversityTypeDetails.objects.filter(id=university_type_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/university_type_settings/')



def type_settings(request):
    type_recs = TypeDetails.objects.filter()
    return render(request, 'type_settings.html', {'type_recs': type_recs})


def add_type(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            if not TypeDetails.objects.filter(type=type).exists():
                TypeDetails.objects.create(type=type,status = status)
            else:
                messages.warning(request, "Type already exists.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/type_settings/')
    return render(request, 'add_type.html')

def edit_type(request, type_id=None):
    type_obj = TypeDetails.objects.get(id=type_id)
    if request.method == 'POST':
        type = request.POST.get('type')
        status = request.POST.get('status')
        if status == 'on':
            status = True
        else:
            status = False
        try:
            if not TypeDetails.objects.filter(type=type).exclude(id=type_id).exists():
                type_obj.type = type
                type_obj.status = status
                type_obj.save()
                messages.success(request, "Record saved.")
            else:
                messages.warning(request, "Type already exists.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/type_settings/')
    return render(request, "edit_type.html", {'type_obj': type_obj})

def delete_type(request):
    if request.method == 'POST':
        type_delete_id = request.POST.get('type_delete_id')
        try:
            TypeDetails.objects.filter(id=type_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/type_settings/')


def view_semester_subject_list(request, program_id=None):
    study_plan_recs = StudyPlanDetails.objects.filter(program_id = program_id)
    return render(request, 'view_semester_subject_list.html',{'study_plan_recs':study_plan_recs,'program_id':program_id})

def edit_study_plan(request, program_id=None):
    if request.method == 'POST':
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        semester_program_category = request.POST.get('semester_program_category')
        course_count = request.POST.get('course_count')

        if semester_program_category == 'Semester Based':
            ProgramDetails.objects.filter(id = program_id).update(is_semester_based = True)
        else:
            ProgramDetails.objects.filter(id = program_id).update(is_semester_based = False)


        try:
            study_plan_obj = StudyPlanDetails.objects.create(program_id = program_id,academic_year_id=year,study_semester_id = semester)
            for count in range(int(course_count)):
                try:
                    count = count + 1
                    course_obj = CourseDetails.objects.create(code=request.POST['code_' + str(count)],
                                                          title=request.POST['title_' + str(count)],
                                                          unit=request.POST['unit_' + str(count)],
                                                          type=request.POST['type_' + str(count)])
                    study_plan_obj.course.add(course_obj)
                except Exception as e:
                    pass
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/view_semester_subject_list/'+str(program_id))


def delete_semester_based(request):
    if request.method == 'POST':
        semester_delete_id = request.POST.get('semester_delete_id')
        program_id = request.POST.get('program_id')
        try:
            study_plan_obj = StudyPlanDetails.objects.get(id=semester_delete_id)
            study_plan_obj.course.clear()
            StudyPlanDetails.objects.filter(id=semester_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/view_semester_subject_list/'+str(program_id))

def edit_semester_based(request, semester_id=None):
    study_plan_obj = StudyPlanDetails.objects.get(id=semester_id)
    if request.method == 'POST':
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        course_count = request.POST.get('course_count')
        try:
            study_plan_obj.academic_year_id = year
            study_plan_obj.study_semester_id = semester
            study_plan_obj.start_date = start_date
            study_plan_obj.end_date = end_date
            study_plan_obj.save()
            study_plan_obj.course.clear()
            for count in range(int(course_count)):
                try:
                    count = count + 1
                    course_obj = CourseDetails.objects.create(code=request.POST['code_' + str(count)],
                                                              title=request.POST['title_' + str(count)],
                                                              unit=request.POST['unit_' + str(count)],
                                                              type=request.POST['type_' + str(count)])
                    study_plan_obj.course.add(course_obj)
                except Exception as e:
                    pass
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/view_semester_subject_list/'+str(study_plan_obj.program.id))
    else:
        year_recs = YearDetails.objects.all()
        course_total_count = study_plan_obj.course.all().count()
        year_list = []
        semester_recs = SemesterDetails.objects.filter(university_id=study_plan_obj.program.university.id)
        if semester_recs:
            for rec in semester_recs:
                raw_dict = {}
                raw_dict['id'] = rec.year.id
                raw_dict['year'] = rec.year.year_name
                year_list.append(raw_dict)

        semester_list = []
        semester_recs = SemesterDetails.objects.all()
        if study_plan_obj.academic_year:
            semester_recs = semester_recs.filter(year_id=study_plan_obj.academic_year.id)
        if study_plan_obj.program.university:
            semester_recs = semester_recs.filter(university_id=study_plan_obj.program.university.id)
        if semester_recs:
            for rec in semester_recs:
                for sem in rec.semester.all():
                    raw_dict = {}
                    raw_dict['id'] = sem.id
                    raw_dict['semester'] = str(sem.semester + ' ' + (str(sem.start_date) + ' - ' + str(sem.end_date)))
                    semester_list.append(raw_dict)

        return render(request, "edit_semester_based.html",{'study_plan_obj':study_plan_obj,
                                                           'year_recs':year_recs,
                                                           'course_total_count':course_total_count,
                                                           'year_list':year_list,
                                                           'semester_list':semester_list})


def semester_fee_details(request, semester_id=None):
    study_plan_obj = StudyPlanDetails.objects.get(id = semester_id)
    semester_fee_obj = ''
    if SemesterBasedFeeDetails.objects.filter(study_plan_id=semester_id).exists():
        semester_fee_obj = SemesterBasedFeeDetails.objects.get(study_plan_id=semester_id)
    semester_count = 0
    if semester_fee_obj:
        semester_count = semester_fee_obj.semester_fee.all().count()
    if request.method == 'POST':
        program_fee_count = request.POST.get('program_fee_count')
        try:
            if SemesterBasedFeeDetails.objects.filter(study_plan_id=semester_id).exists():
                semester_fee_obj = SemesterBasedFeeDetails.objects.get(study_plan_id=semester_id)
            else:
                semester_fee_obj = SemesterBasedFeeDetails.objects.create(study_plan_id=semester_id)
            semester_fee_obj.semester_fee.clear()
            for x in range(int(program_fee_count)):
                try:
                    x = x + 1
                    semester_fee_type_obj = SemesterFeeType.objects.create(
                        fee_type=request.POST.get('fee_type_' + str(x)),
                        amount=request.POST.get('amount_' + str(x))
                        )
                    semester_fee_obj.semester_fee.add(semester_fee_type_obj)
                except:
                    pass
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/view_semester_subject_list/'+str(study_plan_obj.program.id))
    return render(request, 'semester_fee_details.html', {
        'semester_fee_obj': semester_fee_obj,
        'study_plan_obj': study_plan_obj,
        'semester_count': semester_count,
    })


def course_master_settings(request):
    prerequisite_course_details = PrerequisiteCourseDetails.objects.all()
    return render(request, 'prerequisite_course_details.html', {'prerequisite_course_details': prerequisite_course_details})

def add_courses(request):
    code = request.POST.get('code')
    course = request.POST.get('course')
    try:
        if not PrerequisiteCourseDetails.objects.filter(code=code,course = course).exists():
            PrerequisiteCourseDetails.objects.create(code=code,course = course)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Course already exists.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/course_master_settings/')


def update_course(request):
    course_id = request.POST.get('course_id')
    code = request.POST.get('code')
    course = request.POST.get('course')
    try:
        if not PrerequisiteCourseDetails.objects.filter(~Q(id=course_id), code=code,course = course).exists():
            PrerequisiteCourseDetails.objects.filter(id=course_id).update(code=code,
                                                                  course=course)
            messages.success(request, "Record saved.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
        else:
            messages.warning(request, "Course already exists.")
            return HttpResponse(json.dumps({'success': 'Record saved.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/course_master_settings/')


def delete_course(request):
    if request.method == 'POST':
        course_mode_delete_id = request.POST.get('course_mode_delete_id')
        try:
            PrerequisiteCourseDetails.objects.filter(id=course_mode_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/course_master_settings/')

def credit_study_plan(request, program_id=None):
    if request.method == 'POST':
        min_credit = request.POST.get('min_credit')
        max_credit = request.POST.get('max_credit')
        credit_year = request.POST.get('credit_year')
        credit_semester = request.POST.get('credit_semester')
        credit_program_category = request.POST.get('credit_program_category')
        credit_course_count = request.POST.get('credit_course_count')

        if credit_program_category == 'Semester Based':
            ProgramDetails.objects.filter(id = program_id).update(is_semester_based = True)
        else:
            ProgramDetails.objects.filter(id = program_id).update(is_semester_based = False)

        try:
            credit_study_plan_obj = CreditStudyPlanDetails.objects.create(program_id = program_id,min_credit=min_credit,max_credit = max_credit,academic_year_id = credit_year,semester_id = credit_semester)
            for count in range(int(credit_course_count)):
                try:
                    count = count + 1
                    if request.POST['credit_prerequisite_' + str(count)] == 'Yes':
                        credit_prerequisite = True
                        if request.POST['credit_course_' + str(count)] == '':
                            credit_course = None
                        else:
                            credit_course = request.POST['credit_course_' + str(count)]
                    else:
                        credit_prerequisite = False
                        credit_course = None
                    course_obj = CreditCourseDetails.objects.create(code=request.POST['credit_code_' + str(count)],
                                                          title=request.POST['credit_title_' + str(count)],
                                                          unit=request.POST['credit_unit_' + str(count)],
                                                          type=request.POST['credit_type_' + str(count)],
                                                          is_prerequisite=credit_prerequisite,
                                                          course_id=credit_course,
                                                                    )
                    credit_study_plan_obj.credit_course.add(course_obj)
                except Exception as e:
                    pass
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/view_credit_study_plan/'+str(program_id))

def view_credit_study_plan(request, program_id=None):
    credit_study_plan_recs = CreditStudyPlanDetails.objects.filter(program_id = program_id)
    return render(request, 'view_credit_study_plan.html',{'credit_study_plan_recs':credit_study_plan_recs,'program_id':program_id})

def edit_credit_based(request, credit_id=None):
    credit_study_plan_obj = CreditStudyPlanDetails.objects.get(id=credit_id)
    if request.method == 'POST':
        min_credit = request.POST.get('min_credit')
        max_credit = request.POST.get('max_credit')
        credit_course_count = request.POST.get('credit_course_count')
        credit_year = request.POST.get('credit_year')
        credit_semester = request.POST.get('credit_semester')
        try:
            credit_study_plan_obj.min_credit = min_credit
            credit_study_plan_obj.max_credit = max_credit
            credit_study_plan_obj.academic_year_id = credit_year
            credit_study_plan_obj.semester_id = credit_semester
            credit_study_plan_obj.save()
            credit_study_plan_obj.credit_course.clear()
            for count in range(int(credit_course_count)):
                try:
                    count = count + 1
                    if request.POST['credit_prerequisite_' + str(count)] == 'Yes':
                        credit_prerequisite = True
                        if request.POST['credit_course_' + str(count)] == '':
                            credit_course = None
                        else:
                            credit_course = request.POST['credit_course_' + str(count)]
                    else:
                        credit_prerequisite = False
                        credit_course = None
                    course_obj = CreditCourseDetails.objects.create(code=request.POST['credit_code_' + str(count)],
                                                          title=request.POST['credit_title_' + str(count)],
                                                          unit=request.POST['credit_unit_' + str(count)],
                                                          type=request.POST['credit_type_' + str(count)],
                                                          is_prerequisite=credit_prerequisite,
                                                          course_id=credit_course,
                                                                    )
                    credit_study_plan_obj.credit_course.add(course_obj)
                except Exception as e:
                    pass
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/view_credit_study_plan/' + str(credit_study_plan_obj.program.id))
    else:
        prerequisite_course_recs = PrerequisiteCourseDetails.objects.all()
        credit_course_total_count = credit_study_plan_obj.credit_course.all().count()
        year_list = []
        semester_recs = SemesterDetails.objects.filter(university_id=credit_study_plan_obj.program.university.id)
        if semester_recs:
            for rec in semester_recs:
                raw_dict = {}
                raw_dict['id'] = rec.year.id
                raw_dict['year'] = rec.year.year_name
                year_list.append(raw_dict)

        semester_list = []
        semester_recs = SemesterDetails.objects.all()
        if credit_study_plan_obj.academic_year:
            semester_recs = semester_recs.filter(year_id=credit_study_plan_obj.academic_year.id)
        if credit_study_plan_obj.program.university:
            semester_recs = semester_recs.filter(university_id=credit_study_plan_obj.program.university.id)
        if semester_recs:
            for rec in semester_recs:
                for sem in rec.semester.all():
                    raw_dict = {}
                    raw_dict['id'] = sem.id
                    raw_dict['semester'] = str(sem.semester + ' ' + (str(sem.start_date) + ' - ' + str(sem.end_date)))
                    semester_list.append(raw_dict)

        return render(request, "edit_credit_based.html",{'credit_study_plan_obj':credit_study_plan_obj,
                                                         'prerequisite_course_recs':prerequisite_course_recs,
                                                         'credit_course_total_count':credit_course_total_count,
                                                         'year_list':year_list,
                                                         'semester_list':semester_list})

def delete_credit_based(request):
    if request.method == 'POST':
        credit_delete_id = request.POST.get('credit_delete_id')
        program_id = request.POST.get('program_id')
        try:
            credit_study_plan_obj = CreditStudyPlanDetails.objects.get(id=credit_delete_id)
            credit_study_plan_obj.credit_course.clear()
            CreditStudyPlanDetails.objects.filter(id=credit_delete_id).delete()
            messages.success(request, "Record deleted.")
        except:
            messages.warning(request, "Record not deleted.")
        return redirect('/masters/view_credit_study_plan/' + str(program_id))


def year_semester_already_exists(request):
    semester = request.POST.get('semester', None)
    year = request.POST.get('year', None)
    program_id = request.POST.get('program_id', None)
    study_plan_id = request.POST.get('study_plan_id', None)
    semester_exists = False
    if study_plan_id:
        if StudyPlanDetails.objects.filter(program_id=program_id, academic_year_id=year,
                                           study_semester_id=semester).exclude(id = study_plan_id).exists():
            semester_exists = True
        else:
            semester_exists = False
        return JsonResponse(semester_exists, safe=False)
    else:
        if StudyPlanDetails.objects.filter(program_id = program_id,academic_year_id=year,study_semester_id = semester).exists():
            semester_exists = True
        else:
            semester_exists = False
        return JsonResponse(semester_exists, safe=False)


def credit_year_semester_already_exists(request):
    semester = request.POST.get('semester', None)
    year = request.POST.get('year', None)
    program_id = request.POST.get('program_id', None)
    credit_study_id = request.POST.get('credit_study_id', None)
    semester_exists = False
    if credit_study_id:
        if CreditStudyPlanDetails.objects.filter(program_id=program_id, academic_year_id=year,
                                                 semester_id=semester).exclude(id = credit_study_id).exists():
            semester_exists = True
        else:
            semester_exists = False
        return JsonResponse(semester_exists, safe=False)
    else:
        if CreditStudyPlanDetails.objects.filter(program_id = program_id,academic_year_id=year,semester_id = semester).exists():
            semester_exists = True
        else:
            semester_exists = False
        return JsonResponse(semester_exists, safe=False)


def change_program_categorization(request):
    program_categorizetion_type = request.POST.get('program_categorizetion_type', None)
    program_id = request.POST.get('program_id', None)
    if program_categorizetion_type == 'Semester Based':
        is_semester_based = True
    else:
        is_semester_based = False
    ProgramDetails.objects.filter(id = program_id).update(is_semester_based = is_semester_based)
    return JsonResponse(True, safe=False)

def credit_fee_details(request, credit_id=None):
    credit_obj = CreditStudyPlanDetails.objects.get(id = credit_id)
    if request.method == 'POST':
        credit_fee = request.POST.get('credit_fee')
        try:
            credit_obj.credit_fee = credit_fee
            credit_obj.save()
            messages.success(request, "Record saved.")
        except:
            messages.warning(request, "Record not saved.")
        return redirect('/masters/view_credit_study_plan/'+str(credit_obj.program.id))
    return render(request, 'credit_fee_details.html',{
        'credit_obj':credit_obj,
    })