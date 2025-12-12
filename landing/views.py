from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth import authenticate,login, logout
from landing.forms import  RegisterForm, PostForm,ProfileForm,ComentarioForm
from landing.models import Posteos, Perfil,RequestFriend,Friendship, User,Like, Comentario,Compartir
from django.db.models import Q
import hashlib
from urllib.parse import urlencode
# Create your views here.

def logoutPage(request):
     logout(request)
     return redirect('login')

def landingPage(request):
    return render (request, './index.html')

def loginPage(request):
     return redirect('two_factor:login')


def registerPage(request): 
     registerForm = RegisterForm(request.POST)
     if request.method == 'POST':
          if registerForm.is_valid():
               usuario = registerForm.save()
               perfil = Perfil(
                    user = usuario,
                    biografia = '',
                    enlaces = '',
                    preferencias = ''
               )
               perfil.save()
               return redirect('home')
          else:
               errors = {}
          for field, error_list in registerForm.errors.items():
                    errors[field] = [str(e) for e in error_list]
                    return render(request, './login/register.html',{"registerForm":registerForm, 'errors' : errors})       
     return render(request, './login/register.html',{"registerForm":registerForm}) 


     
# Funciones Posteo

def crearPosteo(request):
     if request.user.is_authenticated:
          if request.method == 'POST':
               usuario = Perfil.objects.get(pk=request.user.id)
               formulario = PostForm(request.POST)
               if formulario.is_valid():
                    formularioListo = formulario.cleaned_data
                    titulo_form = formularioListo.get('titulo')
                    contenido_form = formularioListo.get('contenido')
                    publicado_form = formularioListo.get('publicado')
                    imagen_form = request.FILES.get('image_Field')
                    posteos = Posteos(
                         titulo = titulo_form,
                         contenido = contenido_form,
                         publicado = publicado_form,
                         user = usuario,
                         image_field = imagen_form
                    )
                    posteos.save()
                    return redirect('home')     
               else:
                    errores = formulario.errors
                    return render(request,'./post/crearPost.html',{'formulario':formulario, 'errores' :errores})
                    
          else:
               formulario = PostForm()
               return render(request,'./post/crearPost.html',{'formulario':formulario})
               
     else:
          return redirect('login')

def detallePosteo(request,id):
     if request.user.is_authenticated:
          try:
               post = Posteos.objects.get(pk=id)
               comentarios = Comentario.objects.filter(posteo_original=post).order_by('-fecha')
          except Exception:
               print(Exception)
          if request.method == 'POST':
               form = ComentarioForm(request.POST)
               if form.is_valid():
                    contenido = form.cleaned_data['contenido']
                    perfil = Perfil.objects.get(user=request.user)
                    Comentario.objects.create(
                         posteo_original=post,
                         user=perfil,
                         contenido=contenido
               )
               return redirect('detallePosteo', id=id)
          else:
               form = ComentarioForm()
     
          return render(request, './post/postDetalle.html',{'form': form,'post': post, 'comentarios': comentarios})
               
     else:
          return redirect('login')
     

def home(request):
     if request.user.is_authenticated:
          try:
               todos_los_posteos = Posteos.objects.all().order_by('-fecha')
               
          except Exception:
               print(Exception)
          return render(request, './post/mostrarPost.html',{'posts': todos_los_posteos})
               
     else:
          return redirect('login')
     
def eliminarPosteo(request, id):
     posteo = Posteos.objects.get(pk=id)
     posteo.delete()
     return redirect('showProfile')

def modificarPosteo(request, id):
     posteo = Posteos.objects.get(pk=id)
     if request.method == 'POST':
          formulario = PostForm(request.POST,request.FILES)
          if formulario.is_valid():
                    formularioListo = formulario.cleaned_data
                    titulo_form = formularioListo.get('titulo')
                    contenido_form = formularioListo.get('contenido')
                    publicado_form = formularioListo.get('publicado')
                    imagen_form = request.FILES.get('image_Field')
                    posteos = Posteos.objects.get(pk=id)
                    posteos.titulo = titulo_form
                    posteos.contenido = contenido_form
                    posteos.publicado = publicado_form
                    posteos.imagen_form = imagen_form
                    posteos.save()
                    return redirect('showProfile')     
          else:
               errores = formulario.errors
               return render(request,'./post/crearPost.html',{'formulario':formulario, 'errores' :errores})
     else:
          contenidoPost = {
            'titulo': posteo.titulo,
            'contenido': posteo.contenido,
            'publicado': posteo.publicado,
            }
          
          formulario = PostForm(initial=contenidoPost)
          return render(request,'./post/crearPost.html',{'formulario':formulario})

def mostrarBorradores(request):
     if request.user.is_authenticated:
          try:
               todos_los_posteos = Posteos.objects.all()
          except Exception:
               print(Exception)
          username = request.user.username
          return render(request, './perfil/perfil.html',{'posts': todos_los_posteos, 'username' :username.rstrip()})
               
     else:
          return redirect('login')

def likePost(request,id):
     if request.user.is_authenticated:
          username= request.user
          post = Posteos.objects.get(pk=id)
          like_filter = Like.objects.filter(post_id = id, username = username)
          if like_filter:
               like_filter.delete()
               post.nom_of_likes = post.nom_of_likes-1
               post.save()
               return redirect(request.META.get('HTTP_REFERER', '/'))
          else:
               new_like  = Like(
                    post_id = id,
                    username = username
               )
               new_like.save()
               post.nom_of_likes = post.nom_of_likes+1
               post.save()
               return redirect(request.META.get('HTTP_REFERER', '/'))
               
     else:
          return redirect('login')


# Perfil/Usuarios

def editarPerfil(request,id):
     perfil = Perfil.objects.get(pk=id)
     if request.user.is_authenticated:
          if request.method == 'POST':
               formulario = ProfileForm(request.POST, request.FILES)
               if formulario.is_valid():
                    formularioListo = formulario.cleaned_data
                    foto_perfil_form =request.FILES.get('foto_perfil')
                    biografia_form = formularioListo.get('biografia')
                    enlaces_form = formularioListo.get('enlaces')
                    preferencias_form = formularioListo.get('preferencias')
                    perfil.foto_perfil = foto_perfil_form
                    perfil.biografia = biografia_form
                    perfil.enlaces = enlaces_form
                    perfil.preferencias = preferencias_form
                    perfil.save()
                    return redirect('showProfile',id) 
               else:
                    errores = formulario.errors
                    return render(request,'./perfil/editarPerfil.html',{'formulario':formulario, 'errores' :errores})
                    
          else:
               datosPerfil = {
                    'foto_perfil':perfil.foto_perfil,
                    'biografia': perfil.biografia,
                    'enlaces': perfil.enlaces,
                    'preferencias': perfil.preferencias,
                    }
               formulario = ProfileForm(initial=datosPerfil)
               return render(request,'./perfil/editarPerfil.html',{'formulario':formulario})
               
     else:
          return redirect('login')
                    

def mostrarPerfilUsuario(request, id):
     if request.user.is_authenticated:
          try:
               todos_los_posteos = Posteos.objects.all()
               perfil = Perfil.objects.get(pk=id)
               
          except Exception:
               print(Exception)
          return render(request, './perfil/perfil.html',{'posts': todos_los_posteos, 'perfil':perfil})
               
     else:
          return redirect('login')
     


def buscarUsuario(request):
     if request.user.is_authenticated:
          if request.method == 'POST':
               busqueda =  request.POST['busqueda']
               try:
                    todos_los_posteos = Posteos.objects.filter(Q(user__user__username__contains=busqueda) | Q(user__user__email__contains=busqueda))
                    todos_los_perfiles = Perfil.objects.filter(Q(user__username__icontains=busqueda) | Q(user__email__icontains=busqueda)| Q(preferencias__icontains=busqueda))
                    friend_requests = RequestFriend.objects.all()
               except Exception:
                    print(Exception)
               return render(request, 'resultado_busqueda.html',{'posts': todos_los_posteos, 'perfiles': todos_los_perfiles, 'friend_requests':friend_requests})
               
     else:
          return redirect('login')

# Amistad

def requestFriend(request,id):
     if request.user.is_authenticated:
          to_user = User.objects.get(pk=id)
          request_friend = RequestFriend(
               from_user = request.user,
               to_user = to_user,
               status= 'pending'        
          )
          request_friend.save()
          return redirect('home')     
          
     else:
          return redirect('login')
     
def cancelRequest(request,id):
     if request.user.is_authenticated:
          request_friend = RequestFriend.objects.get(pk=id)
          request_friend.delete()
          return redirect('showSentRequest')
     else:
               return redirect('login')
    

     
def acceptRequest(request,id):
     if request.user.is_authenticated:
          request_friend = RequestFriend.objects.get(pk=id)
          request_friend.status = 'accepted'
          request_friend.save()
          friend=Friendship(
               user1 = request_friend.from_user, 
               user2 =  request_friend.to_user
          )
          friend.save()
          return redirect('showSentRequest')
     else:
          return redirect('login')

def showFriendRequest(request):
     if request.user.is_authenticated:
          friend_request = RequestFriend.objects.filter(to_user = request.user.id)    
          profile_request = Perfil.objects.filter()

          return render(request, './friendship/request.html',{'friend_request': friend_request,'profile_request':profile_request})
          
     else:
          return redirect('login')
     
def showSentRequest(request):
     if request.user.is_authenticated:
          friend_request = RequestFriend.objects.filter(from_user = request.user.id)    
          profile_request = Perfil.objects.filter()
          return render(request, './friendship/sent_request.html',{'friend_request': friend_request,'profile_request':profile_request})
          
     else:
          return redirect('login')
     
def showFriendship(request, id):
     if request.user.is_authenticated:
          friends = Friendship.objects.filter(Q(user2__id = id)| Q(user1__id = id))    
          perfiles = Perfil.objects.all()
          return render(request, './friendship/show_friends.html',{'friends': friends,'perfiles':perfiles})
          
     else:
          return redirect('login')
     
def deleteFriendship(request, id):
     if request.user.is_authenticated:
          friend = Friendship.objects.get(pk=id)
          friend.delete()
          return redirect('showFriends',id=request.user.id)
     else:
          return redirect('login')
     
     
def eliminarComentario(request, id):
     if request.user.is_authenticated:
          comentario = Comentario.objects.get(pk=id)
          if comentario.user.user == request.user:
               comentario.delete()
               return redirect(request.META.get('HTTP_REFERER', '/'))
     else:
          return redirect('login')
    
    
def compartirPost(request, id):
    if request.user.is_authenticated:
          post = Posteos.objects.get(pk=id)
          compartidos = Compartir.objects.filter(posteo_original = id, username = request.user.username)
          if compartidos:
               compartidos.delete()
          else:
               compartir = Compartir(
                    posteo_original=post,
                    username=request.user.username
               )
               compartir.save()
          return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect('login')
   
#FUNCIONES SUGERIDOS Y TENDENCIAS
def sugerenciasPerfiles(request):
    if request.user.is_authenticated:
     perfil = Perfil.objects.get(user=request.user)
     preferencias = perfil.preferencias.split()
     query = Q()
     for palabra in preferencias:
          query |= Q(preferencias__icontains=palabra)

     sugeridos = Perfil.objects.filter(query).exclude(user=request.user).distinct()

     return render(request, 'sugerencias.html', {'perfiles': sugeridos})
    else:
        return redirect('login')
   
def tendencias(request):
    populares = Posteos.objects.filter(publicado=True).order_by('-nom_of_likes', '-fecha')[:10]
    return render(request, 'tendencias.html', {'posts': populares})


def mostrarCompartidos(request, id):
     if request.user.is_authenticated:
          try: 
               perfil = Perfil.objects.get(pk=id)
               compartidos = Compartir.objects.filter(username = perfil.user.username)
          except Exception:
               print(Exception)
          return render(request, './perfil/compartidos.html',{'perfil': perfil,'compartidos':compartidos})
               
     else:
          return redirect('login')
     
def mostrarLikes(request, id):
     if request.user.is_authenticated:
          try: 
               perfil = Perfil.objects.get(pk=id)
               likes = Like.objects.all().order_by('-fecha')
               todos_los_posteos = Posteos.objects.all()
          except Exception:
               print(Exception)
          return render(request, './perfil/likes.html',{'perfil': perfil,'likes':likes,'posts':todos_los_posteos})
               
     else:
          return redirect('login')