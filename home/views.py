import os
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import *
from django.db.models import Q
# Create your views here.
from .send_sms import *
import random
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 




def send_email(subject,message,to_mail):
    subject=subject
    message=message
    from_email = settings.EMAIL_HOST_USER
    
    recepient_list = [to_mail]

    send_mail(subject,message,from_email,recepient_list)
    

def verify(request,code):
  try:
    resev = list(Reservation.objects.filter(booking_code=code,Check_Out=False,room__booked=True).values_list('id','Phone','days_of_staying','Name','Email','room__number','Date_Check_In','Date_Check_Out'))
    if len(resev) <=0:
        return JsonResponse({'status':'No record'})
    else:
    # SR_8142
    # resev = list(resev)
    #Reservation.objects.filter(datefield__range[start_date,end_date])
    
    
     return JsonResponse({'status':resev[0]})
  except Exception as e:
     return JsonResponse({'status':e})

    
    
def df(request,start,end):
        r = list(Reservation.objects.filter(Q(Date_Check_Out__gt=start) & Q(Date_Check_In__lt=end) & Q(room__booked=True)).values_list('room__number',flat=True))
        d = Reservation.objects.filter(Date_Check_In__gte=start,Date_Check_Out__lte=end)
        # list(Reservation.objects.filter(Q(Date_Check_Out__lte=end) & (Q(Date_Check_In__gte=start)| Q(Date_Check_In__lte=start))).values_list('room_id',flat=True))
     
        print(r)
        resev = list(Rooms.objects.exclude(number__in=r).values_list('number',flat=True))
        return JsonResponse({'status':resev})
def data(request):
    resev = list(Rooms.objects.filter(reserved=False).values_list('id',flat=True))
    
    send_email("hellow","hllow",'rsiphael@gmail.com')
    
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
    # if request.method=='POST':
    #     send_sms()
    return render(request, "reservation.html")
def contact(request):
    return  render (request, "contact.html")
def blog (request):
    chambres = Categories.objects.all()
    return render (request, "blog.html",{'chambres': chambres})
def about(request):
    return render (request, 'about.html')


def rooms(request):
    rooms = Rooms.objects.exclude(id=8).exclude(Q(booked=True)| Q(reserved=True)).count()
    room = Rooms.objects.filter(id=8,reserved=False,booked=False).count()
    cat = Categories.objects.all()
    rum = Rooms.objects.exclude(id=8).exclude(Q(booked=True)| Q(reserved=True))
    return render (request, 'rooms.html',{'rooms':rooms,'cat':cat,'room':room,'rum':rum})


def book(request):
    rooms = Rooms.objects.exclude(id=8).exclude(Q(booked=True)| Q(reserved=True)).count()
    room = Rooms.objects.filter(id=8,reserved=False,booked=False).count()
    cat = Categories.objects.all()
    rum = Rooms.objects.exclude(id=8).exclude(Q(booked=True)| Q(reserved=True))
    return render (request, 'booking.html',{'rooms':rooms,'cat':cat,'room':room,'rum':rum})


def generate_code():
    
    num = random.randint(10,9999) 
    sijura = f"SR_{num}"
   
    
    return sijura


def booking(request):
 try:
   if request.method == 'POST':
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    room = request.POST.get('room')
    days=request.POST.get('days')
    checkin = request.POST.get('checkin')
    year,month,day = str(checkin).split('-')
    checkin = datetime.datetime(int(year),int(month),int(day)).date()
    day = datetime.timedelta(days=int(days))
    checkout = checkin+day
    print(name,phone,room,email,checkin,checkout)
    code = generate_code()
    try:
        reserv = Reservation.objects.create(Name=name,Phone=int(phone),Email=email,room_id=room,days_of_staying=int(days),Date_Check_In=checkin,Date_Check_Out=checkout,booking_code=code)
        print("*****************")
        print(reserv.room_id)
        if reserv:
            rooms = Rooms.objects.filter(number=reserv.room_id).update(booked=True)
    except Exception as e:
        messages.error(request,e)
    
    if rooms:
        subject = "📑 BOOKING CONFIRMATION 📑"
        body = f"Hellow {str(name).upper()} \n🏨 WELCOME TO SIJURA LODGE 🏨 \n🙏 THANKS FOR BOOKING ROOM NO.{room}🛌 \n🔑 YOUR CONFIRMATION CODE IS {code} 🔑 \n⚠️ KEEP IT SAFE FOR IT WILL BE NEEDED LATER FOR YOUR BOOKING CONFIRMATION⚠️ \n🙏THANK YOU AND WELCOME AGAIN 😊 \n"
        send_email(subject,body,email)
        messages.success(request,'Booked Successful Check your Email  to see your booking code ⚠️ dont loose the code its Important')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 except Exception as e:
     messages.error(request,e)
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 
 
def cancel_book(request,id):
    
    rec = Reservation.objects.get(id=id)
    print("**************")
    print(rec.room_id)
    rev = Reservation.objects.filter(id=id).update(cancel_book=True,booked_on=today)
    # print(rev)
    Rooms.objects.filter(id=rec.room_id).update(booked=False)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))