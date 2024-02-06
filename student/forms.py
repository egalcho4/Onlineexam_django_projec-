from django import forms
from django.contrib.auth.models import User
from . import models
from exam import models as QMODEL
from .models import Student
class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username']
        widgets = {
        'password': forms.PasswordInput()
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model=models.Student
        fields=['profile_pic','gender','sem']
class StudentUpdate(forms.ModelForm):
    class Meta:
        model=Student
        fields=['address','mobile','profile_pic']
class UserStudentUpdate(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']
        

