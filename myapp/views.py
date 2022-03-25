from multiprocessing import context
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import MyPasswordResetForm, ProfileUpdateForm, RegistrationForms, UserUpdateForm
from django.views import View


# from django.views.generic import CreateView
# from django.shortcuts import render

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Recheck your password')

    context = {'page' : page}
    return render(request, 'myapp/login.html', context)

def logoutUser(request):
            logout(request)
            return redirect('login')

# def registerPage(request):
#     form = RegistrationForms()

#     if request.method == 'POST':
#         form = RegistrationForms(request.POST)
#         if form.is_valid():
#             messages.success(request,'Successfully registered')
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             form.save()
#             login(request, user)
#             return redirect('login')
#         else:
#             messages.error(request, 'An error occured during registration.')
    
#     return render(request, 'myapp/register.html', {'form': form})


def main(request):
    return render(request, 'main.html')

def ticketPage(request):
    return render(request, 'ticket.html')

class registerpageView(View):
    def get(self, request):
        form = RegistrationForms()
        return render(request,'myapp/register.html',{'form':form})

    def post(self,request):
        form = RegistrationForms(request.POST)
        if form.is_valid():
            messages.success(request,'You have been succesfully registered!')
            form.save()
        return render(request,'myapp/register.html',{'form':form})

# class registerManagerpageView(View):
#     def get(self, request):
#         form = RegistrationForms()
#         return render(request,'myapp/register.html',{'form':form})

#     def post(self,request):
#         form = RegistrationForms(request.POST)
#         if form.is_valid():
#             messages.success(request,'You have been succesfully registered!')
#             is_manager = True
#             form.save()
#         return render(request,'myapp/registervenuemanager.html',{'form':form})

