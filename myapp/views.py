from audioop import reverse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from myapp.forms import RegisterForm
from myapp.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from userprofile.models import Profile
from itertools import chain
from django.views.generic.edit import DeleteView

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


def register(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            form.save()
            # user = form.save()
            return redirect('login')
        else:
            msg = 'Error occured during registration'
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('login')
    template_name = 'myapp/user_delete_confirm.html'


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


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        results = User.objects.filter(username__contains = searched)
        return render(request, 'myapp/search.html', {'searched':searched,'results':results})
    else:
        return render(request, 'myapp/search.html')


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
    # sort and chain querys and unpack the tickets list

    if len(tickets)>0:
        ts = sorted(chain(*tickets), reverse=True, key=lambda obj: obj.created_at)
    return render(request,'ticket.html',{'profile':profile,'tickets':ts})











