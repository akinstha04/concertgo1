from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .forms import ProfileUpdateForm, UserUpdateForm

urlpatterns = [

    path('profile/', views.profilePage, name = "profile"),
    path('profile/<pk>/', views.ProfileVisit.as_view(), name = "profileVisit"),
    path('profileUpdate/', views.profileUpdate, name = "profileUpdate"),
    path('follow/<int:pk>', views.follow,name='follow'),

    path('post_upload/', views.PostUpload.as_view(), name = 'postUpload'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name = "postDetail"),
    path('post_update/<int:pk>', views.PostUpdate.as_view(), name = 'postUpdate'),
    path('post_delete/<int:pk>', views.PostDelete.as_view(), name = 'postDelete'),

    path('likepost/', views.likeUnlikePost,name='likeUnlikePost'),
    path('post/comment/<int:pk>', views.AddComment.as_view(), name='commentPost'),

    path('ticket_upload/', views.TicketUpload.as_view(), name = 'ticketUpload'),
    path('ticket/<int:pk>/', views.TicketDetail.as_view(), name = "ticketDetail"),
    path('ticket_update/<int:pk>', views.TicketUpdate.as_view(), name = 'ticketUpdate'),
    path('ticket_delete/<int:pk>', views.TicketDelete.as_view(), name = 'ticketDelete'),

    path('add_wishlist/', views.addWishlist, name='addWishlist'),
    path('removewishlist/', views.removeWishlist, name='removeWishlist'),
    path('ticketwishlist/', views.ticketWishlistPage, name = "ticketWishlist"),
]
urlpatterns += staticfiles_urlpatterns()