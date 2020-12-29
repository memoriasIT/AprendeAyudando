from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class RecoverForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class UploadForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), required=False)
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_repeat', 'first_name', 'last_name']