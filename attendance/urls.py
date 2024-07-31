# attendance/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static




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

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)