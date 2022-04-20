from itertools import chain
from operator import truediv
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse, reverse_lazy

from myapp.models import User
from .forms import ProfilePicUpdateForm, ProfileUpdateForm, UserUpdateForm, ProfilePicUpdateForm
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Profile, Wishlist, Like

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
    if profile.followers.filter(id=my_profile.id).exists():
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