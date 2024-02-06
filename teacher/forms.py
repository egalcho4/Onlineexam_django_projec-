from django import forms
from django.contrib.auth.models import User
from .models import * 
from student.models import *
from exam.models import *
from student.models import Student
class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model=Teacher
        fields=['profile_pic','depart']
"""class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['address','mobile','profile_pic']"""
class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['address','mobile']
class QuestionForm(forms.ModelForm):
    class Meta:
        model=Question
        fields=['marks','question','dran']
class YearADD(forms.ModelForm):
    """ def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for visible in visible_fields:
            visible.field.widgets.attrs['class']="form-control"""
    class Meta:
        model=Year_now
        fields=('__all__')


