from django.db import models

from django.db.models import Q,Sum
# Create your models here.


# class Chambre(models.Model):
#     nom = models.CharField(max_length=20)
#     prix = models.IntegerField(default=0)
#     description = models.TextField()
#     image = models.ImageField(upload_to='pics')
#     disponibilité = models.BooleanField(default=True)

#     def __str__(self): 
#         return self.nom
# class Catalogue(models.Model):
#     image = models.ImageField(upload_to='pics')
# class Testimonial(models.Model):
#     nom = models.CharField(max_length=20)
#     avis = models.TextField()
#     image = models.ImageField(upload_to='media/pics')
#     def __str__(self):
#         return self.nom
# class Reservation(models.Model):
#     Name = models.CharField(max_length=20)
#     Phone = models.IntegerField(default=0)
#     Email = models.EmailField(max_length=40)
#     Date_Check_In = models.DateField(auto_now=False)
#     Date_Check_Out  = models.DateField(auto_now=False)
#     Adulte = models.IntegerField (default=0)
#     Children = models.IntegerField(default=0)
#     Note = models.TextField()
#     def __str__(self):
#         return self.Name


# date = datetime.datetime.now()
# print(date.strftime("%Y-%m-%d %H:%M:%S"))

# days = datetime.timedelta(days=2)
# days = date+days
# print(days.strftime("%Y-%m-%d %H:%M:%S"))

# if reserved_day < today:
#     =+amount
#     =+debt 
import datetime
todays = datetime.datetime.now().date()
today = datetime.datetime.now().date().strftime("%Y-%m-%d")

class Categories(models.Model):
    Name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/pics')
    price = models.IntegerField(default=0)
    description = models.TextField()
    
    def __str__(self):
         return self.Name
    
class Rooms(models.Model):
    category = models.ForeignKey(Categories,on_delete=models.CASCADE) 
    number = models.IntegerField(default=0)
    exclude = models.BooleanField(default=False)
    
    
    
    def __str__(self):
        
        return str(self.number)
    
    
class Reservation(models.Model):
    PAID_CHOICE = (('PAID','PAID'),('DEBT','DEBT'))
    Name = models.CharField(max_length=20)
    Phone = models.CharField(max_length=20)
    Email = models.EmailField(max_length=40,null=True,blank=True)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    Date_Check_In = models.DateField(default=today)
    Date_Check_Out  = models.DateField(blank=True,null=True) 
    booking_code = models.CharField(max_length=100,null=True,blank=True)
    reserved = models.BooleanField(default=False)
    booked = models.BooleanField(default=False) 
    booked_on = models.DateField(default=today,blank=True,null=True)
    view_booked = models.BooleanField(default=False)
    Check_Out = models.BooleanField(default=False)
    cancel_book = models.BooleanField(default=False)
    cancel_book_on = models.DateField(blank=True,null=True)
    
    discount = models.IntegerField(default=0,blank=True,null=True)
    # payment = models.CharField(choices=PAID_CHOICE,max_length=50,blank=True,null=True)
    paid_on = models.DateField(blank=True,null=True)
    update_at = models.DateField(default=today,blank=True,null=True)
     
    
    
    @property
    def get_amount(self):
        
        if self.Check_Out==False: 
            
            
            
            year,month,day = str(self.Date_Check_In).split('-')
            
            d = datetime.datetime(int(year),int(month),(int(day))).date()
         
            days = datetime.datetime.now().date()
            dates = datetime.datetime.now().date()
            today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            years,months,daz = str(dates).split('-')
            
            dt = datetime.datetime(int(years),int(months),(int(daz)),10,00,00).strftime('%Y-%m-%d %H:%M:%S')
            
            
            
            # if today >  dt:
            #     print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            # else:
            #     print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

            # print(dt)
            # print(today-dt)
            days = days-d
            # print(days)
            if today > dt:
             if (str(days).split(' ')[0]) != '0:00:00':
                
            
            
                self.days = int(str(days).split(' ')[0])+1
                # print("&&&&&&&&&&&&&&&&&")
                # print(self.days)
                
                self.amount = (self.room.category.price * self.days)-self.discount
                
                
                return self.amount
             else:
                return  self.room.category.price * 1
            else:
                
                if (str(days).split(' ')[0]) != '0:00:00':
                
            
            
                    self.days = int(str(days).split(' ')[0])
                    
                    self.amount = (self.room.category.price * self.days)-self.discount
                    
                    
                    return self.amount
                else:
                 return  self.room.category.price * 1
    
    def __str__(self):
        
        return str(self.room.number)
    

class Booking(models.Model):

    Name = models.CharField(max_length=20)
    Phone = models.CharField(max_length=11)
    Email = models.EmailField(max_length=40)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    days_of_staying = models.IntegerField(default=0)
    Date_Check_In = models.DateField(today)
    Date_Check_Out  = models.DateField(blank=True,null=True) 
    booking_code = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        
        return self.Name


class Billing(models.Model):
    reservation = models.ForeignKey(Reservation,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    total_paid = models.IntegerField(default=0)
    paid_on = models.DateField(null=True,blank=True)
    created_at = models.DateField(default=today)
    
    @property
    def total_remain(self):
        if self.reservation.Check_Out==False:
            # b = Billing.objects.filter(reservation_id=self.reservation.id).order_by('-created_at').first()
            
            # self.remain = Billing.objects.filter(reservation_id=self.reservation.id).aggregate(Sum('amount'))['amount__sum'] - self.reservation.get_amount
            self.remain = self.total_paid - self.reservation.get_amount
          
            
            return self.remain
        else:
            pass
      
    @property
    def status(self):
    
      
      if self.reservation.Check_Out == False:
        if '-' in str(self.total_remain):
            
            return 'DEBT'
        elif int(self.total_remain) > 0:
            return 'CREDICT'
        else:
            return 'PAID'
        
      else:
          return "CHECKOUT"
        
    
   
    
    
    def __str__(self):
        
        return str(self.amount)
    
class Debt(models.Model):
    reservation = models.OneToOneField(Reservation,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    
    def __str__(self):
        
        return self.amount
    
    
class Gallery(models.Model):
    file = models.FileField(upload_to='media/pics')
    
    
    def __str__(self):
        
        return self.file.name
    
    
    

    
    
    
    