from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Register(UserCreationForm):
    birth_date = forms.CharField(max_length=50)
    class Meta:
        model=User
        fields = ['username','email','password'] 

class Login(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(max_length=20)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    

class RegisterForm(UserCreationForm):
    birth_date = forms.CharField(max_length=50)
    class Meta:
        model=User
        fields = ['username','email','password1','password2'] 