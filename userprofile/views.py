from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myapp.forms import ProfileUpdateForm, UserUpdateForm

# Create your views here.
def profilePage(request):
    return render(request, 'userprofile/profile.html')

@login_required
def profileUpdate(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.sucess(request, 'Your account has been updated')
            return redirect('profileUpdate')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'userprofile/profile_update.html')

# def profileUpdate(request):
#     return render(request, 'userprofile/profile_update.html')