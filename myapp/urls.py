from django.urls import path
from myapp.forms import MyPasswordResetForm
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('register/', views.register, name = "register"),

    path('<int:pk>/delete', views.UserDelete.as_view(), name='user_delete'),

    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name='myapp/password_reset.html', form_class = MyPasswordResetForm), name = "password_reset"),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_resetdone.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='myapp/password_resetconfirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='myapp/password_resetcomplete.html'),name='password_reset_complete'),

    path('search/', views.search, name = "search"),
    path('ticket/', views.ticketPage, name = "ticket"),

    path('main/', views.main, name = "main")
    
]
urlpatterns += staticfiles_urlpatterns()