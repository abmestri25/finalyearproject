from django.urls import path
from .import  views

urlpatterns=[
     path('faculty_register/',views.faculty_register.as_view(), name='faculty_register'),
     path('student_register/',views.student_register.as_view(), name='student_register'),
     path('',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
     path('report_pdf/<str:report_id>',views.generate_report_pdf, name='generate_report_pdf'),
     
     path('hod_home/',views.hod_home,name="hod_home"),
     path('hod/assign_task/',views.assign_task,name="assign_task"),
     path('hod/all_reports/',views.all_reports,name="all_reports"),
     path('hod/faculties/',views.faculties,name="faculties"),
     path('hod/students/',views.students,name="students"),
     path('hod/task_assigned/',views.task_assigned,name="task_assigned"),
     path('hod/profile/',views.profile,name="profile"),
     path('hod/approve_report/<str:report_id>',views.approve_report,name="approve_report"),
     path('hod/disapprove_report/<str:report_id>',views.disapprove_report,name="disapprove_report"),
     path('hod/add_student/',views.add_student,name="add_student"),
     path('hod/add_faculty/',views.add_faculty,name="add_faculty"),
     path('hod/all_reports/view_report/<str:report_id>/',views.view_report,name="view_report"),
     path('hod/all_reports/delete_report/<str:report_id>/',views.delete_report,name="delete_report"),
     path('hod/all_faculties/delete_faculty/<str:faculty_id>/',views.delete_faculty,name="delete_faculty"),
     path('hod/all_students/delete_student/<str:student_id>/',views.delete_student,name="delete_student"),
     path('hod/all_tasks/delete_task/<str:task_id>/',views.delete_task,name="delete_task"),
     path('hod/faculties/edit_faculty/<str:faculty_id>/',views.edit_faculty,name="edit_faculty"),
     path('hod/students/edit_student/<str:student_id>/',views.edit_student,name="edit_student"),
     path('hod/assigned_tasks/edit_task/<str:task_id>/',views.edit_task,name="edit_task"),

     path('faculty_home/',views.faculty_home,name="faculty_home"),
     path('faculty/create_report/',views.create_report,name="create_report"),
     path('faculty/my_reports/edit_report/<str:report_id>/',views.edit_report,name="edit_report"),
     path('faculty/my_reports/view_report/<str:report_id>/',views.faculty_view_report,name="faculty_view_report"),
     path('faculty/my_reports/',views.my_reports,name="my_reports"),
     path('faculty/my_reports/delete_report/<str:report_id>/',views.faculty_delete_report,name="faculty_delete_report"),
     path('faculty/messages/',views.messages,name="messages"),
     path('faculty/profile/',views.faculty_profile,name="faculty_profile"),

     path('student_home/',views.student_home,name="student_home"),
     path('student/reports/',views.reports,name="reports"),
     path('student/profile/',views.student_profile,name="student_profile"),

     path('report/',views.reportpdf,name="report_pdf")
]