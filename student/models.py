from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from exam.models import Teacher

gen={("male","male"),("female","female"),("costom","costome")}
class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    dep=models.IntegerField(null=True)
    regby=models.IntegerField(null=True)
    ex_status=models.IntegerField(default=0)
    sid=models.CharField(max_length=255,null=True)
    password=models.CharField(max_length=255,null=True)
    fname=models.CharField(max_length=255,null=True)
    lname=models.CharField(max_length=255,null=True)
    motion=models.IntegerField(default=0)
    obj=models.CharField(max_length=255,null=True)
    insession = models.BooleanField(default=True)
    gender=models.CharField(max_length=255,choices=gen,null=True)
    gen=models.CharField(max_length=255,choices=gen,null=True)
    sem=models.IntegerField(null=True)
    urlf=models.URLField(max_length=1000,null=True)
    exam_code=models.IntegerField(default=1)
    def __str__(self):
        return  self.user.first_name+" "+self.user.last_name
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
class Message(models.Model):
    sender=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    dep=models.IntegerField(null=True)
    message=models.TextField(null=True)
    replay=models.TextField(null=True)
    pending=models.CharField(max_length=255,null=True)
    depsend=models.TextField(null=True)
    receiver=models.IntegerField(null=True)
    messega=models.ManyToManyField(Teacher)
    def __str__(self):
          return self.depsend or self.message
class Exam_control(models.Model):
      name=models.CharField(max_length=255,null=True)
      user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
      motion=models.CharField(max_length=255,null=True)
      mot_count=models.IntegerField(default=0)
      material=models.CharField(max_length=255,null=True)
      exam=models.IntegerField(null=True)
      dat=models.DateTimeField(auto_now=True)
      tyme=models.IntegerField(null=True)
      def __str__(self):
          return self.name
class Report(models.Model):
    name=models.CharField(max_length=255,null=True)
    
    mot_count=models.IntegerField(null=True)
    material=models.CharField(max_length=255,null=True)
    user=models.IntegerField(null=True)
    def __str__(self):
          return self.name
class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Answer(models.Model):
    exam=models.IntegerField(null=True)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    answer=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    real=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    dran=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    lanswer=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    lreal=ArrayField(models.CharField(max_length=200), blank=True,null=True)
    typ=models.IntegerField(default=0)
    tes=models.IntegerField(null=True,default=1)

class Sms_feedback(models.Model):
    sender=models.IntegerField(null=True)
    fname=models.CharField(max_length=255,null=True)
    lname=models.CharField(max_length=255,null=True)
    rec=models.ManyToManyField(User)
    msg=models.TextField(null=True)
    replay=models.TextField(null=True)
    dep=models.IntegerField(null=True)
    status=models.CharField(max_length=255,null=True)
    seen=models.IntegerField(default=0)
    dt=models.DateTimeField(auto_now=True)
class Ip_adress(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    ip=models.CharField(max_length=222,null=True,unique=True)
    host=models.CharField(max_length=255,null=True)
    dep=models.IntegerField(null=True)
    tim=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.ip

