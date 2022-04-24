from django import forms
from django.utils.translation import gettext, gettext_lazy as _
# from django.contrib.auth.models import User
from myapp.models import User
from .models import Profile, Comment, Ticket



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

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control mr-3','placeholder':'Write a comment'}),
        label=_(""),
        strip=True
        )

    class Meta:
        model = Comment
        fields = ('body',)

class TicketCreate(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['image','title','detail','date','ex_date','price','quantity']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}), 'ex_date': forms.DateInput(attrs={'type': 'date'})}

        # widgets = {'image':forms.ImageField(attrs={'class':'form-control'}),'title':forms.TimeField(attrs={'class':'form-control'}),'date': forms.NumberInput(attrs={'type': 'date'}),'ex_date':forms.DateTimeInput(attrs={'class':'form-control', 'type':'date'}), 'price':forms.IntegerField(attrs={'class':'form-control'}),'quantity':forms.IntegerField(attrs={'class':'form-control'})}