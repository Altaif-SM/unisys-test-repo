from django.shortcuts import render

# Create your views here.
def template_donor_dashboard(request):
    return render(request, "template_donor_dashboard.html")

def template_student_selection(request):
    return render(request, "template_student_selection.html")

def template_student_reports(request):
    return render(request, "template_student_reports.html")