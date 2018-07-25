from django.shortcuts import render, redirect
from student.models import ApplicationDetails, ApplicantAcademicProgressDetails, StudentDetails
from django.contrib import messages
from masters.models import GuardianStudentMapping
from common.utils import get_current_year
# Create your views here.

def template_parent_dashboard(request):
    return render(request, "template_parent_dashboard.html")

def template_student_academic_report(request):
    try:

        stud_ids = GuardianStudentMapping.objects.filter(guardian__user_id=request.user.id).values("student")
        applicatin_recs = ApplicationDetails.objects.filter(student__in=stud_ids)

        application_recs = ApplicantAcademicProgressDetails.objects.filter(applicant_id__year=get_current_year(),
                                                                           applicant_id__in=applicatin_recs).order_by(
            '-last_updated')

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/parent/template_academic_progress/')

    return render(request, 'template_student_academic_report.html',
                  {'application_recs': application_recs})

def template_student_application_progress_history(request):
    applicant_recs = ''
    try:
        stud_ids = GuardianStudentMapping.objects.filter(guardian__user_id=request.user.id).values("student")
        applicant_recs = ApplicationDetails.objects.filter(student__in=stud_ids)

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))

    return render(request, 'template_student_progress_history.html',
                  {'applicant_recs': applicant_recs})


def filter_application_history(request):
    if request.POST:
        request.session['form_data'] = request.POST
        application = request.POST.get('application')
    else:
        form_data = request.session.get('form_data')
        application = form_data.get('application')

    try:

            stud = GuardianStudentMapping.objects.filter(guardian__user_id=request.user.id).values("student")

            applicant_recs = ApplicationDetails.objects.filter(student__in=stud,
                                                               is_sponsored=True)
            application_obj = ApplicationDetails.objects.get(id=application)

            application_history_recs = ApplicationDetails.objects.get(id=application).applicant_history_rel.all()

    except Exception as e:
        messages.warning(request, "Form have some error" + str(e))
        return redirect('/parent/template_student_application_progress_history/')

    return render(request, 'template_student_progress_history.html',
                  {'applicant_recs': applicant_recs, 'application_history_recs': application_history_recs,
                   'application_obj': application_obj})