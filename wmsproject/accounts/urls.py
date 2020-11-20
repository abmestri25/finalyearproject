from django.urls import path
from .import  views

urlpatterns=[
     path('faculty_register/',views.faculty_register.as_view(), name='faculty_register'),
     path('student_register/',views.student_register.as_view(), name='student_register'),
     path('',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
     
     path('hod_home/',views.hod_home,name="hod_home"),
     path('hod/assign_task/',views.assign_task,name="assign_task"),
     path('hod/all_reports/',views.all_reports,name="all_reports"),
     path('hod/faculties/',views.faculties,name="faculties"),
     path('hod/task_assigned/',views.task_assigned,name="task_assigned"),
     path('hod/profile/',views.profile,name="profile"),
     path('hod/approve_report/<str:report_id>',views.approve_report,name="approve_report"),
     path('hod/disapprove_report/<str:report_id>',views.disapprove_report,name="disapprove_report"),
     path('hod/add_student/',views.add_student,name="add_student"),
     path('hod/add_faculty/',views.add_faculty,name="add_faculty"),

     path('faculty_home/',views.faculty_home,name="faculty_home"),
     path('faculty/create_report/',views.create_report,name="create_report"),
     path('faculty/my_reports/',views.my_reports,name="my_reports"),
     path('faculty/messages/',views.messages,name="messages"),
     path('faculty/profile/',views.faculty_profile,name="faculty_profile"),

     path('student_home/',views.student_home,name="student_home"),
     path('student/reports/',views.reports,name="reports"),
     path('student/profile/',views.student_profile,name="student_profile"),

]