from django.shortcuts import redirect, render
from .models import Order,Ticket,Profile
from django.http import JsonResponse

# Create your views here.
def orderTicket(request,pk):
    pks = pk
    tickets = Ticket.objects.filter(pk=pks)
    bb = request.GET.get('quantity')
    print("akinquan"+str(bb))
    for a in tickets:
        print(a.price)
        tot = int(a.price) * int(bb)
    print(tot)
    
    # ordered = Order.obects.filter(user=request.user)
    return render(request, 'order/order.html',{'tickets':tickets,'a':a,'tot':tot,'quantity':bb})

def increment(request):
    
    quan = request.GET['increase']
    print(quan)

    data={
        'bool': quan
    }
    return JsonResponse(data)

def decrement(request):
    quan = request.GET['increase']
    print(quan)

    data={
        'bool': quan
    }
    return JsonResponse(data)

def paymentDone(request):
    
    bb = request.GET.get('tquan')
    print("ohshit"+str(bb))
    cc =request.GET.get('ticketid')
    cd = Ticket.objects.get(id=cc)
    print("abc"+str(cc))
    print("oh no oh no oh no")
    use = request.user.profile
    Order(buyer=use,ticket=cd,quantity=bb).save()
    return redirect('/ticket')
    # return render(request,'ticket.html')
    