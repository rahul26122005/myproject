from django.shortcuts import render, redirect
import openpyxl
import os
from django.http import JsonResponse, HttpResponse
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from datetime import datetime
from io import BytesIO
from .models import Student, Attendance
from .forms import MonthYearForm, UploadFileForm, UserRegisterForm, LoginForm, ClassSectionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
import logging
from concurrent.futures import ThreadPoolExecutor


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Index View
class IndexView(LoginRequiredMixin, View):
    def get(self, request):

        return render(request, 'index.html')

# Custom Login View
class CustomLoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f"You Are Successfully Logged In!!...  {user.username}")
                return redirect('home')

        return render(request, self.template_name, {'form': form})

# Logout View
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, f"You Are Successfully Logged Out !!...  {request.user.username}")
        return redirect('home')

# Registration View
class register(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group, _ = Group.objects.get_or_create(name='YourGroupName')
            user.groups.add(group)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, ("You Are Successfully Logged In !!...  "))
            messages.success(request, ("wellcome {username} "))
            return redirect('home')
        return render(request, 'signup.html', {'form': form})

# Upload Students View

class UploadStudentFileView(LoginRequiredMixin,View):
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

            with transaction.atomic():
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
        return render(request, 'upload_students.html', {'form': form})

# Download Template View

"""def DownloadTemplateView(request):
    file_path = os.path.join('C:/StudioProjects/myproject/attendance/templates/student_template.xlsx')
    return HttpResponse(request,open(file_path, 'rb'), as_attachment=True, filename='student_template.xlsx')"""

class DownloadTemplateView(View):
    def get(self,request):

        return render(request, 'student_template.html')

# Attendance Mark View
class View1(LoginRequiredMixin, View):
    def get(self, request):
        form = ClassSectionForm(request.GET or None)
        students = []
        today = timezone.now().date()
        if form.is_valid():
            student_class = form.cleaned_data['student_class']
            section = form.cleaned_data['section']
            students = Student.objects.filter(
                user=request.user,
                student_class=student_class,
                section=section
            )
        return render(request, 'attendance/mark_attendance.html', {
            'form': form,
            'students': students,
            'today': today
        })

    def post(self, request):
        student_class = request.POST.get('student_class')
        section = request.POST.get('section')
        date = request.POST.get('date') or timezone.now().date()
        students = Student.objects.filter(
            user=request.user,
            student_class=student_class,
            section=section
        )
        with transaction.atomic():
            for student in students:
                status = request.POST.get(f'status_{student.roll_number}')
                if status:
                    Attendance.objects.update_or_create(
                        student=student,
                        date=date,
                        defaults={'status': status}
                    )
        return JsonResponse("Marked sucessfully")  

class View2(LoginRequiredMixin,View):
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

            # Setup Title and Header
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

            headers = ['ST Name', 'Reg Number', 'Class', 'Section']
            for day in range(1, 32):
                try:
                    current_date = datetime(year, month, day)
                    headers.append(current_date.strftime('%a %d'))
                except ValueError:
                    break
            headers.append('Total Days Present')
            headers.append('Total Days Absents')

            for col_num, header in enumerate(headers, 1):
                cell = sheet.cell(row=5, column=col_num) # type: ignore
                cell.value = header # type: ignore
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center')
                if col_num > 4:
                    cell.fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")

            # Optimized database query with prefetch_related
            students = Student.objects.filter(student_class=student_class, section=section).prefetch_related('attendance_set')

            def process_student(student):
                total_days_present = 0
                total_days_absent = 0
                student_row = [student.name, student.roll_number, student.student_class, student.section]
                for day in range(1, 32):
                    try:
                        current_date = datetime(year, month, day)
                        attendance = student.attendance_set.filter(date=current_date).first()
                        if attendance:
                            status = attendance.status
                            if status in ['present', 'od']:
                                total_days_present += 1
                            if status in ['absent']:
                                total_days_absent += 1
                        else:
                            status = ''
                        student_row.append(status)
                    except ValueError:
                        break
                student_row.append(total_days_present)
                student_row.append(total_days_absent)
                return student_row

            # Parallel processing using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=10) as executor:
                student_rows = list(executor.map(process_student, students))
            
            for row_num, student_row in enumerate(student_rows, 6):
                for col_num, cell_value in enumerate(student_row, 1):
                    sheet.cell(row=row_num, column=col_num).value = cell_value # type: ignore

            for col_num in range(1, len(headers) + 1):
                sheet.column_dimensions[get_column_letter(col_num)].width = 15 # type: ignore

            buffer = BytesIO()
            workbook.save(buffer)
            buffer.seek(0)

            response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename=attendance_{year}_{month}.xlsx'
            
            return response

        return render(request, self.template_name, {'form': form})
    