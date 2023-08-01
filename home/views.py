import os
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import *
from admins.models import *
from django.db.models import Q,F
# Create your views here.
from .send_sms import *
import random
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 
from django.db.models import Q,Sum
import calendar
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.functions import ExtractMonth
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
import requests



image1_path = 'static/img/sijura/sijura1.jpg'
image2_path = 'static/img/sijura/sijura22.png'

def send_email(to_mail,sub,html,context):
    # subject=subject
    # message=message
    # from_email = settings.EMAIL_HOST_USER
    
    # recepient_list = [to_mail]

    # send_mail(subject,message,from_email,recepient_list)
    with open(image1_path, 'rb') as f1, open(image2_path, 'rb') as f2:
        image1_data = f1.read()
        image2_data = f2.read()
    
    year = datetime.datetime.now().date().year
    html_context = render_to_string(html,context)

    text_context = strip_tags(html_context)
    email=EmailMultiAlternatives(
        sub,
        text_context,
        settings.EMAIL_HOST_USER,
        [to_mail]
        )
    email.attach_alternative(html_context,'text/html')
    image1 = MIMEImage(image1_data)
    image1.add_header('Content-ID', '<image_id1>')
    email.attach(image1)

    # Attach the second image as inline attachment and reference it in the HTML using cid
    image2 = MIMEImage(image2_data)
    image2.add_header('Content-ID', '<image_id2>')
    email.attach(image2)

    
    email.send()

def send_sms(phone,sms):
    
    url = 'http://smsportal.imartgroup.co.tz/app/smsapi/index.php'
    phone_number = phone
    
    params = {
                    'campaign' : 266,
                    'routeid' : 8,
                    'key' : '36281862404933',
                    'type' : 'text',
                    'contacts' : phone_number, 
                    'senderid' : 'Spring-Tech',
                    'msg' : sms,
    }
    p = requests.post(url,data=params)



def verify(request,code):
  try:
   
    
    resev = list(Reservation.objects.filter(booking_code=code,Check_Out=False,booked=True,exclude=False).values_list('id','Phone','Name','Email','room__number','Date_Check_In','Date_Check_Out'))
    
    print(resev)
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
        r = list(Reservation.objects.filter(Q(Date_Check_Out__gte=start) & Q(Date_Check_In__lte=end) & Q(Q(booked=True) |Q(reserved=True))).values_list('room__number',flat=True))
        d = Reservation.objects.filter(Date_Check_In__gte=start,Date_Check_Out__lte=end)
        # list(Reservation.objects.filter(Q(Date_Check_Out__lte=end) & (Q(Date_Check_In__gte=start)| Q(Date_Check_In__lte=start))).values_list('room_id',flat=True))
     
        print(r)
        resev = list(Rooms.objects.exclude(exclude=True).exclude(number__in=r).values_list('number',flat=True))
        return JsonResponse({'status':resev})
def data(request):
    current_year = datetime.datetime.now().year
    res = Billing.objects.filter(paid_on__year=current_year).annotate(month=ExtractMonth('paid_on')).values('month').annotate(total_amount=Sum('amount'))
   
    
    
    
    # Create a dictionary to store the sums for each month.
    month = []
    months = []
    data = [] 
    exess = []
    excess_date = []
    monthly_sum = {calendar.month_name[entry['month']]: entry['total_amount'] for entry in res}
    
    for r in res:
       months.append(r['month'])
       month.append(calendar.month_name[r['month']]) 
       data.append(r['total_amount'])
   
    ex = Expenses.objects.filter(date__year=current_year).annotate(month=ExtractMonth('date')).values('month').annotate(total_amount=Sum('amount'))
   
    print("*************************")
    for r in ex:
        exess.append(r['total_amount'])
        excess_date.append(r['month'])
    res = {'month':months,'data':data,'ex':exess}
  
    
    for d in months:
        if d in excess_date:
          
         print(d)
        else:
            index = months.index(d)
            
            excess_date.insert(index,0)
            exess.insert(index,0)
    
    # print(excess_date) 
    # print(exess)   
    return JsonResponse({'month':month,'data':data,'ex':exess})







    
    return JsonResponse({'status':resev})
def index (request):
    cat= Categories.objects.all()
    gallery= Gallery.objects.all()
    resev = list(Reservation.objects.filter(reserved=False).values_list('room_id',flat=True))
    
    # for r in Reservation.objects.all():
    #     if str(r.total_remain).startswith('-'):
    #         print("deni")
    #     else:
    #         print(r.get_amount,r.total_remain)
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
    return render(request,"index.html",{'cat': cat,'gallery': gallery})
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
    l = Reservation.objects.filter(Q(reserved=True) | Q(booked=True)).values_list('room_id',flat=True)
    roo = Rooms.objects.exclude(id=8).exclude(id__in=l).count()
    k = list(Reservation.objects.filter(Q(Q(reserved=True) | Q(booked=True)) & Q(Q(Date_Check_In__lte=today) & Q(Date_Check_Out__gte=today) & Q(Check_Out=False))).values_list('room_id',flat=True))
    m =list(Reservation.objects.filter(Q(Date_Check_Out__gte=today) & Q(Date_Check_In__lte=today) & Q(Q(booked=True) |Q(reserved=True))).values_list('room__number',flat=True))
    print(m)
    # n = list(Reservation.objects.filter(Q(Q(reserved=True) | Q(booked=True)) & Q(Q(Date_Check_In__lte=today))).values_list('room_id',flat=True))
    # print(n)
    rooms = Rooms.objects.exclude(exclude=True).exclude(id=8).exclude(id__in=m).count()
    
    if 8 in m:
        print('***********')
        room =0
    else:
        room =1
    # room = Reservation.objects.filter(room_id=8).count()
    cat = Categories.objects.all()
    rum = Rooms.objects.exclude(exclude=True).exclude(id=8).exclude(id__in=m)
    return render (request, 'rooms.html',{'rooms':rooms,'cat':cat,'room':room,'rum':rum})


def book(request):
    k = list(Reservation.objects.filter(Q(Q(reserved=True) | Q(booked=True)) & Q(Q(Date_Check_In__lte=today) & Q(Date_Check_Out__gte=today) & Q(Check_Out=False))).values_list('room_id',flat=True))
    rooms = Rooms.objects.exclude(id=8).exclude(id__in=k).count()
    if 8 in k:
        print('***********')
        room =0
    else:
        room =1
    cat = Categories.objects.all()
    rum = Rooms.objects.exclude(id=8).exclude(id__in=k)
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
    # days=request.POST.get('days')
    price = Rooms.objects.get(number=room)
    price = price.category.price
    checkin = request.POST.get('checkin')
    year,month,day = str(checkin).split('-')
    checkin = datetime.datetime(int(year),int(month),int(day)).date()
    day = datetime.timedelta(days=1)
    checkout = checkin+day
    print(name,phone,room,email,checkin,checkout)
    code = generate_code()
    try:
        reserv = Reservation.objects.create(Name=name,Phone=int(phone),Email=email,room_id=room,Date_Check_In=checkin,Date_Check_Out=checkout,booking_code=code,booked=True)
        
        
    except Exception as e:
        messages.error(request,e)
    
    if reserv:
        sub = "📑 BOOKING CONFIRMATION 📑"
        html = 'email.html'
        context= {'name':str(name).upper(),'code':code,'year':year,'room':room}
        message = f'{name} \nWELCOME TO SIJURA LODGE\nTHANK YOU FOR YOU BOOKING ON ROOM {room}\nYOUR BOOKING CODE IS {code}\n KEEP IN SAFE\nWelcome to Sijura Lodge\nCome,Stay and Enjoy'
        send_email(email,sub,html,context)
        send_sms(phone[1:],message)
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