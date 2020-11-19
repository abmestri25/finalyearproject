from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_hod = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    
class HOD(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    middle_name = models.CharField (max_length=50)
    phone_number = models.CharField(max_length=20)
    profile_pic = models.ImageField( upload_to='HOD/profile_pic/')
    address = models.CharField(max_length=200)
    gender = (
        ('Male','Male'),
        ('Female','Female')
    )
    sex = models.CharField(choices=gender, max_length=50)
    branches =  (
        ('COMPUTER','COMPUTER'),
        ('EXTC','EXTC'),
        ('MECHANICAL','MECHANICAL'),
        ('AUTOMOBILE','AUTOMOBILE')
    )
    branch = models.CharField( choices = branches, max_length=50)
    joined_at = models.DateField( auto_now=False,null=True,blank=True)
    qualification = models.CharField( max_length=500)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    class Meta:
        verbose_name_plural = 'HODs'
    
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    middle_name = models.CharField (max_length=50)
    phone_number = models.CharField(max_length=20)
    profile_pic = models.ImageField( upload_to='Faculty/profile_pic/')
    address = models.CharField(max_length=200)

    gender = (
        ('Male','Male'),
        ('Female','Female')
    )
    sex = models.CharField(choices=gender, max_length=50)
    branches =  (
        ('COMPUTER','COMPUTER'),
        ('EXTC','EXTC'),
        ('MECHANICAL','MECHANICAL'),
        ('AUTOMOBILE','AUTOMOBILE')
    )
    branch = models.CharField( choices = branches, max_length=50)
    joined_at = models.DateField( auto_now=False ,null=True)
    qualification = models.CharField( max_length=500)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    class Meta:
        verbose_name_plural = 'Faculties'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    middle_name = models.CharField (max_length=50)
    phone_number = models.CharField(max_length=20)
    profile_pic = models.ImageField( upload_to='Student/profile_pic/')
    address = models.CharField(max_length=200)
    gender = (
        ('Male','Male'),
        ('Female','Female')
    )
    sex = models.CharField(choices=gender, max_length=50)
    branches =  (
        ('COMPUTER','COMPUTER'),
        ('EXTC','EXTC'),
        ('MECHANICAL','MECHANICAL'),
        ('AUTOMOBILE','AUTOMOBILE')
    )
    branch = models.CharField( choices = branches, max_length=50)
    roll_number = models.IntegerField(blank=True,null=True)
    years = (
        ('FE','FE'),
        ('SE','SE'),
        ('TE','TE'),
        ('BE','BE')
    )
    year = models.CharField(choices=years, max_length=50)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        verbose_name_plural = 'Students'

class TaskAssigned(models.Model):
    # id= models.AutoField(primary_key=True)
    event_title = models.CharField(max_length=50)
    branches =  (
        ('COMPUTER','COMPUTER'),
        ('EXTC','EXTC'),
        ('MECHANICAL','MECHANICAL'),
        ('AUTOMOBILE','AUTOMOBILE')
    )
    # email = models.EmailField(Faculty.user, max_length=254)
    org_department = models.CharField(max_length=50, choices = branches)
    forwhome = (
        ('Student','Student'),
        ('Faculty','Faculty')
    )
    forwhome = models.CharField(max_length=50,choices = forwhome)
    res_person = models.CharField(max_length=150)
    types = (
        ('Workshop','Workshop'),
        ('Seminar','Seminar')
    )
    types = models.CharField(max_length=50,choices = types)
    event_coordinator = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.event_title

    class Meta:
        verbose_name_plural = 'Tasks Assigned'


class Report(models.Model):
    academic_year = models.IntegerField(null=True,blank=True)
    event_title = models.ForeignKey(TaskAssigned,on_delete=models.CASCADE)
    event_coordinator = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    branches =  (
        ('COMPUTER','COMPUTER'),
        ('EXTC','EXTC'),
        ('MECHANICAL','MECHANICAL'),
        ('AUTOMOBILE','AUTOMOBILE')
    )
    org_department = models.CharField(max_length=50,choices = branches)
    res_person = models.CharField( max_length=150)
    res_person_profile_pic = models.ImageField( upload_to='Resource Person/Profile Pic/',null=True,blank=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    duration = models.IntegerField()
    types = (
        ('Workshop','Workshop'),
        ('Seminar','Seminar')
    )
    types = models.CharField(max_length=50,choices = types)
    forwhome = (
        ('Student','Student'),
        ('Faculty','Faculty')
    )
    forwhome = models.CharField(max_length=50,choices = forwhome)
    no_participants = models.IntegerField()
    remark = models.CharField( max_length=50,blank=True)
    p_link = models.URLField( max_length=200)
    description = models.TextField(blank=True)
    status = models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    # email = models.EmailField(Faculty.user, max_length=254)
   

    def __str__(self):
        return str(self.event_title)

    class Meta:
        verbose_name_plural = 'Reports'

    

        