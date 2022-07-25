from django.contrib import admin
from .models import Perfil,Portafolio,Post

# Register your models here.
admin.site.register(Portafolio)
admin.site.register(Post)
admin.site.register(Perfil)