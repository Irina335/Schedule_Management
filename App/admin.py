from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from App.models import *
# Register your models here.
class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)
admin.site.register(Matiere)
admin.site.register(Etudiants)
admin.site.register(Schedule)
admin.site.register(Niveau)

