from django import forms
from django.contrib.auth.models import User
from .models import LoginCacthModel

class FormularioSingup(forms.Form):
    email = forms.EmailField(label="email")
    senha = forms.PasswordInput()
    nome = forms.CharField()
    sobrenome = forms.CharField()
    usuario = forms.CharField()


class FormularioLogin(forms.Form):
    email = forms.EmailField(label="email")
    senha = forms.PasswordInput()


class FormularioAnalise(forms.Form):
    termo_busca = forms.CharField(label="termo_busca")
    quantidade_produtos = forms.IntegerField()


class LoginCatchForm(forms.ModelForm):
    class Meta:
        model = LoginCacthModel()
        fields = {'email', 'senha'}