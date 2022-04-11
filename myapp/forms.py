from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
# from django.contrib.auth.models import User
from myapp.models import User
from userprofile.models import Post
from django.views.generic import ListView, DetailView, CreateView


# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()
#     username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
#     email = forms.CharField(required= True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    
#     class Meta:
#         model = User
#         fields = ['username', 'email']

# class ProfileUpdateForm(forms.ModelForm):
#     bio = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Bio'}))
#     class Meta:
#         model = Profile
#         fields = ['bio']

# class ProfilePicUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image']


# class PostUpload(CreateView):
#     model = Post
#     fields = ['image','description']

#     def form_valid(self,form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)

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
    # is_manager = forms.CheckboxInput(widget=forms.CheckboxInput(attrs={'class':'control control--checkbox mb-0','label':'Register as Manager'}))
    # is_customer = forms.BooleanField(widget = forms.CheckboxInput(attrs={'class':'checkbox form-control'}))
    # is_manager = forms.BooleanField(widget = forms.CheckboxInput(attrs={'class':'required checkbox form-control'}))
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

# class PostUpload(CreateView):
#     model = Post
#     fields = ['image','description']

#     def form_valid(self,form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)