from django.shortcuts import render
from .models import *
# Create your views here.
from .send_sms import send_sms
def index (request):
    cat= Categories.objects.all()
    gallery= Gallery.objects.all()
    # testimonials = Testimonial.objects.all()
    # render(request,'index.html',{'testimonial': testimonials})
    render (request,'index.html',{'cat': cat})
    return render(request,"index.html",{'cat': cat,'gallery': gallery})
def reservation (request):
    if request.method=='POST':
        send_sms()
    return render(request, "reservation.html")
def contact(request):
    return  render (request, "contact.html")
def blog (request):
    chambres = Categories.objects.all()
    return render (request, "blog.html",{'chambres': chambres})
def about(request):
    return render (request, 'about.html')


def rooms(request):
    rooms = Rooms.objects.exclude(id=8).filter(reserved=False,booked=False).count()
    room = Rooms.objects.filter(id=8,reserved=False,booked=False).count()
    cat = Categories.objects.all()
    rum = Rooms.objects.exclude(id=8).filter(reserved=False,booked=False)
    return render (request, 'rooms.html',{'rooms':rooms,'cat':cat,'room':room,'rum':rum})