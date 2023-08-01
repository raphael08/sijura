from django.db import models

# Create your models here.

from home.models import *
today = datetime.datetime.now().date().strftime("%Y-%m-%d")

class Sells(models.Model):

    total_amount = models.IntegerField(default=0)
    date = models.DateField(default=today)


class Debts(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    total_debt = models.IntegerField(default=0)
    amount_paid = models.IntegerField(default=0)
    amount_remain = models.IntegerField(default=0)
    discount = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateField(default=today)


class Expenses(models.Model):
    item = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)
    date = models.DateField(default=today)
