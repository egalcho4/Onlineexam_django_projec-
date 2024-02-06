from django.shortcuts import render,redirect,reverse

from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from student import models as SMODEL
from exam import forms as QFORM
from .models import Teacher,Schedule
from django.contrib.auth.models import User
from exam.models import Question
from exam.models import Course,Departiment,Year_now
from student import forms as sforms
from student import forms as SFORM
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib import messages
from . import forms,models
from django.db.models import F, Q, When
import base64
#import threading, wave, pyaudio,pickle,struct
import sys
import queue
from django.db.models.lookups import GreaterThan, LessThan
import json
import os
#import imutils, socket
import numpy as np
import time,cv2
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from student.models import *
from agora_token_builder import RtcTokenBuilder
from concurrent.futures import ThreadPoolExecutor
import random

#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        return HttpResponseRedirect('teacherlogin')
    return render(request,'teacher/teachersignup.html',context=mydict)



def is_teacher(user):
    
    return user.groups.filter(name='TEACHER').exists()
@csrf_exempt
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    request.session['username']=request.user.username
    teacher=User.objects.get(username=request.session['username'])
    tech=Teacher.objects.get(user_id=teacher.id)
    teach=Teacher.objects.get(user_id=request.user.id)
    
    dict={
    
    'total_course':QMODEL.Course.objects.filter(dp_id=teach.depart).count(),
    'total_question':QMODEL.Question.objects.filter(dep=teach.depart).count(),
    'total_student':SMODEL.Student.objects.filter(dep=teach.depart).count(),
    'usertype':tech.type,
    }
    user=request.user.id
    teach=QMODEL.Teacher.objects.get(user_id=user)
    
   
    if is_ajax(request=request):
        msa=SMODEL.Sms_feedback.objects.filter(dep=teach.depart,seen="0").count()  
        

        return JsonResponse({"num":msa},status=200)

    return render(request,'teacher/teacher_dashboard.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm=QFORM.CourseForm()
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
            messages.success(request,"exam created successfully")
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher/teacher_add_exam.html',{'courseForm':courseForm,'usertype':teach.type})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all()
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher/teacher_view_exam.html',{'courses':courses,'usertype':teach.type})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    
    course.delete()
    messages.success(request,"exam deleted successfully")
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@login_required(login_url='adminlogin')
def teacher_question_view(request):
    tc=Teacher.objects.get(user_id=request.user.id)
    course=tc.course
    cor=QMODEL.Course.objects.get(id=course)
    tes=QMODEL.Test_hand.objects.filter(course=course)
    teach=Teacher.objects.get(user_id=request.user.id)
    if request.method=="POST":
        tname=request.POST.get('tname',False)
        tq=request.POST.get('tq',False)
        tm=request.POST.get('tm',False)
        te=QMODEL.Test_hand(name=tname,course=cor,tquest=tq,tmark=tm)
        te.save()
        messages.success(request,"exam added successfully")
    return render(request,'teacher/teacher_question.html',{'course':course,'usertype':teach.type,'tes':tes})
def delet_test(request,id):
    tes=QMODEL.Test_hand.objects.get(id=id)
    tes.delete()
    messages.success(request,"exam added successfully")
    return redirect('../teacher-question')
def exam_password_set(request):
    if request.method=="POST":
        id=request.POST.get('id',False)
        pas=request.POST.get('pas',False)
        tes=QMODEL.Test_hand.objects.get(id=id)
        tes.pas=pas
        tes.save()
        messages.success(request,"password seted sucessfully")
        #return redirect('teacher:teacher_add_question',id)
        return redirect('teacher:teacher-question')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request,id):
    tes=QMODEL.Test_hand.objects.get(id=id)
    request.session['tid']=id
    if request.method=='POST' :
        #myfile = request.FILES.get('image',False)
        #fs = FileSystemStorage()
        #filename = fs.save(myfile.name, myfile)
        course=request.POST.get('course',False)
        code=request.POST.get('code',False)
        question=request.POST.get('question',False)
        option1=request.POST.get('option1',False)
        option2=request.POST.get('option2',False)
        option3=request.POST.get('option3',False)
        option4=request.POST.get('option4',False)
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
        dep=request.POST.get('id',False)
        cv=Course.objects.get(id=course)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        img="2"
        typ=0
        qtn=Question(tes=tes,code=code,typ=typ,image=img,adby=t_dep,marks=mark,course=cv,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,dep=dep)
        qtn.save()
        messages.success(request,"question created successfully")
    
        return redirect('teacher:teacher_add_question',id)
    
        #return HttpResponseRedirect('/teacher/teacher-view-question')
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    depart=t_dep.pk
    dep=Teacher.objects.get(user_id=depart)
    dp_id=dep.depart
    t_course=dep.course
    cours=Course.objects.get(id=t_course)
    course=cours.id
    course_name=cours.course_name
    cour=QMODEL.Course.objects.get(id=course)
    questions=QMODEL.Question.objects.filter(course=cour,tes=tes)
    student=QMODEL.Result.objects.filter(exam_id=course)
    #if request.method=='POST':
    #    pass
    #response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    #response.set_cookie('course_id',course.id)
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher/add_question.html',{'usertype':teach.type,'exam':student,'username':dp_id,'course':course,'questions':questions,'course_name':course_name,'id':id})

def blanck_question(request):
     if request.method=="POST":
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
        dep=request.POST.get('id',False)
        id=request.POST.get('idt',False)
        exp=request.POST.get('exp',False)
        code=request.POST.get('code',False)
        
        cv=Course.objects.get(id=course)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        tes=QMODEL.Test_hand.objects.get(id=id)
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
        ans=answer.split(",")
        print(ans)
        img="2"
        typ=1
        qtn=Question(tes=tes,code=code,typ=typ,image=img,adby=t_dep,marks=mark,course=cv,question=question,answer=answer,dep=dep,dran=ans,exp=exp)
        qtn.save()
        messages.success(request,"question created successfully")
    
        return redirect('teacher:teacher_add_question',id)

def short_question(request):
    if request.method=="POST":
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
        exp=request.POST.get('exp',False)
        dep=request.POST.get('id',False)
        id=request.POST.get('idt',False)
        code=request.POST.get('code',False)
        cv=Course.objects.get(id=course)
        tes=QMODEL.Test_hand.objects.get(id=id)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
       
        img="2"
        typ=2
        qtn=Question(tes=tes,code=code,typ=typ,image=img,adby=t_dep,marks=mark,course=cv,question=question,answer=answer,dep=dep,short=answer,exp=exp)
        qtn.save()
        messages.success(request,"question created successfully")
    
        return redirect('teacher:teacher_add_question',id)

def true_false_question(request):
    if request.method=="POST":
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
        id=request.POST.get('idt',False)
        dep=request.POST.get('id',False)
        cv=Course.objects.get(id=course)
        username=request.session['username']
        code=request.POST.get('code',False)
        tes=QMODEL.Test_hand.objects.get(id=id)
        t_dep=User.objects.get(username=username)
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
        option1="True"
        option2="False"
        img="2"
        typ=3
        qtn=Question(tes=tes,code=code,typ=typ,image=img,adby=t_dep,marks=mark,course=cv,question=question,answer=answer,dep=dep, option1= option1, option2= option2)
        qtn.save()
        messages.success(request,"question created successfully")
    
        return redirect('teacher:teacher_add_question',id)

def paragraph(request):
    if request.method=="POST":
        id=request.POST.get('id',False)
        #course=request.POST.get('course',False)
        question=request.POST.get('question',False)
        
        """ dep=request.POST.get('id',False)
        cv=Course.objects.get(id=course)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        mark=request.POST.get('mark',False)
       
        code=request.POST.get('code',False)
        img="2"
        typ=4"""
        qt=Question.objects.get(id=id)
        qt.para=question
        #qtn=Question(code=code,typ=typ,image=img,adby=t_dep,course=cv,question=question,dep=dep,marks=mark)
        qt.save()
        messages.success(request,"question created successfully")
        id=request.session['tid']
        return redirect('teacher:teacher_add_question',id)
def makepretest(request,id):
    tes=QMODEL.Test_hand.objects.get(id=id)
    course=tes.course_id
    te=QMODEL.Test_hand.objects.filter(course_id=course)
     
    for t in te:
        t.pr=0
        t.save()

    tes.pr=1
    tes.save()
    messages.success(request,"exam seted frist at exam queue")
    return redirect('../teacher-question')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    techer_id=Teacher.objects.get(user_id=t_dep.id)
    
    courses= QMODEL.Course.objects.filter(id=techer_id.course)
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher/teacher_view_question.html',{'courses':courses,'usertype':teach.type})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request,'teacher/see_question.html',{'questions':questions})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    messages.success(request,"question deleted successfully")
    return HttpResponseRedirect('/teacher/teacher-view-question')

def exam_schedule(request,id):
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    depart=t_dep.id
    dep=Teacher.objects.get(user_id=depart)
    dp_id=dep.id
    dc=dep.depart
    t_course=dep.course
    cours=Course.objects.get(id=id)
    excourse=cours.id
    
    if request.method=="POST":
        time=request.POST.get('time',False)
        dat=request.POST.get('date',False)
        dur=request.POST.get('dr',False)
        
        sc=Schedule.objects.get(exam=excourse)
        sc.tim=time
        sc.dat=dat
        sc.dur=dur
        sc.dep=dep.depart
        sc.sem=cours.sem
        co=Course.objects.filter(dp=dc,sem=cours.sem)
        for b in co:
          
           
            b.pre=0
            b.save()
        cours=Course.objects.get(id=id)
        cours.pre=1
        cours.save()
        sc.save()
        messages.success(request,"exam scheduled successfully")
        return redirect('teacher:teacher_manage_course')
    cr=Course.objects.filter(dp_id=dc)
    ex=Schedule.objects.filter(exam=cours.id)
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,"teacher/exam_schedule.html",{'ex':ex,'cr':cr,'usertype':teach.type})

def teacher_manage_course(request):
    courseForm=QFORM.CourseForm()
    user=request.session['username']
    teacher_id=User.objects.get(username=user)
    depart=Teacher.objects.get(user_id=teacher_id.pk)
    dp_id=depart.depart
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
            c_c=courseForm.cleaned_data['c_code']
            c_name=courseForm.cleaned_data['course_name']
           
            qd=QMODEL.Course.objects.get(course_name=c_name)
            dat="2023-03-19"
            time="11:17"
            dur=120
            dpe_id=QMODEL.Departiment.objects.get(id=depart.depart)
            qd.dp=dpe_id
            qd.save()
            sc=Schedule(dat=dat,tim=time,dur=dur,adby=dp_id,exam= qd.id)
            sc.save()
            messages.success(request,"course created successfully")
        else:
            print("form is invalid")
        return redirect('teacher:teacher_manage_course')
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    depart=t_dep.id
    dep=Teacher.objects.get(user_id=depart)
    course=Course.objects.filter(dp=dep.depart)
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher/teacher_manage_course.html',{'courseForm':courseForm,'coures':course,'usertype':teach.type})

def qtdelete(request,id):
    question=QMODEL.Question.objects.get(id=id)
    question.delete()
    messages.success(request,"question deleted successfully")
    return redirect('teacher:teacher-question')

def teacher_wiew_course(request):
    courses = QMODEL.Course.objects.all()
    return render(request,"teacher_wiew_course.html",{'courses':courses})

def register_student_view(request):
    teach=Teacher.objects.get(user_id=request.user.id)
    context={'total_student':SMODEL.Student.objects.filter(dep=teach.depart).count(),
             'usertype':Teacher.objects.get(user_id=request.user.id),
              }
    return render(request,"teacher/register_student.html",context=context)
def add_year(request):
    user=request.user.id
    teacher=Teacher.objects.get(user_id=user)
    form=forms.YearADD()
    #yer=models.Year_now.objects.all()
    if request.method=="POST":
        form=forms.YearADD(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"year successfully added")
    ye=Year_now.objects.filter(dep_id=teacher.depart)
    return render(request,"teacher/add_year.html",{'form':form,'ye':ye})

def teacher_add_student(request,sem):
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    
    techer=Teacher.objects.get(user_id=t_dep.id)
    student= SMODEL.Student.objects.filter(dep=techer.depart,sem=sem)
    userForm=SFORM.StudentUserForm()
    studentForm=forms.StudentForm()
    
    userForm=SFORM.StudentUserForm()
    studentForm=SFORM.StudentForm()
    teach=Teacher.objects.get(user_id=request.user.id)
    mydict={'userForm':userForm,'studentForm':studentForm,'students':student,'usertype':teach.type}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST)
        studentForm=SFORM.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            image=studentForm.cleaned_data['profile_pic']
            student=studentForm.save(commit=False)
            student.user=user
            student.dep=techer.depart
            #student.profile_pic=image
            student.save()
            messages.success(request,"student added successfully")
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return redirect('teacher:teacher_add_student')
    return render(request,"teacher/teacher_add_student.html",context=mydict)
    

def delete_student(request,id):
    st= SMODEL.Student.objects.get(id=id)
    st.delete()
    user=User.objects.get(id=st.user_id)
    user.delete()
    messages.success(request,"student removed successfully")
    return redirect('teacher:teacher_add_student')

def student_marks(request):
    user=request.user.id
    t_user=Teacher.objects.get(user_id=user)
   # courses = QMODEL.Result.objects.filter(dep=t_user.depart)
    teach=Teacher.objects.get(user_id=request.user.id)
    courses=QMODEL.Course.objects.filter(dp=t_user.depart,lct=teach.id)
   
    

    return render(request,"teacher/student_marks.html",{'courses':courses,'usertype':teach.type})

def student_mark_report(request,id):
    user=request.user.id
    t_user=Teacher.objects.get(user_id=user)
    courses = QMODEL.Result.objects.filter(dep=t_user.depart,exam=id).order_by("-perc")
    above_sevent=0
    above_five=0
    bellow_fift=0
    fabove_sevent=0
    fabove_five=0
    fbellow_fift=0
    for i in courses:
        if i.perc>=75 and i.perc<=100:
            above_sevent+=1
        if i.perc>=50 and i.perc<75:
            above_five+=1
        if i.perc<=50 and i.perc>0:
            bellow_fift+=1

    




    teach=Teacher.objects.get(user_id=request.user.id)
    total_questions=QMODEL.Question.objects.filter(course_id=id).count()
   
    
    return render(request,"teacher/student_mark_report.html",{'courses':courses,'total':total_questions,'above_seven':above_sevent,'above_fift':above_five,'below_fift':bellow_fift})

  
   
   
   
    #return render(request,"teacher/student_mark_report.html",{'courses':courses,'total':total_questions})
@csrf_exempt
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    username=request.session['username']
        
    t_dep=User.objects.get(username=username)
    techer=Teacher.objects.get(user_id=t_dep.id)
    stud= SMODEL.Student.objects.filter(dep=techer.depart)
    teach=Teacher.objects.get(user_id=request.user.id)
    mydict={'userForm':userForm,'studentForm':studentForm,'students':stud,'usertype':teach.type}
 
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student.user=user
            student.regby=t_dep.id
            student.dep=techer.depart
            studentForm.save()
            messages.success(request,"student updated successfully")
            return redirect('teacher:teacher_add_student')
    return render(request,'teacher/update_student.html',context=mydict)
@csrf_exempt
def livestreaming(request):
    username=request.session['username']
        
    t_dep=User.objects.get(username=username)
    tcher=Teacher.objects.get(id=t_dep.pk)
    St=SMODEL.Student.objects.filter(dep=tcher.depart)
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,"teacher/livestreaming.html",{'st':St,'usertype':teach.type})
@csrf_exempt
def assgine_lecturer(request,id):
    if request.method=="POST":
        cou_id=request.POST.get('course',False)
        lectur=request.POST.get('lectur',False)
        lec=Teacher.objects.get(id=lectur)
        lec.course=cou_id
        dp=Course.objects.get(id=id)
        dp.lct=lec.id
        lec.save()
        dp.save()
        messages.success(request,"lecturer assigned successfully")
    dp=Course.objects.get(id=id)
    lec=Teacher.objects.filter(depart=dp.dp_id)
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,"teacher/assgine_lectur.html",{'lec':lec,'id':id,'usertype':teach.type})
def settings(request):
    if request.method=="POST":
        cam=request.POST.get('camera',False)
        ex=request.POST.get('ex',False)
        reg=request.POST.get('reg',False)
    return render(request,"teacher/setting.html")
def enable_student(request,id):
    st=SMODEL.Student.objects.get(id=id)
    st.ex_status=1
    st.save()
    messages.success(request,"exam enabled successfully")
    return redirect('teacher:teacher_add_student')
def disable_student(request,id):
    st=SMODEL.Student.objects.get(id=id)
    st.ex_status=2
    st.save()
    messages.success(request,"exam disabled successfully")
    return redirect('teacher:teacher_add_student')
def control_exam_status(request,id):
    username=request.session['username']
    course=Course.objects.get(id=id)
    t_dep=User.objects.get(username=username)
    #tcher=Teacher.objects.get(id=t_dep.pk)
    msg=SMODEL.Message.objects.filter(dep=course.dep)
    St=SMODEL.Student.objects.filter(dep=course.dep)
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,"teacher/control_exam_status.html",{'st':St,'msg':msg,'usertype':teach.type,'course':course,'username':request.user})
def sendmsg(request):
    if request.method=="POST":
        id=request.POST.get('id',False)
        msg=request.POST.get('msg',False)
        st=SMODEL.Student.objects.get(id=id)
        sdep=st.dep
        mg=SMODEL.Message(depsend=msg,receiver=id,dep=sdep)
        mg.save()
        messages.success(request,"message sent successfully")
        return redirect('teacher:livestreaming')
def delete_courses(request,id):
    cs=Course.objects.get(id=id)
    cs.delete()
    messages.success(request,"course remove successfully")
    return redirect('teacher:teacher_manage_course')
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH')=='XMLHttpRequest'
@csrf_exempt
def msgsender(request):
    teach=Teacher.objects.get(user_id=request.user.id)
    dep=teach.depart
   
    if request.method=="POST":
        id=request.POST.get('id',False)
        msg=request.POST.get('msg',False)
        ms=Message(receiver=id,dep=dep,depsend=msg)
        ms.save()
        messages.success(request,"messege sent successfully")
    return render(request,"teacher/messega_replay.html",{})
@csrf_exempt
def see_message(request,id):
    teach=Teacher.objects.get(user_id=request.user.id)
    dep=teach.depart
    select=SMODEL.Student.objects.get(id=id)
   
    if is_ajax(request=request):
        msg=Message.objects.filter(sender=select)
        for  sm in msg:
            mgst=sm.message
       
        msg2=Message.objects.filter(receiver=id)
        for m in msg2:
            msgd=m.depsend
           
            
        
       
        
        return JsonResponse({'msgd':msgd,'stm':mgst})
    return render(request,"teacher/messega_replay.html",{'student':select,'id':id})
@csrf_exempt
def first_exam(request,id):
    cour=QMODEL.Course.objects.get(id=id)
    
    curse=QMODEL.Course.objects.filter(dp_id=cour.dp_id)
    for c in curse:
        c.pre=0
        c.save()
    cour.pre=1
    cour.save()
    messages.success(request,"scheduled successfully")
    courseForm=QFORM.CourseForm()
    user=request.session['username']
    teacher_id=User.objects.get(username=user)
    depart=Teacher.objects.get(user_id=teacher_id.pk)
    dp_id=depart.depart
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
            c_c=courseForm.cleaned_data['c_code']
            c_name=courseForm.cleaned_data['course_name']
           
            qd=QMODEL.Course.objects.get(course_name=c_name)
            dat="2023-03-19"
            time="11:17"
            dur=120
            dpe_id=QMODEL.Departiment.objects.get(id=depart.depart)
            qd.dp=dpe_id
            qd.save()
            sc=Schedule(dat=dat,tim=time,dur=dur,adby=dp_id,exam= qd.id)
            sc.save()
            messages.success(request,"course created successfully")
        else:
            print("form is invalid")
        return redirect('teacher:teacher_manage_course')
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    depart=t_dep.id
    dep=Teacher.objects.get(user_id=depart)
    course=Course.objects.filter(dp=dep.depart)
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher/teacher_manage_course.html',{'courseForm':courseForm,'coures':course,'usertype':teach.type})

@csrf_exempt
def report(request,id):
    
    return render(request,"teacher/report.html")
@csrf_exempt
def control_exam(request):
    teach=Teacher.objects.get(user=request.user)
    dep=teach.depart
    cour=Course.objects.get(dp_id=dep,pre=1)
    return render(request,"teacher/control_exam_status.html",{'course':cour.course_name})
def lobby(request):
    teach=Teacher.objects.get(user=request.user)
    dep=teach.depart
    cour=Course.objects.get(dp_id=dep,pre=1)
    st=Student.objects.filter(dep=dep)
    return render(request, 'teacher/lobby.html',{'course':cour.course_name,'st':st})

def room(request):
    teach=Teacher.objects.get(user=request.user)
    dep=teach.depart
    cour=Course.objects.get(dp_id=dep,pre=1)
    st=Student.objects.filter(dep=dep)
    return render(request, 'teacher/room.html',{'course':cour.course_name,'st':st})

@csrf_exempt
def getToken(request):
    appId = "c7d8770db57247ff99b35f234fb77e4e"
    appCertificate = "edd4527ce66941dcb2850092ad69045c"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)
@csrf_exempt
def notfication(request):
    user=request.user.id
    teach=QMODEL.Teacher.objects.get(user_id=user)
    msa=SMODEL.Sms_feedback.objects.filter(dep=teach.depart)
    #st=SMODEL.Student.objects.filter(user_id=msa.sender)
    if is_ajax(request=request):
        msar=SMODEL.Sms_feedback.objects.filter(dep=teach.depart,status="pending").count()
       
        msg_sent=""
        for i in msa:

           msg_sent=i.msg

        return JsonResponse({"sent":msg_sent,"num":msar},status=200)
    return render(request,"teacher/notfication.html",{'msd':msa})
@csrf_exempt
def seen_not(request):
     if is_ajax(request=request):
        
        mn=SMODEL.Sms_feedback.objects.filter(seen=0,status="pending")
        for m in mn:
            mn.seen=1
        mn.save()
        return redirect('teacher:notfication')
@csrf_exempt
def not_repl(request,id):
    if request.method=="POST":
        rep=request.POST.get('msg',False)
        mn=SMODEL.Sms_feedback.objects.get(id=id)
        mn.replay=rep
        mn.status="replayed"
        mn.save()
        messages.success(request,"replayed succefully")
        return redirect('teacher:notfication')

    return render(request,"teacher/feedback.html")
@csrf_exempt
def start_all_exam(request):
    user=request.user.id
    teach=QMODEL.Teacher.objects.get(user_id=user)
    course=Course.objects.filter(dp=teach.depart,pre="1")

    return render(request,"teacher/start_all_exam.html",{"course":course})
@csrf_exempt
def start_now(request,id):
    cour=Course.objects.get(id=id)
    dep=cour.dp_id
    sem=cour.sem
    st=Student.objects.filter(sem=sem,dep=dep)
    for s in st:
        s.ex_status=1
        s.save()

    messages.success(request,"exam started now")
    return redirect("teacher:start_all_exam")
@csrf_exempt
def stop_now(request,id):
    cour=Course.objects.get(id=id)
    dep=cour.dp_id
    sem=cour.sem
    st=Student.objects.filter(sem=sem,dep=dep)
    for s in st:
        s.ex_status=0
        s.save()
   
    messages.success(request,"exam stoped now")
    return redirect("teacher:start_all_exam")
@csrf_exempt
def show_answer_now(request,id):
    cour=Course.objects.get(id=id)
    cour.answer=1
    cour.save()
    messages.success(request,"automatic evaluation enabled")
    return redirect("teacher:start_all_exam")
@csrf_exempt
def dont_show_answer_now(request,id):
    cour=Course.objects.get(id=id)

    cour.answer=0
    cour.save()
    #ans=SMODEL.Answer.objects.filter(exam=id)
    #ans.delete()
    messages.warning(request,"automatic evaluation disabled")
    return redirect("teacher:start_all_exam")
@csrf_exempt
def register_student_view_code(request):
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    
    techer=Teacher.objects.get(user_id=t_dep.id)
    student= SMODEL.Student.objects.filter(dep=techer.depart)
    userForm=SFORM.StudentUserForm()
    studentForm=forms.StudentForm()
    
    userForm=SFORM.StudentUserForm()
    studentForm=SFORM.StudentForm()
    teach=Teacher.objects.get(user_id=request.user.id)
    mydict={'userForm':userForm,'studentForm':studentForm,'students':student,'usertype':teach.type}
    return render(request,"teacher/register_student_view_code.html",mydict)

def enable_student_code(request,id):
    st=Student.objects.get(id=id)

    if request.method=="POST":
        codeg=request.POST.get('code',False)
        st.exam_code=codeg
        st.save()
        messages.success(request,"code satted succefully")
    return render(request,"teacher/code_set.html",{'code':st.exam_code})
@csrf_exempt
def account_update(request):
    teach=Teacher.objects.get(user=request.user)
    user=User.objects.get(username=teach.user)
    if request.method=="POST" or request.FILES:
        fname=request.POST.get('fname',False)
        lname=request.POST.get('lname',False)
        email=request.POST.get('email',False)
        mob=request.POST.get('mob',False)
        add=request.POST.get('add',False)
        image=request.FILES['image']
        user.first_name=fname
        user.last_name=lname
        user.email=email
        user.save()
        teach.mobile=mob
        teach.address=add
        teach.profile_pic=image
        teach.save()
        messages.success(request,"profile Updated successfully")

    return render(request,"teacher/account_update.html",{'user':user,'teach':teach})
@csrf_exempt
def change_password(request):
    username=request.user
    usa=User.objects.get(username=username)
    if is_ajax(request=request):
        pas=request.POST.get('pas')
        pas1=request.POST.get('pas1')
        us=authenticate(request,username=request.user,password=pas1)
        if us  is not None:
            if pas1 ==pas2:
                usa.set_password(pas)
                usa.save()
                messages.success(request,"password changed successfully")
            else:
                messages.error(request,"two password note match")
        
        else:
            messages.error(request,"current password not correct")
   
        
        return redirect('teacher:account_update')
    return render(request,"teacher/cange.html")
def asissment(request):
    user=request.user.id
    teach=Teacher.objects.get(user=request.user)
    course=QMODEL.Course.objects.get(id=teach.course)
    ass=QMODEL.Assiment.objects.filter(exam=course)
    return render(request,"teacher/asiment.html",{'stud':ass})
def ipadress(request):
    user=request.user.id
    teach=Teacher.objects.get(user=request.user)
    ip=SMODEL.Ip_adress.objects.filter(dep=teach.depart)
    return render(request,"teacher/ipdress.html",{'stud':ip})

def removeipfrom(request):
    user=request.user.id
    teach=Teacher.objects.get(user=request.user)
    ip=SMODEL.Ip_adress.objects.filter(dep=teach.depart)
    ip.delete()
    messages.success(request,"all ip was removed")
    return redirect('teacher:ipadress')
@csrf_exempt
def see_exam_detail(request,id):
    res=QMODEL.Result.objects.get(id=id)
    student=res.student.id
    studen=Student.objects.get(id=student)
    
    course=QMODEL.Course.objects.get(id=res.exam.id)
    tes=QMODEL.Test_hand.objects.get(course=course,pr=1)
    questions=QMODEL.Question.objects.filter(tes=tes,course=res.exam,code=studen.exam_code)
    
    answ=Answer.objects.get(student=studen,exam=res.exam.id,tes=tes.id)
    mrk=res.marks
    tot=0
    
    for i in questions:
        tot+=1*i.marks
        
    
    if request.method=="POST":
            ans=request.POST.get('ua',False)
            um=request.POST.get('um',False)
            pe=int(mrk)+int(um)
            try:
                perc=(pe/tot)*100
                res.marks=pe
                res.perc=perc
                res.save()
                messages.success(request,"updated sucessfully")
            except:
                pass
    teach=QMODEL.Teacher.objects.get(user_id=request.user.id)
    
   
    
    msa=SMODEL.Sms_feedback.objects.filter(dep=teach.depart,seen="0").count()  
        

        
    if is_ajax(request=request):
            return JsonResponse({"num":msa,"selected":answ.answer,"real":answ.real,'stans':answ.lanswer},status=200)
        
    return render(request,"teacher/see_exam_detail.html",{'questions':questions,'mrk':mrk})
def add_tabele(request):
    if request.method=="POST":
        name=request.POST.get('tname',False)
        data1=request.POST.get('data1',False)
        data2=request.POST.get('data2',False)
        data3=request.POST.get('data3',False)
        data4=request.POST.get('data4',False)
        data5=request.POST.get('data5',False)
        data6=request.POST.get('data6',False)
        data7=request.POST.get('data7',False)
        data8=request.POST.get('data8',False)
        data9=request.POST.get('data9',False)
        data10=request.POST.get('data10',False)
        data11=request.POST.get('data11',False)
        data12=request.POST.get('data12',False)
        data13=request.POST.get('data13',False)
        dan1=data1.split(",")
        dan2=data2.split(",")
        dan3=data3.split(",")
        dan4=data4.split(",")
        dan5=data5.split(",")
        dan6=data6.split(",")
        dan7=data7.split(",")
        dan8=data8.split(",")
        dan9=data9.split(",")
        dan10=data10.split(",")
        dan11=data11.split(",")
        dan12=data12.split(",")
        dan13=data13.split(",")
        id=request.POST.get('id',False)
        
        
        _m=QMODEL.Tables.objects.update_or_create(name=name)
        tble=QMODEL.Tables.objects.get(name=name)
        tble.data1=dan1
        tble.data2=dan2
        tble.data3=dan3
        tble.data4=dan4
        tble.data5=dan5
        tble.data6=dan6
        tble.data7=dan7
        tble.data8=dan8
        tble.data9=dan9
        tble.data10=dan10
        tble.data11=dan11
        tble.data12=dan12
        tble.data13=dan13
        tble.save()
       
        
        
        tq=QMODEL.Question.objects.get(id=id)
        tq.tabl=tble
        tq.save()
        messages.success(request,"table added successfully")
        return redirect('teacher:qedit',id)
def image_upadeta(request):
     if request.method=="POST" and request.FILES:
        
        file=request.FILES['img']
       
        id=request.POST.get('id',False)
        
        tq=QMODEL.Question.objects.get(id=id)
        tq.image=file
        tq.save()
        messages.success(request,"table added successfully")
        return redirect('teacher:qedit',id)
@csrf_exempt
def cqeditblanck(request,id):
    if request.method=='POST':
        #myfile = request.FILES.get('image',False)
        #fs = FileSystemStorage()
        #filename = fs.save(myfile.name, myfile)
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
       
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
        dep=request.POST.get('id',False)
        cv=Course.objects.get(id=course)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        qtn=Question.objects.get(id=id)
        
        qtn.adby=t_dep
        qtn.marks=mark
        qtn.course=cv
        qtn.question=question
        an=answer.split(",")
        qtn.dran=an
        qtn.dep=dep
        qtn.save()
        messages.success(request,"question created successfully")
        return redirect('teacher:qeditblanck',id)
       # return HttpResponseRedirect('/teacher/teacher-add-question')
        
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    depart=t_dep.pk
    dep=Teacher.objects.get(user_id=depart)
    dp_id=dep.depart
    t_course=dep.course
    cours=Course.objects.get(id=t_course)
    course=cours.id
    course_name=cours.course_name
    cour=QMODEL.Course.objects.get(id=course)
    questions=QMODEL.Question.objects.get(id=id)
    student=QMODEL.Result.objects.filter(exam_id=course)
    #if request.method=='POST':
    #    pass
    #response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    #response.set_cookie('course_id',course.id)
    qtn=Question.objects.get(id=id)
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher/cshort_update.html',{'usertype':teach.type,'qtn':qtn,'exam':student,'username':dp_id,'course':course,'questions':questions,'course_name':course_name,'qid':id})

@csrf_exempt
def qeditblanck(request,id):
    if request.method=='POST':
        #myfile = request.FILES.get('image',False)
        #fs = FileSystemStorage()
        #filename = fs.save(myfile.name, myfile)
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
       
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
        dep=request.POST.get('id',False)
        cv=Course.objects.get(id=course)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        qtn=Question.objects.get(id=id)
        
        qtn.adby=t_dep
        qtn.marks=mark
        qtn.course=cv
        qtn.question=question
       
        qtn.answer=answer
        qtn.dep=dep
        qtn.save()
        messages.success(request,"question created successfully")
        return redirect('teacher:qeditblanck',id)
       # return HttpResponseRedirect('/teacher/teacher-add-question')
        
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    depart=t_dep.pk
    dep=Teacher.objects.get(user_id=depart)
    dp_id=dep.depart
    t_course=dep.course
    cours=Course.objects.get(id=t_course)
    course=cours.id
    course_name=cours.course_name
    cour=QMODEL.Course.objects.get(id=course)
    questions=QMODEL.Question.objects.get(id=id)
    student=QMODEL.Result.objects.filter(exam_id=course)
    #if request.method=='POST':
    #    pass
    #response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    #response.set_cookie('course_id',course.id)
    qtn=Question.objects.get(id=id)
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher/blanck_update.html',{'usertype':teach.type,'qtn':qtn,'exam':student,'username':dp_id,'course':course,'questions':questions,'course_name':course_name,'qid':id})

@csrf_exempt
def qedit(request,id):
    if request.method=='POST'  and request.FILES['image']:
        myfile = request.FILES.get('image',False)
        #fs = FileSystemStorage()
        #filename = fs.save(myfile.name, myfile)
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
        option1=request.POST.get('option1',False)
        option2=request.POST.get('option2',False)
        option3=request.POST.get('option3',False)
        option4=request.POST.get('option4',False)
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
        dep=request.POST.get('id',False)
        cv=Course.objects.get(id=course)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        qtn=Question.objects.get(id=id)
        qtn.image=myfile
        qtn.adby=t_dep
        qtn.marks=mark
        qtn.course=cv
        qtn.question=question
        qtn.option1=option1
        qtn.option2=option2
        qtn.option3=option3
        qtn.option4=option4
        qtn.answer=answer
        qtn.dep=dep
        qtn.save()
        messages.success(request,"question created successfully")
        return redirect('teacher:qedit',id)
       # return HttpResponseRedirect('/teacher/teacher-add-question')
        
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    depart=t_dep.pk
    dep=Teacher.objects.get(user_id=depart)
    dp_id=dep.depart
    t_course=dep.course
    cours=Course.objects.get(id=t_course)
    course=cours.id
    course_name=cours.course_name
    cour=QMODEL.Course.objects.get(id=course)
    questions=QMODEL.Question.objects.get(id=id)
    student=QMODEL.Result.objects.filter(exam_id=course)
    #if request.method=='POST':
    #    pass
    #response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    #response.set_cookie('course_id',course.id)
    qtn=Question.objects.get(id=id)
    teach=Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher/upp_add_question.html',{'usertype':teach.type,'qtn':qtn,'exam':student,'username':dp_id,'course':course,'questions':questions,'course_name':course_name,'qid':id})
def wwitout_image(request):
     if request.method=="POST":
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
        option1=request.POST.get('option1',False)
        option2=request.POST.get('option2',False)
        option3=request.POST.get('option3',False)
        option4=request.POST.get('option4',False)
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
        dep=request.POST.get('id',False)
        id=request.POST.get('id',False)
        cv=Course.objects.get(id=course)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        qtn=Question.objects.get(id=id)
        
        qtn.adby=t_dep
        qtn.marks=mark
        qtn.course=cv
        qtn.question=question
        qtn.option1=option1
        qtn.option2=option2
        qtn.option3=option3
        qtn.option4=option4
        qtn.answer=answer
        qtn.dep=dep
        qtn.save()
        messages.success(request,"question created successfully")
        return redirect('teacher:qedit',id)

        




    




