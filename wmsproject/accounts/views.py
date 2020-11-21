from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Faculty,Student,HOD,TaskAssigned,Report
from .form import HODSignUpForm,StudentSignUpForm,FacultySignUpForm,AssignedTask,ReportForm,UserUpdateForm,HODForm,FacultyForm,StudentForm
from django.core.mail import send_mail, EmailMessage
from wmsproject.settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def login_request(request):
    if request.method == 'POST':   
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                if user.is_student :
                    login(request,user)
                    return redirect('student_home')
                elif user.is_faculty :
                    login(request,user)
                    return redirect('faculty_home')
                elif user.is_hod:
                    login(request,user)
                    return redirect('hod_home')
                else:
                    return HttpResponse("Please Register !")
            else:
                return HttpResponse("Invalid Login Credentials !")


    return render(request,'../templates/login.html')
        



class hod_register(CreateView):
    model = User
    form_class = HODSignUpForm
    template_name = '../templates/hod_register.html'

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request,"HOD Registered Successfully")
        return redirect('login')

class faculty_register(CreateView):
    model = User
    form_class = FacultySignUpForm
    template_name = '../templates/faculty_register.html'

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request,"Faculty Registered Successfully")

        return redirect('login')

class student_register(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = '../templates/student_register.html'

    def form_valid(self, form):
        user = form.save()
        return redirect('login')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('/')



@login_required(login_url='login')
def hod_home(request):
    pending_reports = Report.objects.filter(status=0)
    pending = pending_reports.count()
    faculties = Faculty.objects.all()
    reports = Report.objects.all()
    total_reports = reports.count()
    workshops = reports.filter(types="Workshop").count()
    seminars = reports.filter(types="Seminar").count() 
    context = {
        'faculties' : faculties,
        'reports':reports,
        'pending_reports':pending_reports,
        'total_reports':total_reports,
        'workshops': workshops,
        'seminars':seminars,
        'pending': pending,
    }
    return render(request,'../templates/hod/hod_home.html',context)

@login_required(login_url='login')
def assign_task(request):
    assignform = AssignedTask(request.POST or None)
    if request.method == "POST":
        if assignform.is_valid():
            email = request.POST.get('email')
            assignform.save()
            message= "Hey I have assigned something for uh"
            subject= "HOD has assigned something to uh"
            mail=EmailMessage(subject,message,EMAIL_HOST_USER,[email])
            mail.content_subtype='html'
            mail.send()
            return redirect ('hod_home')
        else:
            print("Errors",assignform.errors)
    context = {
        'assignform': assignform

    }
    return render(request,'../templates/hod/assign_task.html',context)

@login_required(login_url='login')
def all_reports(request):
    pending_reports = Report.objects.filter(status=0)
    pending = pending_reports.count()
    reports = Report.objects.all()
    total_reports = reports.count()
    workshops = reports.filter(types="Workshop").count()
    seminars = reports.filter(types="Seminar").count()
    
    context = {
    'reports':reports,
    'total_reports':total_reports,
    'workshops': workshops,
    'seminars':seminars,
    'pending_reports':pending_reports,
    'pending': pending,
    }
    return render(request,'../templates/hod/allreports.html',context)

@login_required(login_url='login')
def profile(request):
    form = HODForm(request.POST or None,instance=request.user.hod)
    u_form = UserUpdateForm(request.POST or None,instance=request.user)
    if request.method == "POST":
        if form.is_valid() and u_form.is_valid():
            form.save()
            u_form.save()
            return redirect ('hod_home')
        else:
            print("Errors",form.errors)
    context = {
        'form':form,
        'u_form':u_form
    }
    return render(request,'../templates/hod/profile.html',context)

@login_required(login_url='login')
def faculties(request):
    faculties = Faculty.objects.all()
    context = {
    'faculties' : faculties,   
    }
    return render(request,'../templates/hod/faculties.html',context)


@login_required(login_url='login')
def add_student(request):
    studentform = StudentSignUpForm(request.POST)
    context = {
        'studentform':studentform
    }
    return render(request,'../templates/hod/add_student.html',context)

@login_required(login_url='login')
def add_faculty(request):
    faculty_form = FacultySignUpForm(request.POST)
    context = {
        'faculty_form':faculty_form
    }
    return render(request,'../templates/hod/add_faculty.html',context)

@login_required(login_url='login')
def task_assigned(request):
    tasks = TaskAssigned.objects.all()
    context = {
        'tasks':tasks,
    }
    return render(request,'../templates/hod/task_assigned.html',context)

@login_required(login_url='login')
def approve_report(request,report_id):

    report=Report.objects.get(id=report_id)
    email = report.event_coordinator.user.email
    print("this is email " ,email)
    
    report.status=1
    report.save()
    message= "Your Report"+ report.event_title +"is Approved."
    subject= "Report Approval"
    mail=EmailMessage(subject,message,EMAIL_HOST_USER,[email])
    mail.content_subtype='html'
    mail.send()
    return HttpResponseRedirect(reverse("hod_home"))

@login_required(login_url='login')
def disapprove_report(request,report_id):
    report=Report.objects.get(id=report_id)
    email = report.event_coordinator.user.email
    report.status=2
    report.save()
    message= "Your Report"+ report.event_title +"is Rejected.Kindly Resend the report by making desired changes."
    subject= "Report Disapproval"
    mail=EmailMessage(subject,message,EMAIL_HOST_USER,[email])
    mail.content_subtype='html'
    mail.send()
    return HttpResponseRedirect(reverse("hod_home"))


@login_required(login_url='login')
def faculty_home(request):
    pending_reports = Report.objects.filter(status=0)
    pending = pending_reports.count()
    faculties = Faculty.objects.all()
    reports = Report.objects.all()
    total_reports = reports.count()
    workshops = reports.filter(types="Workshop").count()
    seminars = reports.filter(types="Seminar").count() 
    my_tasks = request.user.faculty.taskassigned_set.all()

    context = {
        'faculties' : faculties,
        'reports':reports,
        'pending_reports':pending_reports,
        'total_reports':total_reports,
        'workshops': workshops,
        'seminars':seminars,
        'pending': pending,
    }
    
    return render(request,'../templates/faculty/faculty_home.html',context)

@login_required(login_url='login')
def create_report(request):
    form = ReportForm(request.POST or None)
    if request.method =="POST":
        if form.is_valid():
            form.save()
            return redirect('faculty_home')
            print("working")
        else:
            print("Errors goes here",form.errors)
    context = {
        'form': form,

    }
    return render(request,'../templates/faculty/create_report.html',context)

@login_required(login_url='login')
def faculty_profile(request):
    form = FacultyForm(request.POST or None,instance=request.user.faculty)
    u_form = UserUpdateForm(request.POST or None,instance=request.user)
    if request.method == "POST":
        if form.is_valid() and u_form.is_valid():
            form.save()
            u_form.save()
            return redirect ('faculty_home')
        else:
            print("Errors",form.errors)
    context = {
        'form':form,
        'u_form':u_form
    }
    return render(request,'../templates/faculty/profile.html',context)

@login_required(login_url='login')
def my_reports(request):
    my_reports = request.user.faculty.report_set.all()

    context = {
        'my_reports':my_reports,

    }
    return render(request,'../templates/faculty/my_reports.html',context)

@login_required(login_url='login')
def messages(request):
    my_tasks = request.user.faculty.taskassigned_set.all()

    context = {
        'my_tasks':my_tasks,

    }
    return render(request,'../templates/faculty/messages.html',context)  

@login_required(login_url='login')
def student_home(request):
    
    context = {
    }
    return render(request,'../templates/student/student_home.html',context)

@login_required(login_url='login')
def reports(request):
    student = request.user.student
    department = student.branch
    reports = Report.objects.filter(org_department=department)
    context = {
        'reports':reports

    }
    return render(request,'../templates/student/reports.html',context)

@login_required(login_url='login')
def student_profile(request):
    form = StudentForm(request.POST or None,instance=request.user.student)
    u_form = UserUpdateForm(request.POST or None,instance=request.user)
    if request.method == "POST":
        if form.is_valid() and u_form.is_valid():
            form.save()
            u_form.save()
            return redirect ('student_home')
        else:
            print("Errors",form.errors)
    context = {
        'form':form,
        'u_form':u_form
    }
    return render(request,'../templates/student/student_profile.html',context)