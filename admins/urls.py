from django.urls import path,include
from .views import *

urlpatterns = [
    path('',dashboard,name='login'),
    path('reservations',reservations,name='reservations'),
    path('exclude/<str:id>',exclude,name='exclude'),
    path('dexclude/<str:id>',dexclude,name='dexclude'),
    path('reserv',reserv,name='reserv'),
    path('roomz',roomz,name='roomz'),
    path('reserved-rooms',reservedRoomz,name='reserved-rooms'),
    path('reserve-record',reserveRecord,name='reserve-record '),
    path('billing',billing_report,name='billing'),
    path('expense',Expense,name='expense'),
    path('addExpense',addExpense,name='addExpense'),
    path('salary',salary,name='salary'),
    path('addBill',addBill,name='addBill'),
    path('deleteBill/<str:id>',deleteBill,name='deleteBill'),
    path('deleteExpenses/<str:id>',deleteExpenses,name='deleteExpenses'),
    path('deleteBooking/<str:id>',deleteBooking ,name='deleteBooking '),
    path('booking_record',booking_record,name='booking_record'),
    path('notification',notification,name='notification'),
     path('monthReportSents',monthReportSent,name='monthReportSent'),
     path('viewBook',viewBook,name='viewBook'),
     
     
]
    