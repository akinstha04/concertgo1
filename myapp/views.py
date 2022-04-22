from audioop import reverse
import datetime
from multiprocessing import context
from xml.etree.ElementTree import Comment
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from myapp.forms import RegisterForm
from myapp.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from django.views import View
from userprofile.models import Post, Profile, Ticket, Wishlist
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from itertools import chain


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


# def main(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'main.html', context)






# class registerpageView(View):
#     def get(self, request):
#         form = RegisterForm()
#         return render(request,'myapp/register.html',{'form':form})

#     def post(self,request):
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             # messages.success(request,'You have been succesfully registered!')
#             form.save()
#             return redirect('login')
#         return render(request,'myapp/register.html',{'form':form})


def register(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        else:
            msg = 'Error occured during registration'
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})




def ticketPage(request):
    profile = Profile.objects.get(user=request.user)
    users = [user for user in profile.following.all()]
    tickets = []
    ts = None
    # get posts of people who are followed
    for u in users:
        p = Profile.objects.get(user=u)
        p_tickets = p.ticket_set.all()
        tickets.append(p_tickets)
    # self posts
    my_tickets = profile.profile_tickets()

    tickets.append(my_tickets)


    # ticketsW = Wishlist.objects.filter(user=request.user).order_by('-id')


    # sort and chain querys and unpack the tickets list

    if len(tickets)>0:
        ts = sorted(chain(*tickets), reverse=True, key=lambda obj: obj.created_at)
    return render(request,'ticket.html',{'profile':profile,'tickets':ts})



# def ticketAddPage(request):
#     return render(request, 'myapp/ticket_add.html')

    
# def main(request):
#     return render(request, 'main.html')

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        results = User.objects.filter(username__contains = searched)
        return render(request, 'myapp/search.html', {'searched':searched,'results':results})
    else:
        return render(request, 'myapp/search.html')



# def main(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'main.html', context)




def main(request):
    profile = Profile.objects.get(user=request.user)
    users = [user for user in profile.following.all()]
    posts = []
    tickets = []
    qs = None
    ts = None
    # get posts of people who are followed
    for u in users:
        p = Profile.objects.get(user=u)
        p_posts = p.post_set.all()
        posts.append(p_posts)

        p_tickets = p.ticket_set.all()
        tickets.append(p_tickets)
    # self posts
    my_posts = profile.profile_posts()
    my_tickets = profile.profile_tickets()
    posts.append(my_posts)
    tickets.append(my_tickets)
    # sort and chain querys and unpack the posts list
    if len(posts)>0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.date_posted)

    if len(tickets)>0:
        ts = sorted(chain(*tickets), reverse=True, key=lambda obj: obj.created_at)
    return render(request,'main.html',{'profile':profile,'posts':qs,'tickets':ts})



