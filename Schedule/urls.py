"""Schedule URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App import views , Teacher ,Schedule,Subjects,Class,Student,Room
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Login,name="login"),
    path('home/',views.home,name="home"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('homeT/',Teacher.homeT,name="homeT"),
    path('dashboard_T/',Teacher.dashboard,name="dashboard_T"),
    path('salle/',Room.room,name="salle"),
    path('room_list/',Room.room_list,name="room_list"),
    path('salle/room_edit/<str:salle_id>',Room.room_edit,name="room_edit"),
    path('room_add',Room.room_add,name="room_add"),
    path('room_edit_save/',Room.room_edit_save,name="room_edit_save"),
    path('doLogin',views.doLogin),
    path('logout',views.logout_user),
    path('getDetails', views.GetUserDetails),
    path('student/',Student.student,name="student"),
    path('student_add',Student.student_add,name="student_add"),
    path('student/student_edit/<str:id_etu>',Student.student_edit,name='student_edit'),
    path('student_edit_save/',Student.student_edit_save,name='student_edit_save'),
    path('teacher_add',Teacher.teacher_add,name="teacher_add"), 
    path('register_T/',Teacher.teacher,name="register_T"),
    path('aivability/', Teacher.aivability,name="aivability"),
    path('aivability_list_admin/', views.Aivability_list_admin,name="aivability_list_admin"),
    path('aivability_list/', Teacher.aivability_list,name="aivability_list"),
    path('aivability/aivability_add',Teacher.aivability_add,name="aivability_add"),
    path('my_subjects/',Teacher.subject_list,name="my_subjects"),
    path('my_schedule_list/', Teacher.schedule_list_T, name="my_schedule_list"),
    path('subjects/',Subjects.subject,name="subjects"),  
    path('subjects/subjects/#table',Subjects.subject,name="subjects_search"),
    path('subject_add',Subjects.subject_add,name="subject_add"),
    path('subjects_list',Subjects.subject_list,name="subjects_list"),
    path('schedule/', Schedule.schedule, name="schedule"),
    path('schedule_aivability/', Schedule.schedule_aivability, name="schedule_aivability"),
    path('schedule_add/', Schedule.schedule_add, name="schedule_add"),
    path('schedule_add_aivability/', Schedule.schedule_add_aivability, name="schedule_add_aivability"),
    path('schedule_list/', Schedule.schedule_list, name="schedule_list"),
    path('schedule/schedule_edit/<str:id_s>',Schedule.schedule_edit,name='schedule_edit'),
    path('schedule/schedule_del/<str:id_s>',Schedule.schedule_del,name='schedule_del'),
    path('schedule_save/', Schedule.schedule_edit_save, name="schedule_save"),
    path('schedule_del_save/', Schedule.schedule_del_save, name="schedule_del_save"),
    path('load_subject/', Schedule.load_ajax, name="load_subject"),
    path('load_room/', Schedule.load_ajax_room, name="load_room"),
    path('load_notif_dropdown/', views.notifajax_read, name="notifajax_read"),
    path('load_aivability/',Schedule.load_ajax_aivability, name="load_aivability"),
    path('load_notif/', views.notifajax, name="load_notif"),
    path('load_notif_dropdown/', views.notifajax_read, name="notifajax_read"),
    path('class/',Class.level,name='class'),
    path('class/class_edit/<str:id_class>',Class.level_edit,name='class_edit'),
    path('class/class_edit_save',Class.level,name='class_edit_save'),
    path('class_list/',Class.level_list,name='class_list'),
    path('list_teacher',views.list_teacher,name="list_teacher"),
    path('list_teacher_ajax/',views.list_teacher_ajax,name="list_teacher_ajax"),
    path('aivability_teacher_ajax/',views.aivability_teacher_ajax,name="aivability_teacher_ajax"), 

]

