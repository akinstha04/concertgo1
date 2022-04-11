from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfilePicUpdateForm, ProfileUpdateForm, UserUpdateForm, ProfilePicUpdateForm
from django.views.generic import ListView, DetailView, CreateView
from .models import Post

# Create your views here.
def profilePage(request):
    return render(request, 'userprofile/profile.html')

# def postDetail(request):
#     return render(request, 'userprofile/post_detail.html')

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
