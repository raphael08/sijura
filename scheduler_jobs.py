from admins.views import render_to_pdf, send_pdf_email
from home.views import *
from home.models import Reservation
from admins.views import *

def sendTxt():
 
 days = datetime.datetime.now().date()
 time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

 t = str(days).split('-')
 day = datetime.datetime(int(t[0]),int(t[1]),int(t[2]),9,59,59).strftime("%Y-%m-%d %H:%M:%S")
 print(time,day)
 
 d = datetime.timedelta(days=1) 

 g = str(d+days).split('-')   
 
 exist = EmailSent.objects.filter(date=days).exists()


 if (int(g[2]) == 1):
  if exist:
   ex =  EmailSent.objects.get(date=days)
   if ex.sent == False:
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
        print(month)
        send_pdf_email(f'SIJURA {month} MONTHLY REPORT',f'{month} MONTH REPORT',['rsiphael@gmail.com'],pdf)
        send_sms(656569880,f'SIJURA {month} MONTHLY REPORT HAS BEEN SENT TO YOUR EMAIL')
        EmailSent.objects.filter(date=days).update(sent=True)
        print('hureeeeee')
        return JsonResponse({'status':True})
   else:
      pass 
  else:
      
    month = datetime.datetime.now().date().month
    year = datetime.datetime.now().date().year
    
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
        print(month)
        send_pdf_email(f'SIJURA {month} MONTHLY REPORT',f'{month} MONTH REPORT',['rsiphael@gmail.com'],pdf)
        send_sms(656569880,f'SIJURA {month} MONTHLY REPORT HAS BEEN SENT TO YOUR EMAIL')
        EmailSent.objects.create(date=days,sent=True)
   
     
     
        
        print('hureeeeee')
        return JsonResponse({'status':True})
    return JsonResponse({'status':False})
 return JsonResponse({'status':False})



def birthday():
    
    days = datetime.datetime.now().date()
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    t = str(days).split('-')
    day = datetime.datetime(int(t[0]),int(t[1]),int(t[2]),22,30,00).strftime("%Y-%m-%d %H:%M:%S")
    d = datetime.datetime.now().date().day
    # print(d)
    # print(day)
    # d = datetime.timedelta(days=1) 

    g = str(day).split('-')   
    # print(g)
    exist = EmailSent.objects.filter(date=days).exists()
    if int(d==20):
        if exist:
            pass 
        else:
        # print("happyday")
        #send_sms(629967879,'To the woman who brings light into my life every day, happy birthday and may your day be as radiant as your smile......says Rex Bey')
            EmailSent.objects.create(date=days,sent=True)
            send_sms(629967870,'To the woman who brings light into my life every day, happy birthday and may your day be as radiant as your smile......says Rex Bey')
            send_sms(629967870,'Angalia kwenye begi la kijeshi kuna mfuko ufungue... I LOVE YOU  HAPPY BIRTHDAY MYLOVE ')
            send_sms(656569880,'SENT')
        
        
    
