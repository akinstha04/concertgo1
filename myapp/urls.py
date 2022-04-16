from django.urls import path
from django.urls.resolvers import URLPattern
from myapp.forms import MyPasswordResetForm, MySetPasswordForm, LoginForm
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
# from userprofile.views import PostListView, PostUpload, PostDetail

urlpatterns = [
    path('', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    # path('',auth_views.LoginView.as_view(template_name='myapp/login.html',authentication_form = LoginForm),name='login'),
    # path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    # path('register/', views.registerpageView.as_view(), name = "register"),
    path('register/', views.register, name = "register"),
    # path('register_venuemanager/', views.registerManagerpageView.as_view(), name = "register_venuemanager"),
    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name='myapp/password_reset.html', form_class = MyPasswordResetForm), name = "password_reset"),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_resetdone.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='myapp/password_resetconfirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='myapp/password_resetcomplete.html'),name='password_reset_complete'),
    
    path('search/', views.search, name = "search"),

    path('ticket/', views.ticketPage, name = "ticket"),
    # path('ticket-add/', views.ticketAddPage, name = "ticketAdd"),
    path('ticket_upload/', views.TicketUpload.as_view(), name = 'ticketUpload'),
    path('ticket/<int:pk>/', views.TicketDetail.as_view(), name = "ticketDetail"),
    path('post_upload/', views.PostUpload.as_view(), name = 'postUpload'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name = "postDetail"),


    path('like/<int:pk>', views.likePost,name='likePost'),
    # path('main/', PostListView.as_view(), name = 'main')
    # path('main/', views.main, name = "main")
    path('main/', views.main, name = "main")
    # path('post_upload/', PostUpload.as_view(), name = 'postUpload'),
    # path('post/<int:pk>/', views.PostDetail.as_view(), name = "postDetail"),
    # path('main/', PostListView.as_view(), name = 'main')
    
]
urlpatterns += staticfiles_urlpatterns()