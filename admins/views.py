import random
from django.shortcuts import render,redirect
from home.models import *
from .models import *
from django.db.models import Q,Sum
from django.contrib.auth.models import User,Group,Permission
# Create your views here.
from django.contrib import messages
from home.views import generate_code
def dashboard(request):
    today = datetime.datetime.now().date()
    resev = Reservation.objects.filter(reserved=True,Date_Check_In__lte=today,Check_Out=False)
    # for l in resev:
    #  print(l.get_amount)
    check_out = Reservation.objects.filter(reserved=True,Date_Check_Out=today,Check_Out=True).count()
    resevs = resev.count()
   
    resevs = resevs+check_out
    
    book = Reservation.objects.filter(booked=True,booked_on=today).count()
    parcent = (resevs/10)*100
    parcents = (book/10)*100
    paid_today = Billing.objects.filter(reservation__reserved=True,paid_on=today).count()
    today_payments = Billing.objects.filter(reservation__reserved=True,paid_on=today).exists()
    paid_todays = list(set(Billing.objects.filter(reservation__reserved=True,paid_on=today).values_list('reservation_id',flat=True)))
    paid = Billing.objects.filter(reservation_id__in=paid_todays).last()
    paid_today = len(paid_todays)
    print("**************************************************")
    if paid==None:
        paid=0
    # today_payments = Reservation.objects.filter(reserved=True,Date_Check_In__lte=today,Date_Check_Out=today,Check_Out=True,paid_on=today,payment="PAID").count()
    
  
    if today_payments:
        
    
        today_payment = Billing.objects.filter(reservation__reserved=True,paid_on=today).aggregate(Sum('amount'))['amount__sum']
    else:
        today_payment= 0

        
    
    # if Sells.objects.filter(date=today).exists():
    #  Sells.objects.filter(date=today).update(date=today,total_amount=today_payment)
    # else:
    #   Sells.objects.create(date=today,total_amount=today_payment)
      
    ex = Expenses.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum']
    total_ex = Expenses.objects.all().aggregate(Sum('amount'))['amount__sum']
    total_amount = Billing.objects.all().aggregate(Sum('amount'))['amount__sum']
    profit = total_amount - total_ex
    print(total_ex,total_amount)
   
    if ex == None:
     ex=0
     
    # r = Reservation.objects.filter(payment='DEBT')
    # print("****************")
    # print(len(r))
    # if len(r) >0:
    #  for r in Reservation.objects.all():
        
    #     debt  =+ r.total_remain
      
    # else:
    #     debt=0 
    debt=0 
    excess=0
    # for i in Billing.objects.all():
    #     print(i.total_remain)
    #     print(i.status)
    # r = Reservation.objects.filter(payment='PAID')
   
    # if len(r) >0:
    for k in Billing.objects.all():
        if k.status != None:
         if k.status=='DEBT':
          debt =+k.total_remain
      
         else:
             if k.total_remain==None:
                excess=0
             else:
                excess =+ k.total_remain
        else:
            pass
    
    rem = today_payment-ex
    staff = User.objects.filter(is_staff=True).count()
    context = {'resev':resevs,'today':paid_today,'book':book,'parcent':parcent,'parcents':parcents,'payment':today_payment,'debt':debt,'ex':ex,'rem':rem,'staff':staff,'total_ex':total_ex,'total_amount':total_amount,'profit':profit}
    return render(request,'dashboard.html',context)


def reservation(request):
    
    if request.method=='POST':
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
        
        try:
            reserv = Reservation.objects.create(Name=name,Phone=int(phone),Email=email,room_id=room,days_of_staying=int(days),Date_Check_In=checkin,Date_Check_Out=checkout,)
            if reserv:
                rooms = Rooms.objects.filter(number=reserv.room_id).update(reserved=True)
        except Exception as e:
            messages.error(request,e) 
            
def user(request):
    
    if request.method=='POST':
        first_name = request.POST.get('name')
        first,last= first_name.split(' ')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        group_id = request.POST.get('group')
        num = random.randint(10,9999) 
        User.objects.create(first_name=first_name)
        print(first,last,email,phone,group_id)
    g = Group.objects.all()
    user = User.objects.all()
    
    context = {'g':g,'user':user}
    return render(request,'users.html',context)