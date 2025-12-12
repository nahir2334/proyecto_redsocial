from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    biografia = models.CharField(max_length=400)
    enlaces = models.CharField(max_length=500)
    preferencias = models.CharField(max_length=500)

class Posteos(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.CharField(max_length=500)
    fecha = models.DateField(auto_now_add=True)
    publicado = models.BooleanField()
    user = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=True, blank=True) 
    image_field = models.ImageField(default='null', verbose_name="image", upload_to='images')
    nom_of_likes = models.IntegerField(default=0)
    
class Comentario(models.Model):
    posteo_original = models.ForeignKey(Posteos, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=True, blank=True) 
    contenido = models.CharField(max_length=500)
    fecha = models.DateField(auto_now_add=True)
    
class Like(models.Model):
    post_id = models.IntegerField()
    username = models.CharField(max_length=500) 
    fecha = models.DateField(auto_now_add=True)
    
class Compartir(models.Model):
    posteo_original = models.ForeignKey(Posteos, on_delete=models.CASCADE, null=True, blank=True)
    username =  models.CharField(max_length=500,null=True, blank=True) 
    fecha = models.DateField(auto_now_add=True)
    

class RequestFriend(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="user_send") 
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_receive") 
    request = models.DateField(auto_now_add=True)
    status= models.CharField(max_length=200)

class Friendship(models.Model):
    user1 =models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="friend1") 
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="friend2")
    created = models.DateField(auto_now_add=True)