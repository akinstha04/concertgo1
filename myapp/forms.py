from cProfile import label
from pyexpat import model
from xml.etree.ElementTree import Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
# from django.contrib.auth.models import User
from myapp.models import User
from userprofile.models import Post, Comment, Ticket
from django.views.generic import ListView, DetailView, CreateView


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class':'form-control'}),
    )

    
class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    email = forms.CharField(required= True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    class Meta:
        model=User
        fields = ('username','email','password1','password2','is_manager')




# class RegistrationForms(UserCreationForm): #inheriting usercreationform
#     username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
#     email = forms.CharField(required= True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
#     # email = forms.EmailField(required= True,max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
#     phone = forms.IntegerField(required= True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone number'}))
#     class Meta:#model form
#         model = User
#         fields = ['username','email','password1','password2','phone']
#         # widgets = {'username': forms.TextInput(attrs={'class':'form-control','placeholder':'username'})}

class MyPasswordResetForm(PasswordResetForm):
  email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email','class':'form-control','placeholder':'Email'})
    )

class MySetPasswordForm(SetPasswordForm):
    newpassword12 = forms.CharField(
        label=_("New password 1"),
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'New password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    newpassword22 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password confirmation'}),
    )


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control mr-3','placeholder':'Write a comment'}),
        label=_(""),
        strip=True
        )

    class Meta:
        model = Comment
        fields = ('body',)
        
        
        # widgets= {
        #     'body': forms.TextInput(attrs={'class'})
        # }


class TicketForm(forms.ModelForm):
    model = Ticket
    fields = ['image','title','detail','date','ex_date','price','quantity']

    # date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control'})),
    # ex_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'form-control'})),


    # widgets = {
    #         'title': forms.TextInput(attrs={'class': 'form-control'}),
    #         'detail': forms.TextInput(attrs={'class': 'form-control'}),
    #         'date': forms.DateInput(
    #             format=('%Y-%m-%d'), attrs={
    #                 'class': 'form-control', 
    #                 'placeholder': 'Select a date',
    #                 'type': 'date'
    #             }),
    #         'ex_date': forms.DateTimeInput(
    #             format=('%Y-%m-%d'), attrs={
    #                 'class': 'form-control', 
    #                 'placeholder': 'Select a date',
    #                 'type': 'date'
    #             }),
    #         'price': forms.IntegerField(attrs={'class': 'form-control'}),
            
    #         'quantity': forms.IntegerField(attrs={'class': 'form-control'}),
    #     }