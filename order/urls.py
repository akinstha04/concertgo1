from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('ticket_order/<int:pk>', views.orderTicket, name = "orderTicket"),
    path('increaseticket/', views.increment, name = "increaseTicket"),
    path('decreaseticket/', views.decrement, name = "decreaseTicket"),
    path('payment/',views.paymentDone,name="paymentdone"),
    
    path('mytickets/', views.myTicketPage, name = "myTickets"),
    path('ticket/sales/', views.myTicketSales, name = "myTicketSales"),
]
urlpatterns += staticfiles_urlpatterns()