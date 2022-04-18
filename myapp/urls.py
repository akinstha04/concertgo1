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
    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name='myapp/password_reset.html', form_class = MyPasswordResetForm), name = "password_reset"),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_resetdone.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='myapp/password_resetconfirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='myapp/password_resetcomplete.html'),name='password_reset_complete'),
    
    path('search/', views.search, name = "search"),

    path('post_upload/', views.PostUpload.as_view(), name = 'postUpload'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name = "postDetail"),
    path('post_update/<int:pk>', views.PostUpdate.as_view(), name = 'postUpdate'),
    path('post_delete/<int:pk>', views.PostDelete.as_view(), name = 'postDelete'),

    path('like/<int:pk>', views.likePost,name='likePost'),
    path('post/comment/<int:pk>', views.AddComment.as_view(), name='commentPost'),

    path('ticket/', views.ticketPage, name = "ticket"),
    path('ticket_upload/', views.TicketUpload.as_view(), name = 'ticketUpload'),
    path('ticket/<int:pk>/', views.TicketDetail.as_view(), name = "ticketDetail"),
    path('ticket_update/<int:pk>', views.TicketUpdate.as_view(), name = 'ticketUpdate'),
    path('ticket_delete/<int:pk>', views.TicketDelete.as_view(), name = 'ticketDelete'),

    path('add_wishlist/', views.addWishlist, name='addWishlist'),
    path('removewishlist/', views.removeWishlist, name='addWishlist'),
    
    path('main/', views.main, name = "main")
    
]
urlpatterns += staticfiles_urlpatterns()