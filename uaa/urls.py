from django.urls import path,include
from .views import *

urlpatterns = [
    path('',login,name='login'),
    path('logout',logout,name='logout'),
    path('adduser',adduser,name='adduser'),
    path('edituser/<str:id>',editUser,name='edituser'),
    path('deleteuser/<str:id>',deleteUser,name='deleteuser'),
    path('blockuser/<str:pk>',blockuser,name='blockuser'),
    path('unblockuser/<str:pk>',unblockuser,name='unblockuser'),
    path('reset_password/<str:pk>',reset_password,name='reset_password')
]