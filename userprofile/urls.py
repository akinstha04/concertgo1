from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . views import PostListView
from .forms import ProfileUpdateForm, UserUpdateForm

urlpatterns = [
    # path('', PostListView.as_view(), name = 'home'),
    path('', views.ProfileListView.as_view(), name= "ProfileListView"),
    path('profile/', views.profilePage, name = "profile"),
    path('profileUpdate/', views.profileUpdate, name = "profileUpdate"),
    # path('post_upload/', views.postUpload, name = "postUpload")
    
    path('<pk>/', views.ProfileVisit.as_view(), name = "profileVisit")
    
    # path('main/', views.main, name="main")
]
urlpatterns += staticfiles_urlpatterns()