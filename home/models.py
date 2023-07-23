from django.db import models


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
    reserved = models.BooleanField(default=False)
    booked = models.BooleanField(default=False)
    
    
    def __str__(self):
        
        return str(self.number)
    
    
class Reservation(models.Model):
    Name = models.CharField(max_length=20)
    Phone = models.IntegerField(default=0)
    Email = models.EmailField(max_length=40,null=True,blank=True)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    days_of_staying = models.IntegerField(default=0)
    Date_Check_In = models.DateField(default=today)
    Date_Check_Out  = models.DateField(blank=True,null=True) 
    Check_Out = models.BooleanField(default=False)
    
    def __str__(self):
        
        return self.Name
    

class Booking(models.Model):

    Name = models.CharField(max_length=20)
    Phone = models.IntegerField(default=0)
    Email = models.EmailField(max_length=40)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    days_of_staying = models.IntegerField(default=0)
    Date_Check_In = models.DateField(today)
    Date_Check_Out  = models.DateField(blank=True,null=True) 
    booking_code = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        
        return self.Name


class Billing(models.Model):
    reservation = models.OneToOneField(Reservation,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    
    
    def __str__(self):
        
        return self.amount
    
class Debt(models.Model):
    reservation = models.OneToOneField(Reservation,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    
    def __str__(self):
        
        return self.amount
    
    
class Gallery(models.Model):
    file = models.FileField(upload_to='media/pics')
    
    
    def __str__(self):
        
        return self.file.name
    
    
    
    