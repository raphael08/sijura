import random
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from home.models import *
from .models import *
from django.db.models import Q,Sum,Max
from django.contrib.auth.models import User,Group,Permission
# Create your views here.
from django.contrib import messages
from home.views import generate_code

# from home.views import *

today = datetime.datetime.now().date()
def dashboard(request):
    today = datetime.datetime.now().date()
    resev = Reservation.objects.filter(reserved=True,Date_Check_In__lte=today,Check_Out=False)
    # for l in resev:
    #  print(l.get_amount)
    check_out = Reservation.objects.filter(reserved=True,Date_Check_Out=today,Check_Out=True).count()
    resevs = resev.count()
   
    resevs = resevs+check_out
    
    book = Reservation.objects.filter(booked=True,booked_on=today).count()
   
    books=  Reservation.objects.filter(booked=True,booked_on=today)
    total_book = Reservation.objects.filter(booked=True).count()
    parcent = (resevs/10)*100
    parcents = (book/10)*100
    paid_today = Billing.objects.filter(reservation__reserved=True,paid_on=today).count()
    today_payments = Billing.objects.filter(reservation__reserved=True,paid_on=today).exists()
    paid_todays = list(set(Billing.objects.filter(reservation__reserved=True,paid_on=today).values_list('reservation_id',flat=True)))
    paid = Billing.objects.filter(reservation_id__in=paid_todays).last()
    paid_today = len(paid_todays)
    
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
    profit = 0
    total_amount= 0
    total_ex=0
    ex = Expenses.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum']
    total_ex = Expenses.objects.all().aggregate(Sum('amount'))['amount__sum']
    
    total_amount = Billing.objects.all().aggregate(Sum('amount'))['amount__sum']
    
    if total_amount is None:
        total_amount= 0
    if total_ex is None:
        
        total_ex = 0
   
    profit = total_amount - total_ex
   
   
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
    context = {'resev':resevs,'today':paid_today,'book':book,'parcent':parcent,'parcents':parcents,'payment':today_payment,'debt':debt,'ex':ex,'rem':rem,'staff':staff,'total_ex':total_ex,'total_amount':total_amount,'profit':profit,'total_book':total_book}
    return render(request,'dashboard.html',context)


def reserv(request):
    
    if request.method=='POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        room = request.POST.get('room')
        #days=request.POST.get('days')
        checkin = datetime.datetime.now().date()
        
        # checkin = request.POST.get('checkin')
        # year,month,day = str(checkin).split('-')
        # checkin = datetime.datetime(int(year),int(month),int(day)).date()
        # day = datetime.timedelta(days=int(days))
        # checkout = checkin+day
        amount = request.POST.get('amount')
        days = 0
        if int(amount) == 0:
            days = 1
            day = datetime.timedelta(days=int(days))
            checkout = checkin+day
            reserv = Reservation.objects.create(Name=name,Phone=phone,Email=email,room_id=room,Date_Check_In=checkin,Date_Check_Out=checkout,reserved=True)
       
            Billing.objects.create(reservation_id=reserv.id,amount=amount,total_paid=amount)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        else:
            price = Rooms.objects.get(number=room)
            price = price.category.price
            
            days = int(amount)/price
        #print(int(days))
            day = datetime.timedelta(days=int(days))
            checkout = checkin+day
            #print(name,phone,room,email,checkin,checkout)
            reserv = Reservation.objects.create(Name=name,Phone=phone,Email=email,room_id=room,Date_Check_In=checkin,Date_Check_Out=checkout,reserved=True)
          
            Billing.objects.create(reservation_id=reserv.id,amount=amount,paid_on=today,total_paid=amount)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
# def user(request):
    
#     if request.method=='POST':
#         first_name = request.POST.get('name')
#         first,last= first_name.split(' ')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         group_id = request.POST.get('group')
#         num = random.randint(10,9999) 
#         User.objects.create(first_name=first_name)
#         print(first,last,email,phone,group_id)
#     g = Group.objects.all()
#     user = User.objects.all()
    
#     context = {'g':g,'user':user}
#     return render(request,'users.html',context)


def reservations(request):
    
    m =list(Reservation.objects.filter(Q(Date_Check_In__lte=today) & Q(Check_Out=False) & Q(Q(booked=True) |Q(reserved=True))).values_list('room__number',flat=True))
    
    n = list(Reservation.objects.filter(reserved=True,Date_Check_Out=today,Check_Out=True))
    
    m = list(set(m+n))
    
    
    if request.user.is_superuser:
        rooms = Rooms.objects.exclude(id__in=m)
        
    else:
        rooms = Rooms.objects.exclude(exclude=True).exclude(id__in=m)
    
    
    context={'rooms':rooms}

    return render(request,'reservations.html',context)



def exclude(request,id):
    
   try:
    
     
     Rooms.objects.filter(id=id).update(exclude='True')
     messages.error(request,"Room successful Excluded")
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   except Exception as e:
       messages.error(request,e)
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def dexclude(request,id):
    
   try:
    
     
     Rooms.objects.filter(id=id).update(exclude='False')
     messages.success(request,"Room successful Excluded")
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   except Exception as e:
       messages.error(request,e)
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   
   
   
def roomz(request):
    
    m =list(Reservation.objects.filter(Q(Date_Check_Out__gte=today) & Q(Date_Check_In__lte=today) & Q(Check_Out=False) & Q(Q(booked=True) |Q(reserved=True))).values_list('room__number',flat=True))
    
    rooms  = Rooms.objects.all()
    rooms = Rooms.objects.exclude(id__in=m)
    unavailable = Rooms.objects.filter(id__in=m)
    unavailable = Reservation.objects.filter(Q(Date_Check_Out__gte=today) & Q(Date_Check_In__lte=today) & Q(Check_Out=False) & Q(Q(booked=True) |Q(reserved=True))).values_list('room__number',flat=True)
    unava= list(unavailable)
    bil = Billing.objects.filter(reservation__room__number__in=unava)
    context = {'rooms':rooms,'unavailable':unavailable,'bil':bil}
    
    return render(request,'roomz.html',context)


def reservedRoomz(request):
    
    m =list(Reservation.objects.filter(Q(Date_Check_Out__gte=today) & Q(Date_Check_In__lte=today) & Q(Check_Out=False) & Q(Q(booked=True) |Q(reserved=True))).values_list('room__number',flat=True))
    
    g = Billing.objects.values('paid_on').distinct()

    rooms  = Rooms.objects.all()
    rooms = Rooms.objects.exclude(id__in=m)
    unavailable = Rooms.objects.filter(id__in=m)
    unavailable = Reservation.objects.filter(Q(Date_Check_In__lte=today) & Q(Check_Out=False) & Q(Q(booked=True) |Q(reserved=True))).values_list('id',flat=True)
    
    unava= list(set(list(unavailable)))
    # print(unava)
    bil = Billing.objects.filter(reservation_id__in=unava).order_by('-id')
    
    bils = Billing.objects.filter(reservation_id__in=unava).aggregate(date=Max('paid_on'))
    print("***********")
    print(bils['date'])
    # print(set(list(bils)))
    b = Billing.objects.filter(reservation_id__in=unava).values('reservation_id','reservation__room__number').annotate(amount=Sum('amount'))
    # print((b))
    # k = list(set(b))
    
    # print(k[0][0])
    # for i in bils:
        
    #     #print(i['created_at'])
        
    #     y = Billing.objects.filter(created_at=i['created_at'])
    # today_payment = Billing.objects.values('created_at').annotate(total_amount=Sum('amount'))
    # print(today_payment)
    
    # for i in today_payment:
    #     print(i['total_amount'])
  
        
        
        
        
    context = {'rooms':rooms,'unavailable':unava,'bil':bil,'b':b}
    
    return render(request,'reserve.html',context)

def reserveRecord(request):
    
    bil = Reservation.objects.filter(reserved=True).order_by('-id')
    context = {'bil':bil}
    
    return render(request,'reserve-records.html',context)




def billing(request):
   
   
   bil = Billing.objects.values('created_at').annotate(total_amount=Sum('amount'))
   
   
   for i in bil:
    exe = Expenses.objects.filter(date=i['created_at']).values('date')
    
    
   
   # for j in exe:
    #     print(j.amount) 
  
   ex = Expenses.objects.values('date').annotate(total_amounts=Sum('amount'))
   
#    if len(ex) > len(bil):
#        for i in range(0,len(ex)):
           
#         if i <len(ex) and i<len(bil):    
#          if ex[i]['date'] == bil[i]['created_at']:
#             print(ex[i]['date'])
            
#          else:
#               print("**********",ex[i]['date'])
#         else:
#            print(ex[i]['date'])   
           
           
   #bil =list(bil)+list(ex)
   
   ls = []
#    print(len(ex),len(bil))
   if len(bil) ==  len(ex):
    for i in range(0,len(bil)):
       cont_i = {}
     
       if bil[i]['created_at'] == ex[i]['date']:
           cont_i['date'] = bil[i]['created_at']
           cont_i['amount'] = bil[i]['total_amount']
           cont_i['exp'] = ex[i]['total_amounts']
           cont_i['profit'] = bil[i]['total_amount'] - ex[i]['total_amounts']
           ls.append(cont_i)
    #    elif (bil[i]['created_at'] != ex[i]['date']):
    #        cont_i['date'] = bil[i]['created_at']
    #        cont_i['amount'] = bil[i]['total_amount']
    #        cont_i['amount'] = 0
    #     #    ex[i]['total_amounts'] =0
    #        cont_i['profit'] = bil[i]['total_amount'] - ex[i]['total_amounts']
    #        ls.append(cont_i)
    #    elif (bil[i]['created_at'] != ex[i]['date']) and (bil[i]['created_at'] == "" and ex[i]['date'] != ""):
    #        cont_i['date'] = ex[i]['date']
    #        cont_i['amount'] = 0
    #        ex[i]['total_amounts'] =ex[i]['total_amounts']
    #        cont_i['profit'] = bil[i]['total_amount'] - ex[i]['total_amounts']
    #        ls.append(cont_i)
   elif len(ex) > len(bil):
       for i in range(len(ex)):
        cont_i = {}
        if i<len(ex) and i<len(bil):
         if ex[i]['date'] == bil[i]['created_at']:
           cont_i['date'] = ex[i]['date']
           cont_i['amount'] = bil[i]['total_amount']
           cont_i['exp'] = ex[i]['total_amounts']
           cont_i['profit'] = bil[i]['total_amount'] - ex[i]['total_amounts']
          
           ls.append(cont_i)
         else:
           
           cont_i['date'] = ex[i]['date']
           cont_i['amount'] = bil[i]['total_amount']
           cont_i['exp'] = ex[i]['total_amounts']
           cont_i['profit'] = bil[i]['total_amount'] - ex[i]['total_amounts']
           ls.append(cont_i) 
        else:
           
           cont_i['date'] = ex[i]['date']
           cont_i['amount'] = 0
           cont_i['exp'] = ex[i]['total_amounts']
           cont_i['profit'] = 0 - ex[i]['total_amounts']
           ls.append(cont_i)
   else:
       for i in range(len(bil)):
        cont_i = {}
        if i<len(ex) and i<len(bil):
         if ex[i]['date'] == bil[i]['created_at']:
           cont_i['date'] = bil[i]['created_at']
           cont_i['amount'] = bil[i]['total_amount']
           cont_i['exp'] = 0
           cont_i['profit'] = bil[i]['total_amount'] - 0
           
           ls.append(cont_i)
         else:
           
           cont_i['date'] = ex[i]['date']
           cont_i['amount'] = bil[i]['total_amount']
           cont_i['exp'] = ex[i]['total_amounts']
           cont_i['profit'] = bil[i]['total_amount'] - ex[i]['total_amounts']
           ls.append(cont_i) 
        else:
          
           cont_i['date'] = bil[i]['created_at']
           cont_i['amount'] = bil[i]['total_amount']
           cont_i['exp'] = 0
           cont_i['profit'] = bil[i]['total_amount'] - 0
           ls.append(cont_i)
#    else:
#        for i in range(0,len(ex)):
#         cont_i = {}
       
        
#         if bil[i]['created_at'] == ex[i]['date']:
#            cont_i['date'] = bil[i]['created_at']
#            cont_i['amount'] = bil[i]['total_amount']
#            cont_i['exp'] = ex[i]['total_amounts']
#            cont_i['profit'] = bil[i]['total_amount'] - ex[i]['total_amounts']
#            ls.append(cont_i)
#         elif (bil[i]['created_at'] != ex[i]['date']):
#            cont_i['date'] = bil[i]['created_at']
#            cont_i['amount'] = bil[i]['total_amount']
#            cont_i['amount'] = 0
#         #    ex[i]['total_amounts'] =0
#            cont_i['profit'] = bil[i]['total_amount'] - ex[i]['total_amounts']
#            ls.append(cont_i)
#         elif (bil[i]['created_at'] != ex[i]['date']) and (bil[i]['created_at'] == "" and ex[i]['date'] != ""):
#            cont_i['date'] = ex[i]['date']
#            cont_i['amount'] = 0
#            ex[i]['total_amounts'] =ex[i]['total_amounts']
#            cont_i['profit'] = bil[i]['total_amount'] - ex[i]['total_amounts']
#            ls.append(cont_i)
           
#    print(cont_i)
#    print(ls)
#    print(ex)
   context = {'bil':ls}
   return render(request,'billing.html',context) 






def checkout(request,id):
    
    
    
    Reservation.objects.filter(id=id).update(Check_Out=True,Date_Check_Out=today)
    
    messages.success(request,"Room successful Excluded")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



from django.db.models.functions import TruncDate
from django.db.models import Count
def Expense(request):
    
    
    bil = Expenses.objects.values('date').annotate(total_amount=Sum('amount'))
    
    # ex = Expenses.objects.all().values('date')
    ex = Expenses.objects.values('date').annotate(total=Sum('amount')).order_by('-date')
    # print(ex)
    ls=[]
    for i in ex:
        
        ls_i = []
        amount_i=[]
        cort_i = {}
        cort_i['date'] = i['date']
        cort_i['total'] = i['total']
        # print(ex[i]['count'])
        # print(i['date'])
        for j in Expenses.objects.filter(date=i['date']).order_by('-date'):
                # if ex[i]['count'] == 1:
                ls_i.append(j.item)
                amount_i.append(j.amount)
                #  cort_i['item'] = ls_i
                #  ls.append(cort_i)
                #  print(ls)
                # else:
                #     ls_i.append(j.item)
                    # print(ls_i)
        cort_i['item'] = ls_i
        cort_i['amount'] = amount_i
        # print(cort_i['item'])
        ls.append(cort_i)
                    # print(ls_i)
                    # ls.append(cort_i)
                # cort['items'] =  ls
                # ls.append(j.item)
        # cort_i['item'] = ls_i 
        # ls.append(cort_i) 
    # print(ls)
        
    # for i in range(0,len(ex)):
        
    #     if ex[i]['count'] > 1:
    #      print(ex[i]['date'])
    #     #  ex = Expenses.objects.filter(date = ex[i]['date'])
    #      print(ex)
    #     else:
          
    #       print(ex[i]['date'])  
        
        
        
    # print(ex)
    
    return render(request,'expenses.html',{'ex':ls})


from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template,render_to_string
from django.utils.html import strip_tags


def render_to_pdf(template_src, context_dict={}):
    html_context = render_to_string(template_src,context_dict)

    
    
    result = BytesIO()
    
    pdf = pisa.CreatePDF(html_context, dest=result)
    
    if not pdf.err:
     return result.getvalue()
    return None

from django.core.mail import EmailMessage  
from django.conf import settings  
def send_pdf_email(subject, message, recipient_list, pdf_content):
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    email.attach('document.pdf', pdf_content, 'application/pdf')
    email.send()


def billing_report(request):
    
    
 if request.method=='POST':
    
    to = request.POST.get('to')
    fro = request.POST.get('from')
    email = request.POST.get('email')
    report = request.POST.get('report')
      
    if report == '3' and email == '':
        messages.error(request,"Insert the email")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
    emails =  str(email).split(',')
    
    
    
    bil = Billing.objects.filter(paid_on__lte=to,paid_on__gte=fro).values('paid_on').annotate(total=Sum('amount')).annotate(count=Count('id'))
    
    ex = Expenses.objects.values('date').annotate(total_amounts=Sum('amount'))
    ls=[]
    
    for i in bil:
        lz_i = []
        amount_i=[]
        amount_h=[]
        ls_i = []
        cort_i = {}
        cort_i['date'] = i['paid_on']
        cort_i['total'] = i['total'] 
        b = list(Billing.objects.filter(paid_on=i['paid_on']).values('amount','reservation__room__number'))
        sl = Salary.objects.filter(date=i['paid_on']).aggregate(salary=Sum('amount'))
        b = [x for x in b if x['amount'] != 0]
        total_amt = 0
        print(sl)
        cort_i['room_amount'] = b
        cort_i['rooms'] = len(b)
        total_amt+=i['total']
  
        for j in Expenses.objects.filter(date=i['paid_on']):
            
            lz_i.append(j.item)
            amount_i.append(j.amount)
        amounts =0 
        for l in amount_i:
            if len(amount_i) <= 1:
               amounts = l
            else:
                amounts+=l
        amount_s=0 
        for t in Salary.objects.filter(date=i['paid_on']):  
              amount_h.append(t.amount) 
             
        cort_i['exp'] = amounts   
        cort_i['profit'] = i['total'] - amounts   
      
        cort_i['item'] = lz_i
        cort_i['amount'] = amount_i
        total_exp = 0
       
        ls.append(cort_i)
    total_amt=0
    total_exp=0
    for n in ls:
        total_amt+=n['total']
        total_exp+=n['exp']
    print("***************")
    print(ls)
    tmt = total_amt - total_exp  
    data = {'bil':ls,'total_amt':total_amt,'total_exp':total_exp,'tmt':tmt,'from':fro,'to':to}
    pdf = render_to_pdf('billing-report.html', data)
    if pdf and report == '1':
     #send_pdf_email('REPORT','REPORT','rsiphael@gmail.com',pdf)
     
     return HttpResponse(pdf, content_type='application/pdf')
    elif pdf and report == '2':
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    elif pdf and report == '3' and email != '':
      send_pdf_email('REPORT','REPORT',emails,pdf)
      messages.success(request,"Room successful Excluded")
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 else:
    bilz = Billing.objects.filter(paid_on__lte=today).order_by('-paid_on').values('paid_on').annotate(total=Sum('amount')).annotate(count=Count('id'))
    # print(bilz)
    # print(bil[0]['paid_on'])
    # print(bil[len(bil)-1]['paid_on'])
    # bilz = Billing.objects.filter(paid_on__lte=bil[0]['paid_on'],paid_on__gte=bil[len(bil)-1]['paid_on']).values('paid_on').order_by('paid_on').annotate(total=Sum('amount')).annotate(count=Count('id'))
    print("******************")
    
    ex = list(Billing.objects.values_list('paid_on',flat=True))
    last = ex[-1]
    first=ex[0]
    
    ls=[]
    
    for i in bilz:
        lz_i = []
        amount_i=[]
        amount_h=[]
        ls_i = []
        cort_i = {}
        cort_i['date'] = i['paid_on']
        cort_i['total'] = i['total'] 
        b = list(Billing.objects.filter(paid_on=i['paid_on']).values('amount','reservation__room__number'))
        salary = Salary.objects.filter(date=i['paid_on']).aggregate(salary=Sum('amount'))
        
        b = [x for x in b if x['amount'] != 0]
        total_amt = 0
  
        cort_i['room_amount'] = b
        cort_i['rooms'] = len(b)
        total_amt+=i['total']
        cort_i['salary']=salary['salary']
  
        for j in Expenses.objects.filter(date=i['paid_on']):
            
            lz_i.append(j.item)
            amount_i.append(j.amount)
        amounts =0 
        for l in amount_i:
            if len(amount_i) <= 1:
               amounts = l
            else:
                amounts+=l            
        cort_i['exp'] = amounts   
        cort_i['profit'] = i['total'] - amounts   
      
        cort_i['item'] = lz_i
        cort_i['amount'] = amount_i
        total_exp = 0
       
        ls.append(cort_i)
    total_amt=0
    total_exp=0
    for n in ls:
        total_amt+=n['total']
        total_exp+=n['exp']
    if salary['salary'] is None:
        salary['salary'] = 0
    
        total_exp = salary['salary'] + total_exp
    else:
       total_exp = salary['salary'] + total_exp 
    tmt = total_amt - total_exp 
    # print(ls)  
    data = {'bil':ls,'total_amt':total_amt,'total_exp':total_exp,'tmt':tmt,'first':first,'last':last} 
    return render(request,'billing.html',data)





def addExpense(request):
    
    
    name = request.POST.getlist('name')
    price = request.POST.getlist('price')
    date = datetime.datetime.now().date()
    for i in range(0,len(price)):
        print(name[i],price[i])
    
        Expenses.objects.create(item=name[i],amount=price[i],date=date)
    
    
    
    
    messages.success(request,"success")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  


def addBill(request):
    
    if request.method=='POST':
        room = request.POST.get('room')
        amount = request.POST.get('amount')
        paid_on = datetime.datetime.now().date()
        g =  Billing.objects.filter(reservation_id=int(room),reservation__Check_Out=False).aggregate(total=Sum('amount'))
    
        amounts = int(g['total'])+int(amount)
        
        Billing.objects.create(reservation_id=room,amount=amount,paid_on=paid_on,total_paid=amounts)
        
        messages.success(request,"success")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    
def deleteBill(request,id):
    
    if request.method=='POST':
        
        Billing.objects.filter(id=id).delete()
        
        
        messages.success(request,"success")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    messages.error(request,"success")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deleteExpenses(request,id):
    
    if request.method=='POST':
        print(id)
        Expenses.objects.filter(date=id).delete()
        
        
        messages.success(request,"success")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
    
def salary(request):
    user = User.objects.exclude(is_superuser=True)
    
    bil = Salary.objects.all().order_by('-id')
    date = datetime.datetime.now().year
    month = [1,2,3,4,5,6,7,8,9,10,11,12]
    year = []
    for i in range(2023,date+1):
        year.append(i)
    print(year)
    return render(request,'salary.html',{'bil':bil,'user':user,'year':year,'month':month})


def addSalary(request):
 try:
  if request.method == 'POST':   
    user = request.POST.get('user') 
    amount = request.POST.get('amount')
    year = request.POST.get('year')
    month = request.POST.get('month')
    
    u = Salary.objects.filter(user_id=user).exists()
    l = Salary.objects.filter(month=month).exists()
    k = Salary.objects.filter(year=year).exists()
    
    if u and l and k:
      messages.error(request,"Salary with User exists")
      return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    else : 
        Salary.objects.create(user_id=user,amount=amount,year=year,month=month)
    
        messages.success(request,"success")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 except Exception as e:
     messages.error(request,e)
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def deleteSalary(request,id):
 try:   
    Salary.objects.filter(id=id).delete()
    
    messages.success(request,"success")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 except Exception as e:
     messages.error(request,e)
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 
 
 
 
def booking_record(request):
    
    book = Reservation.objects.filter(booked=True)
    
    
    
    return render(request,'booked.html',{'book':book})


def deleteBooking(request,id):
   try: 
    Reservation.objects.filter(id=id).delete() 
    messages.success(request,"success")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   except Exception as e:
    messages.success(request,e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def notification(request):
    
    book = Reservation.objects.filter(booked=True,booked_on=today,view_booked=True).count()
    

    return JsonResponse({'book':book})

import calendar

def monthReportSent(request):
    
 days = datetime.datetime.now().date()
 time = datetime.datetime.now().strftime("%Y-%m-%d %H:%m:%S")
 print(time)
 t = str(days).split('-')
 day = datetime.datetime(int(t[0]),int(t[1]),int(t[2]),14,10,59).strftime("%Y-%m-%d %H:%m:%S")
 print(day)
 
 d = datetime.timedelta(days=1) 

 g = str(d+days).split('-')
 h = datetime.datetime(int(g[0]),int(g[1]),int(g[2])).date()
#  print(int(g[2]))
 if (int(g[2]) == 17 and time == day):
       
    month = datetime.datetime.now().date().month
    year = datetime.datetime.now().date().year
    print(year)
    date = datetime.datetime(int(year),int(month),1).date()
    fro = date
    to = datetime.datetime.now().date()
    bil = Billing.objects.filter(paid_on__lte=to,paid_on__gte=fro).values('paid_on').annotate(total=Sum('amount')).annotate(count=Count('id'))
    
    ex = Expenses.objects.values('date').annotate(total_amounts=Sum('amount'))
    ls=[]
    
    for i in bil:
        lz_i = []
        amount_i=[]
        amount_h=[]
        ls_i = []
        cort_i = {}
        cort_i['date'] = i['paid_on']
        cort_i['total'] = i['total'] 
        b = list(Billing.objects.filter(paid_on=i['paid_on']).values('amount','reservation__room__number'))
       
        b = [x for x in b if x['amount'] != 0]
        total_amt = 0
  
        cort_i['room_amount'] = b
        cort_i['rooms'] = len(b)
        total_amt+=i['total']
  
        for j in Expenses.objects.filter(date=i['paid_on']):
            
            lz_i.append(j.item)
            amount_i.append(j.amount)
        amounts =0 
        for l in amount_i:
            if len(amount_i) <= 1:
               amounts = l
            else:
                amounts+=l            
        cort_i['exp'] = amounts   
        cort_i['profit'] = i['total'] - amounts   
      
        cort_i['item'] = lz_i
        cort_i['amount'] = amount_i
        total_exp = 0
       
        ls.append(cort_i)
    total_amt=0
    total_exp=0
    for n in ls:
        total_amt+=n['total']
        total_exp+=n['exp']
    
    tmt = total_amt - total_exp  
    data = {'bil':ls,'total_amt':total_amt,'total_exp':total_exp,'tmt':tmt,'from':fro,'to':to}
    pdf = render_to_pdf('billing-report.html', data)
    
    if pdf:
        month = str(calendar.month_name[month]).upper()
      
        send_pdf_email(f'SIJURA {month} MONTHLY REPORT','MONTH REPORT',['rsiphael@gmail.com'],pdf)
        print("&&&&&&&&&&&&&&&&&&&&&&&&")
      
    #   print(month)
      #message = send_pdf_email(f'SIJURA {month} MONTHLY REPORT','MONTH REPORT',['rsiphael@gmail.com'],pdf)
     
     
        
        print('hureeeeee')
        return JsonResponse({'status':True})
    return JsonResponse({'status':False})
 return JsonResponse({'status':False})
    
    
    
def viewBook(request):
    
    
    Reservation.objects.filter(view_booked=True).update(view_booked=False)
        
        
    
    return redirect('/admins/booking_record')





