from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class StudentForm(UserCreationForm):
    class Meta:
        model= Student
        fields= ["address","contact","email"]
        exclude= [""]