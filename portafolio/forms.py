from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from .models import Perfil, Post

class Posteos(forms.Form):
    titulo = forms.CharField(max_length=150)
    descripcion = forms.CharField(max_length=100000)
    class Meta:
        model = Post
        fields = ['titulo','descripcion']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget = forms.PasswordInput)
    password2 = forms.CharField(label='Repetir contraseña', widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        help_texts = {k:"" for k in fields}

class UserEditForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField
    email= forms.EmailField(label='Modificar E-mail')
    password1: forms.CharField(label='Password',widget=forms.PasswordInput)
    password2: forms.CharField(label='Repeat Password',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password1','password2']
        help_texts = {k: "" for k in fields}