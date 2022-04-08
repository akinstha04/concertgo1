from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . views import PostListView
from myapp.forms import ProfileUpdateForm, UserUpdateForm

urlpatterns = [
    # path('', PostListView.as_view(), name = 'home'),
    path('profile/', views.profilePage, name = "profile"),
    path('profile_update/', views.profileUpdate, name = "profileUpdate")
    # path('post_upload/', views.postUpload, name = "postUpload")
    
    # path('main/', views.main, name="main")
]
urlpatterns += staticfiles_urlpatterns()