
from xml.etree.ElementTree import tostring
from django import forms
from App.models import *
from django.db.models import Q



class EditStudentForm(forms.Form):
    id = forms.IntegerField(label="No. Student",widget= forms.NumberInput(attrs={"class":"form-control"}))
    levels = Niveau.objects.all()
    level_list=[]
    for level in levels:
        level_field = (level.id,level.nom_niv)
        level_list.append(level_field)
    niveau =forms.ChoiceField(label="Class",choices=level_list ,widget= forms.Select(attrs={"class":"form-control"}))
    number = forms.IntegerField(label="Number of student",widget= forms.NumberInput(attrs={"class":"form-control"}))
    year_s = forms.IntegerField(label="Year of start",widget= forms.NumberInput(attrs={"class":"form-control"}))
    year_e = forms.IntegerField(label="Year of End",widget= forms.NumberInput(attrs={"class":"form-control"}))

class AddStudentForm(forms.Form):
    levels = Niveau.objects.all()
    level_list=[("","Choose class ...")]
    for level in levels:
        level_field = (level.id,level.nom_niv)
        level_list.append(level_field)
    niveau =forms.ChoiceField(label="",choices=level_list ,widget= forms.Select(attrs={"class":"form-control  ",
    "placeholder":"Enter class name ..."}))
    number = forms.IntegerField(label="",widget= forms.NumberInput(attrs={"class":"form-control",
    "placeholder":"Number of student ..."}))
    year_s = forms.IntegerField(label="",widget= forms.NumberInput(attrs={"class":"form-control",
    "placeholder":"Year of start ..."}))
    year_e = forms.IntegerField(label="",widget= forms.NumberInput(attrs={"class":"form-control",
    "placeholder":"Year of end ..."}))
    
class AddAivabilityForm(forms.Form):
    date_dispo = forms.DateField(label="Date",widget=forms.DateInput(attrs={"class":"form-control",'type': 'date'}))
    heure_deb  = forms.TimeField(label="Hour start",widget=forms.TimeInput(attrs={"class":"form-control",'type': 'time'}))
    heure_fin  = forms.TimeField(label="Hour end",widget=forms.TimeInput(attrs={"class":"form-control",'type': 'time'}))

class AddSubjectForm(forms.Form):
    name_sub =  forms.CharField(label="Subject name",widget= forms.TextInput(attrs={"class":"form-control"}))
    hour = forms.IntegerField(label="Hour rate",widget=forms.NumberInput(attrs={"class":"form-control",'type': 'number'}))
    levels = Niveau.objects.all()
    level_list=[("","---------")]
    for level in levels:
        level_field = (level.id,level.nom_niv)
        level_list.append(level_field)

    id_niv =  forms.ChoiceField(label="Class",choices=level_list ,widget= forms.Select(attrs={"class":"form-control "}))
 
    teachers = Formateur.objects.all()
    teacher_list=[("","---------")]
    for teacher in teachers:
        Teacher_field = (teacher.id,teacher.admin.first_name  + " " +  teacher.admin.last_name)
        teacher_list.append(Teacher_field)

    id_teach = forms.ChoiceField(label="Teacher",choices=teacher_list ,widget= forms.Select(attrs={"class":"form-control "}))


class AddClassForm(forms.Form):
    name_class= forms.CharField(label="Class name",widget= forms.TextInput(attrs={"class":"form-control "}))
    
class AddScheduleForm(forms.Form):
    date = forms.DateField(label= "",widget=forms.TextInput(attrs={"class":"form-control  ","placeholder":"Date ...",
    "onfocus":"(this.type='date')","id":"date_d"}))
    students = Etudiants.objects.all()
    student_list = [("","Choose a student group ...")]
    for student in students:
        student_field = (student.id,student.niveau_id)
        student_list.append(student_field)  
    
    subjects = Matiere.objects.filter(~Q(taux_horaire=0)) 
    subjects_list = [("","Choose a subject ...")]
    for subject in subjects:
        concat =  str(subject.matiere_name) +"   ("+str(subject.formateurId)+")"  
        subject_field = (subject.id,concat)
        subjects_list.append(subject_field)
    
    
    id_etu = forms.ChoiceField(label= "",choices=student_list ,widget= forms.Select(attrs={"class":"form-control","id":"etu"  }))
    id_sub  = forms.ChoiceField(label= "" ,choices=subjects_list ,widget= forms.Select(attrs={"class":"form-control ","id":"sub"}))
    hour_s  = forms.TimeField(label= "",widget=forms.TextInput(attrs={"class":"form-control col-lg-12",
    "placeholder":"Hour of start ...","onfocus":"(this.type='time')","id":"hour_s"}))
    hour_e  = forms.TimeField(label= ""  ,widget=forms.TextInput(attrs={"class":"form-control  col-lg-12",
    "placeholder":"Hour of end ...","onfocus":"(this.type='time')","id":"hour_e"}))

    rooms = Salle.objects.all()
    room_list = [("","Choose a room ...")]
    for room in rooms:
        room_field = (room.id,room.nom_salle)
        room_list.append(room_field)
    id_room  = forms.ChoiceField(label="",choices=room_list ,widget= forms.Select(attrs={"class":"form-control ","id":"room"}))

class AddScheduleForm1(forms.Form):
    date = forms.DateField(label= "",widget=forms.TextInput(attrs={"class":"form-control  ","placeholder":"Date ...",
    "onfocus":"(this.type='date')","id":"date_d"}))
    students = Etudiants.objects.all()
    student_list = [("","Choose a student group ...")]
    for student in students:
        student_field = (student.id,student.niveau_id)
        student_list.append(student_field)  
    
    subjects = Matiere.objects.filter(~Q(taux_horaire=0)) 
    subjects_list = [("","Choose a subject ...")]
    for subject in subjects:
        concat =  str(subject.matiere_name) +" ("+str(subject.formateurId)+")"  
        subject_field = (subject.id,concat)
        subjects_list.append(subject_field)

    teacher = forms.CharField(label= "",widget= forms.TextInput(attrs={"class":"form-control","id":"teacher"  }))
    id_sub  = forms.ChoiceField(label= "" ,choices=subjects_list ,widget= forms.Select(attrs={"class":"form-control ","id":"sub"}))
    id_stu = forms.ChoiceField(label= "",choices=student_list ,widget= forms.Select(attrs={"class":"form-control","id":"etu"  }))
    hour_s  = forms.TimeField(label= "",widget=forms.TextInput(attrs={"class":"form-control col-lg-12",
    "placeholder":"Hour of start ...","onfocus":"(this.type='time')","id":"hour_s"}))
    hour_e  = forms.TimeField(label= ""  ,widget=forms.TextInput(attrs={"class":"form-control  col-lg-12",
    "placeholder":"Hour of end ...","onfocus":"(this.type='time')","id":"hour_e"}))

    rooms = Salle.objects.all()
    room_list = [("","Choose a room ...")]
    for room in rooms:
        room_field = (room.id,room.nom_salle)
        room_list.append(room_field)
    id_room  = forms.ChoiceField(label="",choices=room_list ,widget= forms.Select(attrs={"class":"form-control ","id":"room"}))

class AddTeacher(forms.Form):
    first_name =  forms.CharField(label="First name",widget= forms.TextInput(attrs={"class":"form-control form-control-user "}))
    last_name =  forms.CharField(label="Last name",widget= forms.TextInput(attrs={"class":"form-control form-control-user "}))
    username =  forms.CharField(label="Username ",widget= forms.TextInput(attrs={"class":"form-control form-control-user "}))
    email = forms.CharField(label="Email ",widget= forms.EmailInput(attrs={"class":"form-control form-control-user ",'type': 'email'}))
    password =  forms.CharField(label="Password ",widget= forms.PasswordInput(attrs={"class":"form-control form-control-user ",'type': 'password'}))

class SearchSchedule(forms.Form):
    #week_search =  forms.CharField(label="", help_text="",widget= forms.TextInput(attrs={"class":"form-control bg-light border-0 small"}))
    students = Etudiants.objects.all()
    student_list = []
    for student in students:
        student_field = (student.id,student.niveau_id.nom_niv)
        student_list.append(student_field)
    class_search = forms.ChoiceField(choices=student_list ,label="", help_text="",
    initial="choose class ...", widget= forms.Select(attrs={"class":"form-control bg-light border-0 small"}))

class EditRoom(forms.Form):
    room_name =  forms.CharField(label="Room name:",widget= forms.TextInput(attrs={"class":"form-control",
    "placeholder":""}))
    seat =  forms.CharField(label="Seats:",widget= forms.TextInput(attrs={"class":"form-control ",
    "placeholder":""}))
