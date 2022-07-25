from django.urls import path
from portafolio import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    #Pagina de Portafolio
    path('', views.inicio, name='Inicio'),
    path('contactEmail',views.sendEmail, name='Email'),

    #Perfil de Usuario
    path('perfil/<str:username>/',views.Perfil,name='Perfil'),

    #Pagina de posteos
    path('publi', views.homePost, name='Publi'),
    path('<int:post_id>',views.post,name='postDetail'),
    path('posteo',views.postFormulario,name='Posteo'),
    path('buscar/', views.buscar,name='Buscar'),
    path('elimiar/<titulo>',views.eliminarPost,name='Eliminar'),
    path('editar/<titulo>',views.editarPost,name='Editar'),

    #Login, register, edit perfil, logout
    path('login',views.login_request, name='Login'),
    path('register',views.register, name='Register'),
    path('logout',LogoutView.as_view(template_name='portafolio/portfolio.html'),name='Logout'),
    path('editPerfil',views.editarPerfil,name='EditPerfil'),
]