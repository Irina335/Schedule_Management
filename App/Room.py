from django.contrib import messages
from urllib import request
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from App.EmailBackEnd import EmailBackEnd
from App.models import *
from App.forms import *
from django.db.models import Q
from datetime import  date

def room(request):
    form = EditRoom()
    salles = Salle.objects.all()
    context = {"form":form,"salles":salles}
    return render(request,"Salle.html",context)

def room_list(request):
    date_search = request.GET.get('date_search')
    date_value = date_search
    schedules = []
    salles = Salle.objects.values_list('id',flat=True)
    s = Salle.objects.values_list('nom_salle',flat=True)
    nom_salles = []
    date_now = date.today()
    if date_search != '' and date_search is not None:
        for id_s in salles:
            schedules.append(Schedule.objects.filter(Q(salle_id=id_s) & Q(semaine_de=date_search )))      
    else:
        for id_s in salles:
            schedules.append(Schedule.objects.filter(Q(etudiant_id=id_s) & Q(date_jours=date_now )))
        date_value = date.today()
    for n in s:
        nom_salles.append(n)
        

    context = {"schedules":schedules,"salles":nom_salles,"date_value":date_value}
    return render(request,"Salle_sort.html",context)

def room_add(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        form = EditRoom((request.POST))
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            seat = form.cleaned_data['seat']
    try:
        room_model = Salle(nom_salle=room_name,nb_chaise=seat)
        room_model.save()
        messages.success(request,"Successfully added !")
        return HttpResponseRedirect("/salle")
    except:
        messages.error(request,"Failed to add!")
       # return HttpResponseRedirect("/salle")

def room_edit(request,salle_id):
    request.session['salle_id']=salle_id
    form = EditRoom()
    room   = Salle.objects.get(id=salle_id)
    form.fields['room_name'].initial = room.nom_salle
    form.fields['seat'].initial = room.nb_chaise
    context= {"room":room,"form":form}
    return render(request,"Salle_Edit.html",context)

def room_edit_save(request):
    if request.method !='POST':   
       return HttpResponse("Method not allowed")
    else:
        salle_id = request.session.get("salle_id")
        if salle_id == None:
            return HttpResponseRedirect("/salle")
        form=EditRoom(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data["room_name"]
            seat = form.cleaned_data["seat"]
    try:
        room_model = Salle.objects.get(id=salle_id)
        room_model.nom_salle = room_name
        room_model.nb_chaise = seat
        room_model.save()
        del request.session['salle_id']
        messages.success(request,"Successfully modified !")
        return HttpResponseRedirect("/salle")
    except:
        messages.error(request,"Failed to modify!")
        return HttpResponseRedirect("/salle")
