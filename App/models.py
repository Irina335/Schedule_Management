import email
from datetime import date, timedelta
from email.policy import default
from wsgiref.handlers import format_date_time

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data= ((1,"Personnel"),(2,"Prof"))
    user_type = models.CharField(default=1,choices=user_type_data,max_length=10)



class AdminPersonnel(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Formateur(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.admin.first_name} {self.admin.last_name}' 


class Niveau(models.Model):
    id = models.AutoField(primary_key=True)
    nom_niv = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_niv
    
class Matiere(models.Model):
    id = models.AutoField(primary_key=True)
    matiere_name = models.CharField(max_length=255)
    taux_horaire = models.IntegerField()
    niveauId = models.ForeignKey(Niveau,on_delete=models.SET_NULL, null=True)
    formateurId = models.ForeignKey(Formateur, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.matiere_name

class Disponibilite(models.Model):
    id = models.AutoField(primary_key=True)
    week_of = models.DateField(null=True)
    date_dispo = models.DateField()
    heure_deb = models.TimeField()
    heure_fin = models.TimeField()
    formateur_id = models.ForeignKey(Formateur, on_delete=models.CASCADE)
    status = models.IntegerField(default=0,blank=True)

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    formateur_id = models.ForeignKey(Formateur, on_delete=models.CASCADE)
    msg = models.CharField(max_length=255)
    status = models.IntegerField(default=0,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
class Etudiants(models.Model):
    id = models.AutoField(primary_key=True)
    nb_etu  = models.IntegerField()
    niveau_id = models.ForeignKey(Niveau,on_delete=models.SET_NULL, null=True)
    annee_start = models.IntegerField()
    annee_end = models.IntegerField()

    def __str__(self):
        return self.niveau_id.nom_niv

    
class Salle(models.Model):
    id = models.AutoField(primary_key=True)
    nom_salle = models.CharField(max_length=50)
    nb_chaise = models.IntegerField()
    
    def __str__(self):
        return self.nom_salle

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    date_jours = models.DateField()
    semaine_de = models.DateField(default="2022-01-01")
    heure_deb = models.TimeField()
    heure_fin = models.TimeField()
    matiere_id = models.ForeignKey(Matiere, on_delete=models.PROTECT)
    etudiant_id = models.ForeignKey(Etudiants,on_delete = models.PROTECT)
    salle_id =  models.ForeignKey(Salle,on_delete = models.PROTECT)

        
@receiver(post_save,sender=CustomUser)    
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminPersonnel.objects.create(admin=instance)
        if instance.user_type==2:
            Formateur.objects.create(admin=instance)

@receiver(post_save,sender=CustomUser)  
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminpersonnel.save()
    if instance.user_type==2:
        instance.formateur.save()
    





