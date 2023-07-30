from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from App_beta.models import Client, Freelancer


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# class FreelancerProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Freelancer
#         fields = ['image']
# class ClientProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Client
#         fields = ['image']