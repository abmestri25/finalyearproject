from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Faculty,Student,HOD,TaskAssigned,Report
from .form import HODSignUpForm,StudentSignUpForm,FacultySignUpForm,AssignedTask,ReportForm,UserUpdateForm,HODForm
from django.core.mail import send_mail, EmailMessage
from wmsproject.settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required


# Create your views here.

def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
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
                    return HttpResponse("Please Sign up")

            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    context={
        'form':AuthenticationForm()
        }
    return render(request, '../templates/login.html',context)

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

def logout_view(request):
    logout(request)
    return redirect('/')



@login_required(login_url='login')
def hod_home(request):

    pending_reports = Report.objects.filter(status=0)
    pending = pending_reports.count()
    faculties = Faculty.objects.all()
    tasks = TaskAssigned.objects.all()
    reports = Report.objects.all()
    total_reports = reports.count()
    workshops = reports.filter(types="Workshop").count()
    seminars = reports.filter(types="Seminar").count()
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

    # u_form = UserUpdateForm(request.POST,instance=request.user)
    # h_form = HODForm(request.POST,request.FILES,instance=request.user.hod)
    # if request.method == "POST":
    #     u_form = UserUpdateForm(request.POST,instance=request.user)
    #     h_form = HODForm(request.POST,request.FILES,instance=request.user.hod)
    #     # messages.success(request,"Successfully Updated Profile !")
    #     # return HttpResponseRedirect(reverse("hod_home"))

    # else:
    #     return HttpResponseRedirect(reverse("hod_home"))
    


    context = {
        'faculties' : faculties,
        'tasks':tasks,
        'reports':reports,
        'pending_reports':pending_reports,
        'total_reports':total_reports,
        'workshops': workshops,
        'seminars':seminars,
        'pending': pending,
        'assignform': assignform
       

    }
    return render(request,'../templates/hod/hod_home.html',context)

def assign_task(request):
    
    context = {
    }
    return render(request,'../templates/hod/hod_home.html',context)

@login_required(login_url='login')
def approve_report(request,report_id):
    report=Report.objects.get(id=report_id)
    email = report.event_coordinator.user.email
    print("this is email " ,email)
    
    report.status=1
    report.save()
    message= "Your Report"+ report.event_title +"is Approved"
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
    faculties = Faculty.objects.all()
    my_tasks = request.user.faculty.taskassigned_set.all()
    my_reports = request.user.faculty.report_set.all()
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
        'my_tasks':my_tasks,
        'my_reports':my_reports,
        'faculties':faculties,
    }
    
    return render(request,'../templates/faculty/faculty_home.html',context)

# def hod_profile(request):
    # u_form = UserUpdateForm(request.POST,instance=request.user)
    # h_form = HODForm(request.POST,request.FILES,instance=request.user.hod)
    # if request.method == "POST":
    #     # u_form = UserUpdateForm(request.POST,instance=request.user)
    #     h_form = HODForm(request.POST,request.FILES,instance=request.user.hod)
    #     # messages.success(request,"Successfully Updated Profile !")
    #     # return HttpResponseRedirect(reverse("hod_home"))

    # else:
    #     return HttpResponseRedirect(reverse("hod_home"))
    # context = {
    #     # 'u_form':u_form,
    #     'h_form':h_form
    # }
    # return render(request,'../templates/hod/hod_home.html',context)

@login_required(login_url='login')
def student_home(request):
    return render(request,'../templates/student/student_home.html')