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

        elif YearDetails.objects.filter(~Q(id=year_id)).filter((Q(start_date__lte=start_date) & Q(end_date__gte=end_date)) | Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date))):
            messages.success(request, "Academic year already Exists")
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
            messages.success(request, "Record updated.")
            return HttpResponse(json.dumps({'success': 'Record updated.'}), content_type="application/json")
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
        if not CountryDetails.objects.filter(~Q(id=country_id), country_name=country_name.lower()).exists():
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
    except Exception as e:
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


def delete_semester(request):
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


def delete_program(request):
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