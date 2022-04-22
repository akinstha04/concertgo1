from django import forms
from django.utils.translation import gettext, gettext_lazy as _
# from django.contrib.auth.models import User
from myapp.models import User
from .models import Profile, Post,Comment
from django.views.generic import ListView, DetailView, CreateView


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.CharField(required= True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Bio'}))
    class Meta:
        model = Profile
        fields = ['bio']

class ProfilePicUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

        # fields = '__all__'
        # exclude = ['user']
class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control mr-3','placeholder':'Write a comment'}),
        label=_(""),
        strip=True
        )

    class Meta:
        model = Comment
        fields = ('body',)