from msilib.schema import Class
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from App.EmailBackEnd import EmailBackEnd
from App.models import *
from App.forms import *

def level(request):
    classes = Niveau.objects.all()
    form= AddClassForm()
    context ={"form":form,"classes":classes}
    return render(request,"Class.html",context)

def level_list(request):
    
    context ={}
    return render(request,"Class_list.html",context)

def level_add(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        form=AddClassForm(request.POST)
        if form.is_valid():
            name_class = form.cleaned_data["name_class"]
    try:
        niv_model = Niveau(nom_niv=name_class)
        niv_model.save()
        messages.success(request,"SuccessFully Added !")
        return HttpResponseRedirect("/class")
    except:
        messages.success(request,"Failed to Add!")
        return HttpResponseRedirect("/class")

def level_edit(request,id_class):
    request.session['id_class']=id_class
    form = AddClassForm()
    level = Niveau.objects.get(id=id_class)
    form.fields["name_class"].initial = level.nom_niv
    context= {"form":form,"id_class":id_class}
    return render(request,"Class_edit.html",context)
