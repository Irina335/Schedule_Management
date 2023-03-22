from typing_extensions import Self
from django.contrib import messages
from urllib import request
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from App.EmailBackEnd import EmailBackEnd
from App.models import *
from App.forms import *
from django.db.models import Q
from datetime import  timedelta , date, datetime,time



def schedule(request):
    form     = AddScheduleForm
    schedules = Schedule.objects.all()
    context = {"form":form,"schedules":schedules}
    return render(request,"Schedule.html",context)

def schedule_aivability(request):
    form     = AddScheduleForm1()
    id = request.GET.get('id')
    teacher = request.GET.get('teacher')
    date_dispo = request.GET.get('date')
    hour_s = request.GET.get('hour_s')
    hour_e = request.GET.get('hour_e')
    subjects_list = [("","Choose a subject ...")]
    aiv_model = Disponibilite.objects.get(id=int(id))
    id_teach = aiv_model.formateur_id
    subjects = Matiere.objects.filter(Q(formateurId=id_teach) & ~Q(taux_horaire=0)) 
    for subject in subjects:
        concat =  str(subject.matiere_name)  
        subject_field = (subject.id,concat)
        subjects_list.append(subject_field)
    schedules = Schedule.objects.all()

    form.fields['teacher'].initial = teacher
    form.fields['date'].initial = date_dispo
    form.fields['hour_s'].initial = hour_s
    form.fields['hour_e'].initial = hour_e
    form.fields['id_sub'].choices = subjects_list
    context = {"form":form,"schedules":schedules}
    return render(request,"Schedule_aivability.html",context)

def schedule_add(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        form=AddScheduleForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            id_etu = form.cleaned_data["id_etu"]
            id_sub = form.cleaned_data["id_sub"]
            hour_s = form.cleaned_data["hour_s"]
            hour_e = form.cleaned_data["hour_e"]
            id_room = form.cleaned_data["id_room"]
       
        
         #query_if_teacher_is_Aivable    
        matiere = Matiere.objects.get(id=id_sub)    
        id_teach = matiere.formateurId
        dispo = Disponibilite.objects.filter(formateur_id=id_teach,date_dispo=date,heure_deb=hour_s,heure_fin=hour_e)
        is_taken = Disponibilite.objects.filter(formateur_id=id_teach,date_dispo=date,heure_deb=hour_s,heure_fin=hour_e,status=1)
        #query_if_room_is can content student
        room = Salle.objects.get(id=id_room)
        student = Etudiants.objects.get(id=id_etu)
        #query_if_room_is not aivable:
        room_aivable = Schedule.objects.filter(Q(date_jours =date) & Q(heure_deb=hour_s) & Q(heure_fin=hour_e) 
        & Q(salle_id=room) )
        if room_aivable.exists():
            messages.error(request," Room not aivable at that time")
        elif student.nb_etu > room.nb_chaise :
            messages.error(request," Room capacity smaller than student numbers, room capacity : "+ str(room.nb_chaise) + " and students number = " +str(student.nb_etu) )
            return HttpResponseRedirect("/schedule")
        elif dispo.exists() == False:
            messages.error(request,str(id_teach)+" is not aivable at (" + str((hour_s.strftime("%H:%M"))) +"  to  " + str((hour_e.strftime("%H:%M")))+" )") 
            return HttpResponseRedirect("/schedule")
        elif is_taken.exists():
            messages.error(request,str(id_teach)+" is already taken at (" + str((hour_s.strftime("%H:%M"))) +"  to  " +str((hour_e.strftime("%H:%M")))+")" )
            return HttpResponseRedirect("/schedule")
        else:
            try:
                etu_obj = Etudiants.objects.get(id=id_etu)
                sub_obj = Matiere.objects.get(id=id_sub)
                room_obj = Salle.objects.get(id=id_room)
                monday = date - timedelta(days = date.weekday())
                schedule_model = Schedule(date_jours=date,semaine_de=monday,heure_deb=hour_s,
                heure_fin=hour_e,salle_id=room_obj,etudiant_id=etu_obj,matiere_id=sub_obj)
                schedule_model.save()
                try:
                    #calculate the differenc beetwen two hours and update the related subject's hour
                    diff  = int(hour_e.strftime("%H")) - int(hour_s.strftime("%H"))
                    sub = Matiere.objects.get(id=id_sub)
                    hour_update = sub.taux_horaire - diff
                    sub.taux_horaire = hour_update 
                    sub.save()
                    try:
                        dispo = Disponibilite.objects.filter(formateur_id=id_teach,date_dispo=date,heure_deb=hour_s,heure_fin=hour_e)
                        for d in dispo :
                            id_dispo = d.id
                        dispo_model = Disponibilite.objects.get(id=id_dispo)
                        dispo_model.status = 1
                        dispo_model.save()
                    except:
                        messages.error(request,"Failed to modify the aivability!")
                        return HttpResponseRedirect("/schedule")
                except:
                    messages.error(request,"Failed to modify the subjects!")
                    return HttpResponseRedirect("/schedule")

                messages.success(request,"Successfully Added ! ")
                return HttpResponseRedirect("/schedule")
            except:
                messages.error(request,"Failed to add!")
                return HttpResponseRedirect("/schedule")
            
def schedule_add_aivability(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        form=AddScheduleForm1(request.POST)
        if form.is_valid():
            id_sub = form.cleaned_data["id_sub"]
            date = form.cleaned_data["date"]
            id_etu = form.cleaned_data["id_stu"]
            hour_s = form.cleaned_data["hour_s"]
            hour_e = form.cleaned_data["hour_e"]
            id_room = form.cleaned_data["id_room"] 

        
        try:
            etu_obj = Etudiants.objects.get(id=id_etu)
            sub_obj = Matiere.objects.get(id=id_sub)
            room_obj = Salle.objects.get(id=id_room)
            monday = date - timedelta(days = date.weekday())
            schedule_model = Schedule(date_jours=date,semaine_de=monday,heure_deb=hour_s,
            heure_fin=hour_e,salle_id=room_obj,etudiant_id=etu_obj,matiere_id=sub_obj)
            schedule_model.save()
            try:
                    #calculate the differenc beetwen two hours and update the related subject's hour
                diff  = int(hour_e.strftime("%H")) - int(hour_s.strftime("%H"))
                sub = Matiere.objects.get(id=id_sub)
                hour_update = sub.taux_horaire - diff
                sub.taux_horaire = hour_update 
                sub.save()
                try:
                    matiere = Matiere.objects.get(id=id_sub)    
                    id_teach = matiere.formateurId
                    dispo = Disponibilite.objects.filter(formateur_id=id_teach,date_dispo=date,heure_deb=hour_s,heure_fin=hour_e)
                    for d in dispo :
                        id_dispo = d.id
                    dispo_model = Disponibilite.objects.get(id=id_dispo)
                    dispo_model.status = 1
                    dispo_model.save()
                except:
                    messages.error(request,"Failed to modify the aivability!")
                    return HttpResponseRedirect("/schedule")
            except:
                messages.error(request,"Failed to modify the subjects!")
                return HttpResponseRedirect("/schedule")

            messages.success(request,"Successfully Added ! ")
            return HttpResponseRedirect("/schedule")
        except:
            messages.error(request,"Failed to add!")
            return HttpResponseRedirect("/schedule")
            


def schedule_list(request):
    week_search = request.GET.get('week_search')
    week_value = week_search
    schedules = []
    students_niv = []
    date_now = date.today()
    monday = date_now - timedelta(days = date_now.weekday())
    students = Etudiants.objects.values_list('id',flat=True)
    etu = Etudiants.objects.all()
    form=SearchSchedule()
    date_now = date.today()
    if week_search != '' and week_search is not None:
    #take the schedules per id_stu
        for id_stu in students:
            schedules.append(Schedule.objects.filter(Q(etudiant_id=id_stu) & Q(semaine_de= week_search )))      
    #take the niv of etu to parse in list(just to index in the template)
    else:
        for id_stu in students:
            schedules.append(Schedule.objects.filter(Q(etudiant_id=id_stu) & Q(semaine_de=monday ) ))
        week_value = monday
        
    for niv in etu:
        students_niv.append(niv.niveau_id.nom_niv) 
    context = {"schedules":schedules,"students":students_niv,"form":form,"week_value":week_value}
    return render(request,"Schedule_list.html",context)

def schedule_edit(request,id_s):
    request.session['id_s']=id_s
    form = AddScheduleForm()
    sche_e   = Schedule.objects.get(id=id_s)
    form.fields['date'].initial = sche_e.date_jours
    form.fields['id_etu'].initial = sche_e.etudiant_id .id
    form.fields['id_sub'].initial = sche_e.matiere_id.id
    form.fields['hour_s'].initial = sche_e.heure_deb.strftime("%H:%M")
    form.fields['hour_e'].initial = sche_e.heure_fin.strftime("%H:%M")
    form.fields['id_room'].initial = sche_e.salle_id.id
    context= {"form":form}
    return render(request,"Schedule_edit.html",context)    

def schedule_edit_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        id_s = request.session.get("id_s")
        form=AddScheduleForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            id_etu = form.cleaned_data["id_etu"]
            id_sub = form.cleaned_data["id_sub"]
            hour_s = form.cleaned_data["hour_s"]
            hour_e = form.cleaned_data["hour_e"]
            id_room = form.cleaned_data["id_room"]
         #query_if_teacher_is_Aivable    
    matiere = Matiere.objects.get(id=id_sub)    
    id_teach = matiere.formateurId
    dispo = Disponibilite.objects.filter(formateur_id=id_teach,date_dispo=date,heure_deb=hour_s,heure_fin=hour_e)
    is_taken = Disponibilite.objects.filter(formateur_id=id_teach,date_dispo=date,heure_deb=hour_s,heure_fin=hour_e,status=1)
        #query_if_room_is can content student
    room = Salle.objects.get(id=id_room)
    student = Etudiants.objects.get(id=id_etu)
        #query_if_room_is not aivable:
    room_aivable = Schedule.objects.filter(Q(date_jours =date) & Q(heure_deb=hour_s) & Q(heure_fin=hour_e) 
    & Q(salle_id=room) )
    if room_aivable.exists():
        messages.error(request," Room not aivable at that time")
    elif student.nb_etu > room.nb_chaise :
        messages.error(request," Room capacity smaller than student numbers, room capacity : "+ str(room.nb_chaise) + " and students number = " +str(student.nb_etu) )
        return HttpResponseRedirect("/schedule")
    elif dispo.exists() == False:
        messages.error(request,str(id_teach)+" is not aivable at (" + str((hour_s.strftime("%H:%M"))) +"  to  " + str((hour_e.strftime("%H:%M")))+" )") 
        return HttpResponseRedirect("/schedule")
    elif is_taken.exists():
        messages.error(request,str(id_teach)+" is already taken at (" + str((hour_s.strftime("%H:%M"))) +"  to  " +str((hour_e.strftime("%H:%M")))+")" )
        return HttpResponseRedirect("/schedule")
    else:
        try:
            etu_obj = Etudiants.objects.get(id=id_etu)
            sub_obj = Matiere.objects.get(id=id_sub)
            room_obj = Salle.objects.get(id=id_room)
            monday = date - timedelta(days = date.weekday())
            schedule_model = Schedule.objects.get(id=id_s)
            schedule_model.date_jours = date
            schedule_model.semaine_de = monday
            schedule_model.heure_deb = hour_s
            schedule_model.heure_fin = hour_e
            schedule_model.matiere_id = sub_obj
            schedule_model.etudiant_id  = etu_obj
            schedule_model.salle_id = room_obj
            schedule_model.save()
            del request.session['id_s']
            try:
                    #calculate the differenc beetwen two hours and update the related subject's hour
                diff  = int(hour_e.strftime("%H")) - int(hour_s.strftime("%H"))
                sub = Matiere.objects.get(id=id_sub)
                hour_update = sub.taux_horaire - diff
                sub.taux_horaire = hour_update 
                sub.save()
                try:
                    dispo = Disponibilite.objects.filter(formateur_id=id_teach,date_dispo=date,heure_deb=hour_s,heure_fin=hour_e)
                    for d in dispo :
                        id_dispo = d.id
                    dispo_model = Disponibilite.objects.get(id=id_dispo)
                    dispo_model.status = 1
                    dispo_model.save()
                except:
                    messages.error(request,"Failed to modify the aivability!")
                    return HttpResponseRedirect("/schedule")
            except:
                messages.error(request,"Failed to modify the subjects!")
                return HttpResponseRedirect("/schedule")
            messages.success(request,"Successfully Added ! ")
            return HttpResponseRedirect("/schedule")
        except:
            messages.error(request,"Failed to add!")
            return HttpResponseRedirect("/schedule")

def schedule_del(request,id_s):
    request.session['id_s']=id_s
    sche_e   = Schedule.objects.get(id=id_s)
    date_s = sche_e.date_jours
    stu = sche_e.etudiant_id  
    sub = sche_e.matiere_id  
    teach = sche_e.matiere_id.formateurId 
    hour_s = sche_e.heure_deb.strftime("%H:%M")
    hour_e = sche_e.heure_fin.strftime("%H:%M")
    room = sche_e.salle_id
    context= {"date_s":date_s,"teach":teach,"stu":stu,"sub":sub,"hour_s":hour_s,"hour_e":hour_e,"room":room}
    return render(request,"Schedule_del.html",context) 

def schedule_del_save(request):
    id_s = request.session.get("id_s")
    sche_e   = Schedule.objects.get(id=id_s)
    if request.method=='POST':
        sche_e.delete()
    return HttpResponseRedirect("/schedule")

def load_ajax(request):

    id_stud = request.GET.get('id')
    Etu = Etudiants.objects.filter(id=id_stud)
    id = []
    for  etu in Etu:
        id.append(etu.niveau_id)
    subjects = Matiere.objects.filter(niveauId=id[0])
    context = {"subjects":subjects}
    return render(request,"ajax/subjectdropdown.html",context)

def load_ajax_room(request):
    id_stud = request.GET.get('id')
    hour_s = request.GET.get('hour_s')
    hour_e = request.GET.get('hour_e')
    date_d = request.GET.get('date_d')
    Etu = Etudiants.objects.filter(id=id_stud)
    id = []
    rooms = []
    for  etu in Etu:
        id.append(etu.nb_etu)
    #filter if the nb chair and nb is compatible
    rooms_qt = Salle.objects.filter(nb_chaise__gte=id[0])
    #filter if the room is aivaible in room compatible
    for room in rooms_qt :
        room_aivable = Schedule.objects.filter(Q(date_jours=date_d) & Q(heure_deb=hour_s) & Q(heure_fin=hour_e) 
        & Q(salle_id=room.id) )
        if room_aivable.exists() == False:
            rooms.append(Salle.objects.get(id=room.id))
    context = {"rooms":rooms}
    return render(request,"ajax/roomdropdown.html",context)

def load_ajax_class(request):
    id_sub = request.GET.get('id')
    Etu = Matiere.objects.get(id=int(id_sub))
    id_i = Etu.niveauId
    levels = Etudiants.objects.filter(niveau_id=id_i)
    context = {"levels":levels}
    return render(request,"ajax/classdropdown.html",context)

def load_ajax_aivability(request):
    hour_s = request.GET.get('hour_s')
    hour_e = request.GET.get('hour_e')
    date = request.GET.get('date_d')
    id_sub = request.GET.get('sub')
    h_s = datetime.strptime(hour_s, '%H:%M').time()
    h_e = datetime.strptime(hour_e, '%H:%M').time()
    diff  = int(h_e.strftime("%H")) - int(h_s.strftime("%H")) 
    matiere = Matiere.objects.filter(Q(id=id_sub)  & Q(taux_horaire__lt=diff)  )
    matiere_o = Matiere.objects.get(id=id_sub)
    dispo = Disponibilite.objects.filter(date_dispo=date,heure_deb=hour_s,heure_fin=hour_e)
    context = {"dispo":dispo,"matiere":matiere,"matiere_o":matiere_o,"diff":diff}
    return render(request,"ajax/load_aivability.html",context)


    