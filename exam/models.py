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
    


