from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
import json
from masters.models import *
from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages
from django.db.models import Q


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
        if not YearDetails.objects.filter(~Q(id=year_id), year_name=year_name.lower()).exists():
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
        if not ScholarshipDetails.objects.filter(~Q(id=scholarship_id),
                                                 scholarship_name=scholarship_name.lower()).exists():
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
    degree_type_id = request.POST.get('degree_type')
    university = request.POST.get('university')
    try:
        if not ProgramDetails.objects.filter(program_name=program_name.lower(), degree_type_id=degree_type_id,
                                             university_id=university).exists():
            ProgramDetails.objects.create(program_name=program_name.lower(), degree_type_id=degree_type_id,
                                          university_id=university)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Program, degree type and university relation already exists. Record not saved.")
    except:
        messages.warning(request, "Record not saved.")
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

def template_master_and_phd_master(request):
    master_and_phd_recs = MasterAndPhdFormula.objects.all()
    scholarship_recs = ScholarshipDetails.objects.all()
    return render(request, 'template_master_and_phd_master.html',
                  {'master_and_phd_recs': master_and_phd_recs, 'scholarship_recs': scholarship_recs})


def save_master_and_phd(request):
    scholarship_id = request.POST.get('scholarship')
    result = request.POST.get('result')
    repayment = request.POST.get('repayment')
    try:
        if not MasterAndPhdFormula.objects.filter(scholarship_id=scholarship_id.lower(),
                                                  result=result.lower()).exists():
            MasterAndPhdFormula.objects.create(scholarship_id=scholarship_id,
                                               result=result.lower(), repayment=repayment)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Formula already exists for this master. Record not saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_master_and_phd_master/')


def update_master_and_phd(request):
    master_and_phd_id = request.POST.get('master_and_phd_id')
    scholarship_id = request.POST.get('scholarship_id')
    result = request.POST.get('result')
    repayment = request.POST.get('repayment')
    try:
        if not MasterAndPhdFormula.objects.filter(~Q(id=master_and_phd_id), scholarship_id=scholarship_id,
                                                  result=result.lower()).exists():
            MasterAndPhdFormula.objects.filter(id=master_and_phd_id).update(scholarship_id=scholarship_id.lower(),
                                                                            result=result.lower(),
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


def delete_master_and_phd(request):
    master_and_phd_id = request.POST.get('master_and_phd_id')

    try:
        MasterAndPhdFormula.objects.filter(id=master_and_phd_id).delete()
        messages.success(request, "Record deleted.")
        return HttpResponse(json.dumps({'success': 'Record deleted.'}), content_type="application/json")
    except:
        messages.warning(request, "Record not deleted.")
    return HttpResponse(json.dumps({'error': 'Record not deleted.'}), content_type="application/json")


# *********------------ Master and course work Master ----------***************

def template_master_course_work_master(request):
    course_work_recs = MasterAndCourseFormula.objects.all()
    scholarship_recs = ScholarshipDetails.objects.all()
    return render(request, 'template_course_work_master.html',
                  {'course_work_recs': course_work_recs, 'scholarship_recs': scholarship_recs})


def save_master_course_work(request):
    scholarship_id = request.POST.get('scholarship')
    result_min = request.POST.get('result_min')
    result_max = request.POST.get('result_max')
    repayment = request.POST.get('repayment')
    try:
        if not MasterAndCourseFormula.objects.filter(scholarship_id=scholarship_id.lower(),
                                                     result_max=result_max.lower(),
                                                     result_min=result_min.lower()).exists():
            MasterAndCourseFormula.objects.create(scholarship_id=scholarship_id, result_max=result_max.lower(),
                                                  result_min=result_min.lower(), repayment=repayment)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Formula already exists for this master. Record not saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_master_course_work_master/')


def update_master_course_work(request):
    course_work_id = request.POST.get('course_work_id')
    scholarship_id = request.POST.get('scholarship_id')
    result_min = request.POST.get('result_min')
    result_max = request.POST.get('result_max')
    repayment = request.POST.get('repayment')
    try:
        if not MasterAndCourseFormula.objects.filter(~Q(id=course_work_id), scholarship_id=scholarship_id.lower(),
                                                     result_max=result_max.lower(),
                                                     result_min=result_min.lower()).exists():

            MasterAndCourseFormula.objects.filter(id=course_work_id).update(scholarship_id=scholarship_id.lower(),
                                                                            result_max=result_max.lower(),
                                                                            result_min=result_min.lower(),
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


# *********------------ Master and course work Master ----------***************

def template_degree_formula_master(request):
    degree_recs = DegreeFormula.objects.all()
    scholarship_recs = ScholarshipDetails.objects.all()
    return render(request, 'template_degree_formula_master.html',
                  {'degree_recs': degree_recs, 'scholarship_recs': scholarship_recs})


def save_degree_formula_master(request):
    scholarship_id = request.POST.get('scholarship')
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
            DegreeFormula.objects.create(scholarship_id=scholarship_id, cgpa_max=cgpa_max,
                                         cgpa_min=cgpa_min, grade_max=grade_max,
                                         grade_min=grade_min, repayment=repayment)
            messages.success(request, "Record saved.")
        else:
            messages.warning(request, "Formula already exists for this master. Record not saved.")
    except:
        messages.warning(request, "Record not saved.")
    return redirect('/masters/template_degree_formula_master/')


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


def get_table_data(request):
    # data = {'id': 1, 'column_name': 'abc', 'value': 'ABCD'}

    return HttpResponse(json.dumps(data), content_type="application/json")
