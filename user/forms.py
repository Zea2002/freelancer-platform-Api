from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FreelancerProfile, ClientProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = '__all__'
        exclude = ['user', 'balance']

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = '__all__'
        exclude = ['user', 'balance']
