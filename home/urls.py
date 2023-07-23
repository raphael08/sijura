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
    path ("books",book,name= 'books'),
    path('data',data,name='data'),
    path('df/<str:start>/<str:end>',df,name='df'),
    path('book',booking,name='booking'),
    path('verify/<str:code>',verify,name='verify'),
    path('cancel_book/<str:id>',cancel_book,name='cancel_book'),
]
urlpatterns += staticfiles_urlpatterns()
