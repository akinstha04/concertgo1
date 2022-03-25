from django.urls import path
from django.urls.resolvers import URLPattern
from myapp.forms import MyPasswordResetForm, MySetPasswordForm, LoginForm
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/', views.profilePage, name = "profile"),
    path('profile_update/', views.profileUpdate, name = "profileUpdate")
    # path('main/', views.main, name="main")
]
urlpatterns += staticfiles_urlpatterns()