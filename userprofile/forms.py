from django import forms
from django.utils.translation import gettext, gettext_lazy as _
# from django.contrib.auth.models import User
from myapp.models import User
from .models import Profile, Post
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





# class TicketForm():
#     title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'title'}))
#     detail = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'detail'}))
#     date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
#     ex_date = forms.DateTimeField(required= True, widget=forms.DateTimeInput(attrs={'class':'form-control','placeholder':'Email'}))
#     price = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'price'})) 
#     image = forms.ImageField(default= 'ticket_pics\default.jpg')
#     quantity = forms.IntegerField(default= 1)

#     class Meta:
#         model=User
#         fields = ('title','detail','date','ex_date','price','image','quantity')