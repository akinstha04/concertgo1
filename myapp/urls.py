from django.urls import path
from django.urls.resolvers import URLPattern
from myapp.forms import MyPasswordResetForm, MySetPasswordForm, LoginForm
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    # path('',auth_views.LoginView.as_view(template_name='myapp/login.html',authentication_form = LoginForm),name='login'),
    # path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', views.registerpageView.as_view(), name = "register"),
    # path('register/', views.registerPage, name = "register"),
    # path('register_venuemanager/', views.registerManagerpageView.as_view(), name = "register_venuemanager"),
    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name='myapp/password_reset.html', form_class = MyPasswordResetForm), name = "password_reset"),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_resetdone.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='myapp/password_resetconfirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='myapp/password_resetcomplete.html'),name='password_reset_complete'),
    

    path('ticket/', views.ticketPage, name = "ticket"),
    path('main/', views.main, name="main")
]
urlpatterns += staticfiles_urlpatterns()