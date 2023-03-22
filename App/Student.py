from tkinter.tix import Form
from django.contrib import messages
from urllib import request
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from App.EmailBackEnd import EmailBackEnd
from App.models import *
from App.forms import *

def student(request):
    form=AddStudentForm()
    levels = Niveau.objects.all()
    students = Etudiants.objects.all()
    context={"levels":levels,"students":students,"form":form}
    return render(request,"Student.html",context)

def student_add(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        form=AddStudentForm(request.POST)
        if form.is_valid():
            niveau = form.cleaned_data["niveau"]
            number = form.cleaned_data["number"]
            year_s = form.cleaned_data["year_s"]
            year_e = form.cleaned_data["year_e"]
    try:
        niv_obj = Niveau.objects.get(id=niveau)
        student_model = Etudiants(niveau_id= niv_obj,nb_etu=number,annee_start=year_s,annee_end=year_e)
        student_model.save()
        messages.success(request,"Successfully added")
        return HttpResponseRedirect("/student")
    except:
        messages.error(request,"Failed to Add !")
        return HttpResponseRedirect("/student")

def student_edit(request,id_etu):
    request.session['id_etu']=id_etu
    form = EditStudentForm()
    student_e   = Etudiants.objects.get(id=id_etu)
    form.fields['id'].initial = student_e.id
    form.fields['niveau'].initial = student_e.niveau_id.id
    form.fields['number'].initial = student_e.nb_etu
    form.fields['year_s'].initial = student_e.annee_start
    form.fields['year_e'].initial = student_e.annee_end
    context= {"student_e":student_e,"form":form}
    return render(request,"Student_Edit.html",context)

def student_edit_save(request):
    if request.method !='POST':   
       return HttpResponse("Method not allowed")
    else:
        id_etu = request.session.get("id_etu")
        if id_etu == None:
            return HttpResponseRedirect("/student")
        form=EditStudentForm(request.POST)
        if form.is_valid():
            niveau = form.cleaned_data["niveau"]
            number = form.cleaned_data["number"]
            year_s = form.cleaned_data["year_s"]
            year_e = form.cleaned_data["year_e"]

            try:
                student_model = Etudiants.objects.get(id=id_etu)
                student_model.nb_etu = number
                niv_obj = Niveau.objects.get(id=niveau)
                student_model.niveau_id = niv_obj
                student_model.annee_start = year_s
                student_model.annee_end = year_e
                student_model.save()
                del request.session['id_etu']
                messages.success(request,"SuccessFully Modified !")
                return HttpResponseRedirect("/student")
            except:
                messages.error(request,"Failed to Modify!")
                return HttpResponseRedirect("/student")
        else: 
            form = EditStudentForm()
            student_e   = Etudiants.objects.get(id=id_etu)
            context= {"student_e":student_e,"form":form}
        return render(request,"Student_Edit.html",context)