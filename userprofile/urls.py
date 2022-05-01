from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # profile
    path('profile/', views.profilePage, name = "profile"),
    path('profile/<pk>/', views.ProfileVisit.as_view(), name = "profileVisit"),
    path('profileUpdate/', views.profileUpdate, name = "profileUpdate"),
    path('follow/<int:pk>', views.follow,name='follow'),
    # post
    path('post_upload/', views.PostUpload.as_view(), name = 'postUpload'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name = "postDetail"),
    path('post_update/<int:pk>', views.PostUpdate.as_view(), name = 'postUpdate'),
    path('post_delete/<int:pk>', views.PostDelete.as_view(), name = 'postDelete'),
    # post actions
    path('likepost/', views.likeUnlikePost,name='likeUnlikePost'),
    path('<int:pk>/comment/delete', views.CommentDelete.as_view(), name='comment_delete'),
    # ticket
    path('add_ticket/',views.addTicket.as_view(), name='addTicket'),
    path('ticket/<int:pk>/', views.TicketDetail.as_view(), name = "ticketDetail"),
    path('ticket_update/<int:pk>', views.TicketUpdate.as_view(), name = 'ticketUpdate'),
    path('ticket_delete/<int:pk>', views.TicketDelete.as_view(), name = 'ticketDelete'),
    # ticket actions
    path('add_wishlist/', views.addWishlist, name='addWishlist'),
    path('removewishlist/', views.removeWishlist, name='removeWishlist'),
    path('ticketwishlist/', views.ticketWishlistPage, name = "ticketWishlist"),
]
urlpatterns += staticfiles_urlpatterns()