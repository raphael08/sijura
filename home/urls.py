from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('',index, name= 'index'),
    path ("Reservation",reservation,name= 'reservation'),
    path ("Contact",contact,name= 'contact'),
    path ("Blog",blog,name= 'blog'),
    path ("About",about,name= 'about'),
    path ("rooms",rooms,name= 'rooms'),
    path('data',data,name='data'),
    path('df/<str:start>/<str:end>',df,name='df'),
]
urlpatterns += staticfiles_urlpatterns()
