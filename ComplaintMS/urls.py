from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('',views.home,name='home'),


    path('login_page/',views.login_page,name='login_page'),
    path('signup_page/',views.signup_page,name='signup_page'),


    #urls related to authentication --
    path('student_login/',views.my_login_student,name='my_login_student'),
    path('administrator_login/',views.my_login_administrator,name='my_login_administrator'),
    path('logout_student',views.my_logout_student,name='my_logout_student'),
    path('logout_administrator',views.my_logout_administrator,name='my_logout_administrator'),
    path('signup_student/',views.my_signup_student, name='my_signup_student'),
    path('signup_administrator/',views.my_signup_administrator,name='my_signup_administrator'),


    path('administrator_interface/',views.administrator_interface,name='administrator_interface'),
    path('unaddressed_complaints/',views.unaddressed_complaints,name='unaddressed_complaints'),
    path('assigned_complaints/',views.assigned_complaints,name='assigned_complaints'),
    path('resolved_complaints_admin/',views.resolved_complaints_admin,name='resolved_complaints_admin'),
    path('assign-worker/<complaint_id>/',views.assign_worker,name='assign_worker'),
    path('register_worker/',views.register_worker,name='register_worker'),
    path('all_workers/',views.all_workers,name='all_workers'),
    path('grant_leave/<worker_id>',views.grant_leave,name='grant_leave'),


    path('student_interface/',views.student_interface,name='student_interface'),
    path('resolved_complaints/',views.resolved_complaints,name='resolved_complaints'),
    path('unresolved_complaints/',views.unresolved_complaints,name='unresolved_complaints'),
    path('add_cmp/',views.new_complaint, name='new_complaint'),

]
