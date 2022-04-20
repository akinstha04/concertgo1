from django.shortcuts import render
from .models import Order

# Create your views here.
def orderTicket(request):
    # ordered = Order.obects.filter(user=request.user)
    return render(request, 'order/order.html')