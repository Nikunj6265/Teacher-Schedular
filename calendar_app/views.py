from django.shortcuts import render
from .models import Subject, Lesson
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import HttpResponse
from django.template.loader import render_to_string
#from weasyprint import HTML
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from django.views import View
from django.contrib import messages
#import openpyxl
#from reportlab.pdfgen import canvas
from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa
#import weasyprint
from django.http import HttpResponse
from .models import Subject




@login_required
def dashboard(request):
    subjects = Subject.objects.filter(teacher=request.user)
    lessons = Lesson.objects.filter(subject__in=subjects).order_by('date')
    return render(request, 'calendar_app/dashboard.html', {'subjects': subjects, 'lessons': lessons})

@login_required
def download_schedule(request, format):
    user = request.user
    subjects = Subject.objects.filter(teacher=user)
    lessons = Lesson.objects.filter(subject__in=subjects).order_by('date')

    if format == 'excel':
        df = pd.DataFrame(list(lessons.values('subject__name', 'name', 'date')))
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Schedule')
        output.seek(0)
        response = HttpResponse(output, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=schedule.xlsx'
        return response

    elif format == 'pdf':
        html = render_to_string('calendar_app/schedule_pdf.html', {'lessons': lessons})
        output = BytesIO()
        pisa.CreatePDF(html, dest=output)
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=schedule.pdf'
        return response

class Registration(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'calendar_app/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'calendar_app/register.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('login')