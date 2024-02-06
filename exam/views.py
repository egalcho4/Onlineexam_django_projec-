from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User
from exam.models import Course,Collage,Departiment,Permision
from .forms import Departiment as depart
from django.contrib import messages
from student.models import Student
import csv,io
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView

class LoginFormView(SuccessMessageMixin, LoginView):
    template_name = 'exam/login.html'
    success_url = '/profile'
    success_message = "You were successfully logged in"
    
def home_view(request):
    if request.user.is_authenticated:
        messages.success(request,"loged in soccessfully")
        return HttpResponseRedirect('afterlogin') 
    else:
        messages.error(request,"please chacke your username or password")
        
    return render(request,'exam/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
                
    elif is_teacher(request.user):
        accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('depart/teacher-dashboard')
        else:
            return render(request,'teacher/teacher_wait_for_approval.html')
    else:
        return redirect('exam:admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    'collage':models.Collage.objects.all().count(),
    'departiment':models.Departiment.objects.all().count(),
    }
    return render(request,'exam/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    'salary':TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'exam/admin_teacher.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
    
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            messages.success(request,"teacher updated successfully")
            return redirect('admin-view-teacher')
    return render(request,'exam/update_teacher.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    messages.success(request,"teacher successfully")
    return HttpResponseRedirect('/admin-view-teacher')




@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'exam/admin_view_pending_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def approve_teacher_view(request,pk):
    teacherSalary=forms.TeacherSalaryForm()
    if request.method=='POST':
        teacherSalary=forms.TeacherSalaryForm(request.POST)
        if teacherSalary.is_valid():
           
            dep=request.POST.get('dep',False)
            teacher=TMODEL.Teacher.objects.get(id=pk)
            teacher.salary=teacherSalary.cleaned_data['salary']
           
            teacher.depart=dep
            teacher.status=True
            teacher.save()
            messages.success(request,"teacher approved created successfully")
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-teacher')
    depart=models.Departiment.objects.all()
    course=Course.objects.all()
    return render(request,'exam/salary_form.html',{'teacherSalary':teacherSalary,'course':course,'depart':depart})

@login_required(login_url='adminlogin')
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    messages.success(request,"teacher rejected successfully")
    return HttpResponseRedirect('/admin-view-pending-teacher')

@login_required(login_url='adminlogin')
def admin_view_teacher_salary_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher_salary.html',{'teachers':teachers})




@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'exam/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student.html',{'students':students})
def add_student_info(request,id):
    username=request.user
    request.session['stid']=id
    depid=0
    try:
       depid=request.session['depart_id']
    except:
        depid=id

    dep=User.objects.get(username=username)
    
    #techer=TMODEL.Teacher.objects.get(user_id=dep.pk)
    student= SMODEL.Student.objects.filter(dep=depid,sem=id)
    userForm=SFORM.StudentUserForm()
    studentForm=SFORM.StudentForm()
   
    mydict={'userForm':userForm,'studentForm':studentForm,'students':student,'id':id}
    if request.method=='POST':
        
        t_dep=User.objects.get(username=username)
        userForm=SFORM.StudentUserForm(request.POST)
        studentForm=SFORM.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            passw=User.objects.make_random_password()
            user.set_password(passw)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.regby=dep.id
            student.dep=depid
            student.save()
            dep=Departiment.objects.get(id=depid)
            _,pas=models.Password_manager.objects.update_or_create(
               fname=user.first_name,
               last=user.last_name,
               username=user.username,
               pasword=passw,
               depa=dep.name
               
              
          )
            messages.success(request,"student added successfully")
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
    
    return render(request,"exam/add_student_info.html",context=mydict)


@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            passw=User.objects.make_random_password()
            user.set_password(passw)
            user.save()
            username=userForm.cleaned_data['username']
            last_name=userForm.cleaned_data['last_name']
            first_name=userForm.cleaned_data['first_name']
            print(first_name)
            studentForm.save()
            pas=models.Password_manager.objects.get(username=username)
            pas.fname=first_name
            pas.last=last_name
            pas.username=username
            pas.pasword=passw
            pas.save()
            messages.success(request,"student updated successfully")
            username=request.user.username
    
            dep=User.objects.get(username=username)
            
            #techer=TMODEL.Teacher.objects.get(user_id=dep.pk)
            student= SMODEL.Student.objects.filter(dep=student.dep)
            userForm=SFORM.StudentUserForm()
            studentForm=SFORM.StudentForm()
            mydict={'students':student}
            return render(request,"exam/add_student_info.html",context=mydict)
    return render(request,'exam/update_student.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_student_view(request,id):
    username=request.user.username
    ida=request.session['stid']
    dep=User.objects.get(username=username)
    
    #techer=TMODEL.Teacher.objects.get(user_id=dep.pk)
    student= SMODEL.Student.objects.filter(dep=ida)
    userForm=SFORM.StudentUserForm()
    studentForm=SFORM.StudentForm()
    order="pleas make the csv file in the  order of first_name,last_name,username,address,sid"
    mydict={'userForm':userForm,'studentForm':studentForm,'students':student,'id':id,'order':order}
    student=SMODEL.Student.objects.get(id=id)
    user=User.objects.get(id=student.user_id)
   
    user.delete()
    
    student.delete()
    
    messages.success(request,"student deleted successfully")
    return render(request,"exam/add_student_info.html",context=mydict)
    #return HttpResponseRedirect('exam:delete_student_view')


@login_required(login_url='adminlogin')
def admin_course_view(request,id):
    course=Course.objects.filter(dp_id=id)
    if request.method=="POST":
        try:
            course_name=request.POST.get('course',False)
            total_mark=request.POST.get('total_marks',False)
            sem=request.POST.get('sem',False)
            question=request.POST.get('question',False)
            code=request.POST.get('code',False)
            db=Departiment.objects.get(id=id)
            dep=db.pk
            course=Course.objects.create(dp=db,question_number=question,c_code=code,course_name=course_name,total_marks=total_mark,sem=sem)
            course.save()
            qd=Course.objects.get(course_name=course_name)
            dat="2023-03-19"
            time="11:17"
            dur=120
            dpe_id=Departiment.objects.get(id=id)
            qd.dp=dpe_id
            qd.save()
            sc=TMODEL.Schedule(dat=dat,tim=time,dur=dur,adby=id,exam= qd.id)
            sc.save()
            messages.success(request,"course created successfully")
            course=Course.objects.filter(dp_id=id)
            return render(request,'exam/admin_course.html',{'courses':course})
        except:
            messages.error(request,"samething want wrong")
    return render(request,'exam/admin_course.html',{'courses':course})


@login_required(login_url='adminlogin')
def admin_add_course_view(request):

    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
            c_c=courseForm.cleaned_data['c_code']
            c_name=courseForm.cleaned_data['course_name']
            qd=Course.objects.get(course_name=c_name)
            dat="2023-03-19"
            time="11:17"
            dur=120
            dpe_id=Departiment.objects.get(id=depart.depart)
            qd.dp=dpe_id
            qd.save()
            sc=TMODEL.Schedule(dat=dat,tim=time,dur=dur,adby=dp_id,exam= qd.id)
            sc.save()
            messages.success(request,"course created successfully")
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'exam/admin_add_course.html',{'courseForm':courseForm})


@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'exam/admin_view_course.html',{'courses':courses})

@login_required(login_url='adminlogin')
def delete_course_view(request,pk):
    course=models.Course.objects.get(id=pk)
    ida=course.dp
    dep=Departiment.objects.get(name=ida)
    course.delete()
    messages.success(request,"course deleted successfully")
    course=Course.objects.filter(dp_id=dep.pk)
    return render(request,'exam/admin_course.html',{'courses':course})


@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'exam/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request,id):
    questions=models.Question.objects.all().filter(adby=request.user.id,course_id=id)
    if request.method=='POST' :
        try:
            course=request.POST.get('course',False)
            question=request.POST.get('question',False)
            option1=request.POST.get('option1',False)
            option2=request.POST.get('option2',False)
            option3=request.POST.get('option3',False)
            option4=request.POST.get('option4',False)
            answer=request.POST.get('answer',False)
            mark=request.POST.get('mark',False)
            dep=request.POST.get('id',False)
            cv=Course.objects.get(id=id)
            """ username=request.session['username']
            t_dep=User.objects.get(username=username)"""
            cv=Course.objects.get(id=id)
            dep=Departiment.objects.get(name=cv.dp)
            
            
            t_dep=User.objects.get(id=request.user.id)
            img="2"
            qtn=models.Question(image=img,adby=t_dep,marks=mark,course=cv,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,dep=dep.id)
            qtn.save()
            messages.success(request,"question created successfully")
        except:
             messages.error(request,"please check your input")
   
    
    

        """if request.method=='POST':
            course=request.POST.get('course',False)
            question=request.POST.get('question',False)
            option1=request.POST.get('option1',False)
            option2=request.POST.get('option2',False)
            option3=request.POST.get('option3',False)
            option4=request.POST.get('option4',False)
            answer=request.POST.get('answer',False)
            mark=request.POST.get('mark',False)
            
            cv=Course.objects.get(id=id)
            
            t_dep=User.objects.get(id=request.user.id)
            qtn=models.Question(adby=t_dep,marks=mark,course=cv,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer)
            qtn.save()
            print("form is invalid")"""
      
        return render(request,'exam/admin_add_question.html',{'questions':questions})
    return render(request,'exam/admin_add_question.html',{'questions':questions})
def qedit(request,id):
    if request.method=='POST'  and request.FILES['image']:
        myfile = request.FILES.get('image',False)
        try:
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
            
            t_dep=User.objects.get(username=request.user)
            qtn=models.Question.objects.get(id=id)
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
        except:
            messages.error(request,"please check your input")
        
    
    qu=models.Question.objects.get(id=id)
    
   
    
    dp_id=qu.dep
    t_course=qu.course
    cours=models.Course.objects.get(course_name=t_course)
    course=cours.id
    course_name=cours.course_name
    
    questions=models.Question.objects.filter(id=id)
    student=models.Result.objects.filter(exam_id=course)
    #if request.method=='POST':
    #    pass
    #response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    #response.set_cookie('course_id',course.id)
    qtn=models.Question.objects.get(id=id)
    return render(request,'exam/upp_add_question.html',{'qtn':qtn,'exam':student,'username':dp_id,'course':course,'questions':questions,'course_name':course_name})

@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'exam/admin_view_question.html',{'courses':courses})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=models.Question.objects.filter(course_id=pk)
    return render(request,'exam/view_question.html',{'questions':questions})
def add_question_admin(request,id):
    if request.method=='POST' :
        #myfile = request.FILES.get('image',False)
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
        img="2"
        typ=0
        qtn=models.Question(typ=typ,image=img,adby=t_dep,marks=mark,course=cv,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,dep=dep)
        qtn.save()
        messages.success(request,"question created successfully")
    
        return redirect('teacher:teacher-add-question')
    cours=Course.objects.get(id=id)
    course=cours.id
    course_name=cours.course_name
    cour=models.Course.objects.get(id=course)
    questions=models.Question.objects.all().filter(course=cour)
    questions=models.Question.objects.filter(course_id=id)
    return render(request,"exam/admin_add_question.html",{'questions':questions,'course':course,'course_name':course_name})






def teacher_add_question_view(request):
   
    if request.method=='POST' :
        #myfile = request.FILES.get('image',False)
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
        img="2"
        typ=0
        qtn=models.Question(typ=typ,image=img,adby=t_dep,marks=mark,course=cv,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,dep=dep)
        qtn.save()
        messages.success(request,"question created successfully")
    
        return redirect('teacher:teacher-add-question')
    
        #return HttpResponseRedirect('/teacher/teacher-view-question')
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    depart=t_dep.pk
    dep=models.Teacher.objects.get(user_id=depart)
    dp_id=dep.depart
    t_course=dep.course
    cours=Course.objects.get(id=t_course)
    course=cours.id
    course_name=cours.course_name
    cour=models.Course.objects.get(id=course)
    questions=models.Question.objects.all().filter(course=cour)
    student=models.Result.objects.filter(exam_id=course)
    #if request.method=='POST':
    #    pass
    #response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    #response.set_cookie('course_id',course.id)
    teach=models.Teacher.objects.get(user_id=request.user.id)
    return render(request,'teacher/add_question.html',{'usertype':teach.type,'exam':student,'username':dp_id,'course':course,'questions':questions,'course_name':course_name})
def blanck_question(request):
     if request.method=="POST":
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
        dep=request.POST.get('id',False)
        exp=request.POST.get('exp',False)

        
        cv=Course.objects.get(id=course)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
        ans=answer.split(",")
        print(ans)
        img="2"
        typ=1
        qtn=models.Question(typ=typ,image=img,adby=t_dep,marks=mark,course=cv,question=question,answer=answer,dep=dep,dran=ans,exp=exp)
        qtn.save()
        messages.success(request,"question created successfully")
    
     return redirect('exam:add_question_admin')
def short_question(request):
    if request.method=="POST":
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
        exp=request.POST.get('exp',False)
        dep=request.POST.get('id',False)
        cv=Course.objects.get(id=course)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
        ans=answer.split(",")
        print(ans)
        img="2"
        typ=2
        qtn=models.Question(typ=typ,image=img,adby=t_dep,marks=mark,course=cv,question=question,answer=answer,dep=dep,dran=ans,exp=exp)
        qtn.save()
        messages.success(request,"question created successfully")
    
    return redirect('exam:add_question_admin')
def true_false_question(request):
    if request.method=="POST":
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
        
        dep=request.POST.get('id',False)
        cv=Course.objects.get(id=course)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
        option1="True"
        option2="False"
        img="2"
        typ=3
        qtn=models.Question(typ=typ,image=img,adby=t_dep,marks=mark,course=cv,question=question,answer=answer,dep=dep, option1= option1, option2= option2)
        qtn.save()
        messages.success(request,"question created successfully")
    
    return redirect('teacher:teacher-add-question')
def paragraph(request):
    if request.method=="POST":
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
        
        dep=request.POST.get('id',False)
        cv=Course.objects.get(id=course)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        mark=request.POST.get('mark',False)
       
        
        img="2"
        typ=4
        qtn=models.Question(typ=typ,image=img,adby=t_dep,course=cv,question=question,dep=dep,marks=mark)
        qtn.save()
        messages.success(request,"question created successfully")
    
    return redirect('teacher:teacher-add-question')


@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
   
    question.delete()
    messages.success(request,"question deleted successfully")
    return redirect('exam:admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student_marks.html',{'students':students})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'exam/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'exam/admin_check_marks.html',{'results':results,'course':course})
    




def aboutus_view(request):
    return render(request,'exam/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'exam/contactussuccess.html')
    return render(request, 'exam/contactus.html', {'form':sub})
def register_depart(request,id):
    
    if request.method=='POST':
       depart_name=request.POST.get('depart',False)
       descr=request.POST.get('descr',False)
       colage=Collage.objects.get(id=id)
       try:
            dep_create=models.Departiment.objects.create(name=depart_name,adby=request.user.id,cl_name=colage)
            dep_create.save()
            messages.success(request,"departiment created successfully")
       except:
             messages.error(request,"departiment already exist ")
       courses = models.Departiment.objects.filter(cl_name=id)
       return render(request,'exam/register_depart.html',{'id':id,'courses':courses})
    courses = models.Departiment.objects.filter(cl_name=id)
    return render(request,'exam/register_depart.html',{'id':id,'courses':courses})
def admin_view_departiment(request):
    if request.method=='POST':
       depart_name=request.POST.get('depart',False)
       cl=request.POST.get('cl',False)
       colage=Collage.objects.get(id=cl)
       try:
            dep_create=models.Departiment.objects.create(name=depart_name,adby=request.user.id,cl_name=colage)
            dep_create.save()
            messages.success(request,"departiment created successfully")
       except:
            messages.error(request,"departiment already exist")
    courses = models.Departiment.objects.all()
    collage=models.Collage.objects.all()
    return render(request,'exam/admin_view_departiment.html',{'courses':courses,"colage":collage})
def head(request,id):
     tch=TMODEL.Teacher.objects.filter(depart=id)
     request.session['depid']=id
     return render(request,"exam/teacher_list.html",{'tch':tch})
def assgin_teacher(request,id):
    t= TMODEL.Teacher.objects.get(id=id)
    t.type=1
    ida=request.session['depid']
    dep=models.Departiment.objects.get(id=ida)
    dep.head=id
    t.save()
    dep.save()
    messages.success(request,"teacher assigned successfully")
    return redirect('exam:admin_view_departiment')
def register_collage(request):
    if request.method=="POST":
        name=request.POST.get('collage',False)
        descr=request.POST.get('descr',False)
        try:
            cl=Collage(name=name,descr=descr)
            cl.save()
            messages.success(request,"collage created successfully")
        except:
            messages.error(request,"collage already exist")

        return redirect('exam:register_collage')
    colage=Collage.objects.filter()
    return render(request,"exam/register_collage.html",{'cl':colage})
def colage_edit(request,id):
    colage=Collage.objects.get(id=id)
    if request.method=="POST":
        name=request.POST.get('collage',False)
        descr=request.POST.get('descr',False)
        colage.name=name
        colage.descr=descr
        colage.save()
        messages.success(request,"collage updated successfully")
        return redirect('exam:register_collage')
    return render(request,"exam/colage_update.html",{'colage':colage})
def edit_departiment(request,id):
    colage=Departiment.objects.get(id=id)
    if request.method=="POST":
        name=request.POST.get('depart',False)
        descr=request.POST.get('descr',False)
        colage.name=name
        colage.descr=descr
        colage.save()
        messages.success(request,"collage updated successfully")
        return redirect('exam:register_collage')
    return render(request,"exam/depart_update.html",{'col':colage})
def permistion(request):
     if request.method=="POST":
        perm=request.POST.get('perm',False)
        type=request.POST.get('type',False)
        cl=Permision.objects.get(name=perm)
        cl.name=perm
        cl.perm=type
        cl.save()
        
        return redirect('exam:permistion')
     clas=Permision.objects.filter()
     return render(request,"exam/permision.html",{'cl':clas})
def first_exam(request,id):
    cour=Course.objects.get(id=id)
    cour.pre=1
    cour.save()
    messages.success(request,"scheduled successfully")
    return render(request,'exam/admin_course.html')
def add_student(request):
    courses = models.Departiment.objects.all()
    return render(request,'exam/add_student.html',{'courses':courses})

def view_student_marks(request):
    courses = models.Departiment.objects.all()
    return render(request,"exam/view_student_marks.html",{'courses':courses})
def student_marks(request,id):
    courses = models.Result.objects.filter(exam_id=id)
    return render(request,"exam/tudent_marks.html",{'courses':courses})
def livestreaming(request,id):
    request.session['dp']=id
    St=SMODEL.Student.objects.filter(dep=id)
    return render(request,"exam/livestreaming.html",{'st':St})
def sendmessage(request):
    if request.method=="POST":
        id=request.POST.get('id',False)
        msg=request.POST.get('msg',False)
        snder=User.objects.get(username=request.user)
        st=SMODEL.Student.objects.get(id=id)
        ms=SMODEL.Message(sender=st,dep=st.dep,depsend=msg,receiver=id)
        ms.save()
        messages.success(request,"message sent  successfully")
    id=request.session['dp']
    St=SMODEL.Student.objects.filter(dep=id)
    return render(request,"exam/livestreaming.html",{'st':St})
    
def settingsa(request):
    if request.method=="POST":
        cam=request.POST.get('camera',False)
        ex=request.POST.get('ex',False)
        reg=request.POST.get('reg',False)
        lv=request.POST.get('lv',False)
        cl=Permision.objects.get(name="camera")
        cl.name="camera"
        cl.perm=cam
        cl.save()
        cle=Permision.objects.get(name="exam")
        cle.name="exam"
        cle.perm=ex
        cle.save()
        clr=Permision.objects.get(name="registration")
        clr.name="registration"
        clr.perm=reg
        clr.save()
        liv=Permision.objects.get(name="livestream")
        liv.name="livestream"
        liv.perm=lv
        liv.save()
        messages.success(request," settings saved successfully")
    came=Permision.objects.get(name="camera")
    ex=Permision.objects.get(name="exam")
    reg=Permision.objects.get(name="registration")
    livestream=Permision.objects.get(name="livestream")
    return render(request,"exam/setting.html",{'came':came,'exam':ex,'reg':reg,'live':livestream})
def enable_student(request,id):
    st=Student.objects.get(id=id)
    st.ex_status=1
    st.save()
    messages.success(request,"exam enabled  successfully")
    return redirect('exam:add_student')
def disable_student(request,id):
    st=Student.objects.get(id=id)
    st.ex_status=2
    st.save()
    messages.success(request,"blocked successfully")
    return redirect('exam:add_student')
def departdel(request,id):
    dep=Departiment.objects.get(id=id)
    dep.delete()
    messages.success(request,"departiment deleted  successfully")
    return redirect('exam:admin_view_departiment')
@permission_required('admin.can_add_log_entry')
def uploadscv(request):
    template="exam/add_student_info.html"
    contex={
        "order":"pleas make the csv file in the  order of first_name,last_name,username,address,sid"
    }
    if request.method=="POST":
        file=request.FILES['file']
        id=request.POST.get('id',False)
        if not file.name.endswith('.csv'):
            messages.error(request,"this file is not csv file")
        file_encode=file.read().decode('UTF-8')
        string_file=io.StringIO(file_encode)
        next(string_file)
        for column in csv.reader(string_file,delimiter=',',escapechar="|"):
           pasw=User.objects.make_random_password()
           _,user=User.objects.update_or_create(
               first_name=column[0],
               last_name=column[1],
               username=column[2],
               
              
           )
           us_pas=User.objects.get(username=column[2])
           us_pas.set_password(pasw)
           us_pas.save()
           dep=Departiment.objects.get(name=column[3])
           _,pas=models.Password_manager.objects.update_or_create(
               fname=column[0],
               last=column[1],
               username=column[2],
               pasword=pasw,
              depa=column[3],
              sem=column[4]
              
          )
          
           _,student=SMODEL.Student.objects.update_or_create(
               user=User.objects.get(username=column[2]),
               fname=column[0],
               dep=dep.id,
               sem=column[4]
              
           )
        username=request.user.username
        
        dep=User.objects.get(username=username)
        
        #techer=TMODEL.Teacher.objects.get(user_id=dep.pk)
        student= SMODEL.Student.objects.filter(dep=id)
        userForm=SFORM.StudentUserForm()
        studentForm=SFORM.StudentForm()
        mydict={'userForm':userForm,'studentForm':studentForm,'students':student,'id':id}
        return render(request,"exam/add_student_info.html",context=mydict)
def delet_studentsm(request,id):
        st=SMODEL.Student.objects.get(id=id)
        id=st.dep
        st.delete()
        username=request.user.username
        
        dep=User.objects.get(username=username)
        
        #techer=TMODEL.Teacher.objects.get(user_id=dep.pk)
        student= SMODEL.Student.objects.filter(dep=id)
        userForm=SFORM.StudentUserForm()
        studentForm=SFORM.StudentForm()
        mydict={'userForm':userForm,'studentForm':studentForm,'students':student,'id':id}
        return render(request,"exam/add_student_info.html",context=mydict)
def markdelete(request,id):
    rs=models.Result.objects.get(id=id)
    rs.delete()
    return redirect('exam:view_student_marks')
def search_password(request):
    courses = models.Departiment.objects.all()
    collage=models.Collage.objects.all()
    return render(request,'exam/search_student.html',{'courses':courses,"colage":collage})
    
def depart_password(request,id):
    dep=Departiment.objects.get(id=id)
    ps_manager=models.Password_manager.objects.filter(depa=dep.name)  
    return render(request,"exam/stude_password.html",{'pas':ps_manager})
@permission_required('admin.can_add_log_entry')
def uploadscvad(request):
    template="exam/add_student_info.html"
    contex={
        "order":"pleas make the csv file in the  order of first_name,last_name,username,address,sid"
    }
    if request.method=="POST":
        file=request.FILES['file']
        id=request.POST.get('id',False)
        if not file.name.endswith('.csv'):
            messages.error(request,"this file is not csv file")
        file_encode=file.read().decode('UTF-8')
        string_file=io.StringIO(file_encode)
        next(string_file)
        for column in csv.reader(string_file,delimiter=',',escapechar="|"):
           pasw=User.objects.make_random_password()
           _,user=User.objects.update_or_create(
               first_name=column[0],
               last_name=column[1],
               username=column[2],
               
              
           )
           us_pas=User.objects.get(username=column[2])
           us_pas.set_password(pasw)
           us_pas.save()
           dep=Departiment.objects.get(name=column[3])
           _,pas=models.Password_manager.objects.update_or_create(
               fname=column[0],
               last=column[1],
               username=column[2],
               pasword=pasw,
              depa=column[3],
              sem=column[4]
              
          )
          
           _,student=SMODEL.Student.objects.update_or_create(
               user=User.objects.get(username=column[2]),
               fname=column[0],
               dep=dep.id,
               sem=column[4]
              
           )
        messages.success(request,"student created succefully")
        return redirect('exam:uploadscvad')
    courses = models.Departiment.objects.all()
    return render(request,'exam/add_student.html',{'courses':courses})
def psforgot(request):
    if request.method=='POST':
      
       
       try:
            em=request.POST['email']
            rg=User.objects.get(email=em)
            token=uuid.uuid4()
            rg.token=token
            rg.save()
            
            if rg is not None:
                rg=User.objects.get(token=token)
                subject = 'please change your password by using belloW link from jinka university registerar'
                message = f'Hi {rg.first_name } {rg.last_name}, please use this link to change your password.http://127.0.0.1:8000/forgot/{token}/'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [em, ]
                send_mail( subject, message, email_from, recipient_list )
                messages.success(request,f'email successfully sent to {em},please check it')
                return render(request,'exam/forgot.html',{})
       except:
           
           messages.success(request,'email deas not exist in our database please enter existing one')

           
    return render(request,'exam/forgot.html',{})
def forgot(request,token):
    user=User.objects.get(token=token)
    if request.method=="POST":
        pas1=request.POST.get('pas1',False)
        pas2=request.POST.get('pas2',False)
        if pas1==pas2:
            user.set_password(pas1)
            user.save()
            messages.success(request,"your password changed successfully now go to login page")
        else:
            messages.success(request,"password note match")
            

    return render(request,"exam/forgotpas.html")  
def start_all_exam(request):
    course=Course.objects.filter(pre="1")
    return render(request,"exam/start_all_exam.html",{"course":course})
def start_now(request,id):
    cour=Course.objects.get(id=id)
    cour.start=1
    cour.save()
    messages.success(request,"exam started now")
    return redirect("exam:start_all_exam")
def stop_now(request,id):
    cour=Course.objects.get(id=id)
    cour.start=0
    cour.save()
    messages.success(request,"exam stoped now")
    return redirect("exam:start_all_exam")
def depart_mark_views(request):
    courses = models.Departiment.objects.all()
    collage=models.Collage.objects.all()
    #return render(request,'exam/admin_view_departiment.html',{'courses':courses,"colage":collage})
    return render(request,"exam/depert_mark_views.html",{'courses':courses,"colage":collage})
def all_course(request,id):
    courses=models.Course.objects.filter(dp_id=id)
    
    return render(request,"exam/all_course.html",{'courses':courses})

def student_marks(request,id):
    user=request.user.id
    
    
    courses=models.Course.objects.filter(id=id)
   
    

    return render(request,"exam/student_marks.html",{'courses':courses})
def student_mark_report(request,id):
    user=request.user.id
   
    courses = models.Result.objects.filter(exam=id).order_by("-perc")
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





    
    total_questions=models.Question.objects.filter(course_id=id).count()
   
    
    return render(request,"exam/student_mark_report.html",{'courses':courses,'total':total_questions,'above_seven':above_sevent,'above_fift':above_five,'below_fift':bellow_fift})

def add_year(request,id):
    form=TFORM.YearADD()
    #yer=models.Year_now.objects.all()
    request.session['depart_id']=id
    if request.method=="POST":
        form=TFORM.YearADD(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"year successfully added")
    ye=models.Year_now.objects.filter(dep_id=id)
    return render(request,"exam/add_year.html",{'form':form,'ye':ye})
def general_report(request):
     dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    'collage':models.Collage.objects.all().count(),
    'departiment':models.Departiment.objects.all().count(),
    }
     return render(request,"exam/general_report.html",dict)

    
    
    
    
    
   
   
   




