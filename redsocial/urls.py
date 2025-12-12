from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from landing import views

urlpatterns = [
    path('', views.landingPage, name='landingPage'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logoutPage'),

    path('2faapp/', include(('two_factor.urls', 'two_factor'))),    

    path('home/', views.home, name='home'),

    path('perfil/<int:id>', views.mostrarPerfilUsuario, name='showProfile'),
    path('updateProfile/<int:id>', views.editarPerfil, name='updateProfile'),

    # POST URLS
    path('newPost/', views.crearPosteo, name='newPost'),
    path('post/<int:id>', views.detallePosteo, name='detallePosteo'),
    path('deletePost/<int:id>', views.eliminarPosteo, name='deletePost'),
    path('updatePost/<int:id>', views.modificarPosteo, name='updatePost'),
    path('searchPost/', views.buscarUsuario, name='searchUser'),
    path('borradores/', views.mostrarBorradores, name='showMyDrafts'),
    path('likePost/<int:id>', views.likePost, name='likePost'),
    path('eliminarComentario/<int:id>', views.eliminarComentario, name='eliminarComentario'),
    path('compartirPost/<int:id>', views.compartirPost, name='compartirPost'),
    path('compartidos/<int:id>', views.mostrarCompartidos, name='mostrarCompartidos'),
    path('likes/<int:id>', views.mostrarLikes, name='mostrarLikes'),

    path('sugerencias/', views.sugerenciasPerfiles, name='sugerencias'),
    path('tendencias/', views.tendencias, name='tendencias'),

    # AMIGOS URLS
    path('sentRequest/<int:id>', views.requestFriend, name='sentRequest'),
    path('showFriendRequest/', views.showFriendRequest, name='showFriendRequest'),
    path('showSentRequest/', views.showSentRequest, name='showSentRequest'),
    path('cancelRequest/<int:id>', views.cancelRequest, name='cancelRequest'),
    path('acceptRequest/<int:id>', views.acceptRequest, name='acceptRequest'),
    path('showFriends/<int:id>', views.showFriendship, name='showFriends'),
    path('deleteFriend/<int:id>', views.deleteFriendship, name='deleteFriends'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
