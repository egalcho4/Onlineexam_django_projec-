# Title smart online exam system
![sample image]([Screenshot_20230526-162647_1.jpg](https://photos.app.goo.gl/Ckx8ya6xoyfiZsZPA))

## Introduction 
Smart online examination system is developed by back end Django and front end JavaScript, html, css jQuery, bootstrap5.  Smart online examination system have advanced future than currently existing online examination system same of them listed bellow

- Detect object like book,phone,laptop,student motion
* Control window minimization 
+ Control new tab open and other software open
- Control more than one login per account at a time
* Block the computer to not allow other user login at same exam
+ Evaluate the blank question
- Evaluate short answer question 
* Show answer with fully explanation
+ It allow to start exam of  each student if accidental closed and reported by admin
This little functionality about smart online examination system
## Requirements

1	Python 3.97
2	PostgreSQL server 
3	Django
4	Opencv
5	Widget_tweeks

Above listed software are major requirement to run this project
You will get more about requirements on requirement.txt file
## Installation
To use this software first install python 3.97 on your system
Then create virtual environment like this
Clone this project
‘’’bash
Python –m venv virtual_environment_name
‘’’
Then activate virtual environment
And install requirement like this
‘’’bash
Pip install –r requirement.txt
‘’’
Then you have to download yolo weight  and put it in static/yolo folder inside the project
Aim sorry I can’t able to put yolo weight inside project b/c it has 273mg size and github not allow this much data

 - After then you have to couple of things 
* Incide camera table 
+ Insert same data
  
1 Livestream=0
2 Camera=0
3 Exam=0
4 E,t,c

Then all thing working fine

 Sample code 
```bash python
from django.db import models
from teacher.models import Teacher
from student.models import Student
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import uuid
token=models.CharField(max_length=255,null=True,unique=True)
token.contribute_to_class(User, 'token')

class Collage(models.Model):
    name=models.CharField(max_length=255,null=True,unique=True)
    descr=models.TextField(null=True)
    def __str__(self):
        return self.name

class Departiment(models.Model):
    name=models.CharField(max_length=255,null=True,unique=True)
    colage_name=models.CharField(max_length=255,null=True)
    adby=models.IntegerField(null=True)
    cl_name=models.ForeignKey(Collage,on_delete=models.CASCADE,null=True)
    head=models.IntegerField(null=True)
    def __str__(self):
        return self.name

class Course(models.Model):
   course_name = models.CharField(max_length=50,unique=True)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   dep=models.IntegerField(null=True)
   c_code=models.CharField(max_length=255,null=True,unique=True)
   year=models.IntegerField(null=True)
   sem=models.IntegerField(null=True)
   dp=models.ForeignKey(Departiment,on_delete=models.CASCADE,null=True)
   pre=models.IntegerField(default=0)
   start=models.IntegerField(default=0)
   answer=models.IntegerField(default=0)
   msg=models.TextField(null=True)
   lct=models.IntegerField(null=True)
   def __str__(self):
        return self.course_name

class Tables(models.Model):
    name=models.CharField(max_length=255,null=True)
    data1=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    data2=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    data3=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    data4=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    data5=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    data6=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    data7=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    data8=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    data9=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    data10=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    data11=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    data12=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    data13=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    def __str__(self):
        return self.name
    
class Test_hand(models.Model):
    name=models.CharField(max_length=255,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    tquest=models.IntegerField(null=True)
    tmark=models.IntegerField(null=True)
    pas=models.CharField(max_length=255,null=True)
    pr=models.IntegerField(null=True)
    def __str__(self):
        return self.name
class Assiment(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    exam=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    test=models.ForeignKey(Test_hand,on_delete=models.CASCADE,null=True)
    mark=models.IntegerField(null=True)
    m=models.IntegerField(null=True)
    total=models.IntegerField(null=True)

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','A'),('Option2','B'),('Option3','C'),('Option4','D'))
    answer=models.CharField(max_length=200,choices=cat)
    dep=models.IntegerField(null=True)
    adby=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    examid=models.IntegerField(null=True)
    image=models.ImageField(upload_to="question",null=True)
    dran=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    short=models.CharField(max_length=200,null=True)
    typ=models.IntegerField(default=0)
    exp=models.TextField(default="no explanetion")
    code=models.IntegerField(default=1)
    #table=models.ForeignKey(Table_data,on_delete=models.CASCADE,null=True)
    tabl=models.ForeignKey(Tables,on_delete=models.CASCADE,null=True)
    para=models.TextField(null=True)
    tes=models.ForeignKey(Test_hand,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.question
class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    dep=models.IntegerField(null=True)
    perc=models.IntegerField(null=True)
    tes=models.ForeignKey(Test_hand,on_delete=models.CASCADE,default=1,null=True)
   
   
    
class Permision(models.Model):
      name=models.CharField(max_length=255,null=True)
      perm=models.CharField(max_length=255,null=True)
      def __str__(self):
          return self.name
class Password_manager(models.Model):
    fname=models.CharField(max_length=255,null=True)
    last=models.CharField(max_length=255,null=True)
    sid=models.CharField(max_length=255,null=True)
    username=models.CharField(max_length=255,null=True)
    pasword=models.CharField(max_length=255,null=True)
    dep=models.IntegerField(null=True)
    sem=models.IntegerField(null=True)
    depa=models.CharField(max_length=255,null=True)
    def __str__(self):
        return self.fname+""+self.last
class Year_now(models.Model):
    year=models.CharField(max_length=255,null=True)
    sem=models.IntegerField(null=True)
    tot=models.IntegerField(null=True)
    dep=models.ForeignKey(Departiment,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.year+" "+str(self.sem)
    



```
##

## Acknowledgement
First of all I need to thanks God Who helps me allot to accomplish this project within time and then I would like to thank you jinka university they help me to by giving all requirement on time  ,final I would to thank you my friends and family they are side of me for every situation
##About repository
This repository was created at the finally stage after first repository failed to not updated file and you may not get the commit history for this project sorry for this
## About Me

- My name is Elias Galcho
* I have BSc in computer science
  
## License
[MIT](https://choosealicense.com/licenses/mit/)














