from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from user.models import User

class UserCreationForm(UserCreationForm):
    
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        labels = {
           'username': 'Nombre de usuario:',
           'email': 'Email:',
           'password1': 'Contraseña:',
           'password2': 'Contraseña (confirmación):',
        }


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise forms.ValidationError('Completa tu email.')
        
        try:
            exist = User.objects.get(email = email)
        except Exception as e:
            exist = False
       
        if exist:
            raise forms.ValidationError('El email está siendo usado.')

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            raise forms.ValidationError('Ingresa un nombre de usuario.')

        return username