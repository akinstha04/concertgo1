from itertools import chain
from operator import truediv
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse, reverse_lazy


from .forms import CommentForm, ProfilePicUpdateForm, ProfileUpdateForm, UserUpdateForm, ProfilePicUpdateForm
from django.views.generic import ListView, DetailView, CreateView
from .models import Comment, Post, Profile, Ticket, Wishlist, Like

from django.shortcuts import get_object_or_404, redirect, render
from myapp.models import User
from django.contrib import messages

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# Create your views here.
# def profilePage(request):
#     return render(request, 'userprofile/profile.html')


def profilePage(request):
    profile = Profile.objects.get(user=request.user)
    posts = []
    tickets = []
    qs = None
    ts = None
    following= profile.following.all().count()
    followers= profile.followers.all().count()

    # self posts
    my_posts = profile.profile_posts()
    posts.append(my_posts)
    my_tickets = profile.profile_tickets()
    tickets.append(my_tickets)

    post_count = len(my_posts)
    # sort and chain querys and unpack the posts list
    if len(posts)>0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.date_posted)

    if len(tickets)>0:
        ts = sorted(chain(*tickets), reverse=True, key=lambda obj: obj.created_at)
    return render(request,'userprofile/profile.html',{'profile':profile,'posts':qs, 'following':following,'post_count':post_count,'tickets':ts,'followers':followers})




class ProfileVisit(DetailView):
    model = Profile
    template_name = 'userprofile/profile_visit.html'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        viewProfile = Profile.objects.get(pk = pk)
        return viewProfile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viewProfile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        if viewProfile in my_profile.following.all():
            follow = True
        else:
            follow = False
        context["follow"] = follow
        context["followers"] = self.get_object().total_followers()
        context['following'] = self.get_object().total_following()
        context["posts"] = self.get_object().profile_posts()
        context["tickets"] = self.get_object().profile_tickets()
        context['post_count'] = self.get_object().profile_posts().count()
        
        return context





@login_required
def profileUpdate(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        pp_form = ProfilePicUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid() and pp_form.is_valid:
            u_form.save()
            p_form.save()
            pp_form.save()
            # messages.success(request, 'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        pp_form = ProfilePicUpdateForm()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'pp_form': pp_form
    }
    return render(request, 'userprofile/profile_update.html', context)



    



# def follow_unfollow_profile(request):
#     if request.method=="POST":
#         my_profile = Profile.objects.get(user=request.user)
#         pk = request.POST.get('profile_pk')
#         obj = Profile.objects.get(pk=pk)

#         if obj.user in my_profile.following.all():
#             my_profile.following.remove(obj.user)
#         else:
#             my_profile.following.add(obj.user)
#         return redirect(request.META.get('HTTP_REFERER'))
#     return redirect('userprofile/profile_visit.html')

def follow_unfollow_profile(request):
    if request.method=="POST":
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
            obj.user.profile.followers.remove(my_profile.user)
        else:
            my_profile.following.add(obj.user)
            obj.user.profile.followers.add(my_profile.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('userprofile/profile_visit.html')


def follow(request, pk):
    profile = get_object_or_404(Profile, id = request.POST.get('profile_id'))
    my_profile = Profile.objects.get(user=request.user)
    follow = False
    # if profile.followers.filter(id=my_profile.id).exists():
    if my_profile in profile.followers:
        profile.followers.remove(request.user)
        my_profile.following.remove(profile.user)
        follow = False
    else:
        profile.followers.add(request.user)
        my_profile.following.add(profile.user)
        follow = True
    # return HttpResponseRedirect(reverse('profileVisit'))
    return HttpResponseRedirect(reverse('profileVisit',args = [str(pk)]))


def ticketWishlistPage(request):
    profile = Profile.objects.get(user=request.user)
    ticketsW = Wishlist.objects.filter(user=request.user).order_by('-id')

    return render(request,'userprofile/ticket_wishlist.html',{'profile':profile,'wishlist':ticketsW})


# def likeUnlikePost(request):
#     user = request.user
#     if request.method == 'POST':
#         post_id = request.POST.get('post_id')
#         post_obj = Post.objects.get(id=post_id)
#         profile = Profile.objects.get(user=user)
                    
#         if profile in post_obj.likes.all():
#             post_obj.likes.remove(profile)
#         else:
#             post_obj.likes.add(profile)
            
#         like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

#         if not created:
#             if like.value=='Like':
#                 like.value='Unlike'
#             else:
#                 like.value='Like'
#         else:
#             like.value='Like'

#             post_obj.save()
#             like.save()

#         data = {
#             'value': like.value,
#             'likes': post_obj.likes.all()
#         }
#         return JsonResponse(data, safe=False)
#     return redirect('main')

def likeUnlikePost(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.likes.all():
            post_obj.likes.remove(profile)
        else:
            post_obj.likes.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
                bool = True
            else:
                like.value='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()
    context = {
        'bool':True
    }
        # data = {
        #     'value': like.value,
        #     'likes': post_obj.liked.all().count()
        # }

    return JsonResponse(context)
    # return redirect('main')

# def followUnfollow(request):
#     user = request.user
#     if request.method == 'POST':
#         profile_id = request.POST.get('profile_id')
#         profile_obj = Post.objects.get(id=profile_id)
#         profilem = Profile.objects.get(user=user)

#         if profilem in profile_obj.likes.all():
#             profile_obj.likes.remove(profilem)
#         else:
#             profile_obj.likes.add(profilem)

#         like, created = Like.objects.get_or_create(user=profilem, profile_id=profile_id)

#         if not created:
#             if follow.value=='Follow':
#                 follow.value='Unfollow'
#                 bool = True
#             else:
#                 follow.value='Like'
#         else:
#             follow.value='Like'

#             profile_obj.save()
#             like.save()
#     context = {
#         'bool':True
#     }
#         # data = {
#         #     'value': like.value,
#         #     'likes': post_obj.liked.all().count()
#         # }

#     return JsonResponse(context)

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
    data={
        'bool':True
    }
    return JsonResponse(data)


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

    # widget = {
    #         'title': forms.TextInput(attrs={'class': 'form-control'}),
    #         'detail': forms.TextInput(attrs={'class': 'form-control'}),
    #         'date': forms.DateInput(
    #             format=('%Y-%m-%d'), attrs={
    #                 'class': 'form-control', 
    #                 'placeholder': 'Select a date',
    #                 'type': 'date'
    #             }),
    #         'ex_date': forms.DateInput(
    #             format=('%Y-%m-%d'), attrs={
    #                 'class': 'form-control', 
    #                 'placeholder': 'Select a date',
    #                 'type': 'date'
    #             }),
    #         'price': forms.IntegerField(attrs={'class': 'form-control'}),
            
    #         'quantity': forms.IntegerField(attrs={'class': 'form-control'}),
    #     }

    def form_valid(self,form):
        form.instance.seller = self.request.user.profile
        return super().form_valid(form)

class TicketUpdate(UserPassesTestMixin, UpdateView):
    model = Ticket
    fields = ['title','detail','quantity']
    
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