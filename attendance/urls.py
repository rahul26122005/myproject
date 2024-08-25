# attendance/urls.py
from django.urls import path
#from django.contrib.auth import views as auth_views
from .views import (
    IndexView,
    GroupSpecificView,
    RegisterView,
    UploadStudentFileView,
    SuccessView,
    StudentListView,
    GenerateIndividualReportsView,
    DownloadTemplateView,
    SelectClassView,
    View1,
    View2,
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('group-specific/', GroupSpecificView.as_view(), name='group_specific'),
    path('register/', RegisterView.as_view(), name='register'),
    path('upload-students/', UploadStudentFileView.as_view(), name='upload_students'),
    path('success/', SuccessView.as_view(), name='success'),
    path('student-list/', StudentListView.as_view(), name='student_list'),
    path('generate-reports/', GenerateIndividualReportsView.as_view(), name='generate_individual_reports'),
    path('download-template/', DownloadTemplateView, name='download_template'),
    path('select-class/', SelectClassView.as_view(), name='select_class'),
    path('Attendance/', View1.as_view(), name='take_attendance'),
    path('generate_report/', View2.as_view(), name='generate_report'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



"""
urlpatterns = [
    path('', views.index, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LoginView.as_view(template_name='login.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('group_specific/', views.group_specific_view, name='group_specific'),    
    path('students/', views.student_list, name='student_list'),
    path('templates', views.template_page, name='template_page'),
    path('upload_students/', views.upload_student_file, name='upload_students'),
    path('select_class/', views.select_class, name='select_class'),
    path('Attendance/', views.view1, name='take_attendance'),
    path('generate_report/', views.view2, name='generate_report'),
    path('success/', views.success, name='success'),
    path('download_template/', views.download_template, name='download_template'),
    path('generate_individual_reports/', views.generate_individual_reports, name='generate_individual_reports'),
]

"""
