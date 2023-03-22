from ast import Global
from cgitb import small
from django.contrib import messages
from urllib import request
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login,logout
from App.EmailBackEnd import EmailBackEnd
from App.Teacher import aivability
from App.models import *
from django.db.models import Q
from datetime import  timedelta , date
import json


# Create your views here.
def home(request):
    
    return render(request,"home.html")

def dashboard(request):

    #notif view
    notif = Notification.objects.filter(status=0).count()
    notifs = Notification.objects.all()

    now = date.today()
    room= Salle.objects.count()
    aivabilities = Formateur.objects.count() 
    aivabilities_obj = Disponibilite.objects.filter(date_dispo=now)
    students = Etudiants.objects.count()
    subjects = Matiere.objects.filter(taux_horaire=0).count()
    schedules = []
    room_id = Salle.objects.values_list('id',flat=True)
    label_rooms =[]
    label_room = Salle.objects.all()
    for r in label_room:
        label_rooms.append(r.nom_salle)
    for id in room_id:
        schedules.append(Schedule.objects.filter(Q(date_jours=now ) & Q(salle_id=id)).count())

    today_sched = Schedule.objects.filter(date_jours=now )

   
    context = {"now":now,"room":room,"aivabilities":aivabilities,"today_sched":today_sched,
    "students":students,"subjects":subjects,"schedules":(schedules),"label_rooms":(label_rooms),"notif":notif,"notifs":notifs}

    return render(request,"Dashboard.html",context)

def notifajax(request):
    notif = Notification.objects.filter(status=0).count()
    notifs = Notification.objects.filter(status=0)
    context = {"notif":notif,"notifs":notifs}
    return render(request,"ajax/Notif.html",context)

def notifajax_read(request):
    notif = Notification.objects.all()
    ids = []
    for id in notif:
        ids.append(id.id)
    for i in ids :
        try:
            notif_update = Notification.objects.get(id=i)
            notif_update.status =1
            notif_update.save()
        except:
            print("error")
    return HttpResponseRedirect("/dashboard")


def Login(request):
    return render(request,"index.html")
 
def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2> Method not Allowed </h2>")
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type == "1":
                return HttpResponseRedirect("/dashboard")
            elif user.user_type == "2":
                return HttpResponseRedirect("/dashboard_T")
        else:
            return  HttpResponse("Invalid Login")
        """messages.error(request,"Invalid Login details")"""
        

def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User :" +request.user.email+" usertype : "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def dispo(request):
    context = {}
    return render(request,"Disponibilite.html",context)

def schedule_teacher(request):
    context = {}
    return render(request,"schedule_teacher.html",context)

def Aivability_list_admin(request):
    teacher_search = request.GET.get('teacher_search')
    date_search = request.GET.get('date_search')
    hour_s = request.GET.get('hour_s')
    hour_e = request.GET.get('hour_e')
     
    aivabilities = Disponibilite.objects.all()
    if teacher_search != '' and teacher_search is not None:
        aivabilities = Disponibilite.objects.filter(formateur_id=teacher_search)
    elif date_search != '' and date_search is not None:
        aivabilities = Disponibilite.objects.filter(date_dispo=date_search)
    elif hour_s != '' and hour_s is not None:
        aivabilities = Disponibilite.objects.filter(heure_deb=hour_s)
    elif hour_e != '' and hour_e is not None:
        aivabilities = Disponibilite.objects.filter(heure_fin=hour_e)
    elif (teacher_search != '' and teacher_search is not None) and (date_search != '' and date_search is not None) and (hour_s != '' and hour_s is not None) and ( hour_e != '' and hour_e is not None):
        aivabilities = Disponibilite.objects.filter(Q(formateur_id=teacher_search) & Q(date_dispo=date_search) &
        Q(heure_deb=hour_s) & Q(heure_fin=hour_e))
    teachers = Formateur.objects.all()
    context = {"aivabilities" : aivabilities,"teachers":teachers}
    return render(request,"Aivability_list_admin.html",context)

def list_teacher(request):
    Teacher = Formateur.objects.all()
    context = {"Teacher":Teacher}
    return render(request,"list_teacher.html",context)

def list_teacher_ajax(request):
    id = request.GET.get('id')
    matiere = Matiere.objects.filter(formateurId=id)  
    context = {"matiere":matiere}
    return render(request,"ajax/subject_teacher_ajax.html",context)

def aivability_teacher_ajax(request):
    id = request.GET.get('id')
    date_t  = date.today()
    monday = date_t - timedelta(days = date_t.weekday())
    matiere = Disponibilite.objects.filter(Q(formateur_id=id) & Q(week_of=monday))  
    context = {"aivabilities":matiere}
    return render(request,"ajax/aivability_teacher_ajax.html",context)


