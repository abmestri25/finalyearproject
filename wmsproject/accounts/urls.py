from django.urls import path
from .import  views

urlpatterns=[
     path('faculty_register/',views.faculty_register.as_view(), name='faculty_register'),
     path('student_register/',views.student_register.as_view(), name='student_register'),
     path('',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
     path('hod_home/',views.hod_home,name="hod_home"),
     path('assign_task/',views.assign_task,name="assign_task"),
     # path('hod_profile',views.hod_profile,name="hod_profile"),

     path('approve_report/<str:report_id>',views.approve_report,name="approve_report"),
     path('disapprove_report/<str:report_id>',views.disapprove_report,name="disapprove_report"),

     path('faculty_home/',views.faculty_home,name="faculty_home"),
     path('student_home/',views.student_home,name="student_home"),

]