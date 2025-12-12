from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
# from .models import 

class CustomTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
            kwargs.setdefault('attrs', {})#['class'] = 'tu-clase-css-aqui'
            super(CustomTextInput, self).__init__(*args, **kwargs)

class RegisterForm(UserCreationForm):
        username = forms.CharField(widget=CustomTextInput(
         attrs={
            'placeholder':'Usuario',
            'class': 'input'},
            
        ))
        email=forms.EmailField(widget=CustomTextInput(
         attrs={
            'placeholder':'Email',
            'class': 'input'},
            
    ))
        first_name = forms.CharField(widget=CustomTextInput(
         attrs={
            'placeholder':'Nombre',
            'class': 'input'},
            
    ))
        last_name = forms.CharField(widget=CustomTextInput(
         attrs={
            'placeholder':'Apellido',
            'class': 'input'},
            
    ))
        password1 = forms.CharField(widget=CustomTextInput(
         attrs={
            'placeholder':'Contraseña',
            'class': 'input',
            'type' : 'password'},
            
    ))
        password2 = forms.CharField(widget=CustomTextInput(
         attrs={
            'placeholder':'Contraseña',
            'class': 'input',
            'type' : 'password'},
            
    ))
    
        class Meta:   
            model = User
            fields = ['username','email','first_name','last_name','password1','password2']
 
class PostForm(forms.Form):
    titulo = forms.CharField(
        label = 'titulo',
        max_length = 200,
        required = True,
        widget = CustomTextInput(
            attrs = {
                'placeholder':'titulo',
                'class': 'input'},
            
        ),
    )
    contenido = forms.CharField(
        label='contenido', 
        max_length= 500, 
        required=True,
        widget= forms.Textarea,
    )
    
    options = [
       (1,'Si'),
       (0, 'No'), 
    ]
    
    publicado = forms.TypedChoiceField(
            label= 'publicar',
            choices= options,
    )
    
    image_Field = forms.ImageField(
        label= 'imagen_Fields',
        required= False
    )
    
class ProfileForm(forms.Form):
    foto_perfil = forms.ImageField(
        label= 'foto_perfil',
        required= False
    )
    biografia = forms.CharField(
        label = 'biografia',
        max_length = 400,
        required= False,
        widget= forms.Textarea,
    )
    enlaces = forms.CharField(
        label='enlaces', 
        max_length= 500, 
        required= False,
        widget= forms.Textarea,
    )
    
    preferencias =forms.CharField(
        label='preferencias', 
        max_length= 500, 
        required= False,
        widget= forms.Textarea,
    )
    

    
class ComentarioForm(forms.Form):
    contenido = forms.CharField(
        label='Comentario',
        max_length=300,
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Escribe un comentario...',
            'class': 'input',
            'rows': 4,
        })
)