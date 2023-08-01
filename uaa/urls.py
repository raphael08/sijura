from django.urls import path,include
from .views import *

urlpatterns = [
    path('',login,name='login'),
    path('logout',logout,name='logout'),
    path('adduser',adduser,name='adduser'),
    path('edituser/<str:id>',editUser,name='edituser'),
    path('deleteuser/<str:id>',deleteUser,name='deleteuser')
]