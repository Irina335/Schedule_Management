from sqlite3 import Cursor
from django.contrib import messages
from urllib import request
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from App.EmailBackEnd import EmailBackEnd
from App.models import *
from App.forms import *
from django.db.models import Q

def subject(request):
    search = request.GET.get('search')
    form=AddSubjectForm()
    subjects = Matiere.objects.all()
    context = {"form":form,"subjects":subjects}
    return render(request,"Matiere.html",context)

def subject_list(request):
    subjects = Matiere.objects.all()
    context = {"subjects":subjects}
    return render(request,"subject_list.html",context)

def subject_add(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        form=AddSubjectForm(request.POST)
        if form.is_valid():
            name_sub = form.cleaned_data["name_sub"]
            hour = form.cleaned_data["hour"]
            niveau = form.cleaned_data["id_niv"]
            teacher = form.cleaned_data["id_teach"]
    try:     
        niv_obj = Niveau.objects.get(id=niveau)
        teach_obj = Formateur.objects.get(id=teacher)
        subject_model = Matiere(matiere_name=name_sub,taux_horaire=hour,niveauId=niv_obj,formateurId=teach_obj)
        subject_model.save()
        messages.success(request,"SuccessFully Added !")
        return HttpResponseRedirect("/subjects")
    except:
        messages.error(request,"Failed to Add !")
        return HttpResponseRedirect("/subjects")

    