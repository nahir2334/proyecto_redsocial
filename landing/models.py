from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    foto_perfil = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    biografia = models.CharField(max_length=400, blank=True)
    enlaces = models.CharField(max_length=500, blank=True)
    preferencias = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


class Posteos(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.CharField(max_length=500)
    fecha = models.DateField(auto_now_add=True)
    publicado = models.BooleanField(default=True)
    user = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=True, blank=True)
    image_field = models.ImageField(upload_to="images", default="null", verbose_name="image")
    nom_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    posteo_original = models.ForeignKey(Posteos, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=True, blank=True)
    contenido = models.CharField(max_length=500)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.user.user.username} en {self.posteo_original.titulo}"


class Like(models.Model):
    post = models.ForeignKey(Posteos, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Like de {self.user.user.username} en {self.post.titulo}"


class Compartir(models.Model):
    posteo_original = models.ForeignKey(Posteos, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} compartió {self.posteo_original.titulo}"


class RequestFriend(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_send")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_receive")
    request = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Solicitud de {self.from_user.username} para {self.to_user.username}"


class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="friend1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="friend2")
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.username} es amigo de {self.user2.username}"
