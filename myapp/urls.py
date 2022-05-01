from re import template
from django.urls import path
from myapp.forms import MyPasswordResetForm
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    # user login register
    path('', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('register/', views.register, name = "register"),
    # user account actions
    path('<int:pk>/delete', views.UserDelete.as_view(), name='user_delete'),
    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name='myapp/password_reset.html', form_class = MyPasswordResetForm), name = "password_reset"),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_resetdone.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='myapp/password_resetconfirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='myapp/password_resetcomplete.html'),name='password_reset_complete'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='myapp/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='myapp/password_change_done.html'), name='password_change_done'),
    # social
    path('search/', views.search, name = "search"),
    path('ticket/', views.ticketPage, name = "ticket"),
    path('main/', views.main, name = "main")
]
urlpatterns += staticfiles_urlpatterns()