#forms.py

from django import forms
from .models import Student
from .models import Myclass
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

class LoginoutForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

class UploadFileForm(forms.Form):
    file = forms.FileField()

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'student_class', 'section']


class MyclassForm(forms.ModelForm):
        class Meta:
            model = Myclass
            fields = ['student', 'status']

class MonthYearForm(forms.Form):
    month = forms.IntegerField(min_value=1, max_value=12, label='Month')
    year = forms.IntegerField(min_value=2000, max_value=2100, label='Year')
    student_class = forms.CharField(label='Class', max_length=50)
    section = forms.CharField(label='Section', max_length=50)
   
class UserRegisterForm(UserCreationForm):
    username= forms.CharField(max_length=30)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


