from django.urls import path,include
from .views import *

urlpatterns = [
    path('',dashboard,name='login'),
    path('user',user,name='user'),
]