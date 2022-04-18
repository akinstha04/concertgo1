from audioop import reverse
import datetime
from multiprocessing import context
from xml.etree.ElementTree import Comment
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
# from django.contrib.auth.models import User
from myapp.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, CommentForm
from django.views import View
from userprofile.models import Post, Profile, Ticket, Wishlist
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from itertools import chain
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django import forms

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


    ticketsW = Wishlist.objects.filter(user=request.user).order_by('-id')
    # sort and chain querys and unpack the posts list

    if len(tickets)>0:
        ts = sorted(chain(*tickets), reverse=True, key=lambda obj: obj.created_at)
    return render(request,'ticket.html',{'profile':profile,'tickets':ts,'wishlist':ticketsW})



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

class PostListView(ListView):
    model = Post
    template_name = 'main.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetail(DetailView):
    model=Post
    pk ="pk"
    count_hit = True
    form = CommentForm
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user.profile
            form.instance.post = post
            form.save()

            return redirect(reverse("postDetail",kwargs={
                "pk": post.pk
            }))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        return context
    # template_name = 'userprofile/post_detail.html'
    # pk="pk"
    # count_hit = True
    # def post (self,request,*args,**kwargs):
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         post = self.get_object()
    #         form.instance.user = request.user
    #         form.instance.post = post
    #         form.save()
            
    #         return redirect(reverse("post",kwargs={'pk':post.pk}))
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["form"] = self.form
    #     return context


    # template_name = 'post_detail.html'
    # def get_context_data(self, *args, **kwargs):
    #     post = get_object_or_404(Post,id = self.kwargs['pk'])
    #     likes = post.total_likes()
        
    #     liked = False
    #     if post.likes.filter(id=self.request.user.profile.id).exists():
    #         liked = True

    #     context["likes"] = likes
    #     context["liked"] = liked
    #     return context

class PostUpload(CreateView):
    model = Post
    fields = ['image','detail']

    def form_valid(self,form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)
    
class PostUpdate(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['detail']
    
    def form_valid(self, form):
        form.instance.owner.profile = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.owner:
            return True
        return False

    
class PostDelete(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.owner:
            return True
        return False


class TicketListView(ListView):
    model = Ticket
    template_name = 'main.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class TicketDetail(DetailView):
    model=Ticket

class TicketUpload(CreateView):
    model = Ticket
    fields = ['image','title','detail','date','ex_date','price','quantity']

    # date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))   
    
    # widgets = {
    #     'date': forms.DateField(attrs={'class':'form-control'}),
    #     'ex_date': forms.DateTimeField(attrs={'class':'form-control'}),
    # }


    def form_valid(self,form):
        form.instance.seller = self.request.user.profile
        return super().form_valid(form)

class TicketUpdate(UserPassesTestMixin, UpdateView):
    model = Ticket
    fields = ['title','detail']
    
    def form_valid(self, form):
        form.instance.seller.profile = self.request.user
        return super().form_valid(form)

    def test_func(self):
        ticket = self.get_object()
        if self.request.user.profile == ticket.seller:
            return True
        return False

class TicketDelete(UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = '/'
    def test_func(self):
        ticket = self.get_object()
        if self.request.user.profile == ticket.seller:
            return True
        return False

# def main(request):
#     profile = Profile.objects.get(user=request.user)
#     users = [user for user in profile.following.all()]
#     posts = []
#     qs = None
#     # get posts of people who are followed
#     for u in users:
#         p = Profile.objects.get(user=u)
#         p_posts = p.post_set.all()
#         posts.append(p_posts)
#     # self posts
#     my_posts = profile.profile_posts()
#     posts.append(my_posts)
#     # sort and chain querys and unpack the posts list
#     if len(posts)>0:
#         qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.date_posted)
#     return render(request,'main.html',{'profile':profile,'posts':qs})

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


def likePost(request, pk):
    post = get_object_or_404(Post, id = request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.profile.id).exists():
        post.likes.remove(request.user.profile)
        liked = False
    else:
        post.likes.add(request.user.profile)
        liked = True
    return HttpResponseRedirect(reverse('main'))
    # return HttpResponseRedirect(reverse('postDetail',args = [str(pk)]))

# class AddComment(CreateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = 'post_detail.html'

#     def form_valid(self,form):
#         form.instance.post_id = self.kwargs['pk']
#         return super().form_valid(form)
#     success_url = reverse_lazy('postDetail')

class AddComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'userprofile/post_detail.html'

    def form_valid(self,form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user.profile
        return super().form_valid(form)
    success_url = reverse_lazy('postDetail')
    
    
def addWishlist(request):
    # ticket = get_object_or_404(Ticket, id = request.POST.get('ticket_id'))
    tid = request.GET['ticket']
    ticket = Ticket.objects.get(pk=tid)
    data = {}
    checkw = Wishlist.objects.filter(ticket=ticket, user=request.user).count()
    ticketsW = Wishlist.objects.filter(user=request.user).order_by('-id')
    if checkw>0:
        data={
            'bool':False
        }
    else:
        wishlist=Wishlist.objects.create(
            ticket=ticket,
            user=request.user
        )
        data={
            'bool':True,
        }
    return JsonResponse(data)

     
def removeWishlist(request):
    # ticket = get_object_or_404(Ticket, id = request.POST.get('ticket_id'))
    tid = request.GET['ticket']
    a = Wishlist.objects.get(Q(ticket=tid) & Q(user=request.user))
    a.delete()
    # print("akinakinakin")
    data={
        'bool':True
    }
    return JsonResponse(data)