from django.shortcuts import render, redirect
import openpyxl
import os
#from .tasks import make_attendance_task
from django.http import JsonResponse, HttpResponse, FileResponse
from django.http import HttpResponse
import openpyxl
from django.db import transaction
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from datetime import datetime, date
from io import BytesIO
from datetime import datetime , date
from .models import *
from django.conf import settings
from .forms import MonthYearForm, UploadFileForm, UserRegisterForm , MyclassForm
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.views import View
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from .models import Student
from .forms import MyclassForm
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

from django.utils.decorators import method_decorator


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

@method_decorator(user_passes_test(lambda u: u.is_superuser or Group.objects.get_or_create(name='YourGroupName')[0] in u.groups.all()), name='dispatch')
class GroupSpecificView(View):
    def get(self, request):
        return render(request, 'group_specific.html')


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group, created = Group.objects.get_or_create(name='YourGroupName')
            user.groups.add(group)
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
        return render(request, 'register.html', {'form': form})


class UploadStudentFileView(View):
    def get(self, request):
        form = UploadFileForm()
        return render(request, 'upload_students.html', {'form': form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active

            missing_details = []
            for row in sheet.iter_rows(min_row=2, values_only=True): # type: ignore
                name, roll_number, student_class, section = row
                if not all([name, roll_number, student_class, section]):
                    missing_details.append(row)
                else:
                    Student.objects.create(
                        name=name,
                        roll_number=roll_number,
                        student_class=student_class,
                        section=section
                    )

            if missing_details:
                return render(request, 'upload_students.html', {
                    'form': form,
                    'missing_details': missing_details
                })

            return redirect('success')
        return render(request, 'upload_students.html', {'form': form})


class SuccessView(View):
    def get(self, request):
        return HttpResponse(request, "Students uploaded successfully!")


class StudentListView(View):
    def get(self, request):
        file_path = os.path.join('D:/django/attendance/templates', 'student_template.xlsx')
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        students = []
        for row in sheet.iter_rows(min_row=2, values_only=True): # type: ignore
            students.append({
                'name': row[0],
                'roll_number': row[1],
                'department': row[2],
            })

        return render(request, 'attendance/student_list.html', {'students': students})


class GenerateIndividualReportsView(View):
    def post(self, request):
        students = Student.objects.all()
        for student in students:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = 'Student Report' # type: ignore

            sheet['A1'] = 'Student Report' # type: ignore # type: ignore
            sheet['A1'].font = Font(size=14, bold=True) # type: ignore
            sheet['A1'].alignment = Alignment(horizontal='center') # type: ignore
            sheet.merge_cells('A1:D1') # type: ignore

            sheet['A2'] = 'Name:' # type: ignore
            sheet['B2'] = student.name # type: ignore
            sheet['A3'] = 'Roll Number:' # type: ignore
            sheet['B3'] = student.roll_number # type: ignore
            sheet['A4'] = 'Class:'  # type: ignore
            sheet['B4'] = student.student_class  # type: ignore
            sheet['A5'] = 'Section:'  # type: ignore
            sheet['B5'] = student.section  # type: ignore

            for col_num in range(1, 5):
                sheet.column_dimensions[get_column_letter(col_num)].width = 20  # type: ignore

            file_name = f'student_report_{student.roll_number}.xlsx'
            workbook.save(file_name)

        return HttpResponse( request, "Reports generated successfully!")


def DownloadTemplateView(request):
        file_path = os.path.join('D:/django/attendance/templates', 'student_template.xlsx')
        return FileResponse(request, open(file_path, 'rb'), as_attachment=True, filename='student_template.xlsx')


class SelectClassView(View):
    def get(self, request):
        classes = Student.objects.values_list('student_class', flat=True).distinct()

        return render(request, 'select_class.html', {'classes': classes})

class View1(View):
    def get(self, request):
        logging.debug("GET request received")
        
        # Fetch unique classes
        classes = Student.objects.values_list('student_class', flat=True).distinct()
        
        # Get the selected class and sections
        selected_class = request.GET.get('class')
        sections = Student.objects.filter(student_class=selected_class).values_list('section', flat=True).distinct() if selected_class else []
        
        # Get the selected section and filter students
        selected_section = request.GET.get('section')
        students = Student.objects.filter(student_class=selected_class, section=selected_section) if selected_class and selected_section else Student.objects.none()
        
        form = MyclassForm()

        return render(request, 'Attendance.html', {
            'form': form,
            'students': students,
            'classes': classes,
            'selected_class': selected_class,
            'sections': sections,
            'selected_section': selected_section
        })

    def post(self, request):
        logging.debug("POST request received")
        
        # Get the selected class and section
        selected_class = request.GET.get('class')
        selected_section = request.GET.get('section')
        students = Student.objects.filter(student_class=selected_class, section=selected_section)
        form_data = []

        # Process each student's attendance
        for student in students:
            status = request.POST.get(f'status_{student.id}')  # type: ignore
            if status:
                form_data.append({'student': student.id, 'status': status})  # type: ignore

        # Save the form data
        for data in form_data:
            form = MyclassForm(data)
            if form.is_valid():
                form.save()
            else:
                logging.error("Form is not valid: %s", form.errors)
                return JsonResponse({'error': 'Form is not valid', 'details': form.errors}, status=400)

        logging.info("Attendance marked successfully")
        return JsonResponse({'message': 'Attendance marked successfully'})

class View2(View):
    template_name = 'generate_report.html'
    form_class = MonthYearForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            student_class = form.cleaned_data['student_class']
            section = form.cleaned_data['section']

            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = 'Attendance Record' # type: ignore

            sheet['A1'] = 'ATTENDANCE RECORD' # type: ignore
            sheet['A1'].font = Font(size=14, bold=True) # type: ignore
            sheet['A1'].alignment = Alignment(horizontal='center') # type: ignore
            sheet.merge_cells('A1:H1') # type: ignore

            sheet['B2'] = 'Month:' # type: ignore
            sheet['C2'] = datetime(year, month, 1).strftime('%B') # type: ignore
            sheet['B3'] = 'Year:' # type: ignore
            sheet['C3'] = year # type: ignore

            sheet['B2'].alignment = Alignment(horizontal='right') # type: ignore
            sheet['B3'].alignment = Alignment(horizontal='right') # type: ignore

            headers = ['Em Name', 'Roll Number', 'Class', 'Section'] 
            for day in range(1, 32):
                try:
                    current_date = datetime(year, month, day)
                    headers.append(current_date.strftime('%a %d'))
                except ValueError:
                    break
            headers.append('Total Days Present')

            for col_num, header in enumerate(headers, 1):
                cell = sheet.cell(row=5, column=col_num) # type: ignore
                cell.value = header
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center')
                if col_num > 4:
                    cell.fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")

            students = Student.objects.filter(student_class=student_class, section=section)
            for row_num, student in enumerate(students, 6):
                sheet.cell(row=row_num, column=1).value = student.name # type: ignore
                sheet.cell(row=row_num, column=2).value = student.roll_number # type: ignore
                sheet.cell(row=row_num, column=3).value = student.student_class # type: ignore
                sheet.cell(row=row_num, column=4).value = student.section # type: ignore
                total_days_present = 0
                for day in range(1, 32):
                    try:
                        current_date = datetime(year, month, day)
                        attendance = Myclass.objects.filter(student=student, date=current_date).first()
                        if attendance:
                            status = attendance.status
                            if status in ['present', 'od']:
                                total_days_present += 1
                        else:
                            status = ''
                        cell = sheet.cell(row=row_num, column=day+4) # type: ignore
                        cell.value = status
                        if current_date.date() == date.today():
                            cell.fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
                    except ValueError:
                        break
                sheet.cell(row=row_num, column=len(headers)).value = total_days_present # type: ignore

            for col_num in range(1, len(headers) + 1):
                sheet.column_dimensions[get_column_letter(col_num)].width = 15 # type: ignore

            # Create a BytesIO buffer to save the workbook
            buffer = BytesIO()
            workbook.save(buffer)
            buffer.seek(0)

            # Create an HTTP response with the appropriate Excel content type
            response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename=attendance_{year}_{month}.xlsx'
            
            
            return response

        return render(request, self.template_name, {'form': form})