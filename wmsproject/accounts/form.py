from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Faculty,Student,HOD,TaskAssigned,Report
from django.core.mail import send_mail, EmailMessage
from wmsproject.settings import EMAIL_HOST_USER
from django.forms import ChoiceField
from django.forms import ModelForm 
from django.shortcuts import redirect, render




class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass

class HODSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    middle_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    branch = forms.CharField(required=True)
    address = forms.CharField(required=True)
    joined_at = forms.CharField(required=True)
    qualification = forms.CharField(required=True)
    sex = forms.CharField(required=True)
    
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_hod = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        hod = HOD.objects.create(user=user)
        hod.phone_number=self.cleaned_data.get('phone_number')
        hod.middle_name=self.cleaned_data.get('middle_name')
        hod.branch=self.cleaned_data.get('branch')
        hod.address=self.cleaned_data.get('address')
        hod.joined_at=self.cleaned_data.get('joined_at')
        hod.qualification=self.cleaned_data.get('qualification')
        hod.sex=self.cleaned_data.get('sex')
        hod.save()
        return user


class FacultySignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    middle_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    branch = forms.CharField(required=True)
    address = forms.CharField(required=True)
    qualification = forms.CharField(required=True)
    sex = forms.CharField(required=True)
    
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_faculty = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        faculty = Faculty.objects.create(user=user)
        faculty.middle_name=self.cleaned_data.get('middle_name')
        faculty.phone_number=self.cleaned_data.get('phone_number')
        faculty.branch=self.cleaned_data.get('branch')
        faculty.address=self.cleaned_data.get('address')
        faculty.qualification=self.cleaned_data.get('qualification')
        faculty.sex=self.cleaned_data.get('sex')
        faculty.save()
        message= "Thanks for registering with us.Your Username is " + user.username + "Your Password is " + user.password 
        subject= "Registration "
        mail=EmailMessage(subject,message,EMAIL_HOST_USER,[user.email])
        mail.content_subtype='html'
        mail.send()
        return user

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    branch = forms.CharField(required=True)
    address = forms.CharField(required=True)
    year = forms.CharField(required=True)
    roll_number = forms.CharField(required=True)
    sex = forms.CharField(required=True)
    
    
    
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(user=user)
        student.phone_number=self.cleaned_data.get('phone_number')
        student.branch=self.cleaned_data.get('branch')
        student.address=self.cleaned_data.get('address')
        student.year=self.cleaned_data.get('year')
        student.roll_number=self.cleaned_data.get('roll_number')
        student.sex=self.cleaned_data.get('sex')
        student.save()
        message= "Thanks for registering with us.Your Username is " + user.username + "Your Password is " + user.password 
        subject= "Registration "
        mail=EmailMessage(subject,message,EMAIL_HOST_USER,[user.email])
        mail.content_subtype='html'
        mail.send()
        return user

class AssignedTask(forms.ModelForm):
    branches =  (
        ('COMPUTER','COMPUTER'),
        ('EXTC','EXTC'),
        ('MECHANICAL','MECHANICAL'),
        ('AUTOMOBILE','AUTOMOBILE')
    )
    types = (
        ('Workshop','Workshop'),
        ('Seminar','Seminar')
    )
    forwhome = (
        ('Student','Student'),
        ('Faculty','Faculty')
    )



    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    forwhome = forms.ChoiceField(label="Department",choices=forwhome,widget=forms.Select(attrs={"class":"form-control"}))
    event_title=forms.CharField(label="Event Title",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    org_department = forms.ChoiceField(label="Department",choices=branches,widget=forms.Select(attrs={"class":"form-control"}))
    res_person=forms.CharField(label="Resource Person",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    types = forms.ChoiceField(label="Department",choices=types,widget=forms.Select(attrs={"class":"form-control"}))


   
    class Meta:
        model = TaskAssigned
        fields = '__all__'

        widgets = {
            'event_coordinator': forms.Select(attrs={'class': 'form-control'}),
        }



class ReportForm(forms.ModelForm):
    branches =  (
        ('COMPUTER','COMPUTER'),
        ('EXTC','EXTC'),
        ('MECHANICAL','MECHANICAL'),
        ('AUTOMOBILE','AUTOMOBILE')
    )
    types = (
        ('Workshop','Workshop'),
        ('Seminar','Seminar')
    )
    forwhome = (
        ('Student','Student'),
        ('Faculty','Faculty')
    )


    academic_year = forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-control"}))
    
    # event_title=forms.CharField(label="Event Title",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    forwhome = forms.ChoiceField(label="Department",choices=forwhome,widget=forms.Select(attrs={"class":"form-control"}))
    org_department = forms.ChoiceField(label="Department",choices=branches,widget=forms.Select(attrs={"class":"form-control"}))
    res_person=forms.CharField(label="Resource Person",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    types = forms.ChoiceField(label="Department",choices=types,widget=forms.Select(attrs={"class":"form-control"}))
    res_person_profile_pic =forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control-file"}),required=False)
    no_participants = forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-control"}))
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={"class":"form-control"}))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={"class":"form-control"}))
    duration = forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-control"}))
    remark=forms.CharField(label="Event Title",max_length=150,widget=forms.TextInput(attrs={"class":"form-control"}))
    description=forms.CharField(label="Event Title",max_length=550,widget=forms.Textarea(attrs={"class":"form-control","rows":"3"}))
    p_link = forms.URLField(widget=forms.TextInput(attrs={"class":"form-control"}))


   
    class Meta:
        model = Report
        fields = '__all__'

        widgets = {
            'event_title': forms.Select(attrs={'class': 'form-control'}),
            'event_coordinator': forms.Select(attrs={'class': 'form-control'}),
        }

class UserUpdateForm(forms.ModelForm):
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False,disabled=True)
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}),required=False)

    class Meta : 
        model = User
        fields = ['username','first_name','last_name','email']


class HODForm(forms.ModelForm):
    branches =  (
        ('COMPUTER','COMPUTER'),
        ('EXTC','EXTC'),
        ('MECHANICAL','MECHANICAL'),
        ('AUTOMOBILE','AUTOMOBILE')
    )
    genders = (
        ('Male','Male'),
        ('Female','Female')
    )

    middle_name=forms.CharField(label="Middle Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    joined_at = forms.DateTimeField(label="Joined At",widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    branch = forms.ChoiceField(label="Department",choices=branches,widget=forms.Select(attrs={"class":"form-control"}),required=False)
    qualification=forms.CharField(label="Qualification",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    phone_number=forms.CharField(label="Phone Number",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    sex = forms.ChoiceField(label="Gender",choices=genders,widget=forms.Select(attrs={"class":"form-control"}),required=False)
    profile_pic =forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control-file"}),required=False)

    
    class Meta:
        model = HOD
        fields = '__all__'
        exclude = ['user']
        

class FacultyForm(forms.ModelForm):
    branches =  (
        ('COMPUTER','COMPUTER'),
        ('EXTC','EXTC'),
        ('MECHANICAL','MECHANICAL'),
        ('AUTOMOBILE','AUTOMOBILE')
    )
    genders = (
        ('Male','Male'),
        ('Female','Female')
    )
    middle_name=forms.CharField(label="Middle Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    joined_at = forms.DateTimeField(label="Joined At",widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    branch = forms.ChoiceField(label="Department",choices=branches,widget=forms.Select(attrs={"class":"form-control"}),required=False)
    qualification=forms.CharField(label="Qualification",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    phone_number=forms.CharField(label="Phone Number",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    sex = forms.ChoiceField(label="Department",choices=genders,widget=forms.Select(attrs={"class":"form-control"}),required=False)
    profile_pic =forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control-file"}),required=False)
    class Meta:
        model = Faculty
        fields = '__all__'
        exclude = ['user']



class StudentForm(forms.ModelForm):
    branches =  (
        ('COMPUTER','COMPUTER'),
        ('EXTC','EXTC'),
        ('MECHANICAL','MECHANICAL'),
        ('AUTOMOBILE','AUTOMOBILE')
    )
    genders = (
        ('Male','Male'),
        ('Female','Female')
    )
    years = (
        ('FE','FE'),
        ('SE','SE'),
        ('TE','TE'),
        ('BE','BE')
    )
    middle_name=forms.CharField(label="Middle Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    branch = forms.ChoiceField(label="Department",choices=branches,widget=forms.Select(attrs={"class":"form-control"}),required=False)
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    phone_number=forms.CharField(label="Phone Number",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    sex = forms.ChoiceField(label="Gender",choices=genders,widget=forms.Select(attrs={"class":"form-control"}),required=False)
    roll_number = forms.IntegerField(label="Roll Number",widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
    year = forms.ChoiceField(label="Year",choices=years,widget=forms.Select(attrs={"class":"form-control"}),required=False)
    profile_pic =forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control-file"}),required=False)
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user']

    