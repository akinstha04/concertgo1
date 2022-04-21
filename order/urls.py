from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from userprofile.views import PostListView, PostUpload, PostDetail

urlpatterns = [
    path('ticket_order/<int:pk>', views.orderTicket, name = "orderTicket"),
    path('increaseticket/', views.increment, name = "increaseTicket"),
    path('decreaseticket/', views.decrement, name = "decreaseTicket"),
    path('payment/',views.paymentDone,name="paymentdone")
]
urlpatterns += staticfiles_urlpatterns()