from django.contrib import messages
from urllib import request
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from App.EmailBackEnd import EmailBackEnd
from App.models import *
from App.forms import *
from datetime import timedelta , date
from django.db.models import Q

def homeT(request):
    context = {}
    return render(request,"Teacher_home.html",context)

def dashboard(request):
    id_user = Formateur.objects.get(admin=request.user.id)
    date_t  = date.today()
    monday = date_t - timedelta(days = date_t.weekday())
    subjects = Matiere.objects.filter(formateurId=id_user).count()
    aivabilities = Disponibilite.objects.filter(Q(formateur_id=id_user) & Q(week_of=monday) & Q(status=1)).count()
    subjects_C = Matiere.objects.filter(Q(formateurId=id_user) & Q(taux_horaire=0)).count()
    aivabilities_obj = Disponibilite.objects.filter(Q(formateur_id=id_user) & Q(date_dispo=date_t))
    context = {"aivabilities_obj" : aivabilities_obj,"subjects" : subjects,
    "aivabilities":aivabilities,"subjects_C":subjects_C,"date":date_t}
    return render(request,"Dashboard_T.html",context)    

def teacher(request):
    form = AddTeacher()
    context = {"form":form}
    return render(request,"user_teacher.html",context)

def teacher_add(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        form = AddTeacher(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email_user = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
    try: 
        user = CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email_user,user_type=2)
        user.save()
        return HttpResponseRedirect("/")
    except:
        messages.error(request,"Failed to add")

def aivability(request):
    form = AddAivabilityForm() 
    id_user = Formateur.objects.get(admin=request.user.id)
    aivabilities = Disponibilite.objects.filter(formateur_id=id_user)
    context = {"form" : form,"aivabilities" : aivabilities}
    return render(request,"Aivability.html",context)

def aivability_add(request):
    if request.method !='POST':   
       return HttpResponse("Method not allowed")
    else:
        form=AddAivabilityForm(request.POST)
        if form.is_valid():
            dateDispo = form.cleaned_data["date_dispo"]
            hour_s = form.cleaned_data["heure_deb"]
            hour_e = form.cleaned_data["heure_fin"]
            teacher_obj = Formateur.objects.get(admin=request.user.id)
            try:

                monday = dateDispo - timedelta(days = dateDispo.weekday())
                dispo_model = Disponibilite(week_of=monday,date_dispo=dateDispo,heure_deb=hour_s,heure_fin=hour_e,formateur_id=teacher_obj)
                dispo_model.save()
                try:
                    msg_txt = ' added a new aivability on ' + str(dateDispo.strftime("%m/%d/%Y"))+" to " + str(hour_s.strftime("%H:%M")) + "h - "+ str(hour_e.strftime("%H:%M") + "h")
                    notif_modef = Notification(formateur_id=teacher_obj,msg=msg_txt)
                    notif_modef.save()
                except:
                    messages.error(request,"Failed to Add!")
                    return HttpResponseRedirect("/aivability")
                messages.success(request,"SuccessFully Added !")
                return HttpResponseRedirect("/aivability")
            except:
                messages.error(request,"Failed to Add!")
                return HttpResponseRedirect("/aivability")
        else: 
            form = AddAivabilityForm()
        return render(request,"Aivability.html",{"form":form})

def aivability_list(request):
    date_now = date.today()
    monday = date_now - timedelta(days = date_now.weekday())
    id_user = Formateur.objects.get(admin=request.user.id)
    aivabilities = Disponibilite.objects.filter(formateur_id=id_user)
    context = {"aivabilities" : aivabilities,"week":monday}
    return render(request,"Aivability_list.html",context)

def subject_list(request):
    id_user = Formateur.objects.get(admin=request.user.id)
    subjects = Matiere.objects.filter(formateurId=id_user).order_by('niveauId')
    context = {"subjects" : subjects}
    return render(request,"Subject_teacher.html",context)

def schedule_list_T(request):
    id_user = Formateur.objects.get(admin=request.user.id)
    week_search = request.GET.get('week_search')
    week_value = week_search
    schedules=[]
    date_now = date.today()
    monday = date_now - timedelta(days = date_now.weekday())
    form=SearchSchedule()
    subjects = Matiere.objects.filter(formateurId=id_user).values_list('id',flat=True)

    if week_search != '' and week_search is not None:
        for subject in subjects:
            schedules.append(Schedule.objects.filter(Q(matiere_id=subject) & Q(semaine_de=week_search )))
    else:
        for subject in subjects:
            schedules.append(Schedule.objects.filter(Q(matiere_id=subject) & Q(semaine_de=monday)))
        week_value = monday
    isOne = Matiere.objects.filter(formateurId=id_user).count()
    if isOne==1:
        isOne=True
    else:
        isOne=False


    context = {"schedules":schedules,"form":form,"week_value":week_value,"isOne":isOne,"monday":monday}
    return render(request,"schedule_teacher.html",context)

