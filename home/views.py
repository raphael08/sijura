from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from django.db.models import Q
# Create your views here.
from .send_sms import send_sms

def df(request,start,end):
        r = list(Reservation.objects.filter(Q(Date_Check_Out__gt=start) & Q(Date_Check_In__lt=end)).values_list('room__number',flat=True))
        d = Reservation.objects.filter(Date_Check_In__gte=start,Date_Check_Out__lte=end)
        # list(Reservation.objects.filter(Q(Date_Check_Out__lte=end) & (Q(Date_Check_In__gte=start)| Q(Date_Check_In__lte=start))).values_list('room_id',flat=True))
     
        print(r)
        resev = list(Rooms.objects.exclude(number__in=r).values_list('number',flat=True))
        
        # if len(resev)<=1:
        #     pass
        # elif resev[0] > resev[1]:
        #  resev = resev[1:] 
        # else:
        #  resev = resev
        
        return JsonResponse({'status':resev})
def data(request):
    resev = list(Rooms.objects.filter(reserved=False).values_list('id',flat=True))
    #Reservation.objects.filter(datefield__range[start_date,end_date])
    
    return JsonResponse({'status':resev})
def index (request):
    cat= Categories.objects.all()
    gallery= Gallery.objects.all()
    resev = list(Rooms.objects.filter(reserved=False).values_list('id',flat=True))
    # yourModel.objects.filter(room__in=resev)
    #model.objects.filter(datefield__range[start_date,end_date])
    today = datetime.datetime.now()
    days = datetime.timedelta(days=1)
    days = today+days
    days = days.date().strftime("%Y-%m-%d")
    r  = list(Reservation.objects.filter(Date_Check_In__gte=today,Date_Check_Out__lte=days).values_list('room_id',flat=True))
    # print(r)
    # print("*********************************")
    # print(resev)
    # testimonials = Testimonial.objects.all()
    # render(request,'index.html',{'testimonial': testimonials})
    render (request,'index.html',{'cat': cat})
    return render(request,"index.html",{'cat': cat,'gallery': gallery,'data':resev})
def reservation (request):
    if request.method=='POST':
        send_sms()
    return render(request, "reservation.html")
def contact(request):
    return  render (request, "contact.html")
def blog (request):
    chambres = Categories.objects.all()
    return render (request, "blog.html",{'chambres': chambres})
def about(request):
    return render (request, 'about.html')


def rooms(request):
    rooms = Rooms.objects.exclude(id=8).filter(reserved=False,booked=False).count()
    room = Rooms.objects.filter(id=8,reserved=False,booked=False).count()
    cat = Categories.objects.all()
    rum = Rooms.objects.exclude(id=8).filter(reserved=False,booked=False)
    return render (request, 'rooms.html',{'rooms':rooms,'cat':cat,'room':room,'rum':rum})