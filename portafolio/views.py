from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from .models import Portafolio, Post
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout, authenticate
from .forms import *
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

#Perfil de usuario
@login_required
def Perfil(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user
        return render(request,'portafolio/perfil.html',{'user':user,'posts':posts})

#Pagina de Portafolio

def inicio(request):
    proyectos = Portafolio.objects.all()
    return render(request, 'portafolio/portfolio.html', {'proyectos':proyectos})

#Formulario para envio de email para contactarme
@login_required
def sendEmail(request):    
    if request.method == 'POST':
        name = request.POST.get('full-name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        }
        message = '''
        New message: {}

        form:{}
        '''.format(data['message'], data['email'])
        send_mail(data['subject'], message, '', ['alexisescobardev@gmail.com'])

    return render(request, 'portafolio/sendEmail.html', {})

#Pagina de incio de los Posts

def homePost(request):
    posts = Post.objects.all()
    return render(request, 'portafolio/publichome.html', {'posts':posts})
@login_required
def post(request, post_id):
    post = get_object_or_404(Post, pk= post_id)
    return render(request, 'portafolio/post.html', {'post':post})
@login_required
def postFormulario(request):
    usuario = request.user
    if request.method == 'POST':
        form = Posteos(request.POST)
        print(form)
        if form.is_valid:
            informacion = form.cleaned_data
            post = Post (titulo = informacion['titulo'],descripcion = informacion['descripcion'])
            post.user = usuario
            post.save()

            return redirect('Publi')
    else:
        form = Posteos()
        
    return render(request, 'portafolio/postFormulario.html',{'form':form})

#Buscador
@login_required
def buscar(request):
    queryset = request.GET.get('buscar')
    posts = Post.objects.all()
    if queryset:
        posts = Post.objects.filter(
            Q(titulo__icontains = queryset)
        ).distinct()
    return render(request, 'portafolio/resultado.html', {'posts':posts})

#Eliminar Post

def eliminarPost(request,titulo):
    publicaion = Post.objects.get(titulo=titulo)
    publicaion.delete()
    return render(request,'portafolio/delete.html')

#Editar Post

def editarPost(request, titulo):
    posteos = Post.objects.get(titulo=titulo)

    if request.method == 'POST':
        miFormulario = Posteos(request.POST)
        print(miFormulario)
        if miFormulario.is_valid:
            informacion = miFormulario.cleaned_data

            posteos.titulo = informacion['titulo']
            posteos.descripcion = informacion['descripcion']
            posteos.save()
            return render(request, "portafolio/edicion.html")
    else: 
        miFormulario= Posteos(initial={'titulo': posteos.titulo, 'descripcion':posteos.descripcion})

    return render(request, "portafolio/editPost.html", {"miFormulario":miFormulario, "titulo":titulo})

# Login, register, editar perfil

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contraseña = form.cleaned_data.get('password')
            user = authenticate(username=usuario,password=contraseña)
            if user is not None:
                login(request, user)
                return render(request, "portafolio/login.html", {"mensaje":f"Bienvenido {usuario}"})
            else:
                return render(request, "portafolio/login.html",{"mensaje":"Error, datos incorrectos"})
        else:
            return render(request, "portafolio/login.html", {"mensaje":"Error, formulario incorrrecto"})
    form = AuthenticationForm()

    return render(request, "portafolio/login.html", {'form':form})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            messages.success(request, 'Cuenta creada de ' + username)
            return redirect('Login')
    else:
        form = UserRegisterForm()

    return render(request, "portafolio/register.html", {'form':form})

def editarPerfil(request):
    usuario = request.user
    if request.method == 'POST':
        Formulario = UserEditForm(request.POST)
        if Formulario.is_valid():
            informacion = Formulario.cleaned_data
            
            usuario.first_name = informacion['first_name']
            usuario.last_name = informacion['last_name']
            usuario.email = informacion['email']
            usuario.password1 = informacion['password1']
            usuario.password2 = informacion['password2']
            usuario.save()
            return render(request, 'portafolio/edicionPerfil.html')
    else:
        Formulario = UserEditForm(initial={'email':usuario.email})
    
    return render(request, "portafolio/editPerfil.html", {"Formulario": Formulario, "usuario": usuario})
