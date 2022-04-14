from itertools import chain
from operator import truediv
import re
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from myapp.models import User
from .forms import ProfilePicUpdateForm, ProfileUpdateForm, UserUpdateForm, ProfilePicUpdateForm
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Profile

# Create your views here.
# def profilePage(request):
#     return render(request, 'userprofile/profile.html')


def profilePage(request):
    profile = Profile.objects.get(user=request.user)
    users = [user for user in profile.following.all()]
    posts = []
    qs = None
    following= profile.following.all().count()
    
    
    # self posts
    my_posts = profile.profile_posts()
    posts.append(my_posts)
    post_count = len(my_posts)
    # sort and chain querys and unpack the posts list
    if len(posts)>0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.date_posted)
    return render(request,'userprofile/profile.html',{'profile':profile,'posts':qs, 'following':following,'post_count':post_count})




# def profilePage(request):
#     profile = Profile.objects.get(user=request.user)
#     users = [user for user in profile.following.all()]
#     posts = []
#     qs = None
    
#     # get posts of people who are followed
    
#     for u in users:
#         p = Profile.objects.get(user=u)
#         # p_posts = p.post_set.all()
#         # p_posts.append(p_posts)
#         # c= u.count()
    
#     # self posts
#     my_posts = profile.profile_posts()
#     posts.append(my_posts)
#     # sort and chain querys and unpack the posts list
#     if len(posts)>0:
#         qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.date_posted)
#     return render(request,'userprofile/profile.html',{'profile':profile,'posts':qs})



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



class PostListView(ListView):
    model = Post
    template_name = 'main.html','userprofile/profile.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class ProfileListView(ListView):
    model = Profile
    template_name = 'userprofile/profile.html','myapp/search.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)

# class ProfileVisit(DetailView):
#     model = Profile
#     template_name = 'userprofile/profile_visit.html'

#     def get_object(self, **kwargs):
#         pk = self.kwargs.get('pk')
#         viewProfile = Profile.objects.get(pk = pk)
#         return viewProfile
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         viewProfile = self.get_object()
#         my_profile = Profile.objects.get(user=self.request.user)
#         if viewProfile in my_profile.following.all():
#             follow = True
#         else:
#             follow = False
#         context["follow"] = follow
#         return context
    
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
        return context


def follow_unfollow_profile(request):
    if request.method=="POST":
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:ProfileListView')


