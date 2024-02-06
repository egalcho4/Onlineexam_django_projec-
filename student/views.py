from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.http import JsonResponse,HttpRequest,HttpResponse
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL
from student import models as SModel
from django.contrib.auth.models import User
import cv2
from django.contrib.auth import authenticate, login
import os
import numpy as np

from django.db.models import Q
from django.views.decorators import gzip
from exam.models import *
import threading
import cv2,pandas
import time
from datetime import datetime
#import pyttsx3
from django.templatetags.static import static
from django.template.loader import render_to_string
from django.template import loader
from time import sleep
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib import messages
import subprocess
import random

from agora_token_builder import RtcTokenBuilder
from django.contrib.auth.forms import PasswordChangeForm
import json
from django.views.decorators.csrf import csrf_exempt
#for showing signup/login button for student
import socket
from .forms import *

from .models import *
import  socket
import numpy as np
import time
import base64
import threading
import sys
import queue
import os
import json
from concurrent.futures import ThreadPoolExecutor
import uuid
from django.http import StreamingHttpResponse
from .stream import LiveControl,VideoCamera



def studentclick_view(request):
    if request.user.is_authenticated:
        return redirect('exam:afterlogin')
        #return HttpResponseRedirect('reg/afterlogin')
    return render(request,'student/studentclick.html')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.regby=t_dep.id
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    id=request.user.id 
    std=Student.objects.get(user_id=id)
    st=SModel.Student.objects.get(user_id=request.user.id)
    sc=TMODEL.Schedule.objects.filter(dep=st.dep,sem=st.sem)
    request.session['id']=id
    cor=QMODEL.Course.objects.filter(dp_id=st.dep,sem=st.sem)
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'student':SModel.Student.objects.get(user_id=request.user.id),
     'sc':sc,
     'cor':cor,
    }
    return render(request,'student/student_dashboard.html',context=dict)
@csrf_exempt
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    user=request.user
    name=User.objects.get(username=user)
    sid_id=name.id
    st=SModel.Student.objects.get(user_id=sid_id)
    print(st.dep)
    depid=st.dep
    depart=QMODEL.Departiment.objects.get(id=depid)
    cid=depart.pk
    student=SModel.Student.objects.get(user_id=request.user.id)
    courses=QMODEL.Course.objects.get(dp=cid,pre=1,sem=student.sem)
    tes=QMODEL.Test_hand.objects.filter(course=courses)
    exam=QMODEL.Permision.objects.get(name="exam")
    host=socket.gethostname()
    ip=socket.gethostbyname(host)
    try:
        ipa=Ip_adress(ip=ip,host=host,name=name,dep=depid)
        ipa.save()
    except:
        messages.error(request,"this ip already exists ")
    if is_ajax(request=request):
         t=QMODEL.Test_hand.objects.get(course=courses,pr=1)
         pa=t.pas
         sid=t.id
         return JsonResponse({'pas':pa,'id':sid},status=200)

    return render(request,'student/student_exam.html',{'tes':tes,'exam':exam,'courses':courses,'student':student,'cours':courses.id})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    perm=QMODEL.Permision.objects.get(name="camera")
    student=SModel.Student.objects.get(user_id=request.user.id)
    paerm=perm.perm
    request.session['c_id']=pk
    course=QMODEL.Course.objects.get(id=pk)
    tes=QMODEL.Test_hand.objects.get(course=course)
    request.session['course_id']=course.id
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    studentv=User.objects.get(pk=request.user.id)
    stude=SModel.Student.objects.get(user_id=request.user.id)
    coursev=QMODEL.Course.objects.get(dp=stude.dep,pre="1")
    names= request.user.first_name+" "+request.user.last_name
    room=coursev.course_name.strip()
    #return render(request, 'student/lobby.html',{'name':name,'room':course.course_name})
    exam=QMODEL.Permision.objects.get(name="exam")
    
    
    return render(request,'student/take_exam.html',{'tes':tes,'exam':exam,'name':names,'room':room,'student':student,'course':course,'total_questions':total_questions,'total_marks':total_marks,'perm':paerm})

@csrf_exempt
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    
    ida=request.user.id 
    request.session['id']=ida
    
    course=QMODEL.Course.objects.get(id=pk)
    token=uuid.uuid4()
    tes=QMODEL.Test_hand.objects.get(course=course,pr=1)
    questions=QMODEL.Question.objects.all().filter(course=course,tes=tes)
    tes=QMODEL.Test_hand.objects.get(course=course,pr=1)
    total=QMODEL.Question.objects.filter(course=course,tes=tes).count()
    
    start=course.start
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    tes=QMODEL.Test_hand.objects.get(course=course,pr=1)
    questions=QMODEL.Question.objects.all().filter(course=course,tes=tes)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    perm=QMODEL.Permision.objects.get(name="camera")
    lv=QMODEL.Permision.objects.get(name="livestream")
    if is_ajax(request=request):
        b=0
        tim=request.GET.get('tim')
        if tim is None:
            b=b
        elif tim is not None:
            b=tim

        
       
        print(b)
        
       
        sc=TMODEL.Schedule.objects.get(exam=pk)
        st=SModel.Student.objects.get(user_id=ida)
        
        msga=SModel.Message.objects.filter(receiver=st.id).order_by('-id')[:1]
        ex_control=SModel.Exam_control.objects.filter(user_id_id=ida,exam=pk)
        material="" 
        motion=""
        tyme=ex_control.count()
        for n in ex_control:
            material=n.material if n.material==n.material else "none"
            material=material if material==material else "none"
            motion=n.mot_count if n.mot_count==n.mot_count else "none"
            motion=motion  if  motion==motion else "none"
            
            
        
        msg=""
        for i in msga:
            msg=i.depsend
            msg=msg if msg==msg else "no message"
       
        exam=st.ex_status
        exam=exam if exam==st.ex_status else "none stutus"
        time=sc.tim
        time=time
        dat=sc.dat
        dur=sc.dur
        
        quest=QMODEL.Question.objects.all().filter(course=course)
        actual_answer =[]
        for i in range(len(questions)):
        
            actual_answer.append(questions[i].answer) 
       
        
        return JsonResponse({'start':start,'total':total,'dat':dat,'tim':time,'dur':dur,'ex':exam,'msg':msg,'motion':motion,'material':material,'tyme':tyme,'room':course.course_name,'name':request.user.first_name},status=200)
    st=Student.objects.get(user_id=ida)
    tes=QMODEL.Test_hand.objects.get(course=course,pr=1)
    questions=QMODEL.Question.objects.all().filter(course=course,code=st.exam_code,tes=tes)
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'total_questions':total_questions,'total_marks':total_marks,'course':course,'questions':questions,'id':ida,'perm':perm,'lv':lv,'token':token})
    response.set_cookie('course_id',course.id)
    response.set_cookie('id',id)
    return response

@csrf_exempt
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
   
    user=request.user.id
    t_user=Student.objects.get(user_id=user)
    student=Student.objects.get(user_id=request.user.id)
    t_q=QMODEL.Question.objects.filter(dep=t_user.dep).count()
     
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        request.session['cname']=course_id
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        tes=QMODEL.Test_hand.objects.get(course=course,pr=1)
        questions=QMODEL.Question.objects.all().filter(course=course,code=student.exam_code,tes=tes)
        actual=[]
        selected=[]
        mark=[]
        qtm=[]
        qtans=[]
        qt=[]
        ktb=[]
        qtab=[]
        mb=[]
        iq1=[]
        iq2=[]
        lecta=[]
        lectr=[]
        for i in range(len(questions)):
           
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            lectr.append(actual_answer)
            lecta.append(selected_ans)
            if questions[i].typ == 0 or questions[i].typ==3 :
                actual.append(actual_answer)
                selected.append(selected_ans)
               
                if selected_ans==actual_answer:
                    total_marks+=1*questions[i].marks
                    mark.append(questions[i].marks)
            elif questions[i].typ == 1:
                ac="A"
                rl="B"
                iq1.append(i)
                actual.append(ac)
                selected.append(rl)
                
                #print(questions[i].dran[i])
                qt.append(set(questions[i].dran))
                mark.append(questions[i].marks)
                qtans.append(selected_ans)
            
            elif questions[i].typ==2:
                ac="A"
                rl="B"
                cor="A"
                iq2.append(i)  
                mark.append(questions[i].marks)
                try:
                    if selected_ans in questions[i].short:
                        total_marks+=1*questions[i].marks
                        actual.append(ac)
                        selected.append(cor)
                        #mark.append(questions[i].marks)
                    else:
                        actual.append(ac)
                        selected.append(rl)
                except:
                    pass
                #qtab.append(questions[i].short)
                #ktb.append(selected_ans)
                #mb.append(questions[i].marks)
            elif questions[i].typ == 4:
                ac="A"
                rl="B"
                iq1.append(i)
                actual.append(ac)
                selected.append(rl)
                mark.append(questions[i].marks)
        
      
        """for l in range(len(ktb)):
            pass
            cor="A"
            for m in range(len(qtab)):
                if ktb[l]==qtab[m]:
                    total_marks+=1*mb[l]
                    selected[iq2[l]]=cor
                    if m<len(ktb[l])+1:
                        break"""
        try:
            for k in range(len(qtans)):
                bm=list(qt[k]) 
                cor="A"
                b="B"
                for j in range(len(bm)):
                    
                    if bm[j] in qtans[k]:
                        total_marks+=1*mark[k]    
                        selected[iq1[k]]=cor
                    else:
                        total_marks+=0   
                        selected[iq1[k]]=b

                    if j<len(qtans[k])+1:
                        break
        except:
            pass
     
        tt=0
        for t in questions:
            tt+=t.marks
        perc=0
        try:
            perc=total_marks/sum(mark)*100
            print(perc)
        except:
            pass
        
        try:
             an=Answer.objects.get(exam=course_id,student=student)
             if an is not None:
                an.exam=course_id
                an.student=student
                an.answer=selected
                an.real=actual
                an.dran= qtans
                an.lanswer=lecta
                an.lreal=lectr
                an.save()
        except:
            ans=Answer(exam=course_id,student=student,answer=selected,real=actual,dran= qtans,lanswer=lecta,lreal=lectr,tes=tes.id)
            ans.save() 
        
        try:
            ass=Assiment(exam=course,test=tes,student=student,mark=perc,m=total_marks,total=sum(mark))
            ass.save()
        except:
            pass
        
        
            
            
                
        #total_marks= total_marks+questions[i].marks
        student = SModel.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.perc=perc
        result.dep=student.dep
        result.tes=tes
        result.save()
        student.ex_status=0
        student.save()
       
        

        return HttpResponseRedirect('view-result')
def asiment(request):
    user=request.user.id
    t_user=Student.objects.get(user_id=user)
    student=Student.objects.get(user_id=request.user.id)
    ass=QMODEL.Assiment.objects.filter(student=student)
    return render(request,"student/asiment.html",{'stud':ass})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    id= request.session['cname']
    student=SModel.Student.objects.get(user_id=request.user.id)
    courses=QMODEL.Course.objects.get(id=id)
    
    return render(request,'student/view_result.html',{'courses':courses,'student':student})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
@csrf_exempt
def check_marks_view(request,pk):
    
    student=SModel.Student.objects.get(user_id=request.user.id)
    course=QMODEL.Course.objects.get(id=pk)
    anser_show=course.answer
    tes=QMODEL.Test_hand.objects.get(course=course,pr=1)
    questions=QMODEL.Question.objects.all().filter(tes=tes,id=pk,code=student.exam_code)
    answer=Answer.objects.filter(student=student,exam=pk).order_by('-id')[:1]
    actual=[]
    select=[]
    lreal=[]
    total=0
   

    for i in answer:
        actual=i.real
        select=i.answer
        lreal=i.lreal
        if i.real==i.answer:
            total+=1

    student = SModel.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.filter(exam=course,student=student)
    #result= QMODEL.Result.objects.get(exam=course,student=student)
    result=QMODEL.Result.objects.filter(exam=course,student=student).order_by('-id')[:1]
    student=SModel.Student.objects.get(user_id=request.user.id)
    
    total_questions=QMODEL.Question.objects.filter(tes=tes,course=course,code=student.exam_code).count()
   
    questions=QMODEL.Question.objects.filter(course=course,code=student.exam_code,tes=tes)
    total_marks=0
    pers=0
    if total_marks==0:
        total_marks=1
    else:
        total_marks=total_marks
    mark_tot=0
    for mrk in result:
         mark_tot=mrk.marks
    for q in questions:
        total_marks=total_marks + q.marks
    try:
        mark=mark_tot/(total_marks-1)
        pers=mark*100
    except:
        pass
    
    for i in range(0,int(len(actual))-1):
       
        if actual[i]==select[i]:
            total+=1
            #print(actual[0])
   
   
            
    
  
    if is_ajax(request=request):
        return JsonResponse({"selected":select,"real":actual,'pers':pers,'lreal':lreal},status=200)
    
    
    return render(request,'student/check_marks.html',{'answer':answer,'anser_show':anser_show,'actual':actual,'selectd':select,'questions':questions,'persent':pers,'mark':mark_tot,'results':results,'student':student,'total':total_marks-1})
@csrf_exempt
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    student=SModel.Student.objects.get(user_id=request.user.id)

    if is_ajax(request=request):
       sem=request.POST.get('sem',False)
       
       y=Year_now.objects.filter(dep_id=student.dep,sem=sem)
       courses=QMODEL.Course.objects.filter(dp_id=student.dep,sem=sem)
    
       name=[]
       id=[]
       for p in courses:
           name.append(p.course_name)
           id.append(p.id)
        
       return JsonResponse({'name':name,'id':id},status=200)
      
    ye=QMODEL.Year_now.objects.filter(dep_id=student.dep) 
    return render(request,'student/student_marks.html',{'student':student,'yer':ye})



last_face = 'no_face'
current_path = os.path.dirname(__file__)
sound_folder = os.path.join(current_path, 'static/sound/')
face_list_file = os.path.join(current_path, 'face_list.txt')
sound = os.path.join(sound_folder, 'beep.wav')



def studentloginback(request):
     return redirect('student:student-dashboard')

@login_required(login_url='studentlogin')

def st_message(request):
    if request.method=="POST":
        user=SModel.Student.objects.get(user_id=request.user.id)
        message=request.POST.get('msg',False)
        dp=user.dep
        ms=SModel.Message(message=message,sender=user,dep=dp)
        ms.save()
        return redirect('student:student-exam')



@login_required(login_url='studentlogin')
def profile_change(request):
    username=request.user
    user =SModel.Student.objects.get(user=username)
    usera =User.objects.get(username=request.user)
    
    if request.method=="POST":
        user =SModel.Student.objects.get(user=username)
        usera =User.objects.get(username=request.user)
    
        fname=request.POST.get('fname',False)
        lname=request.POST.get('lname',False)
        email=request.POST.get('email',False)
        mob=request.POST.get('mob',False)
        addre=request.POST.get('add',False)
        image=request.FILES['image']
        usera.first_name=fname
        usera.last_name=lname
        usera.email=email
        usera.save()
        user.mobile=mob
        user.profile_pic=image
        user.address=addre
        user.save()
        messages.success(request,"profile updated successfully")
        
     
        
    
    user =SModel.Student.objects.get(user=username)
    usera =User.objects.get(username=request.user)
   
    return render(request,"student/profile.html",{'user':user,'usera':usera, 'student':SModel.Student.objects.get(user_id=request.user.id)})
def change_password(request):
    username=request.user
    usa=User.objects.get(username=username)
    #form=Password_change(us)
    if request.method == 'POST':
        pas=request.POST.get('pas',False)
        pas1=request.POST.get('pas1',False)
        pas2=request.POST.get('pas2',False)
        us=authenticate(request,username=username,password=pas)
        if us  is not None:
            if pas1 ==pas2:
                usa.set_password(pas1)
                usa.save()
                messages.success(request,"password changed successfully")
            else:
                messages.error(request,"two password note match")
        
        else:
            messages.error(request,"current password not correct")
   
       

    user =SModel.Student.objects.get(user=request.user)
    usera =User.objects.get(username=request.user)
    return render(request,"student/profile.html",{'user':user,'usera':usera, 'student':SModel.Student.objects.get(user_id=request.user.id),'usrn':username})
        
class Livestreaming(object):
    id=""
    name=""
    course=""
    token=""
    
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
       
        
        

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    
    def update(self):
        print(self.id)
        
        while True:
            (self.grabbed, self.frame) = self.video.read()
            
                      
            

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livestraming(request,token):
    
    try:
      cam = Livestreaming()
    
      cam.name=request.user
      st=SModel.Student.objects.get(user_id=request.user.id)
      st.urlf=f"http://127.0.0.1:8000/student/livestraming/{token}"
      st.save()
        
      #cam.course= request.session['c_id']
      cam.token=token
     
        
      return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except: 
        pass
def lobby(request):
    return render(request, 'student/lobby.html')

def room(request):
    return render(request, 'student/room.html')


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
def registration(request):
    perm=QMODEL.Permision.objects.get(name="registration")
    st=Student.objects.get(user_id=request.user.id)
    if request.method=="POST":
        sem=request.POST.get('sem',False)
        sm=int(sem)+1
        st=Student.objects.get(user_id=request.user.id)
        st.sem=sm
        st.save()
        messages.success(request,"you are registered successfully")
        
    
    
    return render(request,"student/registration.html",{'sem':st.sem,'perm':perm})
@csrf_exempt
def ask_for_help(request):
    msa=Sms_feedback.objects.filter(sender=request.user.id).order_by('-id')
    if is_ajax(request=request):
        msa=Sms_feedback.objects.filter(sender=request.user.id)
        rp=msa.replay
        msg_sent=""
        for i in msa:

           msg_sent=i.msg

        return JsonResponse({"sent":msg_sent,'rp':rp},status=200)
    
    return render(request,"student/feedback.html",{'ms':msa})
def sent_sms(request):
    if request.method=="POST":
            msg=request.POST.get('msg',False)
            sender=request.user

            dep=Student.objects.get(user_id=sender.id)
            dp=dep.dep
            user=User.objects.get(username=sender)
            pend="pending"
            ms=Sms_feedback.objects.create(sender=sender.id,msg=msg,dep=dp,status=pend,fname=sender.first_name,lname=sender.last_name)
            ms.rec.add(user)
            ms.save()
            messages.success(request,"message sent")
            return redirect('student:ask_for_help')
class VideoCamera(object):
    id=""
    name=""
    course=""
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
        self.GET, self.POST, self.COOKIES, self.META,self.FILES = {}, {}, {}, {}, {}
        

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
        
    
        
    def update(self):
        static_back = None
        motion_list = [ None, None ]
        time = []
        df = pandas.DataFrame(columns = ["Start", "End"])
        while True:
            (self.grabbed, self.frame) = self.video.read()
            motion = 0
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            if static_back is None:
                static_back = gray
                continue
            diff_frame = cv2.absdiff(static_back, gray)
            thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
            thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
            cnts,_ = cv2.findContours(thresh_frame.copy(), 
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in cnts:
                if cv2.contourArea(contour) < 10000:
                    continue
                motion += 1
              
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            motion_list.append(motion)
  
            motion_list = motion_list[-2:]
            if motion_list[-1] == 1 and motion_list[-2] == 0:
              time.append(datetime.now())
              
            st=Student.objects.get(user=self.name)
            dep=Departiment.objects.get(id=st.dep)
            cr=Course.objects.get(dp_id=dep.id,pre=1)
            course=cr.id
            if motion_list[-1] == 0 and motion_list[-2] == 1:
               time.append(datetime.now())
               mn=0
               if motion >= 3:
                         mn+=1
                         
                         ex=SModel.Exam_control(
                           name=self.name,
                           user_id=User.objects.get(pk=self.id),
                           mot_count=motion,
                           tyme=mn,
                           exam=course,
                       )
                         ex.save()
                    
                       
            

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livestram(request):
    
    try:
      cam = VideoCamera()
      cam.id=request.user.id
      st=Student.objects.get(user=request.user)
      dep=Departiment.objects.get(id=st.dep)
      cr=Course.objects.get(dp_id=dep.id)
      cam.name=request.user
      cam.course=cr.id
      #cam.course= request.session['c_id']
      
      return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except: 
        pass
class LiveControl(object):
    id=""
    name=""
    course=""
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.updat, args=()).start()
        
        
    

    def __del__(self):
        self.video.release()

    def get_fram(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def updat(self):
       
       
        
       
       
       
        weight=os.path.abspath(os.getcwd()) +'\static\yolo\yolov3 .weights'
        
        config=os.path.abspath(os.getcwd()) +'\static\yolo\yolov3.cfg'
      
        
        net = cv2.dnn.readNet(weight, config)
        classes = []
        with open(os.path.abspath(os.getcwd()) +'\static\yolo\coco.names', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        outputlayers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        while True:
            (self.grabbed, self.frame) = self.video.read()
            
            
            
            img = cv2.resize(self.frame, None, fx=0.2, fy=0.2)
            height, width, channels = img.shape
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(outputlayers)
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            #print(indexes)
            font = cv2.FONT_HERSHEY_PLAIN
            st=Student.objects.get(user=self.name)
            dep=Departiment.objects.get(id=st.dep)
            cr=Course.objects.get(dp_id=dep.id,pre=1)
            course=cr.id
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    color = colors[class_ids[i]]
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
                    
                    nm=0
                    if label=="laptop" or label=="cell phone" or label=="book" or label=="clock" or label=="remote":
                         
                         ex=SModel.Exam_control(
                           name=self.name,
                           user_id=User.objects.get(pk=self.id),
                           material=label,
                           tyme=nm,
                           exam=course,
                       )
                         ex.save()
                        
                         print(label)                
                    
                    
            

def gena(camera):
    while True:
        frame = camera.get_fram()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def cheating(request):
    
    try:
        cam = LiveControl()
        cam.id=request.user.id
       
        cam.name=request.user
        
        #cam.course= request.session['c_id']
        return StreamingHttpResponse(gena(cam), content_type="multipart/x-mixed-replace;boundary=frame")
      
    except: 
        pass
def sms_delete(request,id):
    sn=Sms_feedback.objects.get(id=id)
    sn.delete()
    messages.warning(request,"removed successfully")
    return redirect('student:ask_for_help')
class VideoCamere(object):
    id=""
    name=""
    course=""
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_framea(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        static_back = None
        motion_list = [ None, None ]
        time = []
        df = pandas.DataFrame(columns = ["Start", "End"])
      
       
        
        while True:
            (self.grabbed, self.frame) = self.video.read()
            motion = 0
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            if static_back is None:
                static_back = gray
                continue
            diff_frame = cv2.absdiff(static_back, gray)
            thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
            thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
            cnts,_ = cv2.findContours(thresh_frame.copy(), 
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            st=Student.objects.get(user=self.name)
            dep=Departiment.objects.get(id=st.dep)
            cr=Course.objects.get(dp_id=dep.id)
            course=cr.id
            for contour in cnts:
                if cv2.contourArea(contour) < 10000:
                    continue
                motion += 1
              
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            motion_list.append(motion)
  
            motion_list = motion_list[-2:]
            if motion_list[-1] == 1 and motion_list[-2] == 0:
              time.append(datetime.now())
              
              
            if motion_list[-1] == 0 and motion_list[-2] == 1:
               time.append(datetime.now())
               mn=0
               if motion >= 3:
                         mn+=1
                         ex=SModel.Exam_control(
                           name=self.name,
                           user_id=User.objects.get(pk=self.id),
                           mot_count=motion,
                           tyme=mn,
                           exam=course,
                       )
                         ex.save()
                    
           

def gen(camera):
    while True:
        frame = camera.get_framea()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livestraminga(request):
    try:
        cam = VideoCamere()
        cam.id=request.user.id
       
        cam.name=request.user
       
       
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass
def vdostremin(request):
    return render(request,"student/livest.html")

